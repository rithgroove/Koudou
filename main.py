import argparse

from controller import Controller
from os.path import join


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", dest='use_view', action='store_true', help="Use UI")
    args = parser.parse_args()


    crtl = Controller()
    if args.use_view:
        crtl.use_view()
        crtl.main_loop()
    else:
        osm_file = join("osm_files","TX-To-TU.osm")
        crtl.load_map(osm_file)
        crtl.print_map()

if __name__ == "__main__":
    main()
