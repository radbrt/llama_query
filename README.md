# Simple query app

I'm pretty sure practically everyone and their cat has made something like this already, but basically:

This is a streamlit app that can be configured to answer natural language questions about a database table.

The slightly notable parts:
- It uses a slightly modified version of llama-index, which uses column comments as additional table information
- It includes an expandable "check the answer" section that again uses gpt to generate a human explanation of the final SQL query, which it displays together with the query.

The whole thing is in Norwegian. It works reasonably well, but errors out on complex queries (and some uncomplicated ones as well) and rarely if ever makes conditions case-insensitive.


## Get it running

The one file that is missing in this repo is the `.env` file that contains all the secrets such as database credentials and openAI API key.

Create a file named `.env` and fill it like this:

```
SNOWFLAKE_ACCOUNT = '<ab12345.my-region.my-cloud>'
SNOWFLAKE_USER = '<my-username>'
SNOWFLAKE_PASSWORD = '<my-password>'
SNOWFLAKE_WAREHOUSE = '<my-warehouse>'
SNOWFLAKE_DATABASE = '<my-database>'
SNOWFLAKE_SCHEMA = '<my-schema-name>'
OPENAI_API_KEY = '<my-openai-api-key>'
```

Additionally, you need to alter the `app.py` file to use the table you want. Database and Schema is already configured above, but the table name(s) must be set in the script itself.

```py
tables_to_query = ["<my_table_name>"]
```

Once this is done, it should suffice to run

```sh
pip install -r requirements.txt
streamlit run app.py
```