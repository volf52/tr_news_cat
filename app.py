from pathlib import Path

from fastapi import FastAPI

from news_cat.config import get_app_settings
from news_cat.web.api import router as api_router
from news_cat.web.config import get_web_config
from news_cat.web.inference import get_model_loader, get_spacy_nlp

app_cfg = get_app_settings()
app_cfg.update_base(Path(".").resolve())

# Startup. Can be done in async startup using a status flag in app_cfg
_ = get_web_config()
_ = get_spacy_nlp()
_ = get_model_loader()

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
