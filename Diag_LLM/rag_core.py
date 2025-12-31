from dotenv import load_dotenv
import os
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
#from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun



# Load embeddings + FAISS
embeddings = OpenAIEmbeddings()

db = FAISS.load_local(
    "faiss_diagnostics",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 4})

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

search = DuckDuckGoSearchRun()


def research_agent(question: str) -> str:
    """Diagnostics research agent using FAISS + Web + LLM"""

    # 1️⃣ Retrieve from FAISS
    docs = retriever.invoke(question)

    pdf_context = "\n".join(d.page_content for d in docs)

    # 2️⃣ Web search
    web_context = search.run(question)

    if not web_context or len(web_context.strip()) == 0:
        raise RuntimeError(
            "Web search is mandatory but returned no results."
        )

    # 3️⃣ LLM synthesis
    prompt = f"""
You are an automotive diagnostics research agent.

ISO 14229 Context:
{pdf_context}

Web Context:
{web_context}

Question:
{question}

Answer clearly and accurately.
"""

    return llm.invoke(prompt).content
