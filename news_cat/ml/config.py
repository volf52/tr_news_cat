from dataclasses import dataclass


@dataclass
class MLConfig:
    raw_data_input = "raw_data.csv"
    raw_data_df_out = "raw_data.feather"
    train_df = "train_df.feather"
    test_df = "test_df.feather"
    valid_df = "valid_df.feather"
