from generate_ttl import concept, scheme
from settings import C4I


def generate():
    concept.write_ttl(C4I)

    scheme.write_ttl(C4I)


if __name__ == "__main__":
    generate()
