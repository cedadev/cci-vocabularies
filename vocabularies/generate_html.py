import codecs

from rdflib import Graph, URIRef
from rdflib.namespace import DC, OWL, RDF, RDFS, SKOS
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

from settings import ONTOLOGIES, SPARQL_HOST_NAME, SPARQL_UPDATE, \
    SPARQL_QUERY, SPARQL_DATASET, HTML_DIRECTORY, CITO, \
    CCI_NAME_SPACE, CMIP_NAME_SPACE, GCOS_NAME_SPACE, GRIB_NAME_SPACE, \
    CCI, CMIP, GCOS, GRIB, GLOSSARY, NAME_SPACE_MAP


PREFIX = """
PREFIX dc:   <%s>
PREFIX owl:  <%s>
PREFIX rdf:  <%s>
PREFIX rdfs: <%s>
PREFIX skos: <%s>
""" % (DC, OWL, RDF, RDFS, SKOS)

SPARQL_URI = 'http://%s/%s' % (SPARQL_HOST_NAME, 'sparql')

HAS_PLATFORM = '%shasPlatform' % CCI_NAME_SPACE
HAS_SENSOR = '%shasSensor' % CCI_NAME_SPACE
RELATED = '%srelated' % SKOS
OBJECT_PROPERTIES = [HAS_PLATFORM, HAS_SENSOR, RELATED]

FILE = None
ONTOLOGY_BASE_URI = None
ONTOLOGY_TTL_URI = None

GRAPH_STORE = {}

class TripleStore(object):
    __store = None

    @classmethod
    def __init_store(self):
        store = SPARQLUpdateStore(queryEndpoint=SPARQL_QUERY,
                                  update_endpoint=SPARQL_UPDATE,
                                  postAsEncoded=False)
        TripleStore.__store = store

    @classmethod
    def get_store(self):
        if TripleStore.__store is None:
            TripleStore.__init_store()
        return TripleStore.__store


def get_classes(graph_name):
    """
    Get the lists of classes that are not also concepts.
    """
    statement = PREFIX + "SELECT Distinct ?subject WHERE {?subject rdf:type owl:Class} ORDER BY ASC(?subject)"
    classes = get_search_results(graph_name, statement)
    non_concept_classes = []
    for _class in classes:
        statement = PREFIX + "SELECT Distinct ?subject WHERE {<" + _class.subject.decode() + "> rdf:type skos:Concept}"
        results = get_search_results(graph_name, statement)
        if len(results) == 0:
            non_concept_classes.append(_class)
    return non_concept_classes


def get_concepts(graph_name):
    statement = PREFIX + "SELECT Distinct ?subject WHERE {?subject rdf:type skos:Concept} ORDER BY ASC(?subject)"
    return get_search_results(graph_name, statement)


def get_concepts_in_scheme(graph_name, uri):
    statement = PREFIX + "SELECT Distinct ?subject WHERE {?subject skos:inScheme <" + uri + ">} ORDER BY ASC(?subject)"
    subs = get_search_results(graph_name, statement)
    result = []
    for sub in subs:
        result.append(sub.subject.decode())
    return result


def get_concept_schemes(graph_name):
    statement = PREFIX + "SELECT Distinct ?subject WHERE {?subject rdf:type skos:ConceptScheme} ORDER BY ASC(?subject)"
    return get_search_results(graph_name, statement)


def get_ontology(graph_name):
    statement = PREFIX + "SELECT Distinct ?subject WHERE {?subject rdf:type owl:Ontology} ORDER BY ASC(?subject)"
    return get_search_results(graph_name, statement)


def get_properties(graph_name):
    statement = PREFIX + "SELECT Distinct ?subject WHERE {?subject rdf:type owl:ObjectProperty} ORDER BY ASC(?subject)"
    return get_search_results(graph_name, statement)


def get_resources(graph_name, uri):
    statement = PREFIX + "SELECT ?p ?o WHERE {<" + uri + "> ?p ?o}"
    return get_search_results(graph_name, statement)


def get_sub_classes(graph_name, uri):
    statement = PREFIX + "SELECT Distinct ?subject WHERE {?subject rdfs:subClassOf <" + uri + ">} ORDER BY ASC(?subject)"
    subs = get_search_results(graph_name, statement)
    result = []
    for sub in subs:
        result.append(sub.subject.decode())
    return result


