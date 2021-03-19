from typing import Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def tfidf_train(txt: np.ndarray, *, max_features=25_000) -> Tuple[TfidfVectorizer, np.ndarray]:
    vectorizer = TfidfVectorizer(max_features=max_features)

    txt_vectors = vectorizer.fit_transform(txt)

    return vectorizer, txt_vectors
