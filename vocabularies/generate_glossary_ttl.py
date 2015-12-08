from generate_ttl import glossary, scheme
from settings import  GLOSSARY


def generate():
    glossary.write_ttl('ipcc-glossary.csv', 'glossary-ipcc.ttl', 'IPCCGlossary', 'IPCC Glossary', GLOSSARY)
    scheme.write_ttl('glossary-schemes.csv', 'glossary-schemes.ttl', GLOSSARY)


if __name__ == "__main__":
    generate()
