from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

import typer
import asyncio

app = typer.Typer(help="Check if your CV fits into the job posting")

def split_text_into_chunks(text: str):
    splitter = CharacterTextSplitter(
        separator="\n\n",       
        chunk_size=1000,         
        chunk_overlap=200,      
        length_function=len
    )
    return splitter.split_text(text)

async def read_cv_text():
    """Reads CV with langchain reader.

    Returns:
        _type_: _description_
    """
    loader = PyPDFLoader("./data/CV.pdf")
    text_content = []

    async for page in loader.alazy_load():
        text_content.append(page.page_content)

    return "\n\n".join(text_content)


@app.command()
def main():
    full_text = asyncio.run(read_cv_text())
    chunks = _split_text_into_chunks(full_text)

    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")
        print(chunk)
        print()

if __name__ == "__main__":
    app()
