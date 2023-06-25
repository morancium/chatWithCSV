import streamlit as st
import tabula as tb
import pandas as pd
from thefuzz import fuzz
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
from utils import cleaning_df, load_doc
import os
import re

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_token=OPENAI_API_KEY, temperature=0)
pandas_ai = PandasAI(llm=llm)
# main_frame=cleaning_df("pdfs/statement_unlocked_feb.pdf")
# main_frame.to_csv("out.csv", sep=',', index=False, encoding='utf-8')
# x=pandas_ai(main_frame, prompt='top five debit amount and when it happend?')
# print(x,"This is the end")
st.title("Talk to your CSV")
pdf_file = st.file_uploader("Upload a pdf \n Note: This code is optimzed for SBI bank statements only", type=["pdf", "csv"])
if pdf_file is not None:
    # Display the video
    st.success("File uploaded successfully!")
    main_frame=cleaning_df(pdf_file)
    prompt = st.text_input('Ask your Query')
    st.write(pandas_ai(main_frame, prompt))
else:
    st.warning("Please upload your File")
