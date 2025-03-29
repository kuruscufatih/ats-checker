import typer

app = typer.Typer(help="Check if your CV fits into the job posting")

@app.command()
def main():
    print("Hello from pp!")


if __name__ == "__main__":
    app()
