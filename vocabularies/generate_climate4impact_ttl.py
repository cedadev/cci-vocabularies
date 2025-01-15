from vocabularies.generate_ttl import collection
from vocabularies.generate_ttl import concept
from vocabularies.generate_ttl import owl
from vocabularies.generate_ttl import scheme
from vocabularies.settings import C4I


def generate():
    collection.write_ttl(C4I)

    concept.write_ttl(C4I)

    owl.write_ttl(C4I)

    scheme.write_ttl(C4I)


if __name__ == "__main__":
    generate()
