# Data

## Overview
This directory contains the data provided by the domain specialists in the form of ods files.

### Ontology
The general construct is that there are a number of ontologies, e.g. *cci*, *cmip*. This ontology name should be the prefix of any files relating to that ontology, e.g. *cmip-realms.ods.

### Concept Scheme
Within an ontology there are one or more concept schemes. A concept scheme is used to represent a controlled vocabulary or glossary.

### Concepts
Concepts are used to represent individual terms in a controlled vocablary or glossary.

## The Spreadsheets
### Ontology and Concept Schemes
Information about the an ontology and its concept schemes are contained in a single sheet in an ods file, with a file name in the format [ontologyName]-schemes.ods, e.g. *cci-schemes.ods*.

### Concepts
A set of terms (concepts) to be included in a vocabulary or glossary should be presented as a single sheet in an ods file, with a file name in the format [ontologyName]-[schemeName].ods, e.g. *cci-sensor.ods*. 

The order of the columns is meaningful.
* Column A - a URI fragment. The hostname and vocabulary name will be prepended to this value. This value must be unique in the context of the ontology.
* Column B - the preferred label. This value must be unique in the context of the ontology.
* Column C - the alternative label.
* Column D - a definition of the concept.

