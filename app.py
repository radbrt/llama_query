import streamlit as st
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index.indices.struct_store.sql_query import SQLDatabase
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from llama_index import LLMPredictor, ServiceContext
import openai
import os
import dotenv

dotenv.load_dotenv(".env")

# Setup the page layout
st.set_page_config(page_title="Spør databasen", layout='wide')

def chat_query_engine():
    
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")

    tables_to_query = ["foretak_siste"]

    conn_str = URL(
        account = account,
        user = user,
        warehouse = warehouse,
        database = database,
        password = password,
        schema = schema
    )

    engine = create_engine(conn_str)

    sql_database = SQLDatabase(engine, include_tables=tables_to_query)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-4"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-4"))

    sql_query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=tables_to_query,
        service_context=service_context
    )

    return sql_query_engine


def main():
    # Add some white space to center the input
    query_engine = chat_query_engine()

    st.markdown("<br>", unsafe_allow_html=True)

    # Create columns for centering the text input
    _, col2, _ = st.columns([1,2,1])
    _, col5, _ = st.columns([1,2,1])
    with col2:
        text = st.text_input('Hva lurer du på?')

    # Output container
    container = col5.container()

    # Now process the text and display it in the container
    with container:
        if text:
            st.subheader("Svar:")
            try:
              response = query_engine.query(text)
            except Exception as e:
                response = "Oops! Noe gikk galt. Prøv igjen."
                

            processed_text = text_process_function(response.response)  # Your text processing function here

            st.write(f'{processed_text}')

            
            query = response.metadata['sql_query']
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                           messages=[
                                                               {"role": "system", "content": "You are a data analyst who give brief explanations of SQL queries"}, 
                                                               {"role": "user", "content": f"Hva gjør denne spørringen? {query}"}
                                                          ]
                                                          )
            with st.expander("Sjekk svaret"):
                st.subheader("Hva skjedde?")
                st.write(
                    f"""
                            {chat_completion["choices"][0]["message"]["content"]}
                    """)
                
                st.code(
                    f"""
                            {response.metadata["sql_query"]}
                    """)



def text_process_function(text):
    # TODO: Implement your text processing here
    # For the purpose of this example, we just return the same text
    return text

if __name__ == "__main__":
    main()