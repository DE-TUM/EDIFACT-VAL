import xml.etree.ElementTree as ET
import os 
from pyshacl import validate
from rdflib import *
from os import *
from subprocess import *
import time 

folder_path = os.path.dirname(__file__) + '/'
        
def ProProcessingStep1(file_name):
    file_namefull = folder_path + str(file_name)
    preTree = ET.parse(file_namefull)
    preRoot = preTree.getroot()
    val = -1
    val2 = 0
    mid = 0
    #brid = 0
    group = 1
    eancomstructure = 0
    org = 0
    details = 0

    Segments = ["S_UNB","Message","S_UNH","S_BGM", "S_DTM", "S_PAI","S_ALI", "S_FTX", "S_RFF", "S_NAD", 
                        "S_FII", "S_CTA", "S_COM", "S_TAX","S_MOA", "S_CUX", "S_PAT", 
                        "S_PCD", "S_TDT", "S_TOD", "S_LOC", "S_PAC", "S_ALC", 
                        "S_QTY", "S_RTE", "S_LIN","S_PIA", "C_C212", "C_C212_2", "C_C212_3", "C_C212_4","S_IMD", "S_MEA", "S_QVR", "S_PRI", 
                        "S_PCI", "S_GIN", "S_LOC", "S_CNT","S_UNS", "S_UNT"] 

    ItemGruppe = ["G_Group_25"] 

    PartnerGruppe = ["G_Group_2", "G_Group_34"] 

    DataElementGroup = [ "C_S001","C_S002","C_S003", "C_S004", "C_S005", "C_S010","C_C002", 
                "C_C507", "C_C534", "C_C107", "C_C108", "C_C506", "C_C082", "C_C058",
                "C_C080", "C_C059", "C_C078", "C_C088", "C_C056", "C_C076", "C_C241", "C_C533",
                "C_C243", "C_C516","C_C504","C_C501", "C_C220","C_C228", "C_C040", "C_C401","C_C112",
                "C_C222", "C_C100", "C_C517", "C_C519", "C_C553", "C_C531", "C_C202", "C_C402", 
                "C_C532", "C_C552", "C_C214", "C_C186", "C_C128", "C_C212", "C_C212_2", "C_C212_3", "C_C212_4", "C_C829" , "C_C273",
                "C_C502" , "C_C174", "C_C279" , "C_C960", "C_C110", "C_C509", "C_C210", "C_C827",
                "C_C208", "C_C270"] 

    DataElement = ["D_3035", "D_2005", "D_1153", "D_5025", "D_7143", "D_2380", "D_1154", "D_3036",
                    "D_5004", "D_7140", "D_3039", "D_6063", "D_6060", "D_1001", "D_1225", "D_5125",
                    "D_5118", "D_6311", "D_6313", "D_6314", "D_6411", "D_MaDim", "D_MaEinheit", "D_QTYMaEinheit", "D_PRIMaEinheit", 
                    "D_AlcRea","D_5463", "D_7161", "D_5245", "D_5482", "D_4279", "D_2151", "D_2475", 
                    "D_2009", "Zahlungsbezugstermin", "Zeitbezug", "ArtZeitspanne", "D_2152", "D_5278", 
                    "D_5153", "D_6343", "D_6345", "Umsatzsteuernummer", "D_1004", "D_3432", "D_3194", 
                    "D_4055", "D_4052", "D_ReFu", "D_PaFu", "D_AlcEx", "D_4347", "D_EC212", "D_Wae", "D_4053",
                    "D_4451", "D_4440", "D_4440_2", "D_4440_3", "D_4440_4", "D_5375", "D_5387", "D_3139", "D_3412","D_5305", "ZeitangabeZahlungsbedingung", "ZeitangabeZahlungsbedingung",
                    "D_0074", "D_3155", "D_3148", "D_6347", "D_3207", "D_Country"] 

    EANCOMStructureDataElements = ["S_UNH","S_UNB","C_S001" ,"C_S002","C_S003","C_S004", "C_S009", "C_S010", "D_0001", "D_0002", "D_0004", "D_0007", "D_0008", "D_0010", "D_0014", "D_0017", "D_0019", 
                "D_0020", "D_0081", "D_0062", "D_0065", "D_0052", "D_0054", "D_0051", "S_UNH","S_UNS", "S_UNT", "S_UNZ", "D_0036", "D_0020"]

    RefdatumGroup = ["G_Group_1", "G_Group_29", "G_Group_49"]

    ALCGroup = ["G_Group_15", "G_Group_38", "G_Group_51"]

    Groups = ["S_UNB", "Message", "S_UNH", "S_BGM", "S_DTM", "G_Group_1", "G_Group_2", "G_Group_7", 
            "G_Group_8", "G_Group_15", "G_Group_25","G_Group_50", "S_MOA", "S_QTY", "S_UNT", "S_UNZ"]

    NIDgroups = ["S_NAD", "S_ALC", "S_TAX", "S_LIN", "S_PIA", "S_IMD", "S_QTY", "S_ALI", "S_MEA", "S_FII", "S_TOD", "S_FTX", "S_CUX", "S_MEA", "S_DTM", "S_QVR", "S_MOA","S_PAT", "S_PCD", "S_PRI", "S_RFF", "S_PAC", "S_GIN", "C_C516"]

    ParentSegment = ["S_MOA", "S_TAX", "S_DTM", "S_RFF", "D_6411", "S_NAD", "D_3035", "S_ALC", "D_5463", "S_PCD", "C_C212", "C_C212_2", "C_C212_3", "C_C212_4", "D_7140", "D_7143","S_CUX", "D_Wae", "C_C504"]

    Group = Segments + DataElementGroup
    Elements = Segments + DataElementGroup + DataElement+ Groups + EANCOMStructureDataElements
    Elementse = ItemGruppe + DataElementGroup + DataElement + NIDgroups
    def addExplainElement(DataElementName,DataElementText):
        FixId = elem.attrib['id']
        added= ET.SubElement(preRoot.find(f'.//{elem.tag}[@id="{FixId}"]/..'), str(DataElementName))
        added.text = str(DataElementText)
        added.set("id", str(FixId))
        return added

    def addExplainMessageElement(DataElementName,DataElementText):
        Mids = elem.attrib['mid']
        added= ET.SubElement(preRoot.find(f'Message[@mid="{Mids}"]'), str(DataElementName))
        added.text = str(DataElementText)
        added.set("mid", str(Mids))
        return added  


    for elem in preTree.iter():
        if elem.tag == "Message": 
            details += 1
        if elem.tag in Segments:  
            val += 1
        if elem.tag in PartnerGruppe:
            org += 1
        if elem.tag in ItemGruppe:  
            val2 += 1
        if elem.tag in RefdatumGroup + ALCGroup:
            group +=1
        if elem.tag in ["Message", "S_NAD", "S_LIN", "S_UNH" ]:
            elem.set("details", "Invoice"+ str(details))
        if elem.tag in Elements:
            elem.set("id", str(val))
        if elem.tag in ["G_Group_15", "S_ALC","D_AlcEx","G_Group_17","S_QTY", "G_Group18", "S_PCD", "D_5245","G_Group_19", "S_MOA","D_5025", "G_Group_20", "S_RTE", "G_Group_21",
                        "S_TAX", "S_MOA", "S_ALI", "G_Group_39", "G_Group_40", "S_PCD", "G_Group_41","G_Group_42", "S_TDT" ,"G_Group_38", "G_Group_51", 
                        "G_Group_1", "G_Group_29", "G_Group_49", "D_2005", "D_ReFu", "D_2380"]:
            elem.set("group", str(group))
        if elem.tag in Elementse:
            elem.set("nid", "Item"+str(val2))
            elem.set('organisation', "Role"+str(org))
        if elem.tag in ParentSegment:  
            s = "S_"
            parentname = preRoot.find(f'.//{elem.tag}[@id="{str(val)}"]/..').tag 
            for x in range(len(s)): 
                parentname = parentname.replace(s[x],"")    
            elem.set("parent",parentname)
        if elem.tag == "Message":
            mid +=1 
        if elem.tag in Elements:
            if elem.tag in EANCOMStructureDataElements: 
                mid1 = mid-1
                elem.set("eancomstructure", "Structure"+str(eancomstructure))
            else:
                elem.set("mid", "InvoiceDetail"+str(mid)) 
        if elem.tag == "D_1153":
            if elem.text == "AAB":
                addExplainElement("D_ReFu","Proforma_Rechnungsnummer") 
            elif elem.text == "AAJ":
                addExplainElement("D_ReFu","Lieferauftragsnummer")
            elif elem.text == "AAK":
                addExplainElement("D_ReFu","Nummer_Lieferschein") 
            elif elem.text == "AAG":
                addExplainElement("D_ReFu","Angebotsnummer")   
            elif elem.text == "ABD":
                addExplainElement("D_ReFu","Zolltarifnummer")
            elif elem.text == "ABO":
                addExplainElement("D_ReFu","Referenz_des_Absenders") 
            elif elem.text == "ACE":
                addExplainElement("D_ReFu","zugehoerige_Dokumentennummer") 
            elif elem.text == "AP":
                addExplainElement("D_ReFu","Nummer_des_Forderungskontos")   
            elif elem.text == "AFO":
                addExplainElement("D_ReFu","Referenz_des_Begünstigten") 
            elif elem.text == "ALL":
                addExplainElement("D_ReFu","Nummer_eines_Bündels_von_Nachrichten")
            elif elem.text == "ALO":
                addExplainElement("D_ReFu","Wareneingangsmeldung_Nummer")
            elif elem.text == "API":
                addExplainElement("D_ReFu","Zusaetzliche_Partneridentifikation_EAN_Code")
            elif elem.text == "BC":
                addExplainElement("D_ReFu","Vertragsnummer_des_Kaeufers")
            elif elem.text == "CIN":
                addExplainElement("D_ReFu","Nummer_einr_konsolidierten_Rechnung_EAN_Code")
            elif elem.text == "CD":
                addExplainElement("D_ReFu","Gutschreliftsnummer")
            elif elem.text == "COE":
                addExplainElement("D_ReFu","Referenznummer_zu_einem Geschaeftskontauszug_EAN_Code") 
            elif elem.text == "CR":
                addExplainElement("D_ReFu","Referenzsnummer_des_Kunden")
            elif elem.text == "CT":
                addExplainElement("D_ReFu","Vertragsnummer")
            elif elem.text == "DL":
                addExplainElement("D_ReFu","Nummer_der_Belastungsanzeige")
            elif elem.text == "DQ":
                addExplainElement("D_ReFu","Lieferscheinnummer")
            elif elem.text == "FC":
                addExplainElement("D_ReFu","Steuernummer")
            elif elem.text == "FI":
                addExplainElement("D_ReFu","Bezeichner_Dateizeilen")
            elif elem.text == "GN":
                addExplainElement("D_ReFu","Regulierungsreferenznummer")
            elif elem.text == "HS":
                addExplainElement("D_ReFu","Nummer_harmonisiertes_System")
            elif elem.text == "IA":
                addExplainElement("D_ReFu","Interne_Lieferantennummer")  
            elif elem.text == "IP":
                addExplainElement("D_ReFu","Import_Lizenznummer") 
            elif elem.text == "IT":
                addExplainElement("D_ReFu","Interne_Kundennummer")  
            elif elem.text == "IV":
                addExplainElement("D_ReFu","Rechnungsnummer")   
            elif elem.text == "LI":
                addExplainElement("D_ReFu","Referenznummer_der_Position")  
            elif elem.text == "ON":
                addExplainElement("D_ReFu","Auftragsnummer_Kaeufer")
            elif elem.text == "PL":
                addExplainElement("D_ReFu","Nummer_der_Preisliste")  
            elif elem.text == "PQ":
                addExplainElement("D_ReFu","Zahlungsreferenz")
            elif elem.text == "PY":
                addExplainElement("D_ReFu","Kontonummer_des_Zahlungsempfänger") 
            elif elem.text == "RF":
                addExplainElement("D_ReFu","Exportreferenznummer")
            elif elem.text == "SS":
                addExplainElement("D_ReFu","Referenznummer_des_Verkaeufers") 
            elif elem.text == "SZ":
                addExplainElement("D_ReFu","Spezelifikationsnummer") 
            elif elem.text == "VA":
                addExplainElement("D_ReFu","Umsatzsteuernummer")
            elif elem.text == "VN":
                addExplainElement("D_ReFu","Auftragsnummer_Lieferant") 
            elif elem.text == "XA":
                addExplainElement("D_ReFu","Unternehmes_oder_Ort_Regisstriernummer")
            else: 
                addExplainElement("D_ReFu", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_3035":
            if elem.text == "AB":
                addExplainElement("D_PaFu","Verkaus Agent")
            elif elem.text == "BO":
                addExplainElement("D_PaFu","Broker- odr Verkaufsbuero")
            elif elem.text == "BS":
                addExplainElement("D_PaFu","Berechnen und liefern an")
            elif elem.text == "BY":
                addExplainElement("D_PaFu","Kaeufer")
            elif elem.text == "CN":
                addExplainElement("D_PaFu","Empfaenger")
            elif elem.text == "CPE":
                addExplainElement("D_PaFu","Zentralregulierer (EAN-Code)")
            elif elem.text == "DP":
                addExplainElement("D_PaFu","Lieferanschrift")
            elif elem.text == "II":
                addExplainElement("D_PaFu","Rechnungssteller")
            elif elem.text == "IV":
                addExplainElement("D_PaFu","Rechnungsempfaenger")
            elif elem.text == "PE":
                addExplainElement("D_PaFu","Zahlungsempfaenger")
            elif elem.text == "PB":
                addExplainElement("D_PaFu","Zahlendes_Kreditinstitut")
            elif elem.text == "PR":
                addExplainElement("D_PaFu","Bezahler")
            elif elem.text == "PW":
                addExplainElement("D_PaFu","Auslieferungspartei")
            elif elem.text == "RB":
                addExplainElement("D_PaFu","Empfangendes_Kreditinstitut")
            elif elem.text == "RE":
                addExplainElement("D_PaFu","Empfaenger der Rechnungsregulierung")
            elif elem.text == "RG":
                addExplainElement("D_PaFu","Rechnungsregulier")
            elif elem.text == "SCO":
                addExplainElement("D_PaFu","Unternehmenszentrale des Lieferanten")
            elif elem.text == "SE":
                addExplainElement("D_PaFu","Verkaeufer")
            elif elem.text == "SN":
                addExplainElement("D_PaFu","Lagernummer")
            elif elem.text == "SR":
                addExplainElement("D_PaFu","Beauftrageter/Agent des Lieferanten")
            elif elem.text == "ST":
                addExplainElement("D_PaFu","Versenden an")
            elif elem.text == "SU":
                addExplainElement("D_PaFu","Lieferant")
            elif elem.text == "WS":
                addExplainElement("D_PaFu","Grosshaendler")
            elif elem.text == "UC":
                addExplainElement("D_PaFu","Endempfaenger")
            else: 
                addExplainElement("D_PaFu", elem.text+ "nicht_vorhanden")
        #MOASegemnt()
        if elem.tag == "D_3207":
            if elem.text == "DE":
                addExplainElement("D_Country", "Deutschland")
            if elem.text == "BE":
                addExplainElement("D_Country", "Belgien")
            if elem.text == "NL":
                addExplainElement("D_Country", "Niederlande")
        if elem.tag == "D_7143":
            C212 = elem.attrib['id']
            if elem.text == "BP":
                addExplainElement("D_EC212","Artikelnummer des Kaeufers")
            elif elem.text == "EN":
                addExplainElement("D_EC212","International Article Number")
            elif elem.text == "PV":
                addExplainElement("D_EC212","Nummer der Aktionsvariante")
            elif elem.text == "HS":
                addExplainElement("D_EC212","Zolltarelifsystem")
            elif elem.text == "GN":
                addExplainElement("D_EC212","Nationaler Produktgruppencode")
            elif elem.text == "IN":
                addExplainElement("D_EC212","Positionsnummer des Kaeufers")
            elif elem.text == "MF":
                addExplainElement("D_EC212","Artikelnummer_des_Herstellers")
            elif elem.text == "LI":
                addExplainElement("D_EC212","Positionszeilennummer")
            elif elem.text == "SA":
                addExplainElement("D_EC212","Artikelnummer des Lieferanten")
            elif elem.text == "UP":
                addExplainElement("D_EC212", "Universal Prodcut Code" )
            else:
                addExplainElement("D_EC212", elem.text + "nicht_vorhanden")
        if elem.tag == "D_6411":
            if elem.attrib["parent"] == "CC186": 
                if elem.text == "M":
                    addExplainElement("D_QTYMaEinheit","Meter")
                elif elem.text == "PCE":
                    addExplainElement("D_QTYMaEinheit","Stueck")
                elif elem.text == "PK":
                    addExplainElement("D_QTYMaEinheit","Packet")
                elif elem.text == "PR":
                    addExplainElement("D_QTYMaEinheit","Paar")
                elif elem.text == "SET":
                    addExplainElement("D_QTYMaEinheit","Set")
                elif elem.text == "CEL":
                    addExplainElement("D_QTYMaEinheit","Celsius")
                elif elem.text == "GRM":
                    addExplainElement("D_QTYMaEinheit","Gramm")
                elif elem.text == "HUR":
                    addExplainElement("D_QTYMaEinheit","Stunde")
                elif elem.text == "MMT":
                    addExplainElement("D_QTYMaEinheit","Millimeter")
                elif elem.text == "MTK":
                    addExplainElement("D_QTYMaEinheit","Quadratmeter")
                else: 
                    addExplainElement("D_QTYMaEinheit",str(elem.text)+ "nicht_vorhanden")
            elif elem.attrib["parent"] == "CC509": 
                if elem.text == "M":
                    addExplainElement("D_PRIMaEinheit","Meter")
                elif elem.text == "PCE":
                    addExplainElement("D_PRIMaEinheit","Stueck")
                elif elem.text == "PK":
                    addExplainElement("D_PRIMaEinheit","Packet")
                elif elem.text == "PR":
                    addExplainElement("D_PRIMaEinheit","Paar")
                elif elem.text == "CEL":
                    addExplainElement("D_PRIMaEinheit","Celsius")
                elif elem.text == "GRM":
                    addExplainElement("D_PRIMaEinheit","Gramm")
                elif elem.text == "MMT":
                    addExplainElement("D_PRIMaEinheit","Millimeter")
                elif elem.text == "MTK":
                    addExplainElement("D_PRIMaEinheit","Quadratmeter")
                else: 
                    addExplainElement("D_PRIMaEinheit",str(elem.text)+ "nicht_vorhanden")
            else: 
                if elem.text == "M":
                    addExplainElement("D_MaEinheit","Meter")
                elif elem.text == "PCE":
                    addExplainElement("D_MaEinheit","Stueck")
                elif elem.text == "PK":
                    addExplainElement("D_MaEinheit","Packet")
                elif elem.text == "PR":
                    addExplainElement("D_MaEinheit","Paar")
                elif elem.text == "CEL":
                    addExplainElement("D_MaEinheit","Celsius")
                elif elem.text == "GRM":
                    addExplainElement("D_MaEinheit","Gramm")
                elif elem.text == "MMT":
                    addExplainElement("D_MaEinheit","Millimeter")
                elif elem.text == "MTK":
                    addExplainElement("D_MaEinheit","Quadratmeter")
                else: 
                    addExplainElement("D_MaEinheit",str(elem.text)+ "nicht_vorhanden")
        if elem.tag == "D_1001":
            if elem.text == "83":
                addExplainMessageElement("Dokumentenname","Wertgutschrift")
            elif elem.text == "84":
                addExplainMessageElement("Dokumentenname","Wertbelastung")
            elif elem.text == "380":
                addExplainMessageElement("Dokumentenname","Handelsrechnung")
            elif elem.text == "381":
                addExplainMessageElement("Dokumentenname","Gutschriftsanzeige")
            elif elem.text == "384":
                addExplainMessageElement("Dokumentenname", "Korrigierte Rechnung")
            elif elem.text == "385":
                addExplainMessageElement("Dokumentenname", "Konsolidierte Rechnung")
            else: 
                addExplainMessageElement("Dokumentenname", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_1225":
            if elem.text == "1":
                addExplainMessageElement("Dokumentenfunktion", "Stornierung")
            elif elem.text == "5":
                addExplainMessageElement("Dokumentenfunktion", "Ersatz")
            elif elem.text == "7":
                addExplainMessageElement("Dokumentenfunktion", "Duplikat")
            elif elem.text == "9":
                addExplainMessageElement("Dokumentenfunktion", "Original")
            elif elem.text == "31":
                addExplainMessageElement("Dokumentenfunktion", "Kopie")
            elif elem.text == "43":
                addExplainMessageElement("Dokumentenfunktion", "Zusaetzliche Uebertragung")
            else: 
                addExplainMessageElement("Dokumentenfunktion", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_5125":
            if elem.text == "AAA":
                addExplainElement("D_PriFu","Nettokalkulation")
                type = "Nettopreis"
            elif elem.text == "AAB":
                addExplainElement("D_PriFu","Bruttokalkulation")
                type = "Bruttopreis"
            elif elem.text == "GRP":
                addExplainElement("PreisArt","Bruttopreis pro Einheit")
                type = "Bruttopreis_pro_Einheit"
            elif elem.text == "INV":
                addExplainElement("D_PriFu","Rechnungspreis")
                type = "Rechnungspreis"
            elif elem.text == "NTP":
                addExplainElement("PreisArt","Nettopreis pro Einheit")
                type = "Nettopreis_pro_Einheit"
            else:
                addExplainElement("D_PriFu",elem.text+ "nicht_vorhanden")
                type = elem.text
        if elem.tag == "D_5375":
            if elem.text == "CA":
                addExplainElement("PreisQuelle","Katalog")
            elif elem.text == "CT":
                addExplainElement("PreisQuelle","Kotrakt")
            else:
                addExplainElement("PreisQuelle", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_5387":
            if elem.text == "DPR":
                addExplainElement("PreisArt","Reduzierter"+ type)
            elif elem.text == "GRP":
                addExplainElement("PreisArt","Bruttopreis pro Einheit")
            elif elem.text == "PPR":
                addExplainElement("PreisArt","Provisoricher"+ type)
            elif elem.text == "PRP":
                addExplainElement("PreisArt","Aktions"+ type)
            elif elem.text == "RTP":
                addExplainElement("PreisArt","Einzelhandels"+ type)
            elif elem.text == "SRP":
                addExplainElement("PreisArt","Empfohlender Einzelhandles"+ type)
            else:
                addExplainElement("PreisArt",elem.text+ "nicht_vorhanden")
        if elem.tag == "D_6313": 
            if elem.text == "AAA":
                addExplainElement("D_MaDim","Nettogewicht einer Einheit")
            elif elem.text == "AAF":
                addExplainElement("D_MaDim","Nettonettogewicht")
            elif elem.text == "HT":
                addExplainElement("D_MaDim","Hoehenmass")
            elif elem.text == "LN":
                addExplainElement("D_MaDim","Laengenmassangaben")
            elif elem.text == "WD":
                addExplainElement("D_MaDim","Breitenabmessung")
            else:
                addExplainElement("D_MaDim", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_7161":
            if elem.text == "AAJ":
                addExplainElement("D_AlcRea", "Kupferzuschlag")
            elif elem.text == "ADS":
                addExplainElement("D_AlcRea", "Palettenweise Bestellung")
            elif elem.text == "ADQ":
                addExplainElement("D_AlcRea", "Produktmix")
            elif elem.text == "ADR":
                addExplainElement("D_AlcRea", "Andere Dienste")
            elif elem.text == "AG":
                addExplainElement("D_AlcRea", "Silberzuschlag")
            elif elem.text == "DI":
                addExplainElement("D_AlcRea", "Rabatt")
            elif elem.text == "FC":
                addExplainElement("D_AlcRea", "Frachtkosten")
            elif elem.text == "HD":
                addExplainElement("D_AlcRea", "Bearbeitung der Sendung")
            elif elem.text == "RAA":
                addExplainElement("D_AlcRea", "Ermaessigung")
            elif elem.text == "SC":
                addExplainElement("D_AlcRea", "Zuschlag")
            elif elem.text == "SF":
                addExplainElement("D_AlcRea", "Spezial Rabatt")
            elif elem.text == "SH":
                addExplainElement("D_AlcRea", "Spezielle Handhabungsdienstleistungen")
            elif elem.text == "TD":
                addExplainElement("D_AlcRea", "Handelsrabatt")
            elif elem.text == "ZD1":
                addExplainElement("D_AlcRea", "Gegenseitig definiert")
            elif elem.text == "ZS1":
                addExplainElement("D_AlcRea", "Gegenseitig definiert")
            elif elem.text == "ZZZ":
                addExplainElement("D_AlcRea", "Gegenseitig definiert")
            else:
                addExplainElement("D_AlcRea", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_5463": 
            if elem.text == "A":
                addExplainElement("D_AlcEx","Abschlag")
            elif elem.text == "C":
                addExplainElement("D_AlcEx","Zuschlag")
            elif elem.text == "N":
                addExplainElement("D_AlcEx","Kein_Abschlag_Zuschlag")
            else:
                addExplainElement("D_AlcEx", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_4279": 
            if elem.text == "1":
                addExplainElement("ZahlungsbedingungsArt", "Wie ueblich")
            elif elem.text == "3":
                addExplainElement("ZahlungsbedingungsArt", "Fixdatum")
            elif elem.text == "7":
                addExplainElement("ZahlungsbedingungsArt", "Verlaengert")
            elif elem.text == "20":
                addExplainElement("ZahlungsbedingungsArt", "Vertragsstrafen")
            elif elem.text == "22":
                addExplainElement("ZahlungsbedingungsArt", "Abzug")
            elif elem.text == "ZZZ":
                addExplainElement("ZahlungsbedingungsArt", "Gemeinsam festgelegt ")
            else:
                addExplainElement("ZahlungsbedingungsArt", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_2475": 
            if elem.text == "5":
                addExplainElement("Zahlungsbezugstermin", "Rechnungsdatum ")
            elif elem.text == "9":
                addExplainElement("Zahlungsbezugstermin", "Rechnungseingengsdatum ")
            else: 
                addExplainElement("Zahlungsbezugstermin", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_2009": 
            if elem.text == "1":
                addExplainElement("Zeitbezug", "")
            elif elem.text == "2":
                addExplainElement("Zeitbezug", "vor ")
            elif elem.text == "3":
                addExplainElement("Zeitbezug", "nach ")
            else:
                addExplainElement("Zeitbezug", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_2151": 
            if elem.text == "D":
                addExplainElement("ArtZeitspanne", " Tag(e) ")
            elif elem.text == "M":
                addExplainElement("ArtZeitspanne", " Monat(e) ")
            elif elem.text == "Y":
                addExplainElement("ArtZeitspanne", " Jahr(e) ")
            else: 
                addExplainElement("ArtZeitspanne", elem.text+ "nicht_vorhanden")
        if elem.tag == "D_4053": 
            addExplainElement("D_4052", "Zustellung am Ort")
        if elem.tag == "D_6345":
            if elem.text == "EUR":
                addExplainElement("D_Wae", "Euro")
            else: 
                addExplainElement("D_Wae", elem.text+ "nicht_vorhanden")
    return preTree.write(folder_path + 'PreINVOIC.xml')


def ProProcessingStep2():
    tree = ET.parse(folder_path + 'PreINVOIC.xml')
    root = tree.getroot()

    def addExplainSubjectD1004(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
        if root.find(f'.//D_1004[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_1004[@id="{FixIds}"]').text
    
    def addExplainSubjectDTM(DataElementName):
        nIds = elem.attrib['group']
        Ids = elem.attrib['id']
        if elem.text == "171":
            added= ET.SubElement(root.find(f'.//{elem.tag}[@group="{nIds}"]/..'), str(DataElementName)+ "_"+ root.find(f'.//C_C506/D_ReFu[@group="{nIds}"]').text)
            if root.find(f'.//C_C507/D_2380[@group="{nIds}"]') != None:    
                added.text = root.find(f'.//C_C507/D_2380[@group="{nIds}"]').text
        else:
            added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{Ids}"]/..'), str(DataElementName))
            if root.find(f'.//C_C507/D_2380[@id="{Ids}"]') != None:    
                added.text = root.find(f'.//C_C507/D_2380[@id="{Ids}"]').text
    def addExplainMessageDTM(DataElementName):
        Ids = elem.attrib['id']
        mIds = elem.attrib['mid']
        nIds = elem.attrib['group']
        if elem.text == "171":
            added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName)+ "_"+ root.find(f'.//C_C506/D_ReFu[@group="{nIds}"]').text)
            if root.find(f'.//C_C507/D_2380[@group="{nIds}"]') != None:    
                added.text = root.find(f'.//C_C507/D_2380[@group="{nIds}"]').text
        else:
            added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
            if root.find(f'.//C_C507/D_2380[@id="{Ids}"]') != None:    
                added.text = root.find(f'.//C_C507/D_2380[@id="{Ids}"]').text

    def PositionOrMessageDTM(NewName):
        if parentgroupDTM in [ "Message", "GGroup1", "GGroup7", "GGroup8", "GGroup50" ]: 
            addExplainMessageDTM(str(NewName))
        else:
            addExplainSubjectDTM(str(NewName))
 
    def PositionOrMessageRFF(DataElementName):
        FixIds = elem.attrib['id']
        Mids = elem.attrib['mid'] 
        org = elem.attrib['organisation']
        if parentgroupRFF == "GGroup3" or parentgroupRFF == "GGroup29"  :    
            added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{FixIds}"]/..'), str(DataElementName))  
        else:
            added= ET.SubElement(root.find(f'Message[@mid="{Mids}"]'), str(DataElementName))
        if root.find(f'.//C_C506/D_1154[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//C_C506/D_1154[@id="{FixIds}"]').text 
            added.set("organisation", str(org))

    def PositionOrMessageNAD(NewName):
        if  parentgroupNAD in ["GGroup2","GGroup34"]:
            addNADattribut(str(NewName))
            addNADGLN(str(NewName))

    def AgentRole(AttributName):
        pid = elem.attrib['id']
        AgentRole = root.find(f'.//S_NAD[@id="{pid}"]')
        AgentRole.set(str('agentRole'), str(AttributName + 'Role'))  
    
    def addNADattribut(AttributName):
        pid = elem.attrib['id']
        mIds = elem.attrib['mid']
        nIds = elem.attrib['nid']
        organisation = elem.attrib['organisation']
        Message = root.find(f'Message[@mid="{mIds}"]')
        Message.set(str(AttributName), str(organisation)) 
            
    def addNADGLN(DataElementName): 
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
        if root.find(f'.//C_C082/D_3039[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//C_C082/D_3039[@id="{FixIds}"]').text
            added.attrib = root.find(f'Message[@mid="{mIds}"]').attrib
    

    def addExplainSubjectFII(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//C_C088/D_3432[@id="{FixIds}"]') != None:
            if root.find(f'.//C_C078/D_3194[@id="{FixIds}"]').text != None:
                added.text =root.find(f'.//C_C088/D_3432[@id="{FixIds}"]').text + " - " +root.find(f'.//C_C078/D_3194[@id="{FixIds}"]').text 
            else:
                added.text =root.find(f'.//C_C088/D_3432[@id="{FixIds}"]').text

    def addExplainSubjectFTX(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//C_C108/D_4440[@id="{FixIds}"]') != None:
            if root.find(f'.//C_C108/D_4440_2[@id="{FixIds}"]') != None:
                if root.find(f'.//C_C108/D_4440_3[@id="{FixIds}"]') != None:
                    if root.find(f'.//C_C108/D_4440_4[@id="{FixIds}"]') != None:
                        added.text =root.find(f'.//C_C108/D_4440[@id="{FixIds}"]').text+ root.find(f'.//C_C108/D_4440_2[@id="{FixIds}"]').text + root.find(f'.//C_C108/D_4440_3[@id="{FixIds}"]').text+ root.find(f'.//C_C108/D_4440_4[@id="{FixIds}"]').text
                    else:
                        added.text =root.find(f'.//C_C108/D_4440[@id="{FixIds}"]').text+ root.find(f'.//C_C108/D_4440_2[@id="{FixIds}"]').text + root.find(f'.//C_C108/D_4440_3[@id="{FixIds}"]').text
                else:
                    added.text =root.find(f'.//C_C108/D_4440[@id="{FixIds}"]').text + root.find(f'.//C_C108/D_4440_2[@id="{FixIds}"]').text 
            else:
                added.text =root.find(f'.//C_C108/D_4440[@id="{FixIds}"]').text 
           

    def addExplainSubjectCTA(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//C_C056/D_3412[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//C_C056/D_3412[@id="{FixIds}"]').text 

    def addExplainSubjectCOM(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//D_3148[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_3148[@id="{FixIds}"]').text  

    def addExplainSubjectTOD(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
        if root.find(f'.//C_C100/D_4052[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//C_C100/D_4052[@id="{FixIds}"]').text 

    def addExplainSubjectMOA(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//C_C516/D_5004[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//C_C516/D_5004[@id="{FixIds}"]').text 
            
    def addExplainMessageMOA(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
        if root.find(f'.//C_C516/D_5004[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//C_C516/D_5004[@id="{FixIds}"]').text  

    def PositionOrMessageMOA(NewName):
        if parentgroupMOA in ["GGroup19","GGroup48","GGroup50"]: 
                addExplainMessageMOA(str(NewName))
        else:
            addExplainSubjectMOA(str(NewName))


    def addExplainSubjectC212(DataElementName):
        mIds = elem.attrib['mid']
        nIds = elem.attrib['nid']
        Message = root.find(f'Message[@mid="{mIds}"]')
        Message.set('Item', str(nIds))
        FixIds = elem.attrib['id']
        intFixID = int(FixIds)
        if root.find(f'.//C_C212/D_7140[@id="{FixIds}"]') != None:
            added= ET.SubElement(root.find(f'.//C_C212/D_7140[@id="{FixIds}"]/..'), str(DataElementName))
            added.text =root.find(f'.//C_C212/D_7140[@id="{FixIds}"]').text 
        elif root.find(f'.//C_C212_2/D_7140[@id="{FixIds}"]') != None:
            added= ET.SubElement(root.find(f'.//C_C212/D_7140[@id="{str(intFixID -1)}"]/..'), str(DataElementName))
            added.text =root.find(f'.//C_C212_2/D_7140[@id="{FixIds}"]').text 
        elif root.find(f'.//C_C212_3/D_7140[@id="{FixIds}"]') != None:
            added= ET.SubElement(root.find(f'.//C_C212/D_7140[@id="{str(intFixID -2)}"]/..'), str(DataElementName))
            added.text =root.find(f'.//C_C212_3/D_7140[@id="{FixIds}"]').text
        elif root.find(f'.//C_C212_4/D_7140[@id="{FixIds}"]') != None:
            added= ET.SubElement(root.find(f'.//C_C212/D_7140[@id="{str(intFixID -3)}"]/..'), str(DataElementName))
            added.text =root.find(f'.//C_C212_4/D_7140[@id="{FixIds}"]').text 

    def addExplainSubjectQTY(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{FixIds}"]/..'),"Menge"+ str(DataElementName))
        if root.find(f'.//C_C186/D_6060[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//C_C186/D_6060[@id="{FixIds}"]').text  

    def addExplainSubjectQTY2(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//C_C186/D_6060[@id="{FixIds}"]') != None:
            if root.find(f'.//C_C186/D_QTYMaEinheit[@id="{FixIds}"]') != None:
                added.text =root.find(f'.//C_C186/D_6060[@id="{FixIds}"]').text+ " "  + root.find(f'.//C_C186/D_QTYMaEinheit[@id="{FixIds}"]').text   
            else:
                added.text =root.find(f'.//C_C186/D_6060[@id="{FixIds}"]').text 
    
    def addExplainSubjectPRI(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//{elem.tag}[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//C_C509/D_5118[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//C_C509/D_5118[@id="{FixIds}"]').text  

    def addExplainSubjectMEA(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//D_6311[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//C_C502/D_MaDim[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//C_C502/D_MaDim[@id="{FixIds}"]').text  

    def addExplainSubjectMEA2(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//C_C174[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//C_C174/D_6314[@id="{FixIds}"]') != None:
            if root.find(f'.//C_C174/D_MaEinheit[@id="{FixIds}"]') != None:
                added.text =root.find(f'.//C_C174/D_6314[@id="{FixIds}"]').text +  " " + root.find(f'.//C_C174/D_MaEinheit[@id="{FixIds}"]').text 
            else: 
                added.text =root.find(f'.//C_C174/D_6314[@id="{FixIds}"]').text

    def PositionOrMessageALC(NewName):
        if parentgroupALC in ["GGroup15"]: 
                addExplainMessageALC(str(NewName))
        else:
            addExplainSubjectALC(str(NewName))
    
    def addExplainMessageALC(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
        if root.find(f'.//D_AlcRea[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_AlcRea[@id="{FixIds}"]').text
        if root.find(f'.//D_7160[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_7160[@id="{FixIds}"]').text

    def addExplainSubjectALC(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'.//D_5463[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//D_AlcRea[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_AlcRea[@id="{FixIds}"]').text
        if root.find(f'.//D_7160[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_7160[@id="{FixIds}"]').text

    def PositionOrMessagePCD(NewName):
        if parentgroupPCD in ["GGroup40"]: 
            addExplainSubjectPCD(str(NewName))
        elif parentgroupPCD in ["GGroup8", "GGroup27"]:
            addExplainSubjectPCD2(str(NewName))
        else:
            addExplainMessagePCD(str(NewName))

    def addExplainSubjectPCD(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'.//C_C501/D_5245[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//D_5482[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_5482[@id="{FixIds}"]').text
    def addExplainSubjectPCD2(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'.//C_C501/D_5245[@id="{FixIds}"]/..'), str(DataElementName)+"Zahlungsbedingungen")
        if root.find(f'.//D_5482[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_5482[@id="{FixIds}"]').text
    def addExplainMessagePCD(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
        if root.find(f'.//D_5482[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_5482[@id="{FixIds}"]').text

    def addExplainSubjectC112(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
        if root.find(f'.//C_C112/D_2152[@id="{FixIds}"]') != None:
            if root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]') != None:
                if root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]') != None:
                    if root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]') != None:
                        added.text =root.find(f'.//C_C112/D_2152[@id="{FixIds}"]').text + root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]').text 
                    else: 
                        added.text =root.find(f'.//C_C112/D_2152[@id="{FixIds}"]').text + root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]').text
                else: 
                    if root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]') != None:
                        added.text =root.find(f'.//C_C112/D_2152[@id="{FixIds}"]').text + root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]').text 
                    else: 
                        added.text =root.find(f'.//C_C112/D_2152[@id="{FixIds}"]').text + root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]').text
            else: 
                if root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]') != None:
                    if root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]') != None:
                        added.text =root.find(f'.//C_C112/D_2152[@id="{FixIds}"]').text  + root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]').text 
                    else: 
                        added.text =root.find(f'.//C_C112/D_2152[@id="{FixIds}"]').text  + root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]').text 
        else: 
            if root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]') != None:
                if root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]') != None:
                    if root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]') != None:
                        added.text = root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]').text 
                    else: 
                        added.text = root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]').text
                else: 
                    if root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]') != None:
                        added.text = root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]').text 
                    else: 
                        added.text = root.find(f'.//C_C112/ArtZeitspanne[@id="{FixIds}"]').text 
            else: 
                if root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]') != None:
                    if root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]') != None:
                        added.text = root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]').text + root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]').text 
                    else: 
                        added.text = root.find(f'.//C_C112/Zeitbezug[@id="{FixIds}"]').text
                else: 
                    if root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]') != None:
                        added.text = root.find(f'.//C_C112/Zahlungsbezugstermin[@id="{FixIds}"]').text 
                    else: 
                        None
                   
    def addExplainSubject4347(DataElementName):
        FixIds = elem.attrib['id']
        FixIds1 = str(int(elem.attrib['id'])+1)
        FixIds2 = str(int(elem.attrib['id'])+2)
        FixIds3 = str(int(elem.attrib['id'])+3)
        if root.find(f'.//C_C212[@id="{FixIds1}"]/..') != None:
            added= ET.SubElement(root.find(f'.//C_C212[@id="{FixIds1}"]/..'), str(DataElementName))
            if root.find(f'.//D_EC212[@id="{FixIds1}"]') != None:
                added.text =root.find(f'.//D_EC212[@id="{FixIds1}"]').text 
        if root.find(f'.//C_C212_2[@id="{FixIds2}"]/..') != None:
            added= ET.SubElement(root.find(f'.//C_C212_2[@id="{FixIds2}"]/..'), str(DataElementName))
            if root.find(f'.//D_EC212[@id="{FixIds2}"]') != None:
                added.text =root.find(f'.//D_EC212[@id="{FixIds2}"]').text
        if root.find(f'.//C_C212_3[@id="{FixIds3}"]/..') != None:
            added= ET.SubElement(root.find(f'.//C_C212_3[@id="{FixIds3}"]/..'), str(DataElementName))
            if root.find(f'.//D_EC212[@id="{FixIds3}"]') != None:
                added.text =root.find(f'.//D_EC212[@id="{FixIds3}"]').text
    def addExplainSubject43475(DataElementName):
        FixIds = elem.attrib['id']
        FixIds4 = str(int(elem.attrib['id']) -1)
        FixIds5 = str(int(elem.attrib['id']) -2)
        if root.find(f'.//C_C212[@id="{FixIds4}"]/..') != None:
            if root.find(f'.//D_4347[@id="{FixIds5}"]/..') == None: 
                added= ET.SubElement(root.find(f'.//C_C212[@id="{FixIds4}"]/..'), str(DataElementName))
                if root.find(f'.//D_EC212[@id="{FixIds4}"]') != None:
                    added.text =root.find(f'.//D_EC212[@id="{FixIds4}"]').text
        if root.find(f'.//C_C212_2[@id="{FixIds4}"]/..') != None:
            if root.find(f'.//D_4347[@id="{FixIds5}"]/..') == None:
                added= ET.SubElement(root.find(f'.//C_C212[@id="{FixIds}"]/..'), str(DataElementName))
                if root.find(f'.//D_EC212[@id="{FixIds}"]') != None:
                    added.text =root.find(f'.//D_EC212[@id="{FixIds4}"]').text
        if root.find(f'.//C_C212_3[@id="{FixIds4}"]/..') != None:
            if root.find(f'.//D_4347[@id="{FixIds5}"]/..') == None:
                added= ET.SubElement(root.find(f'.//C_C212[@id="{FixIds}"]/..'), str(DataElementName))
                if root.find(f'.//D_EC212[@id="{FixIds}"]') != None:
                    added.text =root.find(f'.//D_EC212[@id="{FixIds4}"]').text
        if root.find(f'.//C_C212_4[@id="{FixIds4}"]/..') != None:
            if root.find(f'.//D_4347[@id="{FixIds5}"]/..') == None:
                added= ET.SubElement(root.find(f'.//C_C212[@id="{FixIds}"]/..'), str(DataElementName))
                if root.find(f'.//D_EC212[@id="{FixIds}"]') != None:
                    added.text =root.find(f'.//D_EC212[@id="{FixIds4}"]').text      

    def addExplainSubjectTAX(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//C_C243[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//D_5278[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_5278[@id="{FixIds}"]').text
    def addExplainMessageTAX(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
        if root.find(f'.//D_5278[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_5278[@id="{FixIds}"]').text
    def PositionOrMessageTAX(NewName):
        if parentgroupTAX == "GGroup48" or parentgroupTAX == "GGroup50": 
                addExplainMessageTAX(str(NewName))
        else:
            addExplainSubjectTAX(str(NewName))

    def addExplainSubjectCUX(DataElementName):
        FixIds = elem.attrib['id']
        added= ET.SubElement(root.find(f'.//C_C504[@id="{FixIds}"]/..'), str(DataElementName))
        if root.find(f'.//D_Wae[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_Wae[@id="{FixIds}"]').text
    def addExplainMessageCUX(DataElementName):
        FixIds = elem.attrib['id']
        mIds = elem.attrib['mid']
        added= ET.SubElement(root.find(f'Message[@mid="{mIds}"]'), str(DataElementName))
        if root.find(f'.//D_Wae[@id="{FixIds}"]') != None:
            added.text =root.find(f'.//D_Wae[@id="{FixIds}"]').text
    
    for elem in tree.iter():
        if elem.tag == "D_1004":
            addExplainSubjectD1004("Dokumentennummer")
        if elem.tag == "D_2005":
            parentDTM = root.find(f'.//{elem.tag}[@id="{elem.attrib["id"]}"]/..')
            parentgroupDTM =(root.find(f'.//{parentDTM.tag}[@id="{elem.attrib["id"]}"]/..').attrib["parent"])
            if elem.text == "2":
                PositionOrMessageDTM("geforderter_Liefertermin")
            elif elem.text == "3":
                PositionOrMessageDTM("Rechnungsdatum")
            elif elem.text == "4":
                PositionOrMessageDTM("Bestelldatum")
            elif elem.text == "7":
                PositionOrMessageDTM("Gueltigkeitsdatum")
            elif elem.text == "11":
                PositionOrMessageDTM("Versanddatum")
            elif elem.text == "12":
                PositionOrMessageDTM("Faelligkeitsdatum_bei_Skontoabzug")
            elif elem.text == "13":
                PositionOrMessageDTM("Faelligkeitsdatum_bei_Zahlung_ohne_Abzug")
            elif elem.text == "35":
                PositionOrMessageDTM("tatsaechliches_Lieferdatum")
            elif elem.text == "50":
                PositionOrMessageDTM("Wareneingangsdatum")
            elif elem.text == "134":
                PositionOrMessageDTM("Wechselkursdatum")
            elif elem.text == "137":
                PositionOrMessageDTM("Dokumenten_oder_Nachrichten_Datum")
            elif elem.text == "140":
                PositionOrMessageDTM("Zahlungsfaelligkeitsdatum")
            elif elem.text == "171":
                PositionOrMessageDTM("Referenzdatum")
            elif elem.text == "209":
                PositionOrMessageDTM("ValutaDatum")
            elif elem.text == "263":
                PositionOrMessageDTM("Abechnungszeitraum")
            elif elem.text == "325":
                PositionOrMessageDTM("Steuerperiode")
            elif elem.text == "326":
                PositionOrMessageDTM("Belastungsperiode")
            elif elem.text == "343":
                PositionOrMessageDTM("Datum_Rabattbeendigung")
            else: 
                PositionOrMessageDTM("nicht_vorhanden")
        if elem.tag == "D_3035":
            parentNAD = root.find(f'.//{elem.tag}[@id="{elem.attrib["id"]}"]/..')
            parentgroupNAD = parentNAD.attrib["parent"]
            if elem.text == "AB":
                PositionOrMessageNAD("Verkaufs_Agent")
                AgentRole("SalesAgent")
            elif elem.text == "BO":
                PositionOrMessageNAD("Broker_oder_Verkaufsbuero")
                AgentRole("BrokerOrSalesOffice")
            elif elem.text == "BS":
                PositionOrMessageNAD("Berechnen_und_liefern_an")
                AgentRole("CalculateAndDeliverTo")
            elif elem.text == "BY":
                PositionOrMessageNAD("Kaeufer")
                AgentRole("Buyer")
            elif elem.text == "CN":
                PositionOrMessageNAD("Empfaenger")
                AgentRole("Recipient")
            elif elem.text == "CPE":
                PositionOrMessageNAD("Zentralregulierer_EAN_Code")
                AgentRole("CentralRegulator")
            elif elem.text == "DP":
                PositionOrMessageNAD("Lieferanschrift")
                AgentRole("DeliveryParty")
            elif elem.text == "II":
                PositionOrMessageNAD("Rechnungssteller")
                AgentRole("InvoicingParty")
            elif elem.text == "IV":
                PositionOrMessageNAD("Rechnungsempfaenger")
                AgentRole("Invoicee")
            elif elem.text == "PE":
                PositionOrMessageNAD("Zahlungsempfaenger")
            elif elem.text == "PR":
                PositionOrMessageNAD("Bezahler")
                AgentRole("Payee")
            elif elem.text == "PW":
                PositionOrMessageNAD("Auslieferungspartei")
                AgentRole("DespatchParty")
            elif elem.text == "RE":
                PositionOrMessageNAD("Empfaenger_der_Rechnungsregulierung")
                AgentRole("RecipientOfInvoiceRegulation")
            elif elem.text == "RG":
                PositionOrMessageNAD("Rechnungsregulier")
                AgentRole("Regulator")
            elif elem.text == "SCO":
                PositionOrMessageNAD("Unternehmenszentrale_des_Lieferanten")
                AgentRole("SuppliersCompanyHeadquarter")
            elif elem.text == "SE":
                PositionOrMessageNAD("Verkaeufer")
                AgentRole("Seller")
            elif elem.text == "SN":
                PositionOrMessageNAD("Lagernummer")
                AgentRole("WarehouseNumber")
            elif elem.text == "SR":
                PositionOrMessageNAD("Beauftrageter_oder_Agent_des_Lieferanten")
                AgentRole("RepresentativeOrAgentOfSupplier")
            elif elem.text == "ST":
                PositionOrMessageNAD("Versenden_an")
                AgentRole("SendTo")
            elif elem.text == "SU":
                PositionOrMessageNAD("Lieferant")
                AgentRole("Supplier")
            elif elem.text == "WS":
                PositionOrMessageNAD("Grosshaendler")
                AgentRole("Wholesaler")
            elif elem.text == "UC":
                PositionOrMessageNAD("Endempfaenger")
                AgentRole("FinalConsignee")
            else: 
                PositionOrMessageNAD("nicht_vorhanden")
        if elem.tag == "D_1153":
            parentRFF = root.find(f'.//{elem.tag}[@id="{elem.attrib["id"]}"]/..')
            parentgroupRFF =(root.find(f'.//{parentRFF.tag}[@id="{elem.attrib["id"]}"]/..').attrib["parent"])
            if elem.text == "AAB":
                PositionOrMessageRFF("Proforma_Rechnungsnummer") 
            elif elem.text == "AAJ":
                PositionOrMessageRFF("Nummer_Lieferauftrag")
            elif elem.text == "AAK":
                PositionOrMessageRFF("Nummer_Lieferschein") 
            elif elem.text == "AAG":
                PositionOrMessageRFF("Angebotsnummer")  
            elif elem.text == "ABD":
                PositionOrMessageRFF("Zolltarifnummer")
            elif elem.text == "ABO":
                PositionOrMessageRFF("Referenz_des_Absenders")
            elif elem.text == "ACE":
                PositionOrMessageRFF("zugehoerige_Dokumentennummer") 
            elif elem.text == "AP":
                PositionOrMessageRFF("Nummer_des_Forderungskontos")   
            elif elem.text == "AFO":
                PositionOrMessageRFF("Referenz_des_Beguenstigten") 
            elif elem.text == "ALL":
                PositionOrMessageRFF("Nummer_eines_Buendels_von_Nachrichten")
            elif elem.text == "ALO":
                PositionOrMessageRFF("Wareneingangsmeldung_Nummer")
            elif elem.text == "API":
                PositionOrMessageRFF("Zusaetzliche_Partneridentifikation_EAN_Code")
            elif elem.text == "BC":
                PositionOrMessageRFF("Vertragsnummer_des_Kaeufers")
            elif elem.text == "CIN":
                PositionOrMessageRFF("Nummer_einr_konsolidierten_Rechnung_EAN_Code")
            elif elem.text == "CD":
                PositionOrMessageRFF("Gutschreliftsnummer")
            elif elem.text == "COE":
                PositionOrMessageRFF("Referenznummer_zu_einem_Geschaeftskontauszug_EAN_Code") 
            elif elem.text == "CR":
                PositionOrMessageRFF("Referenzsnummer_des_Kunden")
            elif elem.text == "CT":
                PositionOrMessageRFF("Vertragsnummer")
            elif elem.text == "DL":
                PositionOrMessageRFF("Nummer_der_Belastungsanzeige")
            elif elem.text == "DQ":
                PositionOrMessageRFF("Lieferscheinnummer")
            elif elem.text == "FC":
                PositionOrMessageRFF("Steuernummer")
            elif elem.text == "FI":
                PositionOrMessageRFF("Bezeichner_Dateizeilen")
            elif elem.text == "GN":
                PositionOrMessageRFF("Referenznummer_Regierung")
            elif elem.text == "HS":
                PositionOrMessageRFF("Nummer_harmonisiertes_System")
            elif elem.text == "IA":
                PositionOrMessageRFF("Interne_Lieferantennummer")  
            elif elem.text == "IP":
                PositionOrMessageRFF("Import_Lizenznummer") 
            elif elem.text == "IT":
                PositionOrMessageRFF("Interne_Kundennummer")  
            elif elem.text == "IV":
                PositionOrMessageRFF("Rechnungsnummer")
            elif elem.text == "LI":
                PositionOrMessageRFF("Referenznummer_der_Position")  
            elif elem.text == "ON":
                PositionOrMessageRFF("Auftragsnummer_Kaeufer")
            elif elem.text == "PL":
                PositionOrMessageRFF("Nummer_der_Preisliste")  
            elif elem.text == "PQ":
                PositionOrMessageRFF("Zahlungsreferenz")
            elif elem.text == "PY":
                PositionOrMessageRFF("Kontonummer_des_Zahlungsempfaenger") 
            elif elem.text == "RF":
                PositionOrMessageRFF("Exportreferenznummer")
            elif elem.text == "SS":
                PositionOrMessageRFF("Referenznummer_des_Verkaeufers")
            elif elem.text == "SZ":
                PositionOrMessageRFF("Spezifikationsnummer") 
            elif elem.text == "VA":
                PositionOrMessageRFF("Umsatzsteuernummer")
                #PositionOrMessageRFF("Umsatzsteuernummer_"+ root.find(f'.//D_PaFu[@nid="{nIds}"]').text)
            elif elem.text == "VN":
                PositionOrMessageRFF("Auftragsnummer_Lieferant") 
            elif elem.text == "XA":
                PositionOrMessageRFF("Unternehmes_oder_Ort_Regisstriernummer")
            else: 
                PositionOrMessageRFF("nicht_vorhanden")
        if elem.tag == "D_3035":
            if elem.text == "PB":
                addExplainSubjectFII("Zahlendes_Kreditinstitut")
            elif elem.text == "RB":
                addExplainSubjectFII("Empfangendes_Kreditinstitut") 
        if elem.tag == "D_4451":
            if elem.text =="AAA":
                addExplainSubjectFTX("Warenbeschreibung")
            elif elem.text =="AAI":
                addExplainSubjectFTX("Generelle_Informationen")
            elif elem.text =="AAK":
                addExplainSubjectFTX("Nummer_Lieferschein")
            elif elem.text =="CUS":
                addExplainSubjectFTX("Informatioen_zur_Zollerklaerung")
            elif elem.text =="CHG":
                addExplainSubjectFTX("Aenderungsinformationen")
            elif elem.text =="INV":
                addExplainSubjectFTX("Anweisung_fur_Rechnungssteller")
            elif elem.text =="OSI": 
                addExplainSubjectFTX("Andere_Serviceinformationen")
            elif elem.text =="PUR": 
                addExplainSubjectFTX("Beschaffungsinformation")
            elif elem.text =="REG": 
                addExplainSubjectFTX("Meldeinformationen")
            elif elem.text =="SUR":
                addExplainSubjectFTX("Lieferantenhinweis")
            elif elem.text =="ZZZ":
                addExplainSubjectFTX("Bilateral_vereinbart")
            else:
                addExplainSubjectFTX("nicht_vorhanden")
        if elem.tag == "D_3139":
            if elem.text == "AD":
                addExplainSubjectCTA("Ansprechpartner_Buchhaltung")
            elif elem.text == "AP":
                addExplainSubjectCTA("Ansprechpartner_Kreditorenbuchhaltung")
            elif elem.text == "AR":
                addExplainSubjectCTA("Ansprechpartner_Debitorenbuchaltung")
            elif elem.text == "GR":
                addExplainSubjectCTA("Ansprechpartner_Wareneingang")
            elif elem.text == "IC":
                addExplainSubjectCTA("Ansprechpartner_Information")
            elif elem.text == "SR":
                addExplainSubjectCTA("Ansprechpartner_Verkaufsabteilung")
            elif elem.text == "PD":
                addExplainSubjectCTA("Ansprechpartner_Einkaufabteilung")
            else:
                addExplainSubjectCTA("nicht_vorhanden")
        if elem.tag == "D_3155":
            if elem.text == "EM":
                addExplainSubjectCOM("Ansprechpartner_EmailAdresse")
            elif elem.text == "FX":
                addExplainSubjectCOM("Ansprechpartner_TelefaxNummer")
            elif elem.text == "TE":
                addExplainSubjectCOM("Ansprechpartner_TelefonNummer")
            elif elem.text == "TL":
                addExplainSubjectCOM("Ansprechpartner_TelexNummer")
            elif elem.text == "XF":
                addExplainSubjectCOM("Ansprechpartner_X400Nummer")
            else:
                addExplainSubjectCOM("nicht_vorhanden")
        if elem.tag == "D_4055":
            if elem.text == "1":
                addExplainSubjectTOD("Preis_Bedingungen")
            if elem.text == "3":
                addExplainSubjectTOD("PreisUndAuslieferungsbedingung")
            elif elem.text == "6":
                addExplainSubjectTOD("Lieferbedingung")
            else:
                addExplainSubjectTOD("nicht_vorhanden")
        if elem.tag == "D_5025":
            group = elem.attrib['group']
            parentMOA = root.find(f'.//{elem.tag}[@id="{elem.attrib["id"]}"]/..')
            parentgroupMOA =(root.find(f'.//{parentMOA.tag}[@id="{elem.attrib["id"]}"]/..').attrib["parent"])
            if elem.text == "1":
                PositionOrMessageMOA("Umsatzsteuer_erster_Wert")
            elif elem.text == "8":
                PositionOrMessageMOA( root.find(f'.//D_AlcEx[@group="{group}"]').text + "sbetrag") # Integration der Unterscheding von zu- und Abschlag 
            elif elem.text == "9":
                PositionOrMessageMOA("Faelliger_Betrag_oder_zahlbarerBetrag")
            elif elem.text == "12":
                PositionOrMessageMOA("Uebermittelter_Betrag")
            elif elem.text == "21":
                PositionOrMessageMOA("Barzahlungsrabatt")
            elif elem.text == "23":
                PositionOrMessageMOA("Zuschlagsbetrag")
            elif elem.text == "25":
                PositionOrMessageMOA("Zu_Abschlagsbasis")
            elif elem.text == "52":
                PositionOrMessageMOA("Abzug_Rabatt")
            elif elem.text == "53":
                PositionOrMessageMOA("Faelliger_Abzugsbetrag")
            elif elem.text == "56":
                PositionOrMessageMOA("Steuergrundbetrag")
            elif elem.text == "64":
                PositionOrMessageMOA("Frachtgebuehr")
            elif elem.text == "66":
                PositionOrMessageMOA("WarenpositionInsgesamt")
            elif elem.text == "77":
                PositionOrMessageMOA("Rechnungsbetrag")
            elif elem.text == "79":
                PositionOrMessageMOA("Gesamtpositionsbetrag")
            elif elem.text == "86":
                PositionOrMessageMOA("Gesamtbetrag_Nachricht")
            elif elem.text == "98":
                PositionOrMessageMOA("Originalbetrag")
            elif elem.text == "109":
                PositionOrMessageMOA("Zahlungskuerzung")
            elif elem.text == "113":
                PositionOrMessageMOA("Vorausbezahlter_Betrag")
            elif elem.text == "124":
                PositionOrMessageMOA("Steuerbetrag")
            elif elem.text == "125":
                PositionOrMessageMOA("Steuerpflichtiger_Betrag")
            elif elem.text == "128":
                PositionOrMessageMOA("Gesamtbetrag")
            elif elem.text == "129":
                PositionOrMessageMOA("Gesamtbetrag_unterliegt_Zahlungskuerzung")
            elif elem.text == "131":
                PositionOrMessageMOA("GesamtZu_Abschlaege")
            elif elem.text == "146":
                PositionOrMessageMOA("Preis_pro_Einheit")
            elif elem.text == "150":
                PositionOrMessageMOA("Mehrwertsteuer_Betrag")
            elif elem.text == "176":
                PositionOrMessageMOA("Gesamter_Zoll_Steuer_Gebuehrenbetrag_der_Nachricht")
            elif elem.text == "201":
                PositionOrMessageMOA("Strafbetrag")
            elif elem.text == "203":
                PositionOrMessageMOA("Positionsbetrag")
            elif elem.text == "204":
                PositionOrMessageMOA("Abschlagsbetrag")
            elif elem.text == "236":
                PositionOrMessageMOA("Betrag_unterliegt_einer_Preisberichtigung")
            else:
                PositionOrMessageMOA("nicht_vorhanden")
        if elem.tag == "D_7143":
            #parentC212 = root.find(f'.//{elem.tag}[@id="{elem.attrib["id"]}"]/..')
            #parentgroupC212 =(root.find(f'.//{parentC212.tag}[@id="{elem.attrib["id"]}"]/..').attrib["parent"])
            if elem.text == "BP":
                addExplainSubjectC212("Teilnummer_des_Kaeufers")
            elif elem.text == "EN":
                addExplainSubjectC212("International_Article_Number")
            elif elem.text == "PV":
                addExplainSubjectC212("Nummer_der_Aktionsvariante")
            elif elem.text == "HS":
                addExplainSubjectC212("Harmonisiertes_System")
            elif elem.text == "GN":
                addExplainSubjectC212("Nationaler_Produktgruppencode")
            elif elem.text == "IN":
                addExplainSubjectC212("Artikelnummer_des_Kaeufers")
            elif elem.text == "MF":
                addExplainSubjectC212("Artikelnummer_des_Herstellers")
            elif elem.text == "LI":
                addExplainSubjectC212("Positionszeilennummer")
            elif elem.text == "SA":
                addExplainSubjectC212("Artikelnummer_des_Lieferanten")
            elif elem.text == "UP":
                addExplainSubjectC212("Universal_Prodcut_Code" )
            else: 
                addExplainSubjectC212("nicht_vorhanden")
        if elem.tag == "D_6063":
            if elem.text == "1":
                addExplainSubjectQTY("_Diskret")
            elif elem.text == "12":
                addExplainSubjectQTY("_Sendungen")
            elif elem.text == "46":
                addExplainSubjectQTY("_Geliefert")
            elif elem.text == "47":
                addExplainSubjectQTY("_Berechnet")
            elif elem.text == "59":
                addExplainSubjectQTY("_der_Verbrauchereinheiten_in_einer_Handelseinheit")
            elif elem.text == "61":
                addExplainSubjectQTY("_Retour")
            elif elem.text == "131":
                addExplainSubjectQTY("_Liefer")
            elif elem.text == "192":
                addExplainSubjectQTY("_ohne_Berechnung")
            elif elem.text == "194":
                addExplainSubjectQTY("_Erhalten_und_akzeptiert")
            else: 
                addExplainSubjectQTY("nicht_vorhanden")
        if elem.tag == "D_6063":
            if elem.text == "1":
                addExplainSubjectQTY2("Diskrete_Menge_Einheit")
            elif elem.text == "12":
                addExplainSubjectQTY2("Ausgelieferte_Menge_Einheit")
            elif elem.text == "46":
                addExplainSubjectQTY2("Gelieferte_Menge_Einheit")
            elif elem.text == "47":
                addExplainSubjectQTY2("Berechnete_Menge_Einheit")
            elif elem.text == "59":
                addExplainSubjectQTY2("Anzahl_der_Verbrauchereinheiten_in_einer_Handelseinheit")
            elif elem.text == "61":
                addExplainSubjectQTY2("Retourmenge_Einheit")
            elif elem.text == "131":
                addExplainSubjectQTY2("Liefermenge_Einheit")
            elif elem.text == "192":
                addExplainSubjectQTY2("Menge_ohne_Berechnung_Einheit")
            elif elem.text == "194":
                addExplainSubjectQTY2("Erhalten_und_akzeptiert_Einheit")
            else: 
                addExplainSubjectQTY2("nicht_vorhanden")
        if elem.tag == "D_5125":
            if elem.text == "AAA":
                addExplainSubjectPRI("Nettokalkulation")
            elif elem.text == "AAB":
                addExplainSubjectPRI("Bruttokalkulation")
            elif elem.text == "GRP":
                addExplainSubjectPRI("Bruttopreis_pro_Einheit")
            elif elem.text == "INV":
                addExplainSubjectPRI("Rechnungspreis")
            elif elem.text == "NTP":
                addExplainSubjectPRI("Nettopreis_pro_Einheit")
            else: 
                addExplainSubjectPRI("nicht_vorhanden")
        if elem.tag == "D_6311":
            if elem.text == "AAE":
                addExplainSubjectMEA("Masangabe")
            elif elem.text == "PD":
                addExplainSubjectMEA("Physische_Abmessung")
            elif elem.text == "SO":
                addExplainSubjectMEA("Lagerbeschraenkung")
            elif elem.text == "TL":
                addExplainSubjectMEA("Beschraekung_Transportmittels")
            else:
                addExplainSubjectMEA("nicht_vorhanden")
        if elem.tag == "D_6313":
            if elem.text == "AAA":
                addExplainSubjectMEA2("Nettogewicht_pro_Einheit")
            elif elem.text == "AAF":
                addExplainSubjectMEA2("Nettonettogewicht")
            elif elem.text == "HT":
                addExplainSubjectMEA2("Hoehenmass")
            elif elem.text == "LN":
                addExplainSubjectMEA2("Laengenmassangaben")
            elif elem.text == "WD":
                addExplainSubjectMEA2("Breitenabmessung")
            else: 
                addExplainSubjectMEA2("nicht_vorhanden")
        if elem.tag == "D_5463":
            parentgroupALC = (root.find(f'.//{elem.tag}[@id="{elem.attrib["id"]}"]/..').attrib["parent"])
            if elem.text == "A":
                PositionOrMessageALC("Abschlag")
            elif elem.text == "C":
                PositionOrMessageALC("Zuschlag")
            elif elem.text == "N":
                PositionOrMessageALC("Kein_Abschlag_Zuschlag")
            else: 
                PositionOrMessageALC("nicht_vorhanden")
        if elem.tag == "D_5245":
            group = elem.attrib['group']
            parentPCD = root.find(f'.//{elem.tag}[@id="{elem.attrib["id"]}"]/..')
            parentgroupPCD =(root.find(f'.//{parentPCD.tag}[@id="{elem.attrib["id"]}"]/..').attrib["parent"])
            if elem.text == "1":
                PositionOrMessagePCD("AbschlagProzentsatz")
            elif elem.text == "2":
                PositionOrMessagePCD("ZuschlagProzentsatz")
            elif elem.text == "3":
                surdis = root.find(f'.//D_AlcEx[@group="{group}"]').text
                PositionOrMessagePCD( str(surdis)+"Prozentsatz")
            elif elem.text == "7":
                PositionOrMessagePCD("RechnungsProzentsatz")
            elif elem.text == "12":
                PositionOrMessagePCD("AbzugProzentsatz")
            elif elem.text == "15":
                PositionOrMessagePCD("StrafProzentsatz")
            else: 
                PositionOrMessagePCD("nicht_vorhanden")
        if elem.tag == "C_C112":
            addExplainSubjectC112("ZahlungsbezugsterminTage")
        if elem.tag == "D_4347":
            if elem.text == "1":
                addExplainSubject43475("Produktidentifikation")
                addExplainSubject4347("Zusaetzliche_Produktidentifikation")
            elif elem.text == "4":
                addExplainSubject4347("Produktidentifikation")
            elif elem.text == "5":
                addExplainSubject4347("Produktidentifikation")
                addExplainSubject43475("Produktidentifikation")
            else:
                addExplainSubject4347("nicht_vorhanden")  
        if elem.tag == "D_5305":
            if elem.text == "E":
                FixIds = elem.attrib['id']
                added = ET.SubElement(root.find(f'.//C_C243[@id="{FixIds}"]'), "D_5278")
                added.text == "0"
        if elem.tag == "D_5153":
            parentTAX = root.find(f'.//{elem.tag}[@id="{elem.attrib["id"]}"]/..')
            parentgroupTAX =(root.find(f'.//{parentTAX.tag}[@id="{elem.attrib["id"]}"]/..').attrib["parent"])
            if elem.text == "GST":
                PositionOrMessageTAX("Waren_Dienstleistungssteuer")
            elif elem.text == "VAT":
                PositionOrMessageTAX( "Mehrwertsteuer")
            else: 
                PositionOrMessageTAX("nicht_vorhanden")
        if elem.tag == "D_6343":
            if elem.text == "4":
                addExplainMessageCUX("WaehrungRechnung")
            elif elem.text == "9":
                addExplainSubjectCUX( "WaehrungBestellung")
            elif elem.text == "10":
                addExplainSubjectCUX( "WaehrungPreisangabe")
            elif elem.text == "11":
                addExplainSubjectCUX( "WaehrungZahlung")
            else: 
                addExplainMessageCUX("nicht_vorhanden")
        if elem.tag == "D_6347":
            parentCUX = root.find(f'.//{elem.tag}[@id="{elem.attrib["id"]}"]/..')
            parentgroupCUX =(root.find(f'.//{parentCUX.tag}[@id="{elem.attrib["id"]}"]/..').attrib["parent"])
            if parentgroupCUX == "GGroup7":
                addExplainMessageCUX("Waehrung")
            else: 
                addExplainSubjectCUX("Waehrung")
        
    return tree.write(folder_path + 'INVOIC1.xml')

#Add Elemnts which combine the created descriping elment with the value of the described element 
def ProProcessingStep3():
    tree1 = ET.parse(folder_path +'INVOIC1.xml')
    root1 = tree1.getroot()

    def addProcess():
        mIds = elem.attrib['mid']
        added= ET.SubElement(root1.find(f'Message[@mid="{mIds}"]'), 'ProcessIdentification')
        added.text = "None"
        added.set('mid', str(mIds))

    for elem in tree1.iter():
        if elem.text != None:
            elem.text.replace(",",".")
            if 'nicht_vorhanden' in elem.text:
                print("Unbekannter Qualifier")
                print(elem)
        if elem.tag != None:
            if 'nicht_vorhanden' in elem.tag:
                print("Unbekannter Qualifier")
                print(elem)
            if elem.tag == "S_BGM": 
                addProcess()
            if elem.tag == "Kaeufer":
                FixIds = elem.attrib['id']
                mIds = elem.attrib['mid']
                if elem.text != None:
                    root1.find(f'.//ProcessIdentification[@mid="{mIds}"]').text =  "ProcessExample"
        if elem.text != None:
            elem.text = elem.text.replace(",",".")
        if elem.tag == "ProcessIdentification":
            process = elem.text 
        
    return (tree1.write(folder_path + 'INVOIC2.xml'),process)


def yarrrmlparser():
    p = Popen([folder_path + 'yarrrmlparser.sh'], stdout = PIPE , stderr = PIPE)
    p.communicate()
    p.wait()

def rmlmapper():
    p = Popen([folder_path + 'rmlmapper.sh'], stdout = PIPE , stderr = PIPE)
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
    #print(message_lines)
    for j in range(len(message_lines)):
        parts = message_lines[j].split(';')
        parts = [part.strip() for part in parts]
        message = parts[0].replace('Message:', '')
        print(message)   

    return v_text

