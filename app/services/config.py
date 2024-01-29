from typing import List
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    admin_token: str
    ride2go_query_data: str
    env: str = 'DEV'
    graphhopper_base_url: str = 'https://api.mfdz.de/gh'

config = Config(_env_file='config', _env_file_encoding='utf-8')
