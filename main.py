from langchain.document_loaders import Docx2txtLoader
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

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


loader = Docx2txtLoader('./data/raw/podcast_transcript.docx')
data = loader.load()

file_content = data[0].page_content

def chunk_string(input_string: str, chunk_length: int, overlap: int):
    chunks = []
    start = 0
    while start < len(input_string):
        end = start + chunk_length
        chunks.append(input_string[start:end])
        start = end - overlap  # Overlap the chunks
    return chunks

chunks = chunk_string(file_content, 5000, 50)
print("Audio is splitted into: ", len(chunks))
llm = Ollama(
    model='llama3'
    # other params...
)
print("***** podcast summary ******\n")

extractor = extraction_prompt | llm

key_points = extractor.batch(
    [{"text": data} for data in chunks[:5]],
    {"max_concurrency": 1},  # limit the concurrency by passing max concurrency!
)

for point in key_points:
    print(point + "\n ***** next point ***** ")

# Define prompt
prompt_template = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""
summary_prompt = PromptTemplate.from_template(prompt_template)

joined_string = "\n".join(key_points)
extractor = summary_prompt | llm
summary = extractor.batch(
    [{"text": joined_string}],
    {"max_concurrency": 1},  # limit the concurrency by passing max concurrency!
)[0]

print("*****summary******: \n", summary)

linkedin_template =ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Using the following podcast summary, create an engaging linkedin post announcing the publish of a new podcast episode of Data Tales. Give the episode a title from the mentioned summary and add the main key points to the post as bullet points, summary the keypoints to the most important ones. \n" 
"don't mention the names of the people who stated the information\n Give bullet points in the middle of the post after saying key takeaways: "
        ),
        ("ai", "{text}"),
    ]
)
print("\n\n******linkedIn Post*********\n")
extractor = linkedin_template | llm
linkedin_post = extractor.batch(
    [{"text": summary}],
    {"max_concurrency": 1},  # limit the concurrency by passing max concurrency!
)[0]
print(linkedin_post)
