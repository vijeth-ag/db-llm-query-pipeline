import streamlit as st
import requests

# Set up the title of the app
st.markdown('<h2 style="font-size: 30px;">DB-LLM-QUERY</h2>', unsafe_allow_html=True)

# Create an input box for user input
user_question = st.text_input("Enter query:")

# Create a submit button
if st.button('Submit'):
    # When the button is clicked, display the entered text
    st.write('You entered:', user_question)
    response =  requests.get('http://query-server:8123/query?question='+user_question)
    print("response",response.text)

    st.write(response.text)




