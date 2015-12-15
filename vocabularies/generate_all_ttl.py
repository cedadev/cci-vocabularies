import generate_cci_ttl, generate_climate4impact_ttl, generate_cmip_ttl, \
    generate_gcos_ttl, generate_grib_ttl, generate_glossary_ttl


def generate():
    generate_cci_ttl.generate()
    generate_climate4impact_ttl.generate()
    generate_cmip_ttl.generate()
    generate_gcos_ttl.generate()
    generate_grib_ttl.generate()
    generate_glossary_ttl.generate()


if __name__ == "__main__":
    generate()
