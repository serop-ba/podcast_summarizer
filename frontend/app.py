import streamlit as st
import requests

def get_summary(data):
    url = "http://fastapi:8000/get_summary/"
   
    response = requests.post(url, json=data)
    return response.json()

def pull_model(model):
    url = "http://fastapi:8000/pull_model/"
    response = requests.post(url, json=model)
    return response.json()
st.title("LinkedIn Post Generator")


# Streamlit app title
model_choice = st.selectbox(
    "Choose an LLM model:",
    ["llama3.2", "llama3.2:1b", "llama3.1", "gemma2", "phi3.5", "mistral"]  # Adjust model names as per availability
)


if model_choice:  # This ensures the model is chosen
    with st.spinner("Loading model..."):
        # Pull the selected model
        model_response = pull_model({"text": model_choice})
        st.success(f"Model '{model_choice}' successfully loaded.")

# Text input area for free text
        user_input = st.text_area("Enter text to generate a LinkedIn post", height=300)

        # Button to generate LinkedIn post
        if st.button("Generate LinkedIn Post"):
            if user_input.strip():  # Ensure there's text to summarize
                with st.spinner("Generating..."):
                    summary_result = get_summary({"data": user_input, "model": model_choice},)
                
                # Display the summarized text
                st.write("****** LinkedIn Post ******")
                st.write(summary_result.get("text", "No summary available."))
            else:
                st.error("Please enter the podcast Summary Here.")
