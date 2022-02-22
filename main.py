import argparse
import json

from src.utils.parser import load_parameters
from controller import Controller
from os.path import join

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", dest='use_view', action='store_true', help="Use UI")
    parser.add_argument("-p", dest='param', help="Parameter File")
    args = parser.parse_args()

    parameters = load_parameters(args.param)
    parameters["USE_VIEW"] = args.use_view or parameters["USE_VIEW"]

    crtl = Controller(parameters=parameters)
    crtl.main_loop()

if __name__ == "__main__":
    main()
