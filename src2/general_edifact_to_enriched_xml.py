# general_edifact_to_enriched_xml.py

import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict
import os 
from pyshacl import validate
from rdflib import *
from os import *
from subprocess import *
import time 

folder_path = os.path.dirname(os.path.abspath(__file__)) + os.sep

class EDIFACTToEnrichedXMLConverter:
    def __init__(self, edifact_text):
        self.text = edifact_text
        self.segments = []
        self.message_counter = 1
        self.message = None
        self.current_item = None
        self.last_rff_qualifier = None
        self.mid_counter = 1
        self.organisation_counters = defaultdict(int)
        self.party_roles = {}
        self.line_counter = 0
        self.alc_description = {}
        self.last_alc_type = None  # From D_5463
        self.last_pat_type = None  # From D_4279
        self.last_pat_date = None  # From D_2475
        self.last_nad_role = None
        self.structure_id = "Structure0"
        self.root = ET.Element("Interchange", format="EDIFACT", eancomstructure=self.structure_id)

    def parse_segments(self):
        self.segments = [seg.strip() for seg in self.text.strip().split("'") if seg.strip()]

    def convert(self):
        self.parse_segments()
        for segment in self.segments:
            tag, *data = segment.split('+')

            # Reset LineItem context if a new LIN or UNS segment starts
            if tag in {"LIN", "UNS"}:
                self.current_item = None

            if tag == "UNB":
                self.handle_unb(data)
            elif tag == "UNH":
                self.handle_unh(data)
            elif tag == "BGM":
                self.handle_bgm(data)
            elif tag == "DTM":
                self.handle_dtm(data)
            elif tag == "NAD":
                self.handle_nad(data)
            elif tag == "RFF":
                self.handle_rff(data)
            elif tag == "MOA":
                self.handle_moa(data)
            elif tag == "TAX":
                self.handle_tax(data)
            elif tag == "CUX":
                self.handle_cux(data)
            elif tag == "ALC":
                self.handle_alc(data)
            elif tag == "PCD":
                self.handle_pcd(data)
            elif tag == "PAT":
                self.handle_pat(data)
            elif tag == "LIN":
                self.handle_lin(data)
            elif tag == "PIA":
                self.handle_pia(data)
            elif tag == "CTA":
                self.handle_cta(data)
            elif tag == "TOD":
                self.handle_tod(data)
            elif tag == "IMD":
                self.handle_imd(data)
            elif tag == "QTY":
                self.handle_qty(data)
            elif tag == "COM":
                self.handle_com(data)
            elif tag == "PRI":
                self.handle_pri(data)
            elif tag == "FTX":
                self.handle_ftx(data)
            elif tag == "UNT":
                self.handle_unt(data)
            elif tag == "UNS":
                self.handle_uns(data)
            elif tag == "UNZ":
                self.handle_unz(data)
            else:
                print("Unknown segment:", tag)

        for code, (tag, val) in self.party_roles.items():
            ET.SubElement(self.message, tag).text = val

    def add_meta(self, name, value):
        if value:
            ET.SubElement(self.root, name).text = value

    def handle_unb(self, data):
        self.add_meta("synatxIdentifier", data[0].split(':')[0])
        self.add_meta("synatxVersion", data[0].split(':')[1])
        self.add_meta("senderIndicator", data[1].split(':')[0])
        self.add_meta("recipientIndicator", data[2].split(':')[0])
        self.add_meta("creationDate", data[3].split(':')[0])
        self.add_meta("creationTime", data[3].split(':')[1])
        self.add_meta("dataExchangeReference", data[4])

    def handle_unh(self, data):
        mid_value = f"mid{self.mid_counter}"
        self.mid_counter += 1

        # Use message_counter to create a unique details attribute
        details_value = f"Invoice{self.message_counter}"
        self.message_counter += 1

        self.message = ET.SubElement(self.root, "Message", {
            "details": details_value,
            "type": "INVOIC",
            "version": "D",
            "release": "96A",
            "mid": mid_value, 
            "eancomstructure": self.structure_id
        })
        ET.SubElement(self.message, "ProcessIdentification").text = "None"
        self.add_meta("messageReferenceNumber", data[0])
        parts = data[1].split(':')
        self.add_meta("messageTypeIdentifier", parts[0])
        self.add_meta("versionNumberMessageType", parts[1])
        self.add_meta("releaseNumberMessageType", parts[2])
        self.add_meta("managingOrganisations", parts[3])

    def handle_bgm(self, data):
        """
        Handle BGM segment and replace numeric qualifiers with translations.
        """

        # XML tags in order
        tags = ["Dokumentenart", "Dokumentennummer", "Dokumentenfunktion"]

        # Translation maps for relevant tags
        translation_maps = {
            "Dokumentenart": {
                "380": "Rechnung",
                "381": "Gutschrift",
                "383": "Lastschrift",
                "382": "Rechnungskorrektur",
                "385": "Proformarechnung",
                "389": "Selbstfakturierung"
            },
            "Dokumentenfunktion": {
                "9": "Original",
                "7": "Duplikat",
                "31": "Abschlagsrechnung",
                "46": "Korrigierte Rechnung"
            }
        }

        for i, tag in enumerate(tags):
            if i < len(data):
                val = data[i]
                # Replace with translation if available
                translation = translation_maps.get(tag, {}).get(val, val)
                elem = ET.SubElement(self.message, tag)
                elem.text = translation

    def handle_dtm(self, data):
        for item in data:
            parts = item.split(':')
            if len(parts) >= 2:
                qualifier, value = parts[0], parts[1]

                if qualifier == "171" and self.last_rff_qualifier:
                    tag = f"Referenz_{self.last_rff_qualifier}_Date"
                else:
                    tag = f"DTM_{qualifier}"

                target = self.current_item if self.current_item is not None else self.message
                ET.SubElement(target, tag).text = value
                
    def handle_pcd(self, data):
        if not data or len(data) == 0:
            return

        # Always split first entry by ':', fallback to data[1] if no ':'
        parts = data[0].split(':', 1)
        qualifier = parts[0]
        value = parts[1] if len(parts) > 1 else (data[1] if len(data) > 1 else "")

        # Direct mapping for most qualifiers
        tag_map = {
            "1": "AbschlagProzentsatz",
            "2": "ZuschlagProzentsatz",
            "7": "RechnungsProzentsatz",
            "12": "AbzugProzentsatz",
            "15": "StrafProzentsatz"
        }

        # Determine tag name
        if qualifier == "3":
            if self.last_alc_type_code == "A":
                tag = "MOA_204_Prozentsatz"
                base_tag = "MOA_204"
            elif self.last_alc_type_code == "C":
                tag = "MOA_23_Prozentsatz"
                base_tag = "MOA_23"
            elif self.last_pat_type:
                tag = f"Zahlungsbedingung_{self.last_pat_type}_Prozentsatz"
                base_tag = f"Zahlungsbedingung_{self.last_pat_type}"
            else:
                tag = f"PCD_{qualifier}"
                base_tag = f"PCD_{qualifier}"
        else:
            tag = tag_map.get(qualifier, f"PCD_{qualifier}")
            base_tag = tag_map.get(qualifier, f"PCD_{qualifier}")


        # ✅ Use current_item if exists, else fallback to message
        target = self.current_item if self.current_item is not None else self.message
        ET.SubElement(target, tag).text = value

        # ✅ Add extra element if PAT segment present
        if self.last_pat_type and base_tag:
            additional_tag = f"{base_tag}Zahlungsbedingungen"
            ET.SubElement(target, additional_tag).text = value


                
    def handle_alc(self, data):
        if not data or len(data) == 0:
            return

        alc_type_code = data[0].strip()  # D_5463
        reason_code = data[4].strip() if len(data) > 4 else ""

        if alc_type_code == "A":
            tag_name = "Abschlag"
        elif alc_type_code == "C":
            tag_name = "Zuschlag"
        else:
            return  # Skip unknown type codes

        reason_label_map = {
            "AAJ": "Kupferzuschlag", "ADS": "Palettenweise Bestellung", "ADQ": "Produktmix",
            "ADR": "Andere Dienste", "AG": "Silberzuschlag", "DI": "Rabatt", "FC": "Frachtkosten",
            "HD": "Bearbeitung der Sendung", "RAA": "Ermaessigung", "SC": "Zuschlag",
            "SF": "Spezial Rabatt", "SH": "Spezielle Handhabungsdienstleistungen", "TD": "Handelsrabatt",
            "ZD1": "Gegenseitig definiert", "ZS1": "Gegenseitig definiert", "ZZZ": "Gegenseitig definiert"
        }

        reason_label = reason_label_map.get(reason_code, "")

        self.last_alc_reason_label = reason_label
        self.last_alc_type_code = alc_type_code

        # ✅ Use current_item if it exists, else fallback to message
        target = self.current_item if self.current_item is not None else self.message
        ET.SubElement(target, tag_name).text = reason_label



    def handle_tax(self, data):
        if len(data) < 5:
            return

        tax_type = data[1]  # D_5153, e.g. 'VAT' or 'GST'
        tax_components = data[4].split(':') if len(data) > 4 else []

        if not tax_type or len(tax_components) < 4 or not tax_components[3]:
            return

        tax_value = tax_components[3]  # D_5278 = 4th component in ':::21'

        tag_name = f"TAX_{tax_type}"
        target = self.current_item if self.current_item is not None else self.message
        ET.SubElement(target, tag_name).text = tax_value
        

    def handle_moa(self, data):
        if not data or ':' not in data[0]:
            return

        parts = data[0].split(':')
        if len(parts) < 2:
            return

        code = parts[0].strip()
        value = parts[1].strip()
        currency = parts[2].strip() if len(parts) > 2 else None

        # MOA+8 – Zuschlag or Abschlag based on previous ALC
        if code == "8":
            reason = getattr(self, "last_alc_reason_label", "Unbekannt")
            tag = "MOA_204" if "Abschlag" in reason else "MOA_23"
        else:
            tag = f"MOA_{code}"

        target = self.current_item if self.current_item is not None else self.message
        ET.SubElement(target, tag).text = value

        if currency:
            ET.SubElement(target, "Waehrung").text = currency
        
    def handle_cux(self, data):
        if not data or len(data) == 0:
            return
        print(data)

        currency_tag_map = {
            "4": "WaehrungRechnung",
            "9": "WaehrungBestellung",
            "10": "WaehrungPreisangabe",
            "11": "WaehrungZahlung"
        }

        for entry in data:
            parts = entry.split(":")
            if len(parts) == 3:
                d_6347, d_6345, d_6343 = parts
            elif len(parts) == 2:
                d_6347, d_6345 = parts
                d_6343 = ""  # fallback for missing part
            else:
                continue  # skip this invalid entry

            # Always add general currency tag based on D_6347
            if d_6347:
                ET.SubElement(self.message, "Waehrung").text = d_6345

            # Add specific tag if D_6343 is recognized
            if d_6343 in currency_tag_map:
                ET.SubElement(self.message, currency_tag_map[d_6343]).text = d_6345

            
    def handle_pat(self, data):
        if not data or self.message is None:
            return 
        self.last_pat_type = data[0]
        # D_4279: ZahlungsbedingungsArt
        terms_type_map = {
            "1": "Wie ueblich",
            "3": "Fixdatum",
            "7": "Verlaengert",
            "20": "Vertragsstrafen",
            "22": "Abzug",
            "ZZZ": "Gemeinsam festgelegt"
        }
        ET.SubElement(self.message, "ZahlungsbedingungsArt").text = terms_type_map.get(data[0], f"{data[0]} nicht_vorhanden")

        # C112: D_2475:D_2009:D_2151:D_2152
        if len(data) > 2 and data[2]:
            c112_parts = (data[2].split(':') + [""] * 4)[:4]
            ref_code, relation_code, unit_code, number = c112_parts

            reference_map = {
                "5": "Rechnungsdatum",
                "9": "Rechnungseingangsdatum"
            }
            relation_map = {
                "1": "",
                "2": "vor ",
                "3": "nach "
            }
            unit_map = {
                "D": "Tag(e)",
                "M": "Monat(e)",
                "Y": "Jahr(e)"
            }

            if number:
                ref_label = reference_map.get(ref_code, f"{ref_code} nicht_vorhanden")
                relation_prefix = relation_map.get(relation_code, f"{relation_code} nicht_vorhanden ")
                unit_label = unit_map.get(unit_code, f"{unit_code} nicht_vorhanden")
                text = f"{number} {unit_label} {relation_prefix}{ref_label}".strip()
                ET.SubElement(self.message, "ZahlungsbezugsterminTage").text = text


    def handle_imd(self, data):

        description = data[2].lstrip(':').strip()

        if description:
            ET.SubElement(self.current_item, "Description").text = description

    def handle_nad(self, data):
        if not data or self.message is None:
            return
        # 1. Party Qualifier (BY, SU, etc.)
        party_qualifier = data[0] if len(data) > 0 else "UNKNOWN"

        # 2. Maintain unique counter per party type
        count = self.organisation_counters.get(party_qualifier, 0) + 1
        self.organisation_counters[party_qualifier] = count
        org_value = f"{party_qualifier}{count}"

        # 3. Human-readable agentRole mapping
        agent_role_labels = {
            "AB": "SalesAgentRole", "BO": "BrokerOrSalesOfficeRole",
            "BS": "CalculateAndDeliverToRole", "BY": "BuyerRole",
            "CN": "RecipientRole", "CPE": "Zentralregulierer_EAN_CodeRole",
            "DP": "DeliveryPartyRole", "II": "InvoicingPartyRole",
            "IV": "InvoiceeRole", "PE": "PaymentRecipientRole",
            "PR": "PayeeRole", "PW": "DespatchPartyRole",
            "RE": "RecipientOfInvoiceRegulationRole", "RG": "RegulatorRole",
            "SCO": "SuppliersCompanyHeadquarterRole", "SE": "SellerRole",
            "SN": "WarehouseNumberRole", "SR": "RepresentativeOrAgentOfSupplierRole",
            "ST": "SendToRole", "SU": "SupplierRole", "WS": "WholesalerRole",
            "UC": "FinalConsigneeRole"
        }
        readable_role = agent_role_labels.get(party_qualifier, party_qualifier)

        # 4. Add role attribute directly to the <Message> element
        self.message.attrib[readable_role] = org_value

        # 5. Create <Party> element with `details` attribute from <Message>
        self.last_party_element = ET.SubElement(
            self.message,
            "Party",
            attrib={
                "agentRole": readable_role,
                "organisation": org_value,
                "details": self.message.attrib["details"]  # Attach details from <Message>
            }
        )

        # 6. Strict mapping of EDIFACT NAD segment fields
        field_map = {
            1: ("PartyID", True, ["PartyID", "CodeListQualifier", "CodeListResponsibleAgency"]),
            2: ("NameAddressLine", False, "NameAddressLine"),
            3: ("PartyName", False, "PartyName"),
            4: ("Street", False, "Street"),
            5: ("City", False, "City"),
            6: ("CountrySubEntity", False, "CountrySubEntity"),
            7: ("PostalCode", False, "PostalCode"),
            8: ("CountryCode", False, "CountryCode")
        }

        for idx, (label, is_list, tags) in field_map.items():
            val = data[idx] if len(data) > idx and data[idx] else ""
            if not val:
                continue

            if is_list:
                parts = val.split(':')
                for tag, content in zip(tags, parts):
                    if content:
                        ET.SubElement(self.last_party_element, tag).text = content
            else:
                ET.SubElement(self.last_party_element, tags).text = val

        # Save the last role for later usage (e.g., in handle_rff)
        self.last_nad_role = party_qualifier

    
    def handle_tod(self, data):
        if not data or len(data) == 0:
            return


        # D_4055: Delivery or Transport Terms Function Code
        delivery_function_code = data[0].strip() if len(data) > 0 else ""

        delivery_function_map = {
            "2": "Transport",
            "3": "Lieferbedingung",
            "4": "Transportkosten",
            "5": "LieferbedingungenVereinbart"
            # Add more as needed
        }
        delivery_function_text = delivery_function_map.get(delivery_function_code, f"Lieferbedingung_{delivery_function_code}")

        # C100: D_4053:D_1131:D_3055
        delivery_terms = ""
        if len(data) > 2 and data[2]:
            parts = data[2].split(':')
            if len(parts) >= 1:
                delivery_terms = parts[0].strip()  # Usually the Incoterm (e.g., DAP)

        # Use the last_party_element if available, else fallback to message
        target = self.message

        # Add function code element
        ET.SubElement(target, "LieferbedingungenFunktion").text = delivery_function_text

        # Add delivery terms element if present
        if delivery_terms:
            ET.SubElement(target, "Lieferbedingung").text = delivery_terms
                
    def handle_rff(self, data):
        if not data or len(data) == 0:
            return

        parts = data[0].split(":")
        qualifier = parts[0] if len(parts) >= 1 else None
        ref_value = parts[1] if len(parts) >= 2 else ""  # fallback: empty string if no value provided

        self.last_rff_qualifier = qualifier

        if qualifier == "VA" and self.last_party_element is not None and self.last_nad_role:
            tag = "Umsatzsteuernummer"
            ET.SubElement(self.last_party_element, tag).text = ref_value
        else:
            tag = f"Referenz_{qualifier}"
            target = self.current_item if self.current_item is not None else self.message
            ET.SubElement(target, tag).text = ref_value

    def handle_lin(self, data):
        if not data:
            return

        self.line_counter += 1
        line_id = f"Item{self.line_counter}"

        # Get the details attribute from the parent Message
        message_details = self.message.attrib.get("details", "Invoice1")  # fallback

        # Create LineItem with details attribute
        self.current_item = ET.SubElement(self.message, "LineItem", {
            "nid": line_id,
            "details": message_details
        })

        # Add the product identification element(s)
        if len(data) >= 3:
            parts = data[2].split(':')
            article_number = parts[0] if len(parts) >= 1 else ""
            qualifier = parts[1] if len(parts) >= 2 else ""

            qualifier_map = {
                "BP": "Teilnummer_des_Kaeufers",
                "EN": "International_Article_Number",
                "PV": "Nummer_der_Aktionsvariante",
                "HS": "Harmonisiertes_System",
                "GN": "Nationaler_Produktgruppencode",
                "IN": "Artikelnummer_des_Kaeufers",
                "MF": "Artikelnummer_des_Herstellers",
                "LI": "Positionszeilennummer",
                "SA": "Artikelnummer_des_Lieferanten",
                "UP": "Universal_Product_Code"
            }

            tag = qualifier_map.get(qualifier, f"nicht_vorhanden_{qualifier}")
            if article_number:
                ET.SubElement(self.current_item, tag).text = article_number
                ET.SubElement(self.current_item, "Produktidentifikation").text = qualifier_map.get(qualifier, f"nicht_vorhanden_{qualifier}")

        # Create InvoiceLine element (from D_1082, which is usually in data[1])
        if len(data) > 1 and data[1]:
            ET.SubElement(self.current_item, "InvoiceLine").text = data[1]
        else:
            # Always create it, even if empty
            ET.SubElement(self.current_item, "InvoiceLine").text = ""


    def handle_pia(self, data):
        if not self.current_item or not data:
            return


        qualifier_map = {
            "BP": "Teilnummer_des_Kaeufers",
            "EN": "International_Article_Number",
            "PV": "Nummer_der_Aktionsvariante",
            "HS": "Harmonisiertes_System",
            "GN": "Nationaler_Produktgruppencode",
            "IN": "Artikelnummer_des_Kaeufers",
            "MF": "Artikelnummer_des_Herstellers",
            "LI": "Positionszeilennummer",
            "SA": "Artikelnummer_des_Lieferanten",
            "UP": "Universal_Product_Code"
        }

        # Process each additional product identifier
        for item in data[1:]:
            parts = item.split(':')
            article_number = parts[0] if len(parts) >= 1 else ""
            qualifier = parts[1] if len(parts) >= 2 else ""

            tag = qualifier_map.get(qualifier, f"nicht_vorhanden_{qualifier}")
            if article_number:
                ET.SubElement(self.current_item, tag).text = article_number

        # Determine the first additional product identifier (if any) and set as Zusaetzliche_Produktidentifikation
        zusatz_identifikation = "nicht_vorhanden"
        for item in data[1:]:
            parts = item.split(':')
            qualifier = parts[1] if len(parts) >= 2 else ""
            zusatz_identifikation = qualifier_map.get(qualifier, f"nicht_vorhanden_{qualifier}")
            break  # only the first occurrence

        ET.SubElement(self.current_item, "Zusaetzliche_Produktidentifikation").text = zusatz_identifikation

    def handle_qty(self, data):
        if self.current_item is None or not data or len(data) < 1:
            return
        parts = data[0].split(':')
        if len(parts) < 2:
            return
        qualifier, amount = parts[0], parts[1]
        unit = parts[2] if len(parts) > 2 else ""

        # Mapping of qualifier to element name suffix
        qualifier_map = {
            "1": "Diskrete_Menge",
            "12": "Ausgelieferte_Menge",
            "46": "Gelieferte_Menge",
            "47": "Berechnete_Menge",
            "59": "Verbrauchereinheiten",
            "61": "Retourmenge",
            "131": "Liefermenge",
            "192": "Menge_ohne_Berechnung",
            "194": "Erhalten_und_akzeptiert"
        }

        # Translation of known EDIFACT unit codes
        unit_translation = {
            "PCE": "Stueck",
            "C62": "Einheit",
            "KGM": "Kilogramm",
            "LTR": "Liter",
            "MTR": "Meter",
            "HUR": "Stunde",
            "DAY": "Tag"
            # Add more as needed
        }

        element_base = qualifier_map.get(qualifier, f"Menge_{qualifier}")
        unit_readable = unit_translation.get(unit, unit)
        # Create separate sub-elements
        #ET.SubElement(self.current_item, f"{element_base}_Wert").text = amount
        if unit:
            ET.SubElement(self.current_item, f"{element_base}_Einheit").text = unit_readable
            ET.SubElement(self.current_item, element_base).text = f"{amount} {unit_readable}"
            ET.SubElement(self.current_item, "Mengen_Einheit").text = unit_readable
        else:
            ET.SubElement(self.current_item, element_base).text = amount
            ET.SubElement(self.current_item, f"{element_base}_Einheit").text = amount

    def handle_cta(self, data):
        if not data or len(data) == 0:
            return
        
        
        # D_3139: Contact Function Code
        contact_function_code = data[0].strip() if len(data) > 0 else ""

        # D_3412: Contact Name or Department
        contact_name = data[1].strip() if len(data) > 1 else ""

        # Map for Contact Function Code
        contact_function_map = {
            "AD": "Sachbearbeiter",
            "IC": "Informationskontakt",
            "PD": "LeiterEinkauf",
            "AP": "Kontaktperson",
            "OD": "Bestellkontakt"
            # Add more as needed
        }

        # Determine the tag for the function code
        function_tag = contact_function_map.get(contact_function_code, f"Kontakt_{contact_function_code}")

        # Use the last_party_element if available, else fallback to message
        target = self.last_party_element if self.last_party_element is not None else self.message

        # Add function code element
        ET.SubElement(target, "KontaktFunktion").text = function_tag

        # Add contact name element using the D_3412 element tag
        if contact_name:
            ET.SubElement(target, "D_3412").text = contact_name

    def handle_com(self, data):
        if not data or len(data) == 0:
            return


        # Split the first entry by ':' to get the communication value and channel
        parts = data[0].split(':', 1)
        comm_value = parts[0].strip() if len(parts) > 0 else ""
        comm_channel = parts[1].strip() if len(parts) > 1 else ""

        # Determine the tag for communication channel
        comm_tag_map = {
            "EM": "EmailAdresse",
            "TE": "TelefonNummer",
            "FX": "TelefaxNummer",
            "ED": "EDI-Adresse"
            # Add more as needed
        }

        # Fallback to generic channel if not in map
        channel_label = comm_tag_map.get(comm_channel, f"Kommunikationskanal_{comm_channel}")

        # Final tag name: "Ansprechpartner_" + label
        final_tag = f"Ansprechpartner_{channel_label}"

        # Use the last_party_element if available, else fallback to message
        target = self.last_party_element if self.last_party_element is not None else self.message

        # Add communication tag with value
        if comm_value:
            ET.SubElement(target, final_tag).text = comm_value




    def handle_pri(self, data):
        if self.current_item is None or not data or len(data) == 0:
            return

        parts = data[0].split(':')
        price_type_code = parts[0].strip() if len(parts) > 0 else ""
        price_value = parts[1].strip() if len(parts) > 1 else ""
        preisquelle = parts[2].strip() if len(parts) > 2 else ""
        unit_base = parts[4].strip() if len(parts) > 4 and parts[4] else None
        unit_code = parts[5].strip() if len(parts) > 5 and parts[5] else None

        # Tag naming based on D_5125
        tag_map = {
            "AAA": "Nettokalkulation",
            "AAB": "Bruttokalkulation",
            "GRP": "Bruttopreis_pro_Einheit",
            "INV": "Rechnungspreis",
            "NTP": "Nettopreis_pro_Einheit"
        }
        tag_name = tag_map.get(price_type_code, f"Preis_{price_type_code}")

        # Add price value element
        ET.SubElement(self.current_item, tag_name).text = price_value

        # 🔴 Add PreisArt if GRP or NTP
        if price_type_code in ["GRP", "NTP"]:
            ET.SubElement(self.current_item, "PreisArt").text = tag_name

        # 🔴 PreisQuelle translation mapping
        preisquelle_map = {
            "CT": "Katalog",
            "AA": "Herstellerangabe",
            "AB": "Verkaeuferangabe",
            "AC": "Kaeuferangabe"
            # Add more as needed
        }

        # 🔴 Add PreisQuelle if present
        if preisquelle:
            preisquelle_label = preisquelle_map.get(preisquelle, f"{preisquelle}_nicht_vorhanden")
            ET.SubElement(self.current_item, "PreisQuelle").text = preisquelle_label

        # Handle unit label only if unit_code is valid
        unit_translation = {
            "M": "Meter",
            "PCE": "Stueck",
            "PK": "Packet",
            "PR": "Paar",
            "CEL": "Celsius",
            "GRM": "Gramm",
            "MMT": "Millimeter",
            "MTK": "Quadratmeter"
        }

        if unit_code and unit_code in unit_translation:
            unit_label = unit_translation[unit_code]

            # Add unit element
            ET.SubElement(self.current_item, "Preis_Maßeinheit").text = unit_label

            # Add combined price + unit
            ET.SubElement(self.current_item, f"{tag_name}_Einheit").text = f"{price_value} {unit_label}"

            # Add unit base element only if present
            if unit_base:
                ET.SubElement(self.current_item, "unitPriceBase").text = unit_base




                
    def handle_ftx(self, data):
        if not data or len(data) < 4:
            return

        qualifier = data[0].strip()  # D_4451
        text_components = data[3].split(':') if len(data) >= 4 else []
        full_text = ' '.join(part.strip() for part in text_components if part.strip())
        tag = f"FTX_{qualifier if qualifier else 'UNDEFINED'}"

        target = self.current_item if self.current_item is not None else self.message
        if full_text:
            ET.SubElement(target, tag).text = full_text

    def handle_unt(self, data):
        self.add_meta("totalNumberOfSegments", data[0])

    def handle_uns(self, data):
        self.add_meta("controlSegmentBetweenItemAndTotalPart", data[0])

    def handle_unz(self, data):
        self.add_meta("dataExchangeCounter", data[0])
        self.add_meta("exchangeReference", data[1])

    def to_string(self):
        rough = ET.tostring(self.root, 'utf-8')
        reparsed = minidom.parseString(rough)
        return reparsed.toprettyxml(indent="  ")

