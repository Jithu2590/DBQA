import openai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv(override=True)
api_key = st.secrets.OPEN_API_KEY

openai.api_key = api_key

def get_completion(prompt, text,model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        with st.chat_message("user"):
           st.markdown(text)
        
       
        with st.chat_message("assistant"):
          message_placeholder = st.empty()
        with st.spinner("Generating....."):

                response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.6
                )
        response_message = response.choices[0].message.content
        return response_message
        
              

    
st.title("Code Documentation")
input_text = st.chat_input("Enter the code")


if input_text:
        prompt = f"""Your task is to generate overall techincal documentation and overall software documentation of the code and aslo check whether given code if it is not programming language then display it is a not code
        Review:```{input_text}```
        """
        response = get_completion(prompt,input_text)
        st.markdown(response)

        




