import os
import sys
from pathlib import Path
import logging
import json
from datetime import datetime
from typing import Optional
from googleapiclient.discovery import build
from dotenv import dotenv_values


config = dotenv_values("../.env")
API_KEY = config["API_KEY"]
REGION_CODES_FILE = Path("../data/input/region_codes.txt")
STAGING_DIR = "../data/staging/"
LOG_FILE = Path(STAGING_DIR) / "etl.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