def yarrrmlparser_bash():
    p = Popen([folder_path + 'yarrrmlparser.sh'], stdout = PIPE , stderr = PIPE)
    p.communicate()
    p.wait()

def rmlmapper_bash():
    p = Popen([folder_path + 'rmlmapper.sh'], stdout = PIPE , stderr = PIPE)
    p.communicate()
    p.wait()
    
def yarrrmlparser_batch():
    p = Popen([folder_path + 'yarrrmlparser.bat'], stdout = PIPE , stderr = PIPE)
    p.communicate()
    p.wait()

def rmlmapper_batch():
    p = Popen([folder_path + 'rmlmapper.bat'], stdout = PIPE , stderr = PIPE)
    p.communicate()
    p.wait()

def validates(process):

    data_graph = \
        folder_path + 'invoice.ttl'
    data_graph = path.abspath(data_graph)

    process_type = process+ '.ttl'
    shapes_graph = \
        folder_path + process_type
        
    shapes_graph = path.abspath(shapes_graph)

    conforms, v_graph, v_text = validate(data_graph,data_graph_format="ttl", shacl_graph=shapes_graph,
                                        shacl_graph_format="ttl", inference='rdfs',advanced=True, debug=False, 
                                        serialize_report_graph=True)
    result = v_text.split("\n")
    message_lines = [line for line in result if line.strip().startswith("Message:")]
    for j in range(len(message_lines)):
        parts = message_lines[j].split(';')
        parts = [part.strip() for part in parts]
        message = parts[0].replace('Message:', '')
        print(message)   

    return v_text



if __name__ == "__main__":
    with open("input.edi", "r") as f:
        edi_data = f.read()

    converter = EDIFACTToEnrichedXMLConverter(edi_data)
    converter.convert()
    enriched_xml = converter.to_string()

    with open("enriched_output.xml", "w") as f:
        f.write(enriched_xml)
