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


class StringRequest(BaseModel):
    text: str

class SumRequest(BaseModel):
    data: str
    model: str



@app.post('/pull_model')
async def upload_file(model: StringRequest):
    try:

        pull_model(model.text, service_name='ollama')
        return {'message':'Model Downloaded successfully'}
    except Exception as e: 
        return {'message': f"failed due to {e.with_traceback()}"}



@app.post("/get_summary/")
async def create_summary(request: SumRequest):


    llm = Ollama(
        model=request.model,
        base_url="http://ollama:11434/",
        # other params...
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

    extractor = linkedin_template | llm
    linkedin_post = extractor.batch(
        [{"text": request.data}],
        {"max_concurrency": 1},  # limit the concurrency by passing max concurrency!
    )[0]
    return JSONResponse(content={"text": linkedin_post})


def format_jobs(jobs):
    formatted = "Here are some job listings:\n"
    for job in jobs:
        formatted += f"{job['title']} at {job['company']}\n"
    return formatted

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
