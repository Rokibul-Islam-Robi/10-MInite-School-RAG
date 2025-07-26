import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the generative model. Using 'gemini-1.5-flash-latest' as per your existing code.
generation_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def generate_answer(query, retrieved_chunks):
    """
    Generates an answer based on a query and retrieved context chunks
    using the Gemini generative model, with a focus on exactness.
    """
    context = '\n'.join([chunk[1] for chunk in retrieved_chunks])
    
    # CRITICAL CHANGE: Enhance the prompt for exactness and conciseness
    # Add clear instructions for the model's behavior.
    prompt = f"""
    You are a helpful and precise assistant. Your goal is to provide exact answers
    based *only* on the given context.

    If the answer to the question cannot be found within the provided context,
    you MUST respond with "I cannot find the answer to your question in the provided context."
    Do NOT make up information.
    Provide the answer in a direct and concise manner, avoiding conversational filler.

    Context:
    {context}

    Question: {query}

    Exact Answer:
    """

    try:
        # CRITICAL CHANGE: Set temperature to 0.0 for deterministic, less creative answers.
        # This will make the model more factual and less prone to hallucination or conversational tones.
        response = generation_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.0)
        )
        return response.text
    except Exception as e:
        print(f"ERROR: Gemini Generation API call failed. Error: {e}")
        return f"[Error] Gemini Generation API: {e}"