def get_label(graph_name, uri):
    statement = PREFIX + "SELECT ?label WHERE {<" + uri + "> skos:prefLabel ?label}"
    results = get_search_results(graph_name, statement)
    for resource in results:
        if resource.label != "None":
            return resource.label
    statement = PREFIX + "SELECT ?label WHERE {<" + uri + "> rdfs:label ?label}"
    results = get_search_results(graph_name, statement)
    for resource in results:
        if resource.label:
            return resource.label    
    print "get_label - no label found for %s, using uri" % uri
    return uri


def get_search_results(graph_name, statement):
    try:
        graph = GRAPH_STORE[graph_name]
    except KeyError:
        graph = Graph()
        source = "%s%s-ontology.ttl" % (HTML_DIRECTORY, graph_name)
        graph.parse(source=source, format='n3')
        GRAPH_STORE[graph_name] = graph
    return graph.query(statement)


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
    results = get_ontology(ontology_name)
    for result in results:
        resources = get_resources(ontology_name, result.subject)
        for res in resources:
            if res.p == DC.date:
                date = res.o
            if res.p == DC.description:
                description = res.o
            if res.p == DC.publisher:
                publisher = res.o
            if res.p == DC.rights:
                rights = res.o
            if res.p == DC .title:
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
    FILE.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    FILE.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    FILE.write('<head>\n')
    FILE.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n')
    FILE.write('<title>%s</title>\n' % title)
    FILE.write('<link href="%s.css" rel="stylesheet" type="text/css" />\n' % ontology_name)
    FILE.write('<link href="cci.css" rel="stylesheet" type="text/css" />\n')  # TDDO remove
    FILE.write('</head>\n')

    FILE.write('<body>\n')
    FILE.write('<div class="head">\n')
    FILE.write('<h1>%s</h1>\n' % title)

    FILE.write('<dl>\n')
    FILE.write('<dt>IRI:</dt>\n')
    FILE.write('<dd><a href="%s">%s</a></dd>\n' % (ONTOLOGY_BASE_URI, ONTOLOGY_BASE_URI))
    FILE.write('</dl>\n')

    FILE.write('<dl>\n')
    FILE.write('<dt>Date:</dt>\n')
    FILE.write('<dd>%s</dd>\n' % date)
    FILE.write('<dt>Current Version:</dt>\n')
    FILE.write('<dd>%s</dd>\n' % version)
    FILE.write('</dl>\n')

    FILE.write('<dl>\n')
    if len(creators) > 0:
        FILE.write('<dt>Authors:</dt>\n')
        for creator in creators:
            FILE.write('<dd>%s</dd>\n' % creator)
    if len(contributors) > 0:
        FILE.write('<dt>Contributors:</dt>\n')
        for contributor in contributors:
            FILE.write('<dd>%s</dd>\n' % contributor)
    FILE.write('</dl>\n')

    if publisher != None:
        FILE.write('<dl>\n')
        FILE.write('<dt>Publisher:</dt>\n')
        FILE.write('<dd>%s</dd>\n' % publisher)
        FILE.write('</dl>\n')

    FILE.write('<dl>\n')
    FILE.write('<dt>Other visualisations:</dt>\n')
    FILE.write('<dd><a href="%s">Ontology source</a></dd>\n' % ONTOLOGY_TTL_URI)
    FILE.write('<dd><a href="%s">SPARQL endpoint</a>, dataset:%s, graph:%s</dd>\n'
               % (SPARQL_URI, SPARQL_DATASET, ontology_name))
    FILE.write('</dl>\n')

    FILE.write('<div class="copyright">\n')
    FILE.write('<span class="markdown">%s</span>\n' % rights)
    FILE.write('</div>\n')

    FILE.write('</div>\n')

    FILE.write('<hr />\n\n<h2>Abstract</h2>\n')
    FILE.write('<span class="markdown">%s</span>\n' % abstract)

    FILE.write('<div id="toc">\n')
    FILE.write('<h2>Table of Content</h2>\n')
    FILE.write('<ol>\n')
    FILE.write('<li><a href="#introduction">Introduction</a></li>\n')
    FILE.write('<li><a href="#crossReference">Cross reference for Classes and Properties</a></li>\n')
    FILE.write('<ul>\n')

    if found_classes:
        FILE.write('<li><a href="#classes">Classes</a></li>\n')

    FILE.write('<li><a href="#conceptschemes">Concept Schemes</a></li>\n')
    FILE.write('<li><a href="#concepts">Concepts</a></li>\n')

    if found_properties:
        FILE.write('<li><a href="#objectproperties">Object Properties</a></li>\n')

    FILE.write('<li><a href="#namespacedeclarations">Namespace Declarations</a></li>\n')
    FILE.write('</ul>\n')
    FILE.write('<li><a href="#acknowledgements">Acknowledgements</a></li>\n')
    FILE.write('</ol>\n')
    FILE.write('</div>\n')

    FILE.write('<div id="introduction">\n')
    FILE.write('<h2>1. Introduction</h2>\n')
    FILE.write('<span class="markdown">%s</span>\n' % description)
    FILE.write('</div>\n')

    FILE.write('<div id="crossReference">\n')
    FILE.write('<h2>2. Cross Reference for Classes and Properties <span class="backlink"> back to <a href="#toc">ToC</a></span></h2>\n')
    FILE.write('This section provides details for each class and property defined by the Ontology.\n')


