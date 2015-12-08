import os

from rdflib import Graph
from rdflib.namespace import DC, OWL, SKOS

from settings import CCI, CCI_NAME_SPACE, CMIP, CMIP_NAME_SPACE, GCOS, \
    GCOS_NAME_SPACE, GRIB, GRIB_NAME_SPACE, HTML_DIRECTORY, MODEL_DIRECTORY, \
    NAME_SPACE_MAP, ONTOLOGIES, CITO, GLOSSARY


def _get_graph(ontology_name):
    graph = Graph()
    graph.bind(ontology_name, "%s" % (NAME_SPACE_MAP[ontology_name]))
    graph.bind("dc", DC)
    graph.bind("owl", OWL)
    graph.bind("skos", SKOS)

    if ontology_name == CCI:
        graph.bind(GCOS, GCOS_NAME_SPACE)

    if ontology_name == CMIP:
        graph.bind(GCOS, GCOS_NAME_SPACE)
        graph.bind(GRIB, GRIB_NAME_SPACE)

    if ontology_name == GCOS:
        graph.bind(CCI, CCI_NAME_SPACE)
        graph.bind(CMIP, CMIP_NAME_SPACE)

    if ontology_name == GRIB:
        graph.bind(CMIP, CMIP_NAME_SPACE)

    if ontology_name == GLOSSARY:
        graph.bind('cito', CITO)
    return graph


def _get_graph_from_file(_file, ontology):
    graph = Graph()
    source = "%s%s" % (MODEL_DIRECTORY, _file)
    graph.parse(source=source, format='n3')
    return graph


def generate():
    for ontology in ONTOLOGIES:
        graph = _get_graph(ontology)  
        
        for _file in os.listdir(MODEL_DIRECTORY):
            if _file.endswith(".ttl") and _file.startswith(ontology):
                graph_from_file = _get_graph_from_file(_file, ontology)
                for res in graph_from_file:
                    graph.add(res)

        turtle = graph.serialize(format='turtle')
        file_name = ('%s/%s-ontology.ttl') % (HTML_DIRECTORY, ontology)
        ontology_file = open(file_name, mode='w')
        ontology_file.write(turtle)
        ontology_file.close()
    
        rdf = graph.serialize(format='xml')
        file_name = ('%s/%s-ontology.rdf') % (HTML_DIRECTORY, ontology)
        ontology_file = open(file_name, mode='w')
        ontology_file.write(rdf)
        ontology_file.close()
        
        graph.close() 


if __name__ == "__main__":
    generate()

