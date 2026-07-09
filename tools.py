from dotenv import load_dotenv
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
load_dotenv()

#News fecthing tool
tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)->str:
    """
    Search the web of recent and relaible information on a topic.Return Titles,URLs snippets
    """
    result= tavily.search(query=query,max_results=5)
    
    out=[]
    for r in result["results"]:
     out.append(
        f"Title: {r['title']}\n"
        f"URL: {r['url']}\n"
        f"Content: {r['content']}\n"
     )

    return "\n\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """
    Scrape the title and text content from a webpage URL.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        title = soup.title.text.strip() if soup.title else "No Title"

        content = "\n".join(
            p.get_text(strip=True)
            for p in soup.find_all("p")
        )

        return (
            f"Title: {title}\n\n"
            f"URL: {url}\n\n"
            f"Content:\n{content}"
        )

    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"

    except Exception as e:
        return f"An unexpected error occurred: {e}"
    
