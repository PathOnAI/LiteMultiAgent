from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any
from pydantic import BaseModel, validator
import sys
from logging.handlers import RotatingFileHandler
import requests
import os
import json
_ = load_dotenv()


def connect_local_postgresql():
    return


## example, supbase
## return credentials, SUPABASE_URL & SUPABASE_ANON_KEY
## example, HF
## HF_TOKEN="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"
## HUGGINGFACEHUB_API_TOKEN="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"
def connect_api():
    return

## first look up Bob email address in local database (first login, then lookup),  read a template, and create a new file