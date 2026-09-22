import streamlit as st
from openai import OpenAI

st.title("🔥 Chill Bro AI")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

message = st.text_input("Talk to me, bro 😎")

if st.button("Send"):
    if message:
        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions="You are Chill Bro AI. Talk casually like a friendly bro. Match the user's tone while staying respectful and safe.",
            input=message
        )

        st.write(response.output_text)
