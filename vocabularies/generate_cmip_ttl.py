from generate_ttl import concept, scheme, top_concept, mapping
from settings import CMIP, GCOS, GRIB, MAPPING_1, MAPPING_2, SKOS

def generate():
    concept.write_ttl('cmip-realms.csv', 'cmip-realm.ttl', 'Realm', 'Realm', CMIP)

    top_concept.write_ttl('cmip-top-concepts.csv', 'cmip-top-concepts.ttl', 'Realm', CMIP)

    scheme.write_ttl('cmip-schemes.csv', 'cmip-schemes.ttl', CMIP)

    mapping.write_ttl('cmip-realms-mapping.csv', 'cmip-realms-mapping-1.ttl', MAPPING_1, CMIP, CMIP, SKOS)
    mapping.write_ttl('cmip-realms-mapping.csv', 'cmip-realms-mapping-2.ttl', MAPPING_2, CMIP, CMIP, SKOS)
    mapping.write_ttl('cmip-gcos-mapping.csv', 'cmip-gcos-mapping.ttl', MAPPING_1, CMIP, GCOS, SKOS)
    mapping.write_ttl('cmip-grib-mapping.csv', 'cmip-grib-mapping.ttl', MAPPING_1, CMIP, GRIB, SKOS)


if __name__ == "__main__":
    generate()
