from generate_ttl import concept, scheme, mapping
from settings import CMIP, GRIB, MAPPING_2, SKOS


def generate():
    concept.write_ttl(GRIB)
    
    scheme.write_ttl(GRIB)
    
    mapping.write_ttl('cmip-grib-mapping.csv', 'grib-cmip-mapping.ttl', MAPPING_2, CMIP, GRIB, SKOS)


if __name__ == "__main__":
    generate()
