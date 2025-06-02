from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import sys
import time

from vocabularies import deploy_rdf
from vocabularies import generate_all_ttl
from vocabularies import generate_csv
from vocabularies import generate_html_classes
from vocabularies import generate_html_collection
from vocabularies import generate_html_scheme
from vocabularies import generate_rdf
from vocabularies import validate_csv

from .settings import APP_DIRECTORY, CSV_DIRECTORY, HTML_SOURCE

def create_directories():
    import os
    os.system(f'rm -rf {APP_DIRECTORY}/')
    os.makedirs(f'{APP_DIRECTORY}/html/ontology/cci/cci-content')
    os.makedirs(f'{APP_DIRECTORY}/html/collection/cci/cci-content')
    os.makedirs(f'{APP_DIRECTORY}/html/csv')
    os.makedirs(f'{APP_DIRECTORY}/html/error_pages')
    os.makedirs(f'{APP_DIRECTORY}/html/scheme/cci/cci-content')

    os.system(f'cp -r {CSV_DIRECTORY}/* {APP_DIRECTORY}/html/csv')

    os.system(f'cp -r {HTML_SOURCE}/* {APP_DIRECTORY}/html')

def _generate(deploy):

    print('Creating directories')
    create_directories()
    print(f"{time.strftime('%H:%M:%S')} generate_csv")
    generate_csv.generate()
    print(f"{time.strftime('%H:%M:%S')} validate csv")
    validate_csv.vailidate()
    print(f"{time.strftime('%H:%M:%S')} generate_all_ttl")
    generate_all_ttl.generate()
    print(f"{time.strftime('%H:%M:%S')} generate_rdf")
    generate_rdf.generate()
    print(f"{time.strftime('%H:%M:%S')} generate_html_classes")
    generate_html_classes.generate()
    print(f"{time.strftime('%H:%M:%S')} generate_html_scheme")
    generate_html_scheme.generate()
    print(f"{time.strftime('%H:%M:%S')} generate_html_collection")
    generate_html_collection.generate()

    if deploy is True:
        print(f"{time.strftime('%H:%M:%S')} deploy_rdf")
        deploy_rdf.deploy()


def _parse_command_line(argv):
    parser = ArgumentParser(
        description="Generate the CCI vocabularies.",
        epilog="\n\nA number of `xlsx` files are used as input. CSV versions of the files "
        "are created and then validated. These are used to generate the rdf files and html "
        "pages. By default there is no interaction with the production service.",
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-d",
        "--deploy",
        action="store_true",
        help="If set the production triple store will be updated.",
        default=0,
    )

    return parser.parse_args(argv[1:])


def main():

    args = _parse_command_line(sys.argv)
    _generate(args.deploy)


if __name__ == "__main__":
    main()
    print(f"{time.strftime('%H:%M:%S')} FINISHED")
