import pandas as pd
import glob
import os

csv_files = glob.glob(os.path.join("data", "*.csv"))
if not csv_files:
    raise SystemExit("No CSV files found in ./data/")

dataframes = []
for file_path in csv_files:
    dataframe = pd.read_csv(file_path)
    dataframe.columns = [column.strip() for column in dataframe.columns]
    dataframes.append(dataframe)

combined_dataframe = pd.concat(dataframes, ignore_index=True)

for column_name in ["query", "Budget", "City", "Trip_type", "interest", "Duration"]:
    if column_name not in combined_dataframe.columns:
        combined_dataframe[column_name] = None

combined_dataframe.to_csv("merged_travel_dataset.csv", index=False)
print("Merged CSV saved to merged_travel_dataset.csv")
