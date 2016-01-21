import time

import generate_all_ttl
import generate_csv
import generate_html
import generate_rdf
import deploy_rdf


def generate():
    start_time = time.time()
    print "%s generate_csv" % (time.strftime("%H:%M:%S"))
    generate_csv.generate()
    end_time = time.time()
    if end_time - start_time < 0.5:
        print end_time - start_time
        print "Is Office still open?"
        exit()
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
