# Simple query app

I'm pretty sure practically everyone and their cat has made something like this already, but basically:

This is a streamlit app that can be configured to answer natural language questions about a database table.

The slightly notable parts:
- It uses a slightly modified version of llama-index, which uses column comments as additional table information
- It includes an expandable "check the answer" section that again uses gpt to generate a human explanation of the final query, which it displays together with the original query.

The whole thing is in Norwegian. It works reasonably well, but errors out on complex queries (and some uncomplicated ones as well).