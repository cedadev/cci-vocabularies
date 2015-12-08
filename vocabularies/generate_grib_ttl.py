from generate_ttl import concept, scheme, mapping
from settings import CMIP, GRIB, MAPPING_2, SKOS


def generate():
    concept.write_ttl('grib-disciplines.csv', 'grib-discipline.ttl', 'Discipline', 'Discipline', GRIB)
    
    scheme.write_ttl('grib-schemes.csv', 'grib-schemes.ttl', GRIB)
    
    mapping.write_ttl('cmip-grib-mapping.csv', 'grib-cmip-mapping.ttl', MAPPING_2, CMIP, GRIB, SKOS)


if __name__ == "__main__":
    generate()
