import requests
from bs4 import BeautifulSoup
from dagster import op, Output, MetadataValue

from src.resources import LlamaResource


@op
def get_page_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    return soup.get_text()


@op
def get_paragraph_text(url, word_limit=100):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <p> tags
    p_tags = soup.find_all("p")

    # Get text from each <p> tag and split into words
    words = []
    for p in p_tags:
        words += p.get_text().split()

    # Limit to 100 words
    words = words[:word_limit]

    # Join back into a string
    text = "\n".join(words)

    return text


@op
def summarise_text(text, llama: LlamaResource):
    summary = llama.summarise(text=text)

    return summary
