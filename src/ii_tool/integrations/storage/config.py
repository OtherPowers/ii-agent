from pydantic_settings import BaseSettings
from typing import Literal

class StorageConfig(BaseSettings):
    storage_provider: Literal["gcs"] = "gcs"
    gcs_bucket_name: str
    gcs_project_id: str