import streamlit as st

# Set up the title of the app
st.markdown('<h2 style="font-size: 30px;">DB-LLM-QUERY</h2>', unsafe_allow_html=True)

# Create an input box for user input
user_input = st.text_input("Enter some text:")

# Create a submit button
if st.button('Submit'):
    # When the button is clicked, display the entered text
    st.write('You entered:', user_input)



def get_similar_docs(query_text):
    query_vector = encode(query_text)

    client = MilvusClient(
    uri="http://standalone:19530",
    db_name=DB_NAME
    )

    results = client.search(
        collection_name=COLLECTION_NAME, # Replace with the actual name of your collection
        # Replace with your query vector
        data=[query_vector],
        limit=400, # Max. number of search results to return
        output_fields=["text"]
        # search_params={"params": {"text"}} # Search parameters
    )

    result = results[0]

    similar_results = []

    for res in result:
        similar_results.append(res["entity"]["text"])
    return similar_results