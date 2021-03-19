from dataclasses import dataclass


@dataclass
class Embedding:
    tfidf_vectorizer = "tfidf.jlib"

    train_tfidf = "train_tfidf.npz"
    test_tfidf = "test_tfidf.npz"
    valid_tfidf = "valid_tfidf.npz"

    trainY = "train_lbl.npy"
    testY = "test_lbl.npy"
    validY = "valid_lbl.npy"


@dataclass
class MLConfig:
    raw_data_input = "raw_data.csv"
    raw_data_df_out = "raw_data.feather"

    train_df = "train_df.feather"
    test_df = "test_df.feather"
    valid_df = "valid_df.feather"

    embedding = Embedding()
