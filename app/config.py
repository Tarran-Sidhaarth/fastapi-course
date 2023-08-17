from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Setting(BaseSettings):
    databaseHostName: str
    databasePort: str
    databasePassword: str
    databaseName: str
    databaseUserName: str
    secretKey: str
    algorithm: str
    accessTokenExpiration : int
    
    class Config:
        env_file = ".env"
    
settings = Setting()