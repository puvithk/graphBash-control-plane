from sqlalchemy.dialects.postgresql import Any
from random import randrange
from app.core import config
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
            api_key=config.GROQ_API_KEY,
        )

    def model_provider(self ):
        return "groq"



class ChatLLM():
    def __init__(self , llm_provider = "groq" , llm_model = "llama-3.1-8b-instant"):
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        if self.llm_provider == "groq":
            self.chat_model = GroqLLM(llm_model)
        else:
            raise ValueError("LLM Provider is not supported")
    

    def invoke(self , prompt : str ):
        # Try max for 3 turns 
        for _ in range(config.MAX_LLM_TRIES):
            try:
                response = self.chat_model.invoke(prompt)
                return response
            except Exception as e:
                raise ValueError("LLM Error " + str(e))

    def invoke_with_structured_output(self , prompt : str , output_structure ):
        llm = self.chat_model.with_structured_output(output_structure)
        # Try max for 3 turns 
        for _ in range(config.MAX_LLM_TRIES):
            try:
                response = llm.invoke(prompt)
                return response.json_dump()
            except Exception as e:
                raise ValueError("LLM Error " + str(e))