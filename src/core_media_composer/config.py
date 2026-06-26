from pydantic import BaseModel, Field

class MediaComposerConfig(BaseModel):
    max_concurrent_jobs: int = Field(default=3, description="Job massimi concorrenti")
    default_output_format: str = Field(default="mp4", description="Formato default")
    default_resolution: str = Field(default="1080p", description="Risoluzione default")
