from functools import lru_cache
from typing import List

from pydantic import BaseConfig

from news_cat.web.schemas import MLModel


class WebConfig(BaseConfig):
    available_models: List[MLModel] = [
        MLModel(type="random", filename="", name="random"),
        MLModel(type="scikit", filename="model_logistic.jlib", name="tfidf_25k_logistic")
    ]


@lru_cache(maxsize=1)
def get_web_config() -> WebConfig:
    return WebConfig()
