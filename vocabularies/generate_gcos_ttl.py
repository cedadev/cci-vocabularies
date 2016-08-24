from generate_ttl import collection
from generate_ttl import concept
from generate_ttl import mapping
from generate_ttl import owl
from generate_ttl import scheme
from settings import CCI, CMIP, GCOS, MAPPING_1, MAPPING_2, MAPPING_BOTH, SKOS


def generate():
    collection.write_ttl(GCOS)

    concept.write_ttl(GCOS)

    owl.write_ttl(GCOS)

    scheme.write_ttl(GCOS)

    mapping.write_ttl('gcos-ecv-domain-mapping.csv', 'gcos-ecv-domain-mapping.ttl',
                      MAPPING_BOTH, GCOS, 'ecv/', GCOS, 'domain/', SKOS)
    mapping.write_ttl('gcos-domain-mapping.csv', 'gcos-domain-mapping.ttl',
                      MAPPING_BOTH, GCOS, 'domain/', GCOS, 'domain/', SKOS)
    mapping.write_ttl('cci-gcos-mapping.csv', 'gcos-cci-mapping.ttl',
                      MAPPING_1, GCOS, 'ecv/', CCI, 'ecv/', SKOS)
    mapping.write_ttl('cmip-gcos-domain-mapping.csv', 'gcos-cmip-domain-mapping.ttl',
                      MAPPING_2, CMIP, '', GCOS, 'domain/', SKOS)
    mapping.write_ttl('cmip-gcos-ecv-mapping.csv', 'gcos-cmip-ecv-mapping.ttl',
                      MAPPING_2, CMIP, '', GCOS, 'ecv/', SKOS)


if __name__ == "__main__":
    generate()
