'''
Created on 16 Nov 2015

@author: wilsona
'''

from generate_ttl import cci_concept, scheme, cci_mapping_cci_cf, cci_mapping_cci_gcos, cci_mapping_platform_sensor


cci_concept.write_ttl('cci-ecv.csv', 'cci-ecv.ttl', 'ECV', 'Essential Climate Variable')
cci_concept.write_ttl('cci-platforms.csv', 'cci-platform.ttl', 'Platform', 'Platform')
cci_concept.write_ttl('cci-processing-levels.csv', 'cci-processing-level.ttl', 'ProcessingLevel', 'Processing Level')
cci_concept.write_ttl('cci-sensor.csv', 'cci-sensor.ttl', 'Sensor', 'Sensor')
cci_concept.write_ttl('cci-org.csv', 'cci-org.ttl', 'Organisation', 'Organisation')

scheme.write_ttl('cci-schemes.csv', 'cci-schemes.ttl', 'cci')

cci_mapping_cci_cf.write_ttl('cci-cfparameters.csv', 'cci-cf-mapping.ttl')
cci_mapping_cci_gcos.write_ttl('cci-gcos-mapping.csv', 'cci-gcos-mapping.ttl')
cci_mapping_platform_sensor.write_ttl('cci-platform-sensor-mapping.csv', 'cci-platform-sensor-mapping.ttl')
