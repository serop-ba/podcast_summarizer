import streamlit as st
import requests

def send_file_to_backend(file):
    url = "http://fastapi:8000/upload/"
    response = requests.post(url, files={"file": file})
    return response.json()

def get_summary(data):
    url = "http://fastapi:8000/get_summary/"
    response = requests.post(url, json = data)
    return response.json()

# def get_linkedin_post(data):
#     url = "http://fastapi:8000/get_linkedin_post/"
#     response = requests.post(url, json = data)
#     return response.json()

st.title("Podcast Summarizer")

uploaded_file = st.file_uploader("Choose the podcast .docx file", type="docx")

if uploaded_file is not None:
        with st.spinner("Analyzing..."):
            # Send the file to FastAPI backend
            result = send_file_to_backend(uploaded_file)
        # Send the file to FastAPI backend
        st.write(f"File Successfully uploaded: Total of {len(result.get('text'))} characters")

        # Add buttons for creating summary
        if st.button("Create LinkedIn Post"):
            with st.spinner("Analyzing & Summarizing..."):
                summary_result = get_summary(result)
            st.write("******** Linkedin Post *******")
            st.write(f"{summary_result.get('text')}")
            # if st.button("Create LinkedIn Post"):
            #     with st.spinner("Creating LinkedIn post..."):
            #         linkedin_post = get_linkedin_post(summary_result)
            #     st.write("******** LinkedIn Post *******")
            #     st.write(f"{linkedin_post.get('text')}")

            # st.text_area("Document Summary", summary_result.get("text", ""), height=300)


# # User input
# user_input = st.text_input("Ask Questions about the podcast")

# if st.button("Generate LinkedIn Post"):
#     if user_input:
#         # Make a request to the FastAPI server
#         response = requests.post(
#             "http://fastapi:8000/chat",
#             json={"message": user_input}
#         )
        
#         if response.status_code == 200:
#             data = response.json()

#             # st.text(data["response"])
#             # Display the generated text in a text area
#             st.text_area("Generated Text", data["response"], height=300)

# # Button to copy the text to clipboard
            
#         else:
#             st.error("Failed to fetch job listings.")
#     else:
#         st.error("Please enter a search query.")

