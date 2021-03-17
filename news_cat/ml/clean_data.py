import re

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from news_cat.config import get_app_settings
from news_cat.ml.config import MLConfig

cfg = get_app_settings()

BAD_PATTERNS = [
    r"\'",
    r"\"",
    r"\.",
    r",",
    r"\(",
    r"\)",
    r"\!",
    r"\?",
    r"\;",
    r"\:",
    r"([^\d])\1{2,}",  # all characters except the numerical ones, instead of the alpha only focus we had earlier
    r"\s+",
]

REPLACEMENTS = [
    " ' ",
    "",
    " . ",
    " , ",
    " ( ",
    " ) ",
    " ! ",
    " ? ",
    " ",
    " ",
    r"\1",
    " ",
]

REPL_PAT_LIST = list(
    (re.compile(p, flags=re.UNICODE), r) for p, r in zip(BAD_PATTERNS, REPLACEMENTS)
)


def clean_normalize_text(txt: str) -> str:
    pattern_re: re.Pattern

    for pattern_re, replace_str in REPL_PAT_LIST:
        txt = pattern_re.sub(replace_str, txt)

    return txt


def process_raw_data():
    base_pth = cfg.data_dir

    print("Loading raw data...")  # Can be improved by adding a logger here
    df = pd.read_csv(base_pth.joinpath(MLConfig.raw_data_input))

    print("Saving raw data as feather...")
    df.to_feather(base_pth.joinpath(MLConfig.raw_data_df_out))

    print("Cleaning up the data...")
    df["clean_txt"] = df["text"].apply(clean_normalize_text)
    df.drop(columns="text", inplace=True)

    print("Encoding labels...")
    lbl_encoder = LabelEncoder()
    df["category"] = lbl_encoder.fit_transform(df["category"])
    df["category"] = pd.to_numeric(df["category"], downcast="unsigned")

    joblib.dump(
        list(lbl_encoder.classes_),
        cfg.artifact_dir.joinpath("lbl_encoder.jlib"),
        compress=3,
    )

    print("Splitting the data into train, test and valid (and saving it)...")
    train_df: pd.DataFrame
    test_df: pd.DataFrame
    valid_df: pd.DataFrame
    train_df, test_df = train_test_split(df, test_size=0.1)
    train_df, valid_df = train_test_split(train_df, test_size=test_df.shape[0])

    train_df.reset_index(inplace=True, drop=True)
    test_df.reset_index(inplace=True, drop=True)
    valid_df.reset_index(inplace=True, drop=True)

    train_df.to_feather(base_pth.joinpath(MLConfig.train_df))
    test_df.to_feather(base_pth.joinpath(MLConfig.test_df))
    valid_df.to_feather(base_pth.joinpath(MLConfig.valid_df))

    print("Done")


if __name__ == "__main__":
    process_raw_data()
