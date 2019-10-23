import codecs
import os
from urlparse import urlparse

from rdflib.namespace import DC, OWL, RDF, RDFS, SKOS

from html.html import Helper
from settings import (
    ONTOLOGIES,
    SPARQL_HOST_NAME,
    SPARQL_DATASET,
    HTML_DIRECTORY,
    GLOSSARY,
    ONTOLOGY_MAP,
    COLLECTION_MAP,
    DISPLAY_NAME_MAP,
    SPARQL_GRAPH,
    SPARQL_QUERY,
)


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
FILE_BASE_URI = None
HELPER = None


def write_head(ontology_name, collection_uri, found_properties):
    date = None
    publisher = None
    rights = None
    title = None
    version = None
    creators = []
    contributors = []

    resources = HELPER.get_resources(ontology_name, collection_uri)
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
            creators.append(res.o.decode())
        if res.p == DC.contributor:
            contributors.append(res.o.decode())

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
        "<title>The %s %s Collection</title>\n"
        % (DISPLAY_NAME_MAP[ontology_name], title)
    )
    FILE.write('<link href="../../../vocab.css" rel="stylesheet" type="text/css" />\n')
    FILE.write("</head>\n")

    FILE.write("<body>\n")
    FILE.write('<div class="head">\n')
    FILE.write(
        "<h1>The %s %s Collection</h1>\n" % (DISPLAY_NAME_MAP[ontology_name], title)
    )

    FILE.write("<dl>\n")
    FILE.write("<dt>IRI:</dt>\n")
    FILE.write('<dd><a href="%s">%s</a></dd>\n' % (collection_uri, collection_uri))
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
    FILE.write("<dd>Collection source ")
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

    FILE.write("<hr />\n\n<h2>Abstract</h2>\n")
    FILE.write('<span class="markdown">%s</span>\n' % abstract)

    FILE.write('<div id="introduction">\n')
    FILE.write("<h2>Introduction</h2>\n")
    FILE.write('<span class="markdown">%s</span>\n' % description)

    FILE.write("</div>\n")


def do_stuff(ontology_name, collection_uri):
    write_head(ontology_name, collection_uri, False)

    members = HELPER.get_members(ontology_name, collection_uri)
    nerc_members = HELPER.get_nerc_members(ontology_name, collection_uri)
    FILE.write('<div id="toc">\n')
    FILE.write('<div id="members">\n')
    FILE.write("<h2>Collection Members</h2>\n")
    HELPER.write_contents_table(ontology_name, members, nerc_members)

    HELPER.write_entities(ontology_name, members, "members", "Members", nerc_members)
    FILE.write("</div>\n")

    FILE.write("</div>\n")
    FILE.write("</body>\n")


def get_collection_name(url):
    path = urlparse(url).path
    bits = path.split("/")
    return bits[len(bits) - 1]


def generate():
    for ontology in ONTOLOGIES:
        if ontology == GLOSSARY:
            continue
        global FILE_BASE_URI, FILE, HELPER
        HELPER = Helper()
        HELPER.PREFIX = "PREFIX %s:   <%s> %s" % (
            ontology,
            ONTOLOGY_MAP[ontology],
            PREFIX,
        )
        HELPER.TYPE = "collection"
        graph = HELPER.get_graph(ontology)

        collections = graph.subjects(RDF.type, SKOS.Collection)
        for collection in collections:
            collection_name = get_collection_name(collection)
            HELPER.BASE_URI = "%s%s" % (COLLECTION_MAP[ontology], collection_name)
            FILE_BASE_URI = "http://%s/collection/%s/%s-content/%s" % (
                SPARQL_HOST_NAME,
                ontology,
                ontology,
                collection_name,
            )
            file_name = os.path.join(
                HTML_DIRECTORY,
                "collection",
                ontology,
                ontology + "-content",
                collection_name + ".html",
            )
            FILE = codecs.open(file_name, encoding="utf-8", mode="w")
            HELPER.FILE = FILE
            HELPER.ONTOLOGY_URI = "%s" % (ONTOLOGY_MAP[ontology])

            do_stuff(ontology, collection)


if __name__ == "__main__":
    generate()
