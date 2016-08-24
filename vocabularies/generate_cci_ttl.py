from generate_ttl import cci_mapping_cci_cf
from generate_ttl import collection
from generate_ttl import concept
from generate_ttl import mapping
from generate_ttl import owl
from generate_ttl import scheme
from settings import CCI, GCOS, MAPPING_2, MAPPING_BOTH, SKOS


def generate():
    collection.write_ttl(CCI)

    concept.write_ttl(CCI)

    owl.write_ttl(CCI)

    scheme.write_ttl(CCI)

    cci_mapping_cci_cf.write_ttl('cci-cfparameters.csv', 'cci-cf-mapping.ttl')
    mapping.write_ttl('cci-gcos-mapping.csv', 'cci-gcos-mapping.ttl',
                      MAPPING_2, GCOS, 'ecv/', CCI, 'ecv/', SKOS)
    mapping.write_ttl('cci-dataType-ecv-mapping.csv',
                      'cci-dataType-ecv-mapping.ttl', MAPPING_BOTH, CCI,
                      'dataType/', CCI, 'ecv/', SKOS)
    mapping.write_ttl('cci-platform-sensor-mapping.csv',
                      'cci-platform-sensor-mapping.ttl', MAPPING_BOTH, CCI,
                      'platform/', CCI, 'sensor/', CCI)
    mapping.write_ttl('cci-platform-programme-mapping.csv',
                      'cci-platform-programme-mapping.ttl', MAPPING_BOTH, CCI,
                      'platformProg/', CCI, 'platform/', SKOS)
    mapping.write_ttl('cci-platform-group-mapping.csv',
                      'cci-platform-group-mapping.ttl', MAPPING_BOTH, CCI,
                      'platformGrp/', CCI, 'platformProg/', SKOS)
#     mapping.write_ttl('cci-sensor-mapping.csv', 'cci-sensor-mapping.ttl',
#                       MAPPING_BOTH, CCI, 'sensor/', CCI, 'sensor/', SKOS)


if __name__ == "__main__":
    generate()
