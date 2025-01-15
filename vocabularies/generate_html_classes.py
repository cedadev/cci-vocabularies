import codecs
import os

from rdflib.namespace import DC, OWL, RDF, RDFS, SKOS

from vocabularies.settings import (
    ONTOLOGIES,
    SPARQL_HOST_NAME,
    SPARQL_DATASET,
    HTML_DIRECTORY,
    ONTOLOGY_MAP,
    SPARQL_GRAPH,
    SPARQL_QUERY,
)
from vocabularies.generate_html.html import Helper


PREFIX = """
PREFIX dc:   <%s>
PREFIX owl:  <%s>
PREFIX rdf:  <%s>
PREFIX rdfs: <%s>
PREFIX skos: <%s>
""" % (
    DC,
    OWL,
    RDF,
    RDFS,
    SKOS,
)

FILE = None
ONTOLOGY_BASE_URI = None
FILE_BASE_URI = None
HELPER = None

GRAPH_STORE = {}


def write_head(ontology_name, found_classes, found_properties):
    abstract = None
    date = None
    description = None
    publisher = None
    rights = None
    title = None
    version = None
    creators = []
    contributors = []

    results = HELPER.get_ontology(ontology_name)
    for result in results:
        resources = HELPER.get_resources(ontology_name, result.subject)
        for res in resources:
            if res.p == DC.date:
                date = res.o
            if res.p == DC.description:
                description = res.o
            if res.p == DC.publisher:
                publisher = res.o
            if res.p == DC.rights:
                rights = res.o
            if res.p == DC.title:
                title = res.o
            if res.p == OWL.versionInfo:
                version = res.o
            if res.p == RDFS.comment:
                abstract = res.o
            if res.p == DC.creator:
                creators.append(res.o)
            if res.p == DC.contributor:
                contributors.append(res.o)

    FILE.write('<?xml version="1.0" encoding="utf-8"?>\n')
    FILE.write(
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'
    )
    FILE.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    FILE.write("<head>\n")
    FILE.write(
        '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n'
    )
    FILE.write("<title>%s</title>\n" % title)
    FILE.write('<link href="../../../vocab.css" rel="stylesheet" type="text/css" />\n')
    FILE.write("</head>\n")

    FILE.write("<body>\n")
    FILE.write('<div class="head">\n')
    FILE.write("<h1>%s</h1>\n" % title)

    FILE.write("<dl>\n")
    FILE.write("<dt>IRI:</dt>\n")
    FILE.write(
        '<dd><a href="%s">%s</a></dd>\n' % (ONTOLOGY_BASE_URI, ONTOLOGY_BASE_URI)
    )
    FILE.write("</dl>\n")

    FILE.write("<dl>\n")
    FILE.write("<dt>Date:</dt>\n")
    FILE.write("<dd>%s</dd>\n" % date)
    FILE.write("<dt>Current Version:</dt>\n")
    FILE.write("<dd>%s</dd>\n" % version)
    FILE.write("</dl>\n")

    FILE.write("<dl>\n")
    if len(creators) > 0:
        FILE.write("<dt>Authors:</dt>\n")
        for creator in creators:
            FILE.write("<dd>%s</dd>\n" % creator)
    if len(contributors) > 0:
        FILE.write("<dt>Contributors:</dt>\n")
        for contributor in contributors:
            FILE.write("<dd>%s</dd>\n" % contributor)
    FILE.write("</dl>\n")

    if publisher is not None:
        FILE.write("<dl>\n")
        FILE.write("<dt>Publisher:</dt>\n")
        FILE.write("<dd>%s</dd>\n" % publisher)
        FILE.write("</dl>\n")

    FILE.write("<dl>\n")
    FILE.write("<dt>Other visualisations:</dt>\n")
    FILE.write("<dd>Ontology source ")
    FILE.write('<a href="%s.json">json</a>, ' % FILE_BASE_URI)
    FILE.write('<a href="%s.rdf">rdf</a>, ' % FILE_BASE_URI)
    FILE.write('<a href="%s.ttl">ttl</a></dd>\n' % FILE_BASE_URI)
    FILE.write(
        '<dd><a href="%s">SPARQL endpoint</a>, dataset:%s, graph:%s/%s</dd>\n'
        % (SPARQL_QUERY, SPARQL_DATASET, SPARQL_GRAPH, ontology_name)
    )
    FILE.write("</dl>\n")

    FILE.write('<div class="copyright">\n')
    FILE.write('<span class="markdown">%s</span>\n' % rights)
    FILE.write("</div>\n")

    FILE.write("</div>\n")

    FILE.write("<hr />\n\n<h2>Abstract</h2>\n")
    FILE.write('<span class="markdown">%s</span>\n' % abstract)

    FILE.write('<div id="toc">\n')
    FILE.write("<h2>Table of Content</h2>\n")
    FILE.write("<ol>\n")
    FILE.write('<li><a href="#introduction">Introduction</a></li>\n')

    if found_classes:
        FILE.write('<li><a href="#classes">Classes</a></li>\n')

    if found_properties:
        FILE.write('<li><a href="#objectproperties">Object Properties</a></li>\n')

    FILE.write('<li><a href="#namedIndividuals">Named Individuals</a></li>\n')
    FILE.write('<li><a href="#namespacedeclarations">Namespace Declarations</a></li>\n')
    FILE.write('<li><a href="#acknowledgements">Acknowledgements</a></li>\n')
    FILE.write("</ol>\n")
    FILE.write("</div>\n")

    FILE.write('<div id="introduction">\n')
    FILE.write("<h2>Introduction</h2>\n")
    FILE.write('<span class="markdown">%s</span>\n' % description)
    FILE.write("</div>\n")


