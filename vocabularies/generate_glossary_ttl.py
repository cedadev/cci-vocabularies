from vocabularies.generate_ttl import concept, mapping, scheme
from vocabularies.settings import GLOSSARY, MAPPING_1, SKOS


def generate():
    concept.write_ttl(GLOSSARY)

    scheme.write_ttl(GLOSSARY)

    mapping.write_ttl(
        "glossary-ipcc-mappings.csv",
        "glossary-ipcc-mappings.ttl",
        MAPPING_1,
        GLOSSARY,
        "",
        GLOSSARY,
        "",
        SKOS,
    )


if __name__ == "__main__":
    generate()