def write_contents_table(ontology_name, results):
    FILE.write('<ul class="hlist">\n')
    for resource in results:
        try:
            link = resource.subject.split(ONTOLOGY_BASE_URI)[1]
        except(IndexError):
            print "write_contents_table - IndexError: %s" % resource.subject
            link = resource.subject
        label = get_label(ontology_name, resource.subject)
        FILE.write('<li><a href="#%s" title="%s"><span>%s</span></a></li>\n'
                   % (link, resource.subject, label))
    FILE.write('</ul>\n')


def write_namespace(ontology_name):
    FILE.write('<div id="namespacedeclarations">\n')
    FILE.write('<h2>Namespace Declarations <span class="backlink"> back to <a href="#toc">ToC</a></span></h2>\n')
    FILE.write('<dl>\n')
    FILE.write('<dt><em>default namespace</em></dt>\n')
    FILE.write('<dd>%s</dd>\n' % (NAME_SPACE_MAP[ontology_name]))
    if ontology_name == GLOSSARY:
        FILE.write('<dt>cito</dt>\n')
        FILE.write('<dd>%s</dd>' % CITO)
    if ontology_name == CCI:
        FILE.write('<dt>%s</dt>\n' % GCOS)
        FILE.write('<dd>%s</dd>\n' % (GCOS_NAME_SPACE))
    if ontology_name == CMIP:
        FILE.write('<dt>%s</dt>\n' % GCOS)
        FILE.write('<dd>%s</dd>\n' % (GCOS_NAME_SPACE))
        FILE.write('<dt>%s</dt>\n' % GRIB)
        FILE.write('<dd>%s</dd>\n' % (GRIB_NAME_SPACE))
    if ontology_name == GRIB:
        FILE.write('<dt>%s</dt>\n' % CMIP)
        FILE.write('<dd>%s</dd>\n' % (CMIP_NAME_SPACE))
    if ontology_name == GCOS:
        FILE.write('<dt>%s</dt>\n' % CMIP)
        FILE.write('<dd>%s</dd>\n' % (CMIP_NAME_SPACE))
    FILE.write('<dt>dc</dt>\n')
    FILE.write('<dd>%s</dd>' % DC)
    FILE.write('<dt>owl</dt>\n')
    FILE.write('<dd>%s</dd>' % OWL)
    FILE.write('<dt>rdf</dt>\n')
    FILE.write('<dd>%s</dd>' % RDF)
    FILE.write('<dt>rdfs</dt>\n')
    FILE.write('<dd>%s</dd>' % RDFS)
    FILE.write('<dt>skos</dt>\n')
    FILE.write('<dd>%s</dd>' % SKOS)

def write_link(ontology_name, uri):
    local = True
    try:
        link = uri.split(ONTOLOGY_BASE_URI)[1]
        label = get_label(ontology_name, uri)
    except(IndexError):
        local = False
    if local:
        FILE.write('<a href="#%s" title="%s">%s</a>' % (link, uri, label))
    else:
        FILE.write('<a href="%s" title="%s">%s</a>' % (uri, uri, uri))


