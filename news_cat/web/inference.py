import random
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Dict, List, Tuple

import joblib
import numpy as np
import spacy
import torch
from sklearn.pipeline import Pipeline

from news_cat.config import get_app_settings
from news_cat.ml.clean_data import clean_normalize_text
from news_cat.web.config import get_web_config
from news_cat.web.schemas import MLModel


class Classifier(ABC):
    __slots__ = '_underlying_model'

    @abstractmethod
    def __call__(self, tokens: List[str]) -> np.ndarray:
        pass


class SkClassifier(Classifier):
    def __init__(self, model: Pipeline):
        self._underlying_model = model

    def __call__(self, tokens: List[str]) -> int:
        tok_txt = ' '.join(tokens)
        prediction = self._underlying_model.predict([tok_txt])
        if prediction.size == 1:
            prediction = prediction[0]
        else:
            prediction = prediction.argmax()

        return prediction


class ModelLoader:
    __slots__ = "models", "classes"

    def __init__(self):
        self.models: Dict[str, Classifier] = {}
        self.classes: List[str] = []

    def load_models(self, available_models: List[MLModel]):
        base_pth = get_app_settings().artifact_dir

        print("Loading models...")
        self.classes = joblib.load(base_pth.joinpath("lbl_encoder.jlib"))

        for av_mdl in available_models:
            pth = base_pth.joinpath(av_mdl.filename)
            if av_mdl.type == 'scikit':
                model = SkClassifier(joblib.load(pth))
            elif av_mdl.type == 'torch':
                model = torch.load(pth)
            elif av_mdl.type == 'random':
                model = lambda x: random.randint(0, len(self.classes) - 1)
            else:
                raise ValueError(f"Invalid model type: {av_mdl.type}")

            self.models[av_mdl.name] = model

        print("Done")


@lru_cache(maxsize=1)
def get_model_loader():
    model_loader = ModelLoader()
    web_cfg = get_web_config()

    model_loader.load_models(web_cfg.available_models)

    return model_loader


@lru_cache(maxsize=1)
def get_spacy_nlp():
    nlp = spacy.blank("tr")
    # Optionally initialize lemmatizer here, or load trained pipeline from disk

    return nlp


def clean_and_tokenize(txt: str) -> Tuple[bool, List[str]]:
    txt = clean_normalize_text(txt)
    nlp = get_spacy_nlp()
    tokens = [tok for tok in nlp(txt) if not tok.is_space]

    all_punct = all(tok.is_punct for tok in tokens)

    return all_punct, [tok.lower_ for tok in tokens]
