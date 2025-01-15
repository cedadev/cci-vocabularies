import csv
import os

from rdflib.namespace import OWL, RDF, RDFS, SKOS

from vocabularies.settings import (
    SCHEME_MAP,
    GLOSSARY,
    CITO,
    CSV_DIRECTORY,
    COLLECTION_MAP,
    MODEL_DIRECTORY,
    ONTOLOGY_MAP,
)


# columns in spreadsheet
URI = 0
LABEL = 1
ALT_LABEL = 2
DEF = 3
SEE_ALSO = 4
CITES = 5
HIERARCHY = 5


def write_ttl(ontology_name):
    """
    Write out the concepts for an ontology.

    The ontology name is used to find the *-schemes.csv file. This file is used
    to find the concept files.

    @param ontology_name (str): the ontology name
    """
    in_file = os.path.join(CSV_DIRECTORY, "{}-schemes.csv".format(ontology_name))
    count = 0
    with open(in_file, "r", encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            concept_scheme_uri = row[URI].strip()
            file_name = "%s-%s" % (ontology_name, concept_scheme_uri.lower())
            _write_concepts(file_name, ontology_name, concept_scheme_uri)


def _write_concepts(file_name, ontology_name, concept_scheme_name):
    """
    Write out a list of concepts from a file.

    Add them to a concept scheme and a collection.

    @param file_name (str): the root of the file name
    @param ontology_name (str): the name of the ontology
    @param concept_scheme_name (str): the name of the concept scheme
    """
    in_file_name = "%s.csv" % file_name
    out_file_name = "%s.ttl" % file_name
    out_file = os.path.join(MODEL_DIRECTORY, out_file_name)
    with open(out_file, "w", encoding="utf-8") as ttl_writer:
        prefix_ontology = "%s_ontology" % (ontology_name)
        prefix_scheme = "%s_%s_scheme" % (ontology_name, concept_scheme_name)
        prefix_collection = "%s_%s_coll" % (ontology_name, concept_scheme_name)
        prefix_concept = "%s_%s_concept" % (ontology_name, concept_scheme_name)
        ttl_writer.write(
            "@prefix %s: <%s%s/> .\n"
            % (prefix_concept, COLLECTION_MAP[ontology_name], concept_scheme_name)
        )
        ttl_writer.write(
            "@prefix %s: <%s> .\n" % (prefix_ontology, ONTOLOGY_MAP[ontology_name])
        )
        ttl_writer.write(
            "@prefix %s: <%s%s> .\n"
            % (prefix_collection, COLLECTION_MAP[ontology_name], concept_scheme_name)
        )
        ttl_writer.write(
            "@prefix %s: <%s/%s> .\n"
            % (prefix_scheme, SCHEME_MAP[ontology_name], concept_scheme_name)
        )

        if ontology_name == GLOSSARY:
            ttl_writer.write("@prefix cito: <%s> .\n" % CITO)

        ttl_writer.write("@prefix owl: <%s> .\n" % OWL)
        ttl_writer.write("@prefix rdf: <%s> .\n" % RDF)
        ttl_writer.write("@prefix rdfs: <%s> .\n" % RDFS)
        ttl_writer.write("@prefix skos: <%s> .\n\n\n" % SKOS)

        # concepts
        ttl_writer.write("#\n")
        ttl_writer.write("# concepts\n")
        ttl_writer.write("#\n\n")

        count = 0
        check_hierarchy = False
        in_file = os.path.join(CSV_DIRECTORY, in_file_name)
        with open(in_file, "r", encoding="utf-8") as csvfile:
            cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
            for row in cvsreader:
                count = count + 1
                if (count < 2) or row[URI].strip() == "":
                    # header
                    if len(row) > HIERARCHY and row[HIERARCHY] == "Hierarchy Level":
                        check_hierarchy = True
                        print("check_hierarchy = True")
                    continue
                #             if len(row[URI].strip()) > 8:
                #                 print("ERROR: URI fragment too long for NERC: %s:%s:%s" %
                #                        (ontology_name, concept_scheme_name, row[URI].strip()))
                if "http" in row[URI]:
                    _write_remote_concept(
                        ttl_writer,
                        row,
                        prefix_collection,
                        prefix_scheme,
                        prefix_ontology,
                        concept_scheme_name,
                        check_hierarchy,
                    )
                else:
                    _write_local_concept(
                        ttl_writer,
                        row,
                        prefix_collection,
                        prefix_concept,
                        prefix_ontology,
                        prefix_scheme,
                        ontology_name,
                        concept_scheme_name,
                        check_hierarchy,
                    )


def _write_remote_concept(
    f,
    row,
    prefix_collection,
    prefix_scheme,
    prefix_ontology,
    concept_scheme_name,
    check_hierarchy,
):
    uri = row[URI].strip()

    f.write(
        "<{uri}> a skos:Concept, {ontology}:{scheme};\n".format(
            uri=uri, ontology=prefix_ontology, scheme=concept_scheme_name
        )
    )
    f.write("    skos:inScheme %s: ;\n" % (prefix_scheme))

    #     f.write('<{uri}> skos:inScheme {scheme}: ;\n'.format(uri=uri,
    #                                                          scheme=prefix_scheme))
    if not check_hierarchy or (
        check_hierarchy and len(row) > HIERARCHY and row[HIERARCHY] == "1"
    ):
        # this is top of any hierarchy if present
        f.write("    skos:topConceptOf %s: ;\n" % (prefix_scheme))

    if len(row) > SEE_ALSO and not row[SEE_ALSO] == "":
        if concept_scheme_name == "org":
            f.write(
                "    rdfs:seeAlso <http://isni.org/isni/%s> ;\n" % row[SEE_ALSO].strip()
            )
        elif not row[SEE_ALSO].startswith("?"):
            for also in row[SEE_ALSO].strip().split(" "):
                f.write("    rdfs:seeAlso <%s> ;\n" % also)
    f.write(".\n\n")

    # add to collection
    f.write("%s: skos:member <%s> .\n\n" % (prefix_collection, uri))

    # add line to concept scheme
    if not check_hierarchy or (
        check_hierarchy and len(row) > HIERARCHY and row[HIERARCHY] == "1"
    ):
        # this is top of any hierarchy if present
        f.write("%s: skos:hasTopConcept <%s> .\n\n" % (prefix_scheme, uri))


def _write_local_concept(
    f,
    row,
    prefix_collection,
    prefix_concept,
    prefix_ontology,
    prefix_scheme,
    ontology_name,
    concept_scheme_name,
    check_hierarchy,
):
    f.write(
        "%s:%s a skos:Concept, %s:%s;\n"
        % (prefix_concept, row[URI].strip(), prefix_ontology, concept_scheme_name)
    )
    f.write("    skos:inScheme %s: ;\n" % (prefix_scheme))
    f.write('    skos:prefLabel "%s"@en ;\n' % row[LABEL].strip())
    if row[ALT_LABEL] != "":
        f.write('    skos:altLabel "%s"@en ;\n' % row[ALT_LABEL].strip())
    if len(row) > DEF and not row[DEF] == "":
        f.write('    skos:definition "%s"@en ;\n' % row[DEF].strip())

    # needed for geonetwork
    if len(row) > DEF and not row[DEF] == "":
        f.write('    skos:scopeNote "%s"@en ;\n' % row[DEF].strip())

    if len(row) > SEE_ALSO and not row[SEE_ALSO] == "":
        if concept_scheme_name == "org":
            f.write(
                "    rdfs:seeAlso <http://isni.org/isni/%s> ;\n" % row[SEE_ALSO].strip()
            )
        elif ontology_name == GLOSSARY:
            pass
        elif not row[SEE_ALSO].startswith("?"):
            for also in row[SEE_ALSO].strip().split(" "):
                f.write("    rdfs:seeAlso <%s> ;\n" % also)
    if ontology_name == GLOSSARY and len(row) > CITES and not row[CITES] == "":
        f.write("    cito:citesAsSourceDocument <%s>;\n" % row[CITES].strip())
    if not check_hierarchy or (
        check_hierarchy and len(row) > HIERARCHY and row[HIERARCHY] == "1"
    ):
        # this is top of any hierarchy if present
        f.write("    skos:topConceptOf %s: ;\n" % (prefix_scheme))
    f.write(".\n\n")

    # add to collection
    f.write(
        "%s: skos:member %s:%s .\n\n"
        % (prefix_collection, prefix_concept, row[URI].strip())
    )

    # add line to concept scheme
    if not check_hierarchy or (
        check_hierarchy and len(row) > HIERARCHY and row[HIERARCHY] == "1"
    ):
        # this is top of any hierarchy if present
        f.write(
            "%s: skos:hasTopConcept %s:%s .\n\n"
            % (prefix_scheme, prefix_concept, row[URI].strip())
        )
