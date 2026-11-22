import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


llm = ChatGroq(
    model_name=MODEL_NAME,
    max_tokens=4096,
    temperature=0.3,
    reasoning_effort="low",
)