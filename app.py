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
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
llm = OpenAI(api_token=OPENAI_API_KEY,temperature=0)
pandas_ai = PandasAI(llm=llm)
main_frame=cleaning_df("pdfs/statement_unlocked_feb.pdf")
main_frame.to_csv("out.csv", sep=',', index=False, encoding='utf-8')