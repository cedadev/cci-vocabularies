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
    in_file = os.path.join(CSV_DIRECTORY, f"{ontology_name}-schemes.csv")
    count = 0
    with open(in_file, "r", encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            concept_scheme_uri = row[URI].strip()
            file_name = f"{ontology_name}-{concept_scheme_uri.lower()}"
            _write_concepts(file_name, ontology_name, concept_scheme_uri)


def _write_concepts(file_name, ontology_name, concept_scheme_name):
    """
    Write out a list of concepts from a file.

    Add them to a concept scheme and a collection.

    @param file_name (str): the root of the file name
    @param ontology_name (str): the name of the ontology
    @param concept_scheme_name (str): the name of the concept scheme
    """
    in_file_name = f"{file_name}.csv"
    out_file_name = f"{file_name}.ttl"
    out_file = os.path.join(MODEL_DIRECTORY, out_file_name)
    with open(out_file, "w", encoding="utf-8") as ttl_writer:
        prefix_ontology = f"{ontology_name}_ontology"
        prefix_scheme = f"{ontology_name}_{concept_scheme_name}_scheme"
        prefix_collection = f"{ontology_name}_{concept_scheme_name}_coll"
        prefix_concept = f"{ontology_name}_{concept_scheme_name}_concept"
        ttl_writer.write(
            f"@prefix {prefix_concept}: <{COLLECTION_MAP[ontology_name]}{concept_scheme_name}/> .\n"
        )
        ttl_writer.write(
            f"@prefix {prefix_ontology}: <{ONTOLOGY_MAP[ontology_name]}> .\n"
        )
        ttl_writer.write(
            f"@prefix {prefix_collection}: <{COLLECTION_MAP[ontology_name]}{concept_scheme_name}> .\n"
        )
        ttl_writer.write(
            f"@prefix {prefix_scheme}: <{SCHEME_MAP[ontology_name]}/{concept_scheme_name}> .\n"
        )

        if ontology_name == GLOSSARY:
            ttl_writer.write(f"@prefix cito: <{CITO}> .\n")

        ttl_writer.write(f"@prefix owl: <{OWL}> .\n")
        ttl_writer.write(f"@prefix rdf: <{RDF}> .\n")
        ttl_writer.write(f"@prefix rdfs: <{RDFS}> .\n")
        ttl_writer.write(f"@prefix skos: <{SKOS}> .\n\n\n")

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

    f.write(f"<{uri}> a skos:Concept, {prefix_ontology}:{concept_scheme_name};\n")
    f.write(f"    skos:inScheme {prefix_scheme}: ;\n")

    #     f.write('<{uri}> skos:inScheme {scheme}: ;\n'.format(uri=uri,
    #                                                          scheme=prefix_scheme))
    if not check_hierarchy or (
        check_hierarchy and len(row) > HIERARCHY and row[HIERARCHY] == "1"
    ):
        # this is top of any hierarchy if present
        f.write(f"    skos:topConceptOf {prefix_scheme}: ;\n")

    if len(row) > SEE_ALSO and not row[SEE_ALSO] == "":
        if concept_scheme_name == "org":
            f.write(
                f"    rdfs:seeAlso <http://isni.org/isni/{row[SEE_ALSO].strip()}> ;\n"
            )
        elif not row[SEE_ALSO].startswith("?"):
            for also in row[SEE_ALSO].strip().split(" "):
                f.write(f"    rdfs:seeAlso <{also}> ;\n")
    f.write(".\n\n")

    # add to collection
    f.write(f"{prefix_collection}: skos:member <{uri}> .\n\n")

    # add line to concept scheme
    if not check_hierarchy or (
        check_hierarchy and len(row) > HIERARCHY and row[HIERARCHY] == "1"
    ):
        # this is top of any hierarchy if present
        f.write(f"{prefix_scheme}: skos:hasTopConcept <{uri}> .\n\n")


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
        f"{prefix_concept}:{row[URI].strip()} a skos:Concept, {prefix_ontology}:{concept_scheme_name};\n"
    )
    f.write(f"    skos:inScheme {prefix_scheme}: ;\n")
    f.write(f'    skos:prefLabel "{row[LABEL].strip()}"@en ;\n')
    if row[ALT_LABEL] != "":
        f.write(f'    skos:altLabel "{row[ALT_LABEL].strip()}"@en ;\n')
    if len(row) > DEF and not row[DEF] == "":
        f.write(f'    skos:definition "{row[DEF].strip()}"@en ;\n')

    # needed for geonetwork
    if len(row) > DEF and not row[DEF] == "":
        f.write(f'    skos:scopeNote "{row[DEF].strip()}"@en ;\n')

    if len(row) > SEE_ALSO and not row[SEE_ALSO] == "":
        if concept_scheme_name == "org":
            f.write(
                f"    rdfs:seeAlso <http://isni.org/isni/{row[SEE_ALSO].strip()}> ;\n"
            )
        elif ontology_name == GLOSSARY:
            pass
        elif not row[SEE_ALSO].startswith("?"):
            for also in row[SEE_ALSO].strip().split(" "):
                f.write(f"    rdfs:seeAlso <{also}> ;\n")
    if ontology_name == GLOSSARY and len(row) > CITES and not row[CITES] == "":
        f.write(f"    cito:citesAsSourceDocument <{row[CITES].strip()}>;\n")
    if not check_hierarchy or (
        check_hierarchy and len(row) > HIERARCHY and row[HIERARCHY] == "1"
    ):
        # this is top of any hierarchy if present
        f.write(f"    skos:topConceptOf {prefix_scheme}: ;\n")
    f.write(".\n\n")

    # add to collection
    f.write(
        f"{prefix_collection}: skos:member {prefix_concept}:{row[URI].strip()} .\n\n"
    )

    # add line to concept scheme
    if not check_hierarchy or (
        check_hierarchy and len(row) > HIERARCHY and row[HIERARCHY] == "1"
    ):
        # this is top of any hierarchy if present
        f.write(
            f"{prefix_scheme}: skos:hasTopConcept {prefix_concept}:{row[URI].strip()} .\n\n"
        )
