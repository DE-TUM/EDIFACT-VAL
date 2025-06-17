import platform
import os
import shutil

from general_edifact_to_enriched_xml import (
    EDIFACTToEnrichedXMLConverter,
    yarrrmlparser_bash, rmlmapper_bash,
    yarrrmlparser_batch, rmlmapper_batch,
    validates
)

if __name__ == '__main__':
    edi_files = ["ProcessTest.edi"]
    ttl_file = "ProcessExample"

    for edi_file in edi_files:
        if not os.path.isfile(edi_file):
            print(f"File not found: {edi_file}")
            continue

        base_name = os.path.splitext(os.path.basename(edi_file))[0]
        xml_output_file = "enriched_output.xml"

        print(f"\n--- Processing {edi_file} ---")

        try:
            with open(edi_file, "r", encoding="utf-8") as f:
                edi_data = f.read()
        except UnicodeDecodeError:
            print("UTF-8 decoding failed, trying ISO-8859-1")
            with open(edi_file, "r", encoding="iso-8859-1") as f:
                edi_data = f.read()

        converter = EDIFACTToEnrichedXMLConverter(edi_data)
        converter.convert()
        enriched_xml = converter.to_string()

        with open(xml_output_file, "w", encoding="utf-8") as f:
            f.write(enriched_xml)
        print(f"Enriched XML written to {xml_output_file}")

        print("Running transformation and validation")
        if platform.system() == "Windows":
            yarrrmlparser_batch()
            rmlmapper_batch()
        elif platform.system() in ["Darwin", "Linux"]:
            yarrrmlparser_bash()
            rmlmapper_bash()
        else:
            print("Unsupported platform")
            continue

        validation_output = validates(ttl_file)

        validation_report_file = os.path.join("evaluation", f"{base_name}_{ttl_file}_validation_report.ttl")
        os.makedirs("evaluation", exist_ok=True)
        with open(validation_report_file, "w", encoding="utf-8") as f:
            f.write(validation_output)
        print(f"Validation report saved to {validation_report_file}")

        final_output_file = os.path.join("evaluation", f"{base_name}.ttl")
        if os.path.isfile("invoice.ttl"):
            shutil.move("invoice.ttl", final_output_file)
            print(f"Final output file saved as {final_output_file}")
        else:
            print("invoice.ttl file not found.")
