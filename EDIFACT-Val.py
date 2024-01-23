import platform 
from os import *
from subprocess import *
import time 

from EDIFACT_Val_Functions import ProProcessingStep1, ProProcessingStep2, ProProcessingStep3, yarrrmlparser_bash, rmlmapper_bash, yarrrmlparser_batch, rmlmapper_batch, validates

if __name__ == '__main__':
    file_name = input('Name of the file to be validated in format name.xml: ')
    print(platform.system())
    if platform.system() == "Windows":
        start = time.time()
        ProProcessingStep1(file_name)
        ProProcessingStep2()
        ProProcessingStep3()
        yarrrmlparser_batch()
        rmlmapper_batch()
        validates(ProProcessingStep3()[1])
        end = time.time()
        print('Total Time: {:5.3f}s'.format(end-start))
    elif platform.system() == "Darwin":
        start = time.time()
        ProProcessingStep1(file_name)
        ProProcessingStep2()
        ProProcessingStep3()
        yarrrmlparser_bash()
        rmlmapper_bash()
        validates(ProProcessingStep3()[1])
        end = time.time()
        print('Total Time: {:5.3f}s'.format(end-start))
    elif platform.system() == "Linux":
        start = time.time()
        ProProcessingStep1(file_name)
        ProProcessingStep2()
        ProProcessingStep3()
        yarrrmlparser_bash()
        rmlmapper_bash()
        validates(ProProcessingStep3()[1])
        end = time.time()
        print('Total Time: {:5.3f}s'.format(end-start))
    else: 
        print("Unknown system")