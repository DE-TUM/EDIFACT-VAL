import os 
from os import *
from subprocess import *
import time 

from EDIFACT_Val_Defintions import ProProcessingStep1, ProProcessingStep2, ProProcessingStep3, yarrrmlparser, rmlmapper, validates

if __name__ == '__main__':
    file_name = input('Name of the file to be validated in format name.xml: ')
    start = time.time()
    ProProcessingStep1(file_name)
    print(1)
    ProProcessingStep2()
    print(2)
    ProProcessingStep3()
    print(3)
    yarrrmlparser()
    print(4)
    rmlmapper()
    print(5)
    validates(ProProcessingStep3()[1])
    end = time.time()
    print('Total Time: {:5.3f}s'.format(end-start))
