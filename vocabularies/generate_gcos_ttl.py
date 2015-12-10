from generate_ttl import concept, scheme, top_concept, mapping
from settings import  CCI, CMIP, GCOS, MAPPING_1, MAPPING_2, SKOS


def generate():
    concept.write_ttl('gcos-ecv.csv', 'gcos-ecv.ttl', 'ECV', 'Essential Climate Variable', GCOS)

    top_concept.write_ttl('gcos-top-concepts.csv', 'gcos-top-concepts.ttl', 'ECV', GCOS)
    
    scheme.write_ttl('gcos-schemes.csv', 'gcos-schemes.ttl', GCOS)
    
    mapping.write_ttl('gcos-ecv-mapping.csv', 'gcos-ecv-mapping-1.ttl', MAPPING_1, GCOS, GCOS, SKOS)
    mapping.write_ttl('gcos-ecv-mapping.csv', 'gcos-ecv-mapping-2.ttl', MAPPING_2, GCOS, GCOS, SKOS)
    mapping.write_ttl('cci-gcos-mapping.csv', 'gcos-cci-mapping.ttl', MAPPING_1, GCOS, CCI, SKOS)
    mapping.write_ttl('cmip-gcos-mapping.csv', 'gcos-cmip-mapping.ttl', MAPPING_2, CMIP, GCOS, SKOS)


if __name__ == "__main__":
    generate()