def write_entities(ontology_name, results, _id, title):
    for result in results:
        try:
            link = result.subject.split(ONTOLOGY_BASE_URI)[1]
        except(IndexError):
            print "write_entities - Skipping %s" % result.subject
            continue
        label = get_label(ontology_name, result.subject)
        FILE.write('<div id="%s" class="entity">\n' % link)
        if result.subject.decode() in OBJECT_PROPERTIES:
            FILE.write('<h3>%s<sup title="object property" class="type-op">op</sup>'
                       % label)
        else:
            FILE.write('<h3>%s' % label)        
        FILE.write('<span class="backlink">back to <a href="#toc">ToC</a> or <a href="#%s">%s ToC</a></span></h3>\n'
                   % (_id, title))
        FILE.write('<p><strong>IRI:</strong> %s</p>\n' % result.subject)

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

        date = None
        definition = None
        description = None
        version = None
        
        resources = get_resources(ontology_name, result.subject)
        for res in resources:
            if res.p == URIRef(ONTOLOGY_BASE_URI + 'hasSensor'):
                sensors.append(res.o.decode())
            elif res.p == URIRef(ONTOLOGY_BASE_URI + 'hasPlatform'):
                platforms.append(res.o.decode())
            elif res.p == OWL.inverseOf:
                inverseOf.append(res.o.decode())
            elif res.p == OWL.versionInfo:
                version = res.o
            elif res.p == SKOS.inScheme:
                inSchemes.append(res.o.decode())
            elif res.p == SKOS.altLabel:
                altLabels.append(res.o.decode())
            elif res.p == SKOS.broader:
                broader.append(res.o.decode())
            elif res.p == SKOS.narrower:
                narrower.append(res.o.decode())
            elif res.p == SKOS.broadMatch:
                broadMatch.append(res.o.decode())
            elif res.p == SKOS.broaderTransitive:
                broaderTransitive.append(res.o.decode())
            elif res.p == SKOS.narrowerTransitive:
                narrowerTransitive.append(res.o.decode())
            elif res.p == SKOS.closeMatch:
                closeMatch.append(res.o.decode())
            elif res.p == SKOS.narrowMatch:
                narrowMatch.append(res.o.decode())
            elif res.p == SKOS.relatedMatch:
                relatedMatch.append(res.o.decode())
            elif res.p == SKOS.hasTopConcept:
                hasTopConcepts.append(res.o.decode())
            elif res.p == SKOS.topConceptOf:
                topConceptOf.append(res.o.decode())
            elif res.p == RDFS.seeAlso:
                seeAlso.append(res.o.decode())
            elif res.p == RDFS.range:
                _range.append(res.o.decode())
            elif res.p == RDFS.domain:
                domain.append(res.o.decode())
            elif res.p == RDFS.subClassOf:
                sub_class_of.append(res.o.decode())
            elif res.p == RDFS.subPropertyOf:
                subPropertyOf.append(res.o.decode())
            elif res.p == RDF.type:
                rdf_type.append(res.o.decode())
            elif res.p == RDFS.member:
                member.append(res.o.decode())
            elif res.p == DC.contributor:
                contributor.append(res.o.decode())
            elif res.p == DC.creator:
                creator.append(res.o.decode())
            elif res.p == DC.description:
                description = res.o
            elif  res.p == DC.date:
                date = res.o.decode()
            elif  res.p == URIRef(CITO + 'citesAsSourceDocument'):
                citesAsSourceDocument.append(res.o.decode())
            elif res.p == SKOS.definition:
                definition = res.o
            elif res.p == SKOS.prefLabel:
                pass
            elif res.p == RDFS.label:
                pass
            else:
                print "write_contents_table - ignoring %s %s" % (res.p, res.o)

        has_sub_class = get_sub_classes(ontology_name, result.subject)

        write_comment(definition)
        
        FILE.write('<div class="description">\n')
        write_comment(description)
        
        FILE.write('<dl>\n')
        write_literals(version, "version")
        write_literals(creator, "creator")
        write_literals(contributor, "contributor")
        write_list(ontology_name, rdf_type, "type")
        write_literals(altLabels, "has alternative label")
        write_list(ontology_name, hasTopConcepts, "has top concepts")
        write_list(ontology_name, topConceptOf, "is top concept in scheme")
        write_list(ontology_name, inSchemes, "is in scheme")
#         if _id == 'conceptschemes':
#             has_concept = get_concepts_in_scheme(ontology_name, result.subject)
#             write_list(ontology_name, has_concept, "has concepts")
        write_list(ontology_name, sub_class_of, "has super-classes")
        write_list(ontology_name, has_sub_class, "has sub-classes")
        write_list(ontology_name, subPropertyOf, "has super-properties")
        write_list(ontology_name, member, "has members")
        if result.subject.decode() in OBJECT_PROPERTIES:
            write_list(ontology_name, _range, "has range")
            write_list(ontology_name, domain, "has domain")
        else:
            write_list(ontology_name, _range, "is in range of")
            write_list(ontology_name, domain, "is in domain of")
        write_list(ontology_name, inverseOf, "is inverse of")
        write_list(ontology_name, sensors, "has sensors")
        write_list(ontology_name, platforms, "has platform")
        write_list(ontology_name, broader, "has broader")
        write_list(ontology_name, narrower, "has narrower")
        write_list(ontology_name, broadMatch, "has broader match")
        write_list(ontology_name, broaderTransitive,
                   "has broader transitive")
        write_list(ontology_name, narrowerTransitive,
                   "has narrower transitive")
        write_list(ontology_name, closeMatch, "has close match")
        write_list(ontology_name, relatedMatch, "has related match")
        write_list(ontology_name, narrowMatch, "has narrower match")
        write_list(ontology_name, citesAsSourceDocument, "citesAsSourceDocument")
        write_list(ontology_name, seeAlso, "see also")
        write_literals(date, "date")

        FILE.write('</dl>\n')
        FILE.write('</div></div>\n')


