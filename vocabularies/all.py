import time

import generate_all_ttl, generate_csv, generate_html, generate_rdf, deploy_rdf


def generate():
    print "%s generate_csv" % (time.strftime("%H:%M:%S"))
    generate_csv.generate()
    print "%s generate_all_ttl" % (time.strftime("%H:%M:%S"))
    generate_all_ttl.generate()
    print "%s generate_rdf" % (time.strftime("%H:%M:%S"))
    generate_rdf.generate()
    print "%s generate_html" % (time.strftime("%H:%M:%S"))
    generate_html.generate()
    print "%s deploy_rdf" % (time.strftime("%H:%M:%S"))
    deploy_rdf.deploy()


if __name__ == "__main__":
    generate()
    print "%s FINISHED" % (time.strftime("%H:%M:%S"))
