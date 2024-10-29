from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
from docx import Document
from helper import pull_model
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel

global_text = None

app = FastAPI()

pull_model('llama3', service_name='ollama')

class StringRequest(BaseModel):
    text: str

def read_docx(file: BytesIO) -> str:
    doc = Document(file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

def chunk_string(input_string: str, chunk_length: int, overlap: int):
    chunks = []
    start = 0
    while start < len(input_string):
        end = start + chunk_length
        chunks.append(input_string[start:end])
        start = end - overlap  # Overlap the chunks
    return chunks

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    global_text = read_docx(BytesIO(file_content))
    return JSONResponse(content={"text": global_text})

@app.post("/get_summary/")
async def create_summary(data:StringRequest):
    chunks = chunk_string(data.text, 5000, 50)


    extraction_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert at identifying important keynotes in a podcast conversation. "
                "Only extract important and relevant key notes that might be interesting for business people and aspiring data scientists. Extract nothing if no important information can be found in the text.",
            ),
            ("human", "{text}"),
        ]
    )

    llm = Ollama(
        model='llama3',
        base_url="http://ollama:11434/",
        # other params...
    )
    print("***** podcast summary ******\n")

    extractor = extraction_prompt | llm

    key_points = extractor.batch(
        [{"text": data} for data in chunks],
        {"max_concurrency": 1},  # limit the concurrency by passing max concurrency!
    )
    for point in key_points:
        print(point)



    # Summarize 
    prompt_template = """Write a concise summary of the following, focus on important key notes that are interesting for business people and data scientists trying to implement ai applications in their work:
    "{text}"
    CONCISE SUMMARY:"""
    summary_prompt = PromptTemplate.from_template(prompt_template)

    joined_string = "\n".join(key_points)
    chunks = chunk_string(joined_string, 5000, 50)

    extractor = summary_prompt | llm
    summary = extractor.batch(
        [{"text": data} for data in chunks],
        {"max_concurrency": 1},  # limit the concurrency by passing max concurrency!
    )

 
    linkedin_template =ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Using the following podcast summary, create an engaging linkedin post announcing the publish of a new podcast episode of Data Tales. Give the episode a title from the mentioned summary and add the most important key takeaway points to the post as bullet points. The takeaway should be interesting for business people and data scientists, trying to use AI in their daily work\n" 
    "don't mention the names of the people who stated the information\n "
            ),
            ("ai", "{text}"),
        ]
    )

    print("\n\n******linkedIn Post*********\n")
    final_summary = "\n".join(summary)

    extractor = linkedin_template | llm
    linkedin_post = extractor.batch(
        [{"text": final_summary}],
        {"max_concurrency": 1},  # limit the concurrency by passing max concurrency!
    )[0]
    return JSONResponse(content={"text": linkedin_post})







# # Define the LangChain LLM
# llm = Ollama(
#     base_url="http://ollama:11434/",
#     model='llama3'
#     # other params...
# )
# prompt = hub.pull("rlm/rag-prompt")

# qdrant = QdrantVectorStore.from_existing_collection(collection_name="podcast2", embedding=OllamaEmbeddings( base_url="http://ollama:11434/", model='llama3'), path="./local_qdrant_podcast" )
# retriever = qdrant.as_retriever()

# class ChatRequest(BaseModel):
#     message: str

# class ChatResponse(BaseModel):
#     response: str

# @app.get("/hello")
# def hello_world():
#     return {"message": "Hello, world!"}

# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     def format_docs(docs):
#         return "\n\n".join(doc.page_content for doc in docs)
#     user_message = request.message
#     logging.info(user_message)

#     rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
#     )
#     # Process user message with LangChain and ChatGPT
#     chatgpt_response = rag_chain.invoke({"query": user_message})

#     linkedin_prompt = f"From the following keypoints: {chatgpt_response}, create a linkedIn post about a new podcast episode of Data Tales, add a place for the link, make it short and engaging "
#     linkedin_chain = (
#         linkedin_prompt|
#         llm |
#         StrOutputParser()
#     )
#     linkedin_post = linkedin_chain.invoke()
#     return ChatResponse(response=linkedin_post)

def format_jobs(jobs):
    formatted = "Here are some job listings:\n"
    for job in jobs:
        formatted += f"{job['title']} at {job['company']}\n"
    return formatted

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
