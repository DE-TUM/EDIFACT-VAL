# EDIFACT-VAL

EDIFACT-VAL is an automatic tool to validate the content of EDIFACT messages using Knowledge Graphs technologies. 

## Overview 

The EIDFACT-VAL tool contains the following programs: 

1: Pre-Processing:
  - Python Programm for extension of the XML files

2: RDF Graph Creation for Invoices: 
  - YARRRML Mapping 
  - RML Mapping

3: RDF Validation:  
  - SHACL constraints for exemplary business processes 

All these steps are combined into one Python program called [EDIFACT-Val](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/40dfb22ac88682f0c76911820500c8c304b43c0b/EDIFACT-Val.py).

An overview of the EDIFACT Val tool can be seen here: 
![alt text](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/50bf72c91baedcef7736ddc71d5e5305335ee732/EDIFACT-VAL%20Overview%20.png)

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
