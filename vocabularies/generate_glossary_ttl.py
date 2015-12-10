from generate_ttl import concept, scheme
from settings import  GLOSSARY


def generate():
    concept.write_ttl('ipcc-glossary.csv', 'glossary-ipcc.ttl', 'IPCCGlossary', 'IPCC', GLOSSARY)

    scheme.write_ttl('glossary-schemes.csv', 'glossary-schemes.ttl', GLOSSARY)


if __name__ == "__main__":
    generate()
