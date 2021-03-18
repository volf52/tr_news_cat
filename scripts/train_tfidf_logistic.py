import json

import joblib
import numpy as np
from scipy.sparse import load_npz
from sklearn.pipeline import Pipeline

from news_cat.config import get_app_settings
from news_cat.ml.classifiers import tfidf_logistic_classifier
from news_cat.ml.config import MLConfig


def train_tfidf_logistic():
    print("Loading data...")
    cfg = get_app_settings()

    trainX = load_npz(cfg.data_dir.joinpath(MLConfig.embedding.train_tfidf))
    testX = load_npz(cfg.data_dir.joinpath(MLConfig.embedding.test_tfidf))

    trainY = np.load(cfg.data_dir.joinpath(MLConfig.embedding.trainY))
    testY = np.load(cfg.data_dir.joinpath(MLConfig.embedding.testY))

    print("Training the Logistic classifier...")
    clf, eval_metrics = tfidf_logistic_classifier(trainX, trainY, testX, testY)

    print("Saving the model and associated metrics...")
    tfidf = joblib.load(cfg.artifact_dir.joinpath(MLConfig.embedding.tfidf_vectorizer))
    joblib.dump(
        Pipeline([("tfidf", tfidf), ("logistic_clf", clf)]),
        cfg.artifact_dir.joinpath("model_logistic.jlib"),
    )

    with cfg.metrics_dir.joinpath("metrics_logistic.json").open("w") as f:
        json.dump(eval_metrics, f)

    print("Done")


if __name__ == "__main__":
    train_tfidf_logistic()
