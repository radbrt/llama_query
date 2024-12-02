#%%
import streamlit as st
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index.indices.struct_store.sql_query import SQLDatabase
from langchain.chat_models import ChatOpenAI
from llama_index import LLMPredictor, ServiceContext
import openai

#%%
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import os
import dotenv

dotenv.load_dotenv(".env")
#%%

# llm_predictor = llmpredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-4"))

account = os.getenv("SNOWFLAKE_ACCOUNT")
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")


# tables_to_query = ["foretak_siste"]
#%%
conn_str = URL(
    account = account,
    user = user,
    warehouse = warehouse,
    database = "DBTHOUSE",
    password = password,
    schema = "DEVELOP"
)

e = create_engine(conn_str)
#%%

import sqlalchemy as sa


def get_single_table_info(inspector, table_name: str) -> str:
    """Get table info for a single table."""
    # same logic as table_info, but with specific table names
    template = (
        "Table '{table_name}' has columns: {columns}, "
        "and foreign keys: {foreign_keys}."
    )
    columns = []
    for column in inspector.get_columns(table_name):
        if column.get("comment"):
            columns.append(
                f"{column['name']} ({column['type']!s}): "
                f"'{column.get('comment')}'"
            )
        else:
            columns.append(f"{column['name']} ({column['type']!s})")

    column_str = ", ".join(columns)
    foreign_keys = []
    for foreign_key in inspector.get_foreign_keys(table_name):
        foreign_keys.append(
            f"{foreign_key['constrained_columns']} -> "
            f"{foreign_key['referred_table']}.{foreign_key['referred_columns']}"
        )
    foreign_key_str = ", ".join(foreign_keys)
    return template.format(
        table_name=table_name, columns=column_str, foreign_keys=foreign_key_str
    )

#%%

inspector = sa.inspect(e)
#%%
md = get_single_table_info(inspector, "wrk_foretak_010")
# %%

print(md)
# %%

"""
Table 'wrk_foretak_010' has columns: 
orgnr (VARCHAR(16777216)): 'Company ID', 
navn (VARCHAR(16777216)): 'Company name', 
antall_ansatte (DECIMAL(38, 0)): 'Number of employees', 
nace_1 (VARCHAR(16777216)): 'Industry code', 
and foreign keys: ['nace_1'] -> wrk_nace.['naerk'].
"""

#%%

