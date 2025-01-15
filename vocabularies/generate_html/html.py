import csv
import os
from xml.sax._exceptions import SAXParseException

from rdflib import Graph, URIRef
from rdflib.namespace import DC, OWL, RDF, RDFS, SKOS

from vocabularies.settings import (
    SPARQL_HOST_NAME,
    HTML_DIRECTORY,
    CITO,
    CMIP_ONTOLOGY,
    GCOS_ONTOLOGY,
    GRIB_ONTOLOGY,
    CCI,
    CMIP,
    GCOS,
    GRIB,
    GLOSSARY,
    CSV_DIRECTORY,
    ONTOLOGY_MAP,
    NERC,
)


HAS_PLATFORM = f"{ONTOLOGY_MAP[CCI]}hasPlatform"
HAS_SENSOR = f"{ONTOLOGY_MAP[CCI]}hasSensor"
RELATED = f"{SKOS}related"
OBJECT_PROPERTIES = [HAS_PLATFORM, HAS_SENSOR, RELATED]

TYPES = ["ontology", "scheme", "collection"]


class Helper:
    GRAPH_STORE = {}
    FILE = None
    BASE_URI = None
    ONTOLOGY_URI = None
    PREFIX = None
    TYPE = None
    TOP_ONTOLOGY_BASE_URI = None

    def __init__(self):
        graph = Graph()
        source = "http://vocab.nerc.ac.uk/collection/P07/current/"
        try:
            graph.parse(location=source, format="application/rdf+xml")
        except SAXParseException as ex:
            print(f"ERROR loading NERC vocab from {source}")
            print(f"ERROR: {ex}")
        self.GRAPH_STORE[NERC] = graph

    def get_alt_label(self, graph_name, uri):
        print(f"Get alt label for {uri}")
        statement = (
            f"{self.PREFIX} SELECT ?label WHERE {{<{uri}> skos:altLabel ?label}}"
        )
        results = self.get_search_results(graph_name, statement)
        for resource in results:
            if resource.label != "None":
                return resource.label
        print(f"get_label - no label found for {uri}, using uri")
        return uri

    def get_classes(self, graph_name):
        """
        Get the lists of classes that are not also concepts.
        """
        statement = (
            f"{self.PREFIX} SELECT Distinct ?subject WHERE "
            "{{?subject rdf:type owl:Class}} ORDER BY ASC(?subject)"
        )
        classes = self.get_search_results(graph_name, statement)
        non_concept_classes = []
        for _class in classes:
            statement = f"{self.PREFIX} SELECT Distinct ?subject WHERE {{<{_class.subject}> rdf:type skos:Concept}}"
            results = self.get_search_results(graph_name, statement)
            if len(results) == 0:
                non_concept_classes.append(_class)
        return non_concept_classes

    def get_concepts(self, graph_name):
        statement = f"{self.PREFIX} SELECT Distinct ?subject WHERE {{?subject rdf:type skos:Concept . ?subject skos:prefLabel ?label}} ORDER BY ASC(?label)"
        return self.get_search_results(graph_name, statement)

    def get_concepts_in_scheme(self, graph_name, uri):
        statement = f"{self.PREFIX} SELECT Distinct ?subject WHERE {{?subject skos:inScheme <{uri}> . ?subject skos:prefLabel ?label}} ORDER BY ASC(?label)"
        return self.get_search_results(graph_name, statement)

    def get_individuals_in_class(self, graph_name, uri):
        statement = f"{self.PREFIX} SELECT Distinct ?subject WHERE {{?subject rdf:type <{uri}> . ?subject skos:prefLabel ?label}} ORDER BY ASC(?label)"
        subs = self.get_search_results(graph_name, statement)
        result = []
        for sub in subs:
            result.append(sub.subject)
        return result

    def get_external_individuals_in_class(self, graph_name, uri):
        statement = f'{self.PREFIX} SELECT Distinct ?subject WHERE {{?subject rdf:type <{uri}> FILTER regex(str(?subject), "^http://vocab.nerc.ac.uk", "i")}}'
        subs = self.get_search_results(graph_name, statement)
        result = []
        for sub in subs:
            result.append(sub.subject)
        return result

    def get_label(self, graph_name, uri):
        statement = (
            f"{self.PREFIX} SELECT ?label WHERE {{<{uri}> skos:prefLabel ?label}}"
        )
        results = self.get_search_results(graph_name, statement)
        for resource in results:
            if resource.label != "None":
                return resource.label
        statement = f"{self.PREFIX} SELECT ?label WHERE {{<{uri}> rdfs:label ?label}}"
        results = self.get_search_results(graph_name, statement)
        for resource in results:
            if resource.label:
                return resource.label
        print(f"get_label - no label found for {uri}, using uri")
        return uri

    def get_members(self, graph_name, uri):
        statement = f"{self.PREFIX} SELECT Distinct ?subject WHERE {{<{uri}> <{SKOS.member}> ?subject . ?subject <{SKOS.prefLabel}> ?label}} ORDER BY ASC(?label)"
        return self.get_search_results(graph_name, statement)

    def get_nerc_members(self, graph_name, uri):
        statement = f'{self.PREFIX} SELECT Distinct ?subject WHERE {{<{uri}> <{SKOS.member}> ?subject FILTER regex(str(?subject), "^http://vocab.nerc.ac.uk", "i")}}'
        return self.get_search_results(graph_name, statement)

    def get_ontology(self, graph_name):
        statement = f"{self.PREFIX} SELECT Distinct ?subject WHERE {{?subject rdf:type owl:Ontology}} ORDER BY ASC(?subject)"
        return self.get_search_results(graph_name, statement)

    def get_properties(self, graph_name):
        statement = f"{self.PREFIX} SELECT Distinct ?subject WHERE {{?subject rdf:type owl:ObjectProperty . ?subject rdfs:label ?label}} ORDER BY ASC(?label)"
        return self.get_search_results(graph_name, statement)

    def get_resources(self, graph_name, uri):
        statement = (
            f"{self.PREFIX} SELECT ?p ?o WHERE {{<{uri}> ?p ?o}} ORDER BY ASC(?o)"
        )
        return self.get_search_results(graph_name, statement)

    def get_sub_classes(self, graph_name, uri):
        statement = f"{self.PREFIX} SELECT Distinct ?subject WHERE {{?subject rdfs:subClassOf <{uri}> . ?subject skos:prefLabel ?label}} ORDER BY ASC(?label)"
        subs = self.get_search_results(graph_name, statement)
        result = []
        for sub in subs:
            result.append(sub.subject)
        return result

    def get_search_results(self, graph_name, statement):
        graph = self.get_graph(graph_name)
        return graph.query(statement)

    def get_graph(self, graph_name):
        try:
            graph = self.GRAPH_STORE[graph_name]
        except KeyError:
            graph = Graph()
            source = os.path.join(
                HTML_DIRECTORY,
                "ontology",
                graph_name,
                graph_name + "-content",
                graph_name + "-ontology.ttl",
            )
            graph.parse(source=source, format="n3")
            self.GRAPH_STORE[graph_name] = graph
        return graph

    def write_contents_table(self, ontology_name, results, additional_results=None):
        if additional_results is None:
            additional_results = []
        self.FILE.write('<ul class="hlist">\n')
        for resource in results:
            self.FILE.write("<li>")
            self.write_link(ontology_name, resource.subject)
            self.FILE.write("</li>\n")
        for resource in additional_results:
            self.FILE.write("<li>")
            self.write_link(ontology_name, resource.subject)
            self.FILE.write("</li>\n")
        self.FILE.write("</ul>\n")

    def write_acknowledgements(self, ontology_name):
        in_file_name = "%s-ontology.csv" % ontology_name
        count = 0
        in_file = os.path.join(CSV_DIRECTORY, in_file_name)
        with open(in_file, "r", encoding="utf-8") as csvfile:
            cvsreader = csv.reader(csvfile, delimiter="`", quotechar="|")
            for row in cvsreader:
                count = count + 1
                if count < 2:
                    continue
                if row[10] != "":
                    self.FILE.write('<div id="acknowledgements">\n')
                    self.FILE.write(
                        '<h2>Acknowledgements <span class="backlink"> back to <a href="#toc">ToC</a></span></h2>\n'
                    )
                    self.FILE.write(row[10])
                    self.FILE.write("</div>\n")

    def write_namespace(self, ontology_name):
        self.FILE.write('<div id="namespacedeclarations">\n')
        self.FILE.write(
            '<h2>Namespace Declarations <span class="backlink"> back to <a href="#toc">ToC</a></span></h2>\n'
        )
        self.FILE.write("<dl>\n")
        self.FILE.write("<dt><em>default namespace</em></dt>\n")
        self.FILE.write("<dd>%s</dd>\n" % (ONTOLOGY_MAP[ontology_name]))
        if ontology_name == GLOSSARY:
            self.FILE.write("<dt>cito</dt>\n")
            self.FILE.write("<dd>%s</dd>" % CITO)
        #     if ontology_name == CCI:
        #         self.FILE.write('<dt>%s</dt>\n' % GCOS)
        #         self.FILE.write('<dd>%s</dd>\n' % (GCOS_ONTOLOGY))
        if ontology_name == CMIP:
            self.FILE.write("<dt>%s</dt>\n" % GCOS)
            self.FILE.write("<dd>%s</dd>\n" % (GCOS_ONTOLOGY))
            self.FILE.write("<dt>%s</dt>\n" % GRIB)
            self.FILE.write("<dd>%s</dd>\n" % (GRIB_ONTOLOGY))
        if ontology_name == GRIB:
            self.FILE.write("<dt>%s</dt>\n" % CMIP)
            self.FILE.write("<dd>%s</dd>\n" % (CMIP_ONTOLOGY))
        if ontology_name == GCOS:
            self.FILE.write("<dt>%s</dt>\n" % CMIP)
            self.FILE.write("<dd>%s</dd>\n" % (CMIP_ONTOLOGY))
        self.FILE.write("<dt>dc</dt>\n")
        self.FILE.write("<dd>%s</dd>" % DC)
        self.FILE.write("<dt>owl</dt>\n")
        self.FILE.write("<dd>%s</dd>" % OWL)
        self.FILE.write("<dt>rdf</dt>\n")
        self.FILE.write("<dd>%s</dd>" % RDF)
        self.FILE.write("<dt>rdfs</dt>\n")
        self.FILE.write("<dd>%s</dd>" % RDFS)
        self.FILE.write("<dt>skos</dt>\n")
        self.FILE.write("<dd>%s</dd>" % SKOS)

    def write_entities(
        self, ontology_name, results, _id, title, additional_results=None
    ):
        if additional_results is None:
            additional_results = []
        for result in results:
            self._write_entity(result, ontology_name, _id, title)
        for result in additional_results:
            self._write_entity(result, ontology_name, _id, title)

    def _write_entity(self, result, ontology_name, _id, title):
        try:
            link = result.subject.split(self.BASE_URI)[1]
            try:
                link = link.split("/")[1]
            except IndexError:
                pass
        except IndexError:
            link = result.subject
        if NERC in result.subject:
            label = self.get_alt_label(NERC, result.subject)
        else:
            label = self.get_label(ontology_name, result.subject)
        self.FILE.write('<div id="%s" class="entity">\n' % link)
        if result.subject in OBJECT_PROPERTIES:
            self.FILE.write(
                '<h3>%s<sup title="object property" class="type-op">op</sup>' % label
            )
        else:
            self.FILE.write("<h3>%s" % label)
        self.FILE.write(
            '<span class="backlink">back to <a href="#toc">ToC</a> or <a href="#%s">%s ToC</a></span></h3>\n'
            % (_id, title)
        )

        if SPARQL_HOST_NAME not in result.subject:
            self.FILE.write(
                '<p><strong>IRI:</strong> <a href="{uri}">{uri}</a></p>\n'.format(
                    uri=result.subject
                )
            )
        else:
            self.FILE.write(
                "<p><strong>IRI:</strong> {uri}</p>\n".format(uri=result.subject)
            )

        altLabels = []
        hasTopConcepts = []
        topConceptOf = []
        inverseOf = []
        inSchemes = []
        sub_class_of = []
        sensors = []
        platforms = []
        broader = []
        narrower = []
        broadMatch = []
        closeMatch = []
        narrowMatch = []
        relatedMatch = []
        broaderTransitive = []
        narrowerTransitive = []
        seeAlso = []
        _range = []
        domain = []
        rdf_type = []
        subPropertyOf = []
        contributor = []
        creator = []
        member = []
        citesAsSourceDocument = []
        isDefinedBy = []
        collection_member = []

        date = None
        definition = None
        description = None
        version = None

        resources = self.get_resources(ontology_name, result.subject)
        for res in resources:
            if res.p == URIRef(self.ONTOLOGY_URI + "hasSensor"):
                sensors.append(res.o)
            elif res.p == URIRef(self.ONTOLOGY_URI + "hasPlatform"):
                platforms.append(res.o)
            elif res.p == OWL.inverseOf:
                inverseOf.append(res.o)
            elif res.p == OWL.versionInfo:
                version = res.o
            elif res.p == SKOS.inScheme:
                inSchemes.append(res.o)
            elif res.p == SKOS.altLabel:
                altLabels.append(res.o)
            elif res.p == SKOS.broader:
                broader.append(res.o)
            elif res.p == SKOS.narrower:
                narrower.append(res.o)
            elif res.p == SKOS.broadMatch:
                broadMatch.append(res.o)
            elif res.p == SKOS.broaderTransitive:
                broaderTransitive.append(res.o)
            elif res.p == SKOS.narrowerTransitive:
                narrowerTransitive.append(res.o)
            elif res.p == SKOS.closeMatch:
                closeMatch.append(res.o)
            elif res.p == SKOS.narrowMatch:
                narrowMatch.append(res.o)
            elif res.p == SKOS.relatedMatch:
                relatedMatch.append(res.o)
            elif res.p == SKOS.hasTopConcept:
                hasTopConcepts.append(res.o)
            elif res.p == SKOS.topConceptOf:
                topConceptOf.append(res.o)
            elif res.p == RDFS.seeAlso:
                seeAlso.append(res.o)
            elif res.p == RDFS.range:
                _range.append(res.o)
            elif res.p == RDFS.domain:
                domain.append(res.o)
            elif res.p == RDFS.subClassOf:
                sub_class_of.append(res.o)
            elif res.p == RDFS.subPropertyOf:
                subPropertyOf.append(res.o)
            elif res.p == RDFS.isDefinedBy:
                isDefinedBy.append(res.o)
            elif res.p == RDF.type:
                rdf_type.append(res.o)
            elif res.p == RDFS.member:
                member.append(res.o)
            elif res.p == DC.contributor:
                contributor.append(res.o)
            elif res.p == DC.creator:
                creator.append(res.o)
            elif res.p == DC.description:
                if _id != "conceptschemes":
                    description = res.o
            elif res.p == DC.date:
                date = res.o
            elif res.p == URIRef(CITO + "citesAsSourceDocument"):
                citesAsSourceDocument.append(res.o)
            elif res.p == SKOS.definition:
                definition = res.o
            elif res.p == DC.publisher:
                pass
            elif res.p == DC.rights:
                pass
            elif res.p == DC.title:
                pass
            elif res.p == RDFS.comment:
                pass
            elif res.p == SKOS.member:
                collection_member.append(res.o)
            elif res.p == SKOS.prefLabel:
                pass
            elif res.p == SKOS.scopeNote:
                pass
            elif res.p == RDFS.label:
                pass
            else:
                print("write_entities - ignoring %s %s" % (res.p, res.o))

        has_sub_class = self.get_sub_classes(ontology_name, result.subject)

        self.write_comment(definition)

        self.FILE.write('<div class="description">\n')
        self.write_comment(description)

        self.FILE.write("<dl>\n")
        self.write_literals(version, "version")
        self.write_literals(creator, "creator")
        self.write_literals(contributor, "contributor")
        self.write_list(ontology_name, rdf_type, "type")
        self.write_literals(altLabels, "has alternative label")
        self.write_list(ontology_name, hasTopConcepts, "has top concepts")
        self.write_list(ontology_name, topConceptOf, "is top concept in scheme")
        self.write_list(ontology_name, inSchemes, "is in scheme")
        if _id == "classes":
            class_members = self.get_individuals_in_class(ontology_name, result.subject)
            nerc_members = self.get_external_individuals_in_class(
                ontology_name, result.subject
            )
            class_members.extend(nerc_members)
            self.write_list(ontology_name, class_members, "has members")
        self.write_list(ontology_name, isDefinedBy, "is defined by")
        self.write_list(ontology_name, sub_class_of, "has super-classes")
        self.write_list(ontology_name, has_sub_class, "has sub-classes")
        self.write_list(ontology_name, subPropertyOf, "has super-properties")
        self.write_list(ontology_name, collection_member, "has members")
        self.write_list(ontology_name, member, "has members")
        if result.subject in OBJECT_PROPERTIES:
            self.write_list(ontology_name, _range, "has range")
            self.write_list(ontology_name, domain, "has domain")
        else:
            self.write_list(ontology_name, _range, "is in range of")
            self.write_list(ontology_name, domain, "is in domain of")
        self.write_list(ontology_name, inverseOf, "is inverse of")
        self.write_list(ontology_name, sensors, "has sensors")
        self.write_list(ontology_name, platforms, "has platform")
        self.write_list(ontology_name, broader, "has broader")
        self.write_list(ontology_name, narrower, "has narrower")
        self.write_list(ontology_name, broadMatch, "has broader match")
        self.write_list(ontology_name, broaderTransitive, "has broader transitive")
        self.write_list(ontology_name, narrowerTransitive, "has narrower transitive")
        self.write_list(ontology_name, closeMatch, "has close match")
        self.write_list(ontology_name, relatedMatch, "has related match")
        self.write_list(ontology_name, narrowMatch, "has narrower match")
        self.write_list(
            ontology_name, citesAsSourceDocument, "cites as source document"
        )
        self.write_list(ontology_name, seeAlso, "see also")
        self.write_literals(date, "date")

        self.FILE.write("</dl>\n")
        self.FILE.write("</div></div>\n")

    def write_comment(self, comment):
        if comment is not None:
            self.FILE.write('<div class="comment">\n')
            self.FILE.write('<span class="markdown">%s</span>' % comment)
            self.FILE.write("</div>")

    def write_link(self, ontology_name, uri):
        local = True
        link = ""
        try:
            link = uri.split(self.BASE_URI)[1]
            # may need to split
            try:
                link = link.split("/")[1]
            except IndexError:
                pass
        except IndexError:
            link = uri

        if SPARQL_HOST_NAME in uri and ontology_name in uri:
            label = self.get_label(ontology_name, uri)

            if self.TYPE is None:
                print("ERROR TYPE not set")
            elif self.TYPE == "ontology":
                if "scheme" in uri:
                    local = False
            elif self.TYPE in ["collection", "scheme"]:
                if self.BASE_URI not in uri:
                    local = False

        elif NERC in uri:
            label = self.get_alt_label(NERC, uri)
            local = False
        else:
            local = False
            label = uri

        if local:
            self.FILE.write('<a href="#%s" title="%s">%s</a>' % (link, uri, label))
        else:
            self.FILE.write('<a href="%s" title="%s">%s</a>' % (uri, uri, label))

    def write_list(self, ontology_name, uris, name):
        if len(uris) > 0:
            self.FILE.write("<dt>%s</dt>\n<dd>\n" % name)
            first = True
            for uri in uris:
                if first:
                    first = False
                else:
                    self.FILE.write(", ")
                self.write_link(ontology_name, uri)

                if uri in OBJECT_PROPERTIES:
                    self.FILE.write(
                        '<sup title="object property" class="type-op">op</sup>\n'
                    )

            self.FILE.write("</dd>\n")

    def write_literals(self, uris, name):
        if uris is None:
            return
        if type(uris) == list and len(uris) == 0:
            return

        self.FILE.write("<dt>%s</dt>\n<dd>\n" % name)
        if type(uris) == list:
            first = True
            for uri in uris:
                if first:
                    first = False
                else:
                    self.FILE.write(", ")
                self.FILE.write(uri)
        else:
            self.FILE.write(uris)

        self.FILE.write("</dd>\n")
