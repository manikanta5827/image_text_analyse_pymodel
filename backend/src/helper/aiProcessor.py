import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def process_with_gen_ai(prompt):
        try:
            print(f"AI Processing Started...")
            api_key = os.getenv("GEMINI_API_KEY")
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content( model="gemini-1.5-flash-8b", contents=prompt )
            return response.text
        
        except Exception as error:
            print("Error in aiProcessor file:", error)
            return ""
