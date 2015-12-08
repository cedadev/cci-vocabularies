from generate_ttl import concept, scheme, mapping
from settings import CMIP, GCOS, GRIB, MAPPING_1, SKOS

def generate():
    concept.write_ttl('cmip-realms.csv', 'cmip-realm.ttl', 'Realm', 'Realm', CMIP)
    
    scheme.write_ttl('cmip-schemes.csv', 'cmip-schemes.ttl', CMIP)
    
    mapping.write_ttl('cmip-gcos-mapping.csv', 'cmip-gcos-mapping.ttl', MAPPING_1, CMIP, GCOS, SKOS)
    mapping.write_ttl('cmip-grib-mapping.csv', 'cmip-grib-mapping.ttl', MAPPING_1, CMIP, GRIB, SKOS)


if __name__ == "__main__":
    generate()
