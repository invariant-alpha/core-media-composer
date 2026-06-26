import pytest
from core_media_composer.config import MediaComposerConfig
from core_media_composer.schemas import ComposeRequest
from core_media_composer.composer import MediaComposer

@pytest.fixture
def mock_config():
    return MediaComposerConfig()

@pytest.mark.asyncio
async def test_compose_success(mock_config):
    composer = MediaComposer(mock_config)
    req = ComposeRequest(
        assets=[{"type": "image", "url": "mock1"}],
        composition_spec={"style": "tiktok"},
        output_format="mp4",
        correlation_id="corr_123"
    )
    
    result = await composer.compose(req)
    
    assert result.asset_id is not None
    assert result.format == "mp4"
    assert "mock-bucket" in result.storage_url
    assert result.cost_usd == 0.05
    assert result.correlation_id == "corr_123"