def do_stuff(ontology_name):
    classes = HELPER.get_classes(ontology_name)
    if len(classes) > 0:
        found_classes = True
    else:
        found_classes = False

    properties = HELPER.get_properties(ontology_name)
    if len(properties) > 0:
        found_properties = True
    else:
        found_properties = False

    write_head(ontology_name, found_classes, found_properties)

    if found_classes > 0:
        FILE.write('<div id="classes">\n')
        FILE.write("<h2>Classes</h2>\n")
        HELPER.write_contents_table(ontology_name, classes)
        HELPER.write_entities(ontology_name, classes, "classes", "Classes")
        FILE.write("</div>\n")

    if found_properties:
        FILE.write('<div id="objectproperties">\n')
        FILE.write("<h2>Object Properties</h2>\n")
        HELPER.write_contents_table(ontology_name, properties)
        HELPER.write_entities(
            ontology_name, properties, "objectproperties", "Object Properties"
        )
        FILE.write("</div>\n")

    concepts = HELPER.get_concepts(ontology_name)
    FILE.write('<div id="namedIndividuals">\n')
    FILE.write("<h2>Named Individuals</h2>\n")
    HELPER.write_contents_table(ontology_name, concepts)
    HELPER.write_entities(
        ontology_name, concepts, "namedIndividuals", "Named Individuals"
    )

    FILE.write("</div>\n")

    HELPER.write_namespace(ontology_name)

    HELPER.write_acknowledgements(ontology_name)

    FILE.write("</div>\n")
    FILE.write("</body>\n")


def generate():
    for ontology in ONTOLOGIES:
        global ONTOLOGY_BASE_URI, FILE_BASE_URI, FILE, HELPER
        HELPER = Helper()
        HELPER.PREFIX = "PREFIX %s:   <%s> %s" % (
            ontology,
            ONTOLOGY_MAP[ontology],
            PREFIX,
        )
        HELPER.TYPE = "ontology"
        ONTOLOGY_BASE_URI = "%s" % (ONTOLOGY_MAP[ontology])
        HELPER.BASE_URI = ONTOLOGY_BASE_URI
        FILE_BASE_URI = "http://%s/ontology/%s/%s-content/%s-ontology" % (
            SPARQL_HOST_NAME,
            ontology,
            ontology,
            ontology,
        )
        file_name = os.path.join(
            HTML_DIRECTORY, "ontology", ontology, ontology + "-content", "index.html"
        )
        FILE = codecs.open(file_name, encoding="utf-8", mode="w")
        HELPER.FILE = FILE
        HELPER.ONTOLOGY_URI = "%s" % (ONTOLOGY_MAP[ontology])

        do_stuff(ontology)


if __name__ == "__main__":
    generate()
