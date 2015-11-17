'''
Created on 16 Nov 2015

@author: wilsona
'''

from generate_ttl import gcos_concept, gcos_mapping_gcos_cci, scheme


gcos_concept.write_ttl('gcos-ecv.csv', 'gcos-ecv.ttl', 'ECV', 'Essential Climate Variable')

scheme.write_ttl('gcos-schemes.csv', 'gcos-schemes.ttl', 'gcos')

gcos_mapping_gcos_cci.write_ttl('cci-gcos-mapping.csv', 'gcos-cci-mapping.ttl')

