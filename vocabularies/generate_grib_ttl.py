from vocabularies.generate_ttl import collection
from vocabularies.generate_ttl import concept
from vocabularies.generate_ttl import mapping
from vocabularies.generate_ttl import owl
from vocabularies.generate_ttl import scheme
from vocabularies.settings import CMIP, GRIB, MAPPING_2, SKOS


def generate():
    collection.write_ttl(GRIB)

    concept.write_ttl(GRIB)

    owl.write_ttl(GRIB)

    scheme.write_ttl(GRIB)

    mapping.write_ttl(
        "cmip-grib-mapping.csv",
        "grib-cmip-mapping.ttl",
        MAPPING_2,
        CMIP,
        "Realms/",
        GRIB,
        "Discipline/",
        SKOS,
    )


if __name__ == "__main__":
    generate()
