import generate_cci_ttl
import generate_climate4impact_ttl
import generate_cmip_ttl
import generate_gcos_ttl
import generate_grib_ttl

from settings import ONTOLOGIES, CCI, C4I, CMIP, GCOS, GRIB, GLOSSARY


def generate():
    if CCI in ONTOLOGIES:
        generate_cci_ttl.generate()
    if C4I in ONTOLOGIES:
        generate_climate4impact_ttl.generate()
    if CMIP in ONTOLOGIES:
        generate_cmip_ttl.generate()
    if GCOS in ONTOLOGIES:
        generate_gcos_ttl.generate()
    if GRIB in ONTOLOGIES:
        generate_grib_ttl.generate()
    if GLOSSARY in ONTOLOGIES:
        import generate_glossary_ttl

        generate_glossary_ttl.generate()


if __name__ == "__main__":
    generate()
