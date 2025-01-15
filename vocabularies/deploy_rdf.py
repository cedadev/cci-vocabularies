import os
import time

from rdflib import Graph
from rdflib.namespace import DC, OWL, SKOS
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

from vocabularies.settings import (
    CCI,
    CCI_SCHEME,
    CMIP,
    CMIP_SCHEME,
    GCOS,
    GCOS_SCHEME,
    GRIB,
    GRIB_SCHEME,
    SCHEME_MAP,
    HTML_DIRECTORY,
    ONTOLOGIES,
    SPARQL_GRAPH,
    SPARQL_QUERY,
    SPARQL_UPDATE,
)


def _delete_graph(ontology_name):
    store = _get_store()
    graph_iri = "%s/%s" % (SPARQL_GRAPH, ontology_name)
    print("graph:" + graph_iri)
    graph = Graph(store=store, identifier=graph_iri)
    store.remove_graph(graph)


def _get_graph(ontology_name):
    store = _get_store()
    graph_iri = "%s/%s" % (SPARQL_GRAPH, ontology_name)
    graph = Graph(store=store, identifier=graph_iri)
    graph.bind(ontology_name, "%s" % (SCHEME_MAP[ontology_name]))
    graph.bind("dc", DC)
    graph.bind("owl", OWL)
    graph.bind("skos", SKOS)

    if ontology_name == CCI:
        graph.bind(GCOS, GCOS_SCHEME)

    if ontology_name == CMIP:
        graph.bind(GCOS, GCOS_SCHEME)
        graph.bind(GRIB, GRIB_SCHEME)

    if ontology_name == GCOS:
        graph.bind(CCI, CCI_SCHEME)
        graph.bind(CMIP, CMIP_SCHEME)

    if ontology_name == GRIB:
        graph.bind(CMIP, CMIP_SCHEME)
    return graph


def _get_graph_from_file(_file):
    graph = Graph()
    graph.parse(source=_file, format="n3")
    return graph


def _get_store():
    store = SPARQLUpdateStore(
        queryEndpoint=SPARQL_QUERY, update_endpoint=SPARQL_UPDATE, postAsEncoded=False
    )
    print("update:" + SPARQL_UPDATE)
    return store


def _recreate_graph(ontology):
    _delete_graph(ontology)
    new_graph = _get_graph(ontology)
    _file = os.path.join(
        HTML_DIRECTORY,
        "ontology",
        ontology,
        ontology + "-content",
        ontology + "-ontology.ttl",
    )
    print("%s Processing file %s" % (time.strftime("%H:%M:%S"), _file))
    graph_from_file = _get_graph_from_file(_file)
    for res in graph_from_file:
        new_graph.add(res)
    new_graph.close()


def deploy():
    for ontology in ONTOLOGIES:
        _recreate_graph(ontology)
    print("finished deploying rdf")


if __name__ == "__main__":
    deploy()
