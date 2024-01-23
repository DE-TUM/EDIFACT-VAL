import platform 
from os import *
from subprocess import *

from EDIFACT_Val_Functions import ProProcessingStep1, ProProcessingStep2, ProProcessingStep3, yarrrmlparser_bash, rmlmapper_bash, yarrrmlparser_batch, rmlmapper_batch, validates

if __name__ == '__main__':
    file_name_only  = input('Name of the message to be validated: ')
    file_name = file_name_only + ".xml"
    if platform.system() == "Windows":
        ProProcessingStep1(file_name)
        ProProcessingStep2()
        ProProcessingStep3()
        yarrrmlparser_batch()
        rmlmapper_batch()
        validates(ProProcessingStep3()[1])
    elif platform.system() == "Darwin":
        ProProcessingStep1(file_name)
        ProProcessingStep2()
        ProProcessingStep3()
        yarrrmlparser_bash()
        rmlmapper_bash()
        validates(ProProcessingStep3()[1])
    elif platform.system() == "Linux":
        ProProcessingStep1(file_name)
        ProProcessingStep2()
        ProProcessingStep3()
        yarrrmlparser_bash()
        rmlmapper_bash()
        validates(ProProcessingStep3()[1])
    else: 
        print("Unknown system")
