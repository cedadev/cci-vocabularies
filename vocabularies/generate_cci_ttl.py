from generate_ttl import concept, scheme, cci_mapping_cci_cf, mapping
from settings import CCI, GCOS, MAPPING_2, MAPPING_BOTH, SKOS


def generate():
    concept.write_ttl(CCI)

    scheme.write_ttl(CCI)

    cci_mapping_cci_cf.write_ttl('cci-cfparameters.csv', 'cci-cf-mapping.ttl')
    mapping.write_ttl('cci-gcos-mapping.csv', 'cci-gcos-mapping.ttl',
                      MAPPING_2, GCOS, CCI, SKOS)
    mapping.write_ttl('cci-platform-sensor-mapping.csv',
                      'cci-platform-sensor-mapping.ttl', MAPPING_BOTH, CCI,
                      CCI, CCI)


if __name__ == "__main__":
    generate()
