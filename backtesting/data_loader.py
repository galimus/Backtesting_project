import pandas as pd

def load_returns(file_path: str, sheet_name: str = "Return Indices") -> pd.DataFrame:
    xls = pd.ExcelFile(file_path)
    df = xls.parse(sheet_name)
    df.rename(columns={df.columns[0]: "Date"}, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df.dropna(how="all", subset=df.columns[1:], inplace=True)
    return df.reset_index(drop=True)
