from multion.client import MultiOn
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any
from pydantic import BaseModel, validator
import requests
import os
import json
load_dotenv()

# api_key="ee83f871c4594a8983e349b303d4f8fe"
multion = MultiOn(api_key=os.getenv('MULTION_API_KEY'))
browse = multion.browse(
    cmd="Find the top comment of the top post on Hackernews.",
    url="https://news.ycombinator.com/"
)
print("Browse response:", browse)
print(browse.message)


browse = multion.browse(
    cmd="browse amazon.com to check the brands of dining table and summarize the results in a table",
    url="https://www.amazon.com/"
)
print("Browse response:", browse)
print(browse.message)
# import pdb; pdb.set_trace()

# Browse response: message='It seems that I encountered a CAPTCHA on Amazon. Could you please solve the CAPTCHA so I can continue browsing for dining tables?\n' status='NOT_SURE' url='https://www.amazon.com/errors/validateCaptcha?amzn=7TkaJtSVXE1r0iiaDUPTZA%3D%3D&amzn-r=%2F&field-keywords=dining+table' screenshot='' session_id='df8d2db2-ca2c-4be3-b7ec-842a16f7f8d3' metadata=Metadata(step_count=2, processing_time=6, temperature=0.2)
# It seems that I encountered a CAPTCHA on Amazon. Could you please solve the CAPTCHA so I can continue browsing for dining tables?
