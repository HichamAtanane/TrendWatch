import os
import sys
from pathlib import Path
import logging
import json
from datetime import datetime
from typing import Optional
from googleapiclient.discovery import build
from dotenv import dotenv_values
