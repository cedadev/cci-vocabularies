import codecs
import os
from urllib.parse import urlparse

from rdflib.namespace import DC, OWL, RDF, RDFS, SKOS

from vocabularies.settings import (
    ONTOLOGIES,
    SPARQL_HOST_NAME,
    SPARQL_DATASET,
    HTML_DIRECTORY,
    CITO,
    CMIP_SCHEME,
    GCOS_SCHEME,
    GRIB_SCHEME,
    CCI,
    CMIP,
    GCOS,
    GRIB,
    GLOSSARY,
    SCHEME_MAP,
    ONTOLOGY_MAP,
    DISPLAY_NAME_MAP,
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

HAS_PLATFORM = "%shasPlatform" % ONTOLOGY_MAP[CCI]
HAS_SENSOR = "%shasSensor" % ONTOLOGY_MAP[CCI]
RELATED = "%srelated" % SKOS
OBJECT_PROPERTIES = [HAS_PLATFORM, HAS_SENSOR, RELATED]

FILE = None
SCHEME_BASE_URI = None
TOP_ONTOLOGY_BASE_URI = None
FILE_BASE_URI = None
HELPER = None

GRAPH_STORE = {}


class dummy_result:
    subject = ""


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

    resources = HELPER.get_resources(ontology_name, SCHEME_BASE_URI)
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
    FILE.write(
        "<title>The %s %s Concept Scheme</title>\n"
        % (DISPLAY_NAME_MAP[ontology_name], title)
    )
    FILE.write('<link href="../../../vocab.css" rel="stylesheet" type="text/css" />\n')
    FILE.write("</head>\n")

    FILE.write("<body>\n")
    FILE.write('<div class="head">\n')
    FILE.write(
        "<h1>The %s %s Concept Scheme</h1>\n" % (DISPLAY_NAME_MAP[ontology_name], title)
    )

    FILE.write("<dl>\n")
    FILE.write("<dt>IRI:</dt>\n")
    FILE.write('<dd><a href="%s">%s</a></dd>\n' % (SCHEME_BASE_URI, SCHEME_BASE_URI))
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
    FILE.write("<dd>Concept scheme source ")
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

    FILE.write('<li><a href="#conceptschemes">Concept Schemes</a></li>\n')
    FILE.write('<li><a href="#concepts">Concepts</a></li>\n')

    if found_properties:
        FILE.write('<li><a href="#objectproperties">Object Properties</a></li>\n')

    FILE.write('<li><a href="#namespacedeclarations">Namespace Declarations</a></li>\n')
    FILE.write('<li><a href="#acknowledgements">Acknowledgements</a></li>\n')
    FILE.write("</ol>\n")
    FILE.write("</div>\n")

    FILE.write('<div id="introduction">\n')
    FILE.write("<h2>Introduction</h2>\n")
    FILE.write('<span class="markdown">%s</span>\n' % description)
    FILE.write("</div>\n")


def write_namespace(ontology_name):
    FILE.write('<div id="namespacedeclarations">\n')
    FILE.write(
        '<h2>Namespace Declarations <span class="backlink"> back to <a href="#toc">ToC</a></span></h2>\n'
    )
    FILE.write("<dl>\n")
    FILE.write("<dt><em>default namespace</em></dt>\n")
    FILE.write("<dd>%s</dd>\n" % (SCHEME_MAP[ontology_name]))
    if ontology_name == GLOSSARY:
        FILE.write("<dt>cito</dt>\n")
        FILE.write("<dd>%s</dd>" % CITO)
    if ontology_name == CCI:
        FILE.write("<dt>%s</dt>\n" % GCOS)
        FILE.write("<dd>%s</dd>\n" % (GCOS_SCHEME))
    if ontology_name == CMIP:
        FILE.write("<dt>%s</dt>\n" % GCOS)
        FILE.write("<dd>%s</dd>\n" % (GCOS_SCHEME))
        FILE.write("<dt>%s</dt>\n" % GRIB)
        FILE.write("<dd>%s</dd>\n" % (GRIB_SCHEME))
    if ontology_name == GRIB:
        FILE.write("<dt>%s</dt>\n" % CMIP)
        FILE.write("<dd>%s</dd>\n" % (CMIP_SCHEME))
    if ontology_name == GCOS:
        FILE.write("<dt>%s</dt>\n" % CMIP)
        FILE.write("<dd>%s</dd>\n" % (CMIP_SCHEME))
    FILE.write("<dt>dc</dt>\n")
    FILE.write("<dd>%s</dd>" % DC)
    FILE.write("<dt>owl</dt>\n")
    FILE.write("<dd>%s</dd>" % OWL)
    FILE.write("<dt>rdf</dt>\n")
    FILE.write("<dd>%s</dd>" % RDF)
    FILE.write("<dt>rdfs</dt>\n")
    FILE.write("<dd>%s</dd>" % RDFS)
    FILE.write("<dt>skos</dt>\n")
    FILE.write("<dd>%s</dd>" % SKOS)


def do_stuff(ontology_name):
    found_classes = False

    found_properties = False

    write_head(ontology_name, found_classes, found_properties)

    result = dummy_result
    result.subject = SCHEME_BASE_URI
    concepts_schemes = [result]
    FILE.write('<div id="conceptschemes">\n')
    FILE.write("<h2>Concept Schemes</h2>\n")
    HELPER.write_entities(
        ontology_name, concepts_schemes, "conceptschemes", "Concept Schemes"
    )
    FILE.write("</div>\n")

    write_namespace(ontology_name)

    HELPER.write_acknowledgements(ontology_name)

    FILE.write("</div>\n")
    FILE.write("</body>\n")


def get_scheme_name(url):
    path = urlparse(url).path
    bits = path.split("/")
    return bits[len(bits) - 1]


def generate():
    for ontology in ONTOLOGIES:
        global PREFIX, SCHEME_BASE_URI, TOP_ONTOLOGY_BASE_URI, FILE_BASE_URI, FILE, HELPER
        HELPER = Helper()
        HELPER.PREFIX = "PREFIX %s:   <%s> %s" % (
            ontology,
            ONTOLOGY_MAP[ontology],
            PREFIX,
        )
        HELPER.TYPE = "scheme"
        graph = HELPER.get_graph(ontology)
        HELPER.ONTOLOGY_URI = "%s" % (ONTOLOGY_MAP[ontology])

        concept_schemes = graph.subjects(RDF.type, SKOS.ConceptScheme)

        for scheme in concept_schemes:
            scheme_name = get_scheme_name(scheme)
            if scheme_name == ontology:
                continue
            PREFIX = "PREFIX %s:   <%s> %s" % (ontology, ONTOLOGY_MAP[ontology], PREFIX)
            TOP_ONTOLOGY_BASE_URI = "%s" % (ONTOLOGY_MAP[ontology])
            HELPER.BASE_URI = "%s/%s" % (SCHEME_MAP[ontology], scheme_name)
            SCHEME_BASE_URI = "%s/%s" % (SCHEME_MAP[ontology], scheme_name)
            FILE_BASE_URI = "http://%s/scheme/%s/%s-content/%s" % (
                SPARQL_HOST_NAME,
                ontology,
                ontology,
                scheme_name,
            )
            file_name = os.path.join(
                HTML_DIRECTORY,
                "scheme",
                ontology,
                ontology + "-content",
                scheme_name + ".html",
            )
            print("Writing %s" % file_name)
            FILE = codecs.open(file_name, encoding="utf-8", mode="w")
            HELPER.FILE = FILE
            do_stuff(ontology)


if __name__ == "__main__":
    generate()
