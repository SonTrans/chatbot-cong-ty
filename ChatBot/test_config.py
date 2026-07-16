import os
from dotenv import load_dotenv

load_dotenv()
from src.config.configs import config_models
from src.graph.configuration import LLMConfig
import json

print(json.dumps(config_models.__dict__, default=lambda o: o.__dict__, indent=2))
print("LLMConfig:", LLMConfig().model_dump())
