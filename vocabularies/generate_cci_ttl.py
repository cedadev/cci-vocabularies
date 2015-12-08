from generate_ttl import concept, scheme, cci_mapping_cci_cf, mapping
from settings import CCI, GCOS, MAPPING_2, MAPPING_BOTH, SKOS

def generate():
    concept.write_ttl('cci-ecv.csv', 'cci-ecv.ttl', 'ECV', 'Essential Climate Variable', CCI)
    concept.write_ttl('cci-frequency.csv', 'cci-frequency.ttl', 'Frequency', 'Frequency', CCI)
    concept.write_ttl('cci-platforms.csv', 'cci-platform.ttl', 'Platform', 'Platform', CCI)
    concept.write_ttl('cci-processing-levels.csv', 'cci-processing-level.ttl', 'ProcessingLevel', 'Processing Level', CCI)
    concept.write_ttl('cci-sensor.csv', 'cci-sensor.ttl', 'Sensor', 'Sensor', CCI)
    concept.write_ttl('cci-org.csv', 'cci-org.ttl', 'Organisation', 'Organisation', CCI)
    
    scheme.write_ttl('cci-schemes.csv', 'cci-schemes.ttl', CCI)
    
    cci_mapping_cci_cf.write_ttl('cci-cfparameters.csv', 'cci-cf-mapping.ttl')
    mapping.write_ttl('cci-gcos-mapping.csv', 'cci-gcos-mapping.ttl', MAPPING_2, GCOS, CCI, SKOS)
    mapping.write_ttl('cci-platform-sensor-mapping.csv', 'cci-platform-sensor-mapping.ttl', MAPPING_BOTH, CCI, CCI, CCI)


if __name__ == "__main__":
    generate()
