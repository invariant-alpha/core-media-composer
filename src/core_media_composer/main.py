import asyncio
import logging
import uuid
from datetime import datetime

try:
    from core_bus.client import RedisBusClient
    from core_bus.schemas import EventEnvelope
except ImportError:
    RedisBusClient = None
    EventEnvelope = None

from .config import MediaComposerConfig
from .schemas import ComposeRequest, ComposeCompleted
from .composer import MediaComposer

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting core-media-composer...")

    config = MediaComposerConfig()
    composer = MediaComposer(config)
    
    if not RedisBusClient:
        logger.error("core-bus missing. Running without Bus.")
        return

    bus_client = RedisBusClient()
    await bus_client.connect()

    async def on_compose_requested(envelope: EventEnvelope):
        logger.info(f"Received compose request: {envelope.correlation_id}")
        
        try:
            req = ComposeRequest.model_validate(envelope.payload)
            result: ComposeCompleted = await composer.compose(req)
            
            resp_envelope = EventEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="media.compose.completed",
                source_module="core-media-composer",
                timestamp=datetime.utcnow(),
                correlation_id=envelope.correlation_id,
                payload=result.model_dump()
            )
            await bus_client.publish("media.compose.completed", resp_envelope)
            
        except Exception as e:
            logger.error(f"Composition failed: {e}")
            fail_envelope = EventEnvelope(
                event_id=str(uuid.uuid4()),
                event_type="media.compose.failed",
                source_module="core-media-composer",
                timestamp=datetime.utcnow(),
                correlation_id=envelope.correlation_id,
                payload={"error": str(e)}
            )
            await bus_client.publish("media.compose.failed", fail_envelope)

    await bus_client.subscribe("media.compose.requested", "media_composer_group", on_compose_requested)

    logger.info("core-media-composer is listening for requests...")
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        logger.info("Shutting down core-media-composer...")
    finally:
        await bus_client.close()

if __name__ == "__main__":
    asyncio.run(main())
