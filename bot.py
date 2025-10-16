import pandasai as pai
from pandasai_litellm.litellm import LiteLLM
import os
from dotenv import load_dotenv
from IPython.display import Image, display 
from pandasai import SmartDataframe
import pandas as pd
import base64
import io

load_dotenv()

def initialize():
    api_key = os.getenv("OPENAI_API_KEY")
    llm = LiteLLM(model="gpt-4o-mini", api_key=api_key)

    pai.config.set({
        "llm": llm,
    })
def chat_with_data(df, prompt):
    """
    Chat with data using PandasAI
    
    Args:
        file_path: Path to the CSV file
        prompt: User's question/prompt
    
    Returns:
        Response from PandasAI (could be text or image path)
    """
    initialize()
    df = SmartDataframe(df)
    response = df.chat(prompt)
    return response