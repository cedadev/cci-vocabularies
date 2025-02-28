# -*- coding: utf-8 -*-
import os
from pathlib import Path
from urllib.parse import urlparse

from rdflib import Graph
from rdflib.namespace import DC, OWL, RDF, SKOS

from vocabularies.settings import (
    CCI,
    CMIP,
    GCOS,
    GRIB,
    HTML_DIRECTORY,
    MODEL_DIRECTORY,
    NERC,
    ONTOLOGIES,
    CITO,
    GLOSSARY,
    ONTOLOGY_MAP,
    SCHEME_MAP,
    COLLECTION_MAP,
)


def _get_graph(ontology_name, is_ontology):
    graph = Graph()
    graph.bind(ontology_name, ONTOLOGY_MAP[ontology_name])
    graph.bind("%s-scheme" % ontology_name, "%s/" % SCHEME_MAP[ontology_name])
    graph.bind("%s-collection" % ontology_name, "%s" % COLLECTION_MAP[ontology_name])
    graph.bind("skos", SKOS)

    if is_ontology:
        graph.bind("dc", DC)
        graph.bind("owl", OWL)

    if ontology_name == CCI and is_ontology:
        graph.bind(GCOS, ONTOLOGY_MAP[GCOS])
        graph.bind(NERC, ONTOLOGY_MAP[NERC])

    if ontology_name == CMIP:
        graph.bind(GCOS, ONTOLOGY_MAP[GCOS])
        graph.bind(GRIB, ONTOLOGY_MAP[GRIB])

    if ontology_name == GCOS:
        graph.bind(CCI, ONTOLOGY_MAP[CCI])
        graph.bind(CMIP, ONTOLOGY_MAP[CMIP])

    if ontology_name == GRIB:
        graph.bind(CMIP, ONTOLOGY_MAP[CMIP])

    if ontology_name == GLOSSARY:
        graph.bind("cito", CITO)
    return graph


def _get_graph_from_file(_file):
    graph = Graph()
    source = os.path.join(MODEL_DIRECTORY, _file)
    graph.parse(source=source, format="n3", encoding="utf-8")
    return graph


def _write_ontology(graph, ontology):
    _dir = os.path.join(HTML_DIRECTORY, "ontology", ontology, ontology + "-content")

    json = graph.serialize(format="json-ld")
    file_name = os.path.join(_dir, ontology + "-ontology.json")
    with open(file_name, mode="w", encoding="utf-8") as ontology_file:
        ontology_file.write(json)

    turtle = graph.serialize(format="turtle")
    file_name = os.path.join(_dir, ontology + "-ontology.ttl")
    with open(file_name, mode="w", encoding="utf-8") as ontology_file:
        ontology_file.write(turtle)

    rdf = graph.serialize(format="xml")
    file_name = os.path.join(_dir, ontology + "-ontology.rdf")
    with open(file_name, mode="w", encoding="utf-8") as ontology_file:
        ontology_file.write(rdf)


def _write_files(graph, _type, ontology, name):
    _dir = os.path.join(HTML_DIRECTORY, _type, ontology, ontology + "-content", name)

    json = graph.serialize(format="json-ld")
    file_name = ("%s.json") % (_dir)
    with open(file_name, mode="w", encoding="utf-8") as collection_file:
        collection_file.write(json)

    turtle = graph.serialize(format="turtle")
    file_name = ("%s.ttl") % (_dir)
    with open(file_name, mode="w", encoding="utf-8") as collection_file:
        collection_file.write(turtle)

    rdf = graph.serialize(format="xml")
    file_name = ("%s.rdf") % (_dir)
    with open(file_name, mode="w", encoding="utf-8") as collection_file:
        collection_file.write(rdf)


def _get_name(url):
    path = urlparse(url).path
    bits = path.split("/")
    return bits[len(bits) - 1]


def generate():
    for ontology in ONTOLOGIES:
        graph = _get_graph(ontology, True)

        for _file in os.listdir(MODEL_DIRECTORY):
            if _file.endswith(".ttl") and _file.startswith(ontology):
                graph_from_file = _get_graph_from_file(_file)
                for res in graph_from_file:
                    graph.add(res)

        _write_ontology(graph, ontology)

        if ontology == GLOSSARY:
            continue

        # collections
        collections = graph.subjects(RDF.type, SKOS.Collection)
        for collection in collections:
            triples = graph.triples((collection, None, None))
            collection_graph = _get_graph(ontology, False)
            for t in triples:
                collection_graph.add(t)
            name = _get_name(collection)
            _write_files(collection_graph, "collection", ontology, name)

        # concept schemes
        concept_schemes = graph.subjects(RDF.type, SKOS.ConceptScheme)
        for concept_scheme in concept_schemes:
            triples = graph.triples((concept_scheme, None, None))
            concept_scheme_graph = _get_graph(ontology, False)
            for t in triples:
                concept_scheme_graph.add(t)
                concept_scheme_uri = t[0]
            # concepts in scheme
            concepts = graph.subjects(SKOS.inScheme, concept_scheme_uri)
            for concept in concepts:
                triples = graph.triples((concept, None, None))
                for t in triples:
                    concept_scheme_graph.add(t)

            name = _get_name(concept_scheme)
            _write_files(concept_scheme_graph, "scheme", ontology, name)

        graph.close()


if __name__ == "__main__":
    generate()
