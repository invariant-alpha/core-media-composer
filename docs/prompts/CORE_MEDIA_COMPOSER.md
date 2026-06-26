# Prompt Operativo — CORE_MEDIA_COMPOSER

## Ruolo nel Sistema
Core Engine (Livello 1). Post-produzione e montaggio. 
Riceve istruzioni dal bus (`media.compose.requested`) contenenti una lista di asset grezzi (immagini generati da AI Model Router, clip audio) e le compone in un prodotto finale (es. un file MP4).
Per la fase di MVP/Bootstrap, simuleremo il rendering pesante di `moviepy` o `ffmpeg` con un mockup che genera un "video fittizio" in base64 o semplicemente restituisce un successo se le specifiche sono valide.
Il risultato finale viene poi caricato su `core-storage` emettendo un evento, oppure l'url viene comunicato indietro al bus.

## Lifecycle
Controllabile (RUNNING, PAUSED, STOPPED).
- Se PAUSED, i job di montaggio rimangono in coda.

## Configurazione
```python
from pydantic import BaseModel, Field

class MediaComposerConfig(BaseModel):
    max_concurrent_jobs: int = Field(default=3, description="Job massimi concorrenti")
    default_output_format: str = Field(default="mp4", description="Formato default (es. mp4)")
    default_resolution: str = Field(default="1080p", description="Risoluzione default (es. 1080p, 720p)")
```

## Dipendenze
- Moduli già implementati: `core-bus`.
- Librerie esterne: nessuna (simulazione) per il momento.

## Schema Pydantic Completo
```python
from pydantic import BaseModel
from typing import List, Dict, Optional

class ComposeRequest(BaseModel):
    assets: List[Dict] = []
    composition_spec: dict
    output_format: str = "mp4"
    correlation_id: str

class ComposeCompleted(BaseModel):
    asset_id: str
    storage_url: str
    duration_seconds: float
    format: str
    cost_usd: float
    correlation_id: str
```

## Contratto Redis Streams
- Stream sottoscritti: `media.compose.requested`
- Stream pubblicati: `media.compose.completed`, `media.compose.failed`
- DLQ: `system.dlq.media`

## Flusso Principale
1. Riceve `ComposeRequest`.
2. Valida la presenza di asset e `composition_spec`.
3. Avvia una simulazione asincrona di montaggio (`asyncio.sleep()`).
4. Emette l'evento di successo `media.compose.completed` con un url fittizio e i costi stimati.

## Struttura Directory
```
core-media-composer/
├── Dockerfile
├── pyproject.toml
├── docs/
│   └── prompts/
│       └── CORE_MEDIA_COMPOSER.md
├── src/
│   └── core_media_composer/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── schemas.py
│       └── composer.py
└── tests/
    ├── unit/
    └── integration/
```

## Test Richiesti
- Unit test: testing del behavior mockato (sleep asincrono e restituzione output formattato).

## Definition of Done
- [ ] Tutti i test passano
- [ ] Connessione al bus Redis e pubblicazione eventi.
