# EDIFACT-VAL

EDIFACT-VAL is an automatic tool to validate the content of EDIFACT messages using Knowledge Graphs technologies. 

## Overview 

The EIDFACT-VAL tool contains the following steps: 

1: Pre-Processing:
  - [Python Programm](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/913b1bc12774e8f3c58c2ceca84b50f8093ec4bd/EDIFACT_Val_Defintions.py) for extension of the XML files 

2: RDF Graph Creation for Invoices: 
  - [YARRRML Mapping](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/913b1bc12774e8f3c58c2ceca84b50f8093ec4bd/general.yarrrml) 
  - [RML Mapping](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/913b1bc12774e8f3c58c2ceca84b50f8093ec4bd/general.rml.ttl) 

3: RDF Validation:  
  - [SHACL constraints](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/913b1bc12774e8f3c58c2ceca84b50f8093ec4bd/ProcessExample.ttl) for exemplary business processes 

All these steps are combined into one Python program called [EDIFACT-Val](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/913b1bc12774e8f3c58c2ceca84b50f8093ec4bd/EDIFACT-Val.py)

An overview of the EDIFACT Val tool can be seen here: 
![alt text](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/913b1bc12774e8f3c58c2ceca84b50f8093ec4bd/EDIFACT-VAL%20Overview%20.png)

## Preparations

- Download or clone this repository.
- Install the Python libraries:
  - ```xml.etree.ElementTree```
  - ```os```
  - ```pyshacl```
  - ```subprocess```
  
- Install [RMLmapper](https://github.com/RMLio/rmlmapper-java)
  - download and include the newest .jar file in the same folder as the other files 
- Install [yarrrml-parser](https://github.com/RMLio/yarrrml-parser)
  - ```npm i -g @rmlio/yarrrml-parser```


## Useage

```
python3 EDIFACT-Val.py
```
