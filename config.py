import os
import yaml
from dotenv import load_dotenv
from dataclasses import dataclass
import autogen

load_dotenv()

@dataclass
class API_KEYS():
    apify_api_key: str
    serper_api_key: str

    @classmethod
    def load_env(cls):
        return API_KEYS(
            apify_api_key = os.getenv("APIFY_API_KEY"),
            serper_api_key = os.getenv("SERP_API_KEY"),
        )


@dataclass
class Config():
    gpt4_config: dict
    
    @classmethod
    def load_yaml(cls):
        with open("config.yaml", "r") as file:
            setup = yaml.safe_load(file)
        return Config(
            gpt4_config = {
                "cache_seed": setup['cache_seed'],
                "temperature": setup['temperature'],
                "config_list": autogen.config_list_from_json(
                    "AOAI_CONFIG_LIST",
                    filter_dict={"model": setup['model_name']},
                    ),
                "timeout": setup['timeout'],
            }
        )