def write_comment(comment):
    if comment != None:
        FILE.write('<div class="comment">\n')
        FILE.write('<span class="markdown">%s</span>' % comment)
        FILE.write('</div>')


def write_list(ontology_name, uris, name):
    if len(uris) > 0:
        FILE.write('<dt>%s</dt>\n<dd>\n' % name)
        first = True
        for uri in uris:
            if first:
                first = False
            else:
                FILE.write(', ')
            write_link(ontology_name, uri)
            
            if uri in OBJECT_PROPERTIES:
                FILE.write('<sup title="object property" class="type-op">op</sup>\n')
            
        FILE.write('</dd>\n')


def write_literals(uris, name):
    if uris == None:
        return
    if type(uris) == list and len(uris) == 0:
        return

    FILE.write('<dt>%s</dt>\n<dd>\n' % name)
    if type(uris) == list:
        first = True
        for uri in uris:
            if first:
                first = False
            else:
                FILE.write(', ')               
            FILE.write(uri)
    else:
        FILE.write(uris)

    FILE.write('</dd>\n')


def do_stuff(ontology_name):
    classes = get_classes(ontology_name)
    if len(classes) > 0:
        found_classes = True
    else:
        found_classes = False

    properties = get_properties(ontology_name)
    if len(properties) > 0:
        found_properties = True
    else:
        found_properties = False

    write_head(ontology_name, found_classes, found_properties)
    
    if found_classes > 0:
        FILE.write('<div id="classes">\n')
        FILE.write('<h2>2.1. Classes</h2>\n')
        write_contents_table(ontology_name, classes)
        write_entities(ontology_name, classes, 'classes', 'Classes')
        FILE.write('</div>\n')
     
    concepts_schemes = get_concept_schemes(ontology_name)
    FILE.write('<div id="conceptschemes">\n')
    FILE.write('<h2>2.2. Concept Schemes</h2>\n')
    write_contents_table(ontology_name, concepts_schemes)
    write_entities(ontology_name, concepts_schemes, 'conceptschemes',
                   'Concept Schemes')
    FILE.write('</div>\n')
       
    concepts = get_concepts(ontology_name)
    FILE.write('<div id="concepts">\n')
    FILE.write('<h2>2.3. Concepts</h2>\n')
    write_contents_table(ontology_name, concepts)
    write_entities(ontology_name, concepts, 'concepts', 'Concepts')
    FILE.write('</div>\n')
    
    if found_properties:
        FILE.write('<div id="objectproperties">\n')
        FILE.write('<h2>2.4. Object Properties</h2>\n')
        write_contents_table(ontology_name, properties)
        write_entities(ontology_name, properties, 'objectproperties',
                       'Object Properties')
        FILE.write('</div>\n')

    write_namespace(ontology_name)

    FILE.write('</div>\n')
    FILE.write('</body>\n')


def generate():
    for ontology in ONTOLOGIES:
        global PREFIX, ONTOLOGY_BASE_URI, ONTOLOGY_TTL_URI, FILE
        PREFIX = ('PREFIX %s:   <%s> %s' % 
                  (ontology, NAME_SPACE_MAP[ontology], PREFIX))
        ONTOLOGY_BASE_URI = ('%s' % (NAME_SPACE_MAP[ontology]))
        ONTOLOGY_TTL_URI = ('http://%s/%s/%s-content/%s-ontology.ttl' % 
                            (SPARQL_HOST_NAME, ontology, ontology, ontology))
        print ONTOLOGY_TTL_URI
        file_name = ('%s%s.html') % (HTML_DIRECTORY, ontology)
        FILE = codecs.open(file_name, encoding='utf-8', mode='w')
    
        do_stuff(ontology)


if __name__ == "__main__":
    generate()


