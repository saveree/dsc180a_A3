import pandas as pd
import numpy as np
import requests
import lxml.html as lh
import requests
from bs4 import BeautifulSoup
import re
import json
import sys
import shutil

sys.path.insert(0, 'src') # add library code to path
from etl import get_data

DATA_PARAMS = 'config/data-params.json'
TEST_PARAMS = 'config/config_a1.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)

    return param

def main(targets):

    # make the clean target
    if 'clean' in targets:
        shutil.rmtree('data/temp',ignore_errors=True)
        shutil.rmtree('data/out',ignore_errors=True)
        shutil.rmtree('data/test',ignore_errors=True)

    # make the data target
    if 'data' in targets:
        cfg = load_params(DATA_PARAMS)
        get_data(**cfg)

    # make the test target
    if 'test' in targets:
        cfg = load_params(TEST_PARAMS)
        get_data(**cfg)
    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
