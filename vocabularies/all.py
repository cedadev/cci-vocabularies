import time

import deploy_rdf
import generate_all_ttl
import generate_csv
import generate_html_collection
import generate_rdf
import validate_csv
import generate_html_scheme
import generate_html_classes


def generate():
    start_time = time.time()
    print "%s generate_csv" % (time.strftime("%H:%M:%S"))
    generate_csv.generate()
    end_time = time.time()
    if end_time - start_time < 0.5:
        print end_time - start_time
        print "Is Office still open?"
        exit()
    print "%s validate csv" % (time.strftime("%H:%M:%S"))
    validate_csv.vailidate()
    print "%s generate_all_ttl" % (time.strftime("%H:%M:%S"))
    generate_all_ttl.generate()
    print "%s generate_rdf" % (time.strftime("%H:%M:%S"))
    generate_rdf.generate()
    print "%s generate_html_classes" % (time.strftime("%H:%M:%S"))
    generate_html_classes.generate()
    print "%s generate_html_scheme" % (time.strftime("%H:%M:%S"))
    generate_html_scheme.generate()
    print "%s generate_html_collection" % (time.strftime("%H:%M:%S"))
    generate_html_collection.generate()
    print "%s deploy_rdf" % (time.strftime("%H:%M:%S"))
    deploy_rdf.deploy()


if __name__ == "__main__":
    generate()
    print "%s FINISHED" % (time.strftime("%H:%M:%S"))
