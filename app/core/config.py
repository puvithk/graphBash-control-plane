from dotenv import load_dotenv
import os
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", " ")
ALGORITHM = os.getenv("ALGORITHM" ,"HS256" )


ACCESS_TOKEN_EXPIRE_TIME = int(os.getenv("ACCESS_TOKEN_EXPIRE_TIME" , 30))

DATABASE_URL = os.getenv("DATABASE_URL" ,"localhost:3306/nodebash" )

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MAX_LLM_TRIES = int(os.getenv("MAX_LLM_TRIES" , 3))