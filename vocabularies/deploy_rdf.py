import os
import time

from rdflib import Graph
from rdflib.namespace import DC, OWL, SKOS
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

from settings import CCI, CCI_NAME_SPACE, CMIP, CMIP_NAME_SPACE, GCOS, \
    GCOS_NAME_SPACE, GRIB, GRIB_NAME_SPACE, NAME_SPACE_MAP, \
    HTML_DIRECTORY, ONTOLOGIES, SPARQL_DATA, SPARQL_QUERY, \
    SPARQL_UPDATE


def _delete_graph(ontology_name):
    store = _get_store()
    graph_iri = '%s/%s' % (SPARQL_DATA, ontology_name)
    graph = Graph(store=store, identifier=graph_iri)
    store.remove_graph(graph)


def _get_graph(ontology_name):
    store = _get_store()
    graph_iri = '%s/%s' % (SPARQL_DATA, ontology_name)
    graph = Graph(store=store, identifier=graph_iri)
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
    return graph


def _get_graph_from_file(_file):
    graph = Graph()
    source = "%s%s" % (HTML_DIRECTORY, _file)
    graph.parse(source=source, format='n3')
    return graph


def _get_store():
    store = SPARQLUpdateStore(queryEndpoint=SPARQL_QUERY,
                              update_endpoint=SPARQL_UPDATE,
                              postAsEncoded=False)
    return store


def _recreate_graph(ontology):
    _delete_graph(ontology)
    new_graph = _get_graph(ontology)
    for _file in os.listdir(HTML_DIRECTORY):
        if _file.endswith(".ttl") and _file.startswith(ontology):
            print("%s Processing file %s" % (time.strftime("%H:%M:%S"), _file))       
            graph_from_file = _get_graph_from_file(_file)
            for res in graph_from_file:
                new_graph.add(res)
    new_graph.close()    


def deploy():
    for ontology in ONTOLOGIES:
        _recreate_graph(ontology)   
    print "finished deploying rdf"


if __name__ == "__main__":
    deploy()
