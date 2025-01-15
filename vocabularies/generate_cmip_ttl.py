from vocabularies.generate_ttl import collection
from vocabularies.generate_ttl import concept
from vocabularies.generate_ttl import mapping
from vocabularies.generate_ttl import owl
from vocabularies.generate_ttl import scheme
from vocabularies.settings import CMIP, GCOS, GRIB, MAPPING_1, SKOS, MAPPING_BOTH


def generate():
    collection.write_ttl(CMIP)

    concept.write_ttl(CMIP)

    owl.write_ttl(CMIP)

    scheme.write_ttl(CMIP)

    mapping.write_ttl(
        "cmip-realms-mapping.csv",
        "cmip-realms-mapping.ttl",
        MAPPING_BOTH,
        CMIP,
        "Realms/",
        CMIP,
        "Realms/",
        SKOS,
    )
    mapping.write_ttl(
        "cmip-gcos-domain-mapping.csv",
        "cmip-gcos-domain-mapping.ttl",
        MAPPING_1,
        CMIP,
        "Realms/",
        GCOS,
        "domain/",
        SKOS,
    )
    mapping.write_ttl(
        "cmip-gcos-ecv-mapping.csv",
        "cmip-ecv-gcos-mapping.ttl",
        MAPPING_1,
        CMIP,
        "Realms/",
        GCOS,
        "ecv/",
        SKOS,
    )
    mapping.write_ttl(
        "cmip-grib-mapping.csv",
        "cmip-grib-mapping.ttl",
        MAPPING_1,
        CMIP,
        "Realms/",
        GRIB,
        "Discipline/",
        SKOS,
    )


if __name__ == "__main__":
    generate()
