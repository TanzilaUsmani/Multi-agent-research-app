from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url
import os
from dotenv import load_dotenv
load_dotenv()

#model setup
llm=ChatMistralAI(model="mistral-small-2603",temperature=0)

   #1st agent
def build_search_agent():
    return create_agent(
      model=llm,
      tools=[web_search]
      )
 #2nd Agent
def build_reader_agent():
    return create_agent(
       model=llm,
       tools=[scrape_url]
    )

#write chain

writer_prompt=ChatPromptTemplate.from_messages([
    (
            "system",
            """You are an expert AI Research Assistant.

Your responsibilities:
- Understand the user's query.
- Gather accurate and up-to-date information.
- Search the web whenever required.
- Summarize the findings clearly.
- Mention sources or URLs whenever available.
- Never make up information.
- If information is unavailable, politely say so.
"""
        ),

        (
            "human",
            """Research the following topic thoroughly.

Topic:
{topic}

Provide:
- Introduction
- Key Findings
- Important Facts
- Latest Updates
- Sources

Make the response clear, well-structured, and professional.
"""
        ),
   
])

writer_chain=writer_prompt|llm|StrOutputParser()

#critic chain

critic_prompt=ChatPromptTemplate.from_messages([
   (
            "system",
            """You are an expert editor and research reviewer.

Your responsibilities:
- Critically review the report.
- Verify clarity, accuracy, and completeness.
- Identify missing or weak information.
- Point out factual inconsistencies.
- Suggest specific improvements.
- Ensure the report is well-structured and professional.
- Do not rewrite the report unless asked.
- Provide constructive feedback only.
"""
        ),

        (
            "human",
            """Review the following report.

Topic:
{topic}

Report:
{report}

Evaluate the report based on:

- Accuracy
- Completeness
- Clarity
- Structure
- Grammar
- Missing Information
- Suggestions for Improvement

Provide your review in the following format:

Overall Rating: /10

Strengths:
- ...

Weaknesses:
- ...

Missing Information:
- ...

Suggestions:
- ...

Final Verdict:
Should the report be published? (Yes/No)
"""
        ),
   
])

critic_chain=critic_prompt|llm|StrOutputParser()