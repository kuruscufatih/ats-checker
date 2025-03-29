from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter, HTMLHeaderTextSplitter
from groq import Groq
from dotenv import load_dotenv
import typer
import os
import asyncio

app = typer.Typer(help="Check if your CV fits into the job posting")
load_dotenv()

def split_text_into_chunks(text: str):
    splitter = CharacterTextSplitter(
        separator="\n\n",       
        chunk_size=1000,         
        chunk_overlap=200,      
        length_function=len
    )
    return splitter.split_text(text)

async def read_cv():
    """Reads CV with langchain reader.

    Returns:
        _type_: _description_
    """
    loader = PyPDFLoader("./data/CV.pdf")
    text_content = []

    async for page in loader.alazy_load():
        text_content.append(page.page_content)

    return "\n\n".join(text_content)

def read_job_post(url:str):
    """asdasd
    """
    loader = WebBaseLoader(url)
    documents = loader.load()


def ats_check():
    client = Groq(
        # This is the default and can be omitted
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)


@app.command()
def main():
    full_text = asyncio.run(read_cv())
    chunks = split_text_into_chunks(full_text)
    
    job = read_job_post("https://www.akkodis.com/de-de/karriere/jobs/data-analytics-engineer-wmd-hybrides-arbeiten-remote-prsenz-sindelfingen/729436001900?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic")
    ats_check()

if __name__ == "__main__":
    app()


# TODO: Erweiterung basierend auf Sprache in Metadaten von HTML. Wenn es DE ist soll er das deutsche einlesen