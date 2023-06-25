import tabula as tb
import pandas as pd
from thefuzz import fuzz
import re


def load_doc(path):
    dfs = tb.read_pdf(path, pages="all", stream=True)
    return dfs


def extract_titles(path: str):
    data_heading = [
        "Credit",
        "Debit",
        "Balance",
        "Transaction Reference",
        "Date",
        "Ref.No./Chq.No.",
    ]
    dfs = load_doc(path)
    new_df = []
    dic_list = []

    for docs in dfs:
        dce = docs.columns
        lst = []
        dic = {}
        for name in dce:
            for c_name in data_heading:
                if fuzz.token_sort_ratio(c_name, name) > 75:
                    dic[name] = c_name
                    # print(name)
                    lst.append(name)
        # print("\n")
        if len(lst) >= 3:
            # print(lst)
            dic_list.append(dic)
            dump = docs[lst]
            if (
                fuzz.token_sort_ratio(
                    "Visit https://sbi.co.in Customer Care 1800 1234",
                    dump[lst[0]][len(dump) - 1],
                )
                > 75
            ):
                # print(dump["Date Transaction Reference"][len(dump)-1])
                dump.drop(index=[dump.index[-1]], axis=0, inplace=True)
            new_df.append(dump)
    for i, docs in enumerate(new_df):
        docs.rename(columns=dic_list[i], inplace=True, errors="raise")
    return new_df


def extract_date(data: str):
    pattern = r"(\d{2}-\d{2}-\d{2})\s"  # Matches the pattern of "dd-mm-yy " at the beginning of the string
    # Extract the date from the string
    date_match = re.search(pattern, data)
    if date_match:
        date = date_match.group(1)
    else:
        date = None
    # Remove the date from the string
    result = re.sub(pattern, "", data)
    return date, result


def cleaning_df(path: str):
    new_df = extract_titles(path)
    for docs in new_df:
        if list(docs.columns).count("Date"):
            # print("yes")
            pass
        else:
            dates = []
            ids = []
            for data in docs["Transaction Reference"]:
                # print(data)
                date, id = extract_date(data)
                dates.append(date)
                ids.append(id)
            docs["Transaction Reference"] = ids
            docs.insert(loc=0, column="Date", value=dates)
            # print("no")
    final_frame = pd.concat(new_df, ignore_index=True)
    final_frame.drop(index=[final_frame.index[0]], axis=0, inplace=True)
    final_frame.drop(index=[final_frame.index[len(final_frame) - 1]], axis=0, inplace=True)
    # final cleaning of the table
    final_frame.dropna(subset=["Balance"], inplace=True, how="all")
    final_frame.reset_index(drop=True, inplace=True)
    final_frame["Credit"]=pd.to_numeric(final_frame["Credit"],errors='coerce')
    final_frame["Debit"]=pd.to_numeric(final_frame["Debit"],errors='coerce')
    final_frame["Balance"]=pd.to_numeric(final_frame["Balance"],errors='coerce')
    final_frame.fillna(0,inplace=True)
    # len(final_frame)
    return final_frame


