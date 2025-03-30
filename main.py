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
    return documents

def ats_check(cv, job):
    client = Groq(
        # This is the default and can be omitted
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Du bist ein Recruiter. Deine Aufgabe ist es zu bewerten, ob die Anforderungen aus der Stellenausschreibung mit dem
                Inhalt des Lebenslaufs übereinstimmt. Dafür wirst Du beide Inhalte - die Stellenausschreibung als auch den Lebenslauf erhalten.
                Schreibe ein kurzes Feedback mit relevanten Punkten, ohne zusätzlichen nicht notwendigen Text von Dir."""
            },
            {
                "role": "user",
                "content": f"Hier ist der Lebenslauf: {cv} und hier ist die Stellenausschreibung: {job}",
            },
            {
                "role": "system",
                "content": """Du bist ein Application Tracking System. Deine Aufgabe ist es zu bewerten, ob die Anforderungen aus der Stellenausschreibung mit dem
                Inhalt des Lebenslaufs übereinstimmt. Dafür wirst Du beide Inhalte - die Stellenausschreibung als auch den Lebenslauf erhalten.
                Zähle lediglich die Schlüsselwörter auf, die zu wenig oder gar nicht im Lebenslauf zu finden sind und gebe ein Sentiment 1-10 Punkte ab, 
                ob Du als Application Tracking System den Bewerber einladen würdest.."""
            },
            {
                "role": "user",
                "content": f"Hier ist der Lebenslauf: {cv} und hier ist die Stellenausschreibung: {job}",
            },

        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)


@app.command()
def main():
    full_text = asyncio.run(read_cv())
    chunks = split_text_into_chunks(full_text)
    
    job = read_job_post("https://www.akkodis.com/de-de/karriere/jobs/data-analytics-engineer-wmd-hybrides-arbeiten-remote-prsenz-sindelfingen/729436001900?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic")
    # chunks_job = split_text_into_chunks(job)
    ats_check(chunks, job)

if __name__ == "__main__":
    app()


# TODO: Erweiterung basierend auf Sprache in Metadaten von HTML. Wenn es DE ist soll er das deutsche einlesen
# TODO: Prompt-Strategien anschauen und entsprechend optimieren