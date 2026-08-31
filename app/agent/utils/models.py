from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv
load_dotenv()
class GroqLLM():


    def __init__(self , model = "llama-3.1-8b-instant"):
        self.llm = ChatGroq(
            model = model,
            verbose = True,
            max_tokens = 1000,
            temperature = 0.7,
            top_p = 0.9,
            stream = True,
            api_key=os.getenv("GROQ_API_KEY"),
        )



