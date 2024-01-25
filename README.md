# EDIFACT-VAL

EDIFACT-VAL is an automatic tool to validate the content of EDIFACT messages using Knowledge Graphs technologies. 

## Overview 

The EIDFACT-VAL tool contains the following steps: 

1: Invoice Pre-Processing:
  - Translation of the invoices into XML files

2: RDF Graph Creation of Invoices: 
  - YARRRML Mapping 
  - RML Mapping

3: RDF Validation:  
  - Constraints based on EDIFACT guidelines and reports based on domain experts  

All these steps are combined into one Python program called [EDIFACT-Val](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/80c39b8e2d579a63a7ee9213840585c6fad5d32c/src/EDIFACT-Val.py).

An overview of the EDIFACT Val tool can be seen here: 
![alt text](https://github.com/johannesmaekelburg/EDIFACT-VAL/blob/80c39b8e2d579a63a7ee9213840585c6fad5d32c/docs/EDIFACT-VAL%20Overview%20.png)

## Preparations

- Download or clone this repository.
- Install Python3; this code was tested with Python 3.12.1
- Install the required  packages with the following command:
   ```
  pip install -r requirements.txt
  ````
  
- Install [RMLmapper](https://github.com/RMLio/rmlmapper-java)
  - download and include the newest .jar file in the same folder as the other files 
- Install [yarrrml-parser](https://github.com/RMLio/yarrrml-parser)
  ```
  npm i -g @rmlio/yarrrml-parser
  ```


## Usage

Locate the Files from the Example folder in the src folder. 

Executing the program EDIFACT-Val.py:
```
python EDIFACT-Val.py
```
