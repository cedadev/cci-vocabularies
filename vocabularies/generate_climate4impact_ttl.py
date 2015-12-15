from generate_ttl import concept, scheme
from settings import C4I


def generate():
    concept.write_ttl('climate4impact-themes.csv', 'climate4impact-themes.ttl', 'Theme', 'Theme', C4I)

    scheme.write_ttl('climate4impact-schemes.csv', 'climate4impact-schemes.ttl', C4I)


if __name__ == "__main__":
    generate()
