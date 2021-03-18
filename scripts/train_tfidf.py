import joblib
import numpy as np
import pandas as pd
from scipy.sparse import save_npz

from news_cat.config import get_app_settings
from news_cat.ml.config import MLConfig
from news_cat.ml.embedding import tfidf_train


def vectorize():
    base = get_app_settings().data_dir

    print("Loading data...")
    train_df = pd.read_feather(base.joinpath(MLConfig.train_df))
    test_df = pd.read_feather(base.joinpath(MLConfig.test_df))
    valid_df = pd.read_feather(base.joinpath(MLConfig.valid_df))

    max_features = 25_000
    txt_col = "clean_txt"
    lbl_col = "category"
    print(f"Training Tf-Idf vectorizer with {max_features} max features...")
    vectorizer, trainX = tfidf_train(
        train_df[txt_col].values, max_features=max_features
    )

    print("Transforming test and valid sets...")
    testX = vectorizer.transform(test_df[txt_col].values)
    validX = vectorizer.transform(valid_df[txt_col].values)

    print("Saving vectorizer, vectorized data and labels...")
    artifact_dir = get_app_settings().artifact_dir
    joblib.dump(vectorizer, artifact_dir.joinpath(MLConfig.embedding.tfidf_vectorizer))

    save_npz(base.joinpath(MLConfig.embedding.train_tfidf), trainX)
    save_npz(base.joinpath(MLConfig.embedding.test_tfidf), testX)
    save_npz(base.joinpath(MLConfig.embedding.valid_tfidf), validX)

    np.save(base.joinpath(MLConfig.embedding.trainY), train_df[lbl_col].values)
    np.save(base.joinpath(MLConfig.embedding.testY), test_df[lbl_col].values)
    np.save(base.joinpath(MLConfig.embedding.validY), valid_df[lbl_col].values)

    print("Done...")


if __name__ == "__main__":
    vectorize()
