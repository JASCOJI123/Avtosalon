from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    bot_token:str
    admin_ids:str=""
    database_url:str
    admin_username:str="admin"
    admin_password:str
    secret_key:str
    web_app_url:str=""
    cors_origins:str=""
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    @property
    def admins(self): return [int(x.strip()) for x in self.admin_ids.split(",") if x.strip()]
    @property
    def cors(self): return [x.strip() for x in self.cors_origins.split(",") if x.strip()]
settings=Settings()
