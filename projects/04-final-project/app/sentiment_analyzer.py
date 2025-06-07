import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    # In a real application, you might raise an error or handle this differently
    print("Warning: GOOGLE_API_KEY environment variable not found. Using placeholder.")
    # raise ValueError("No GOOGLE_API_KEY found in environment variables")

def analyze_sentiment(text: str) -> str:
    """Analyzes the sentiment of the given text using Google Gemini via LangChain.

    Args:
        text: The text to analyze.

    Returns:
        A string indicating the sentiment ("Positivo", "Negativo", or "Neutro").
        Returns "Indeterminado" if analysis fails or API key is missing.
    """
    if not GOOGLE_API_KEY:
        print("API Key missing, returning placeholder sentiment.")
        # Fallback placeholder logic if needed (similar to the bot's placeholder)
        if "bom" in text.lower() or "feliz" in text.lower():
            return "Positivo (Placeholder)"
        elif "ruim" in text.lower() or "triste" in text.lower():
            return "Negativo (Placeholder)"
        else:
            return "Neutro (Placeholder)"

    try:
        # Initialize the ChatGoogleGenerativeAI model
        # Make sure you have GOOGLE_API_KEY set in your environment
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0.1)

        # Define the prompt structure
        messages = [
            SystemMessage(
                content="Você é um assistente especializado em análise de sentimento. "
                        "Analise o texto fornecido pelo usuário e classifique o sentimento como 'Positivo', 'Negativo' ou 'Neutro'. "
                        "Responda APENAS com uma dessas três palavras."
            ),
            HumanMessage(content=text),
        ]

        # Invoke the model
        response = llm.invoke(messages)

        # Extract the sentiment from the response content
        if isinstance(response.content, list) and response.content:
            sentiment_text = response.content[0] if isinstance(response.content[0], str) else str(response.content[0])
        else:
            sentiment_text = str(response.content)
        sentiment = sentiment_text.strip().capitalize()

        # Validate the output
        if sentiment in ["Positivo", "Negativo", "Neutro"]:
            return sentiment
        else:
            print(f"Warning: Unexpected sentiment analysis result: {sentiment}")
            # Fallback or attempt to re-process if needed, here just return indeterminate
            return "Indeterminado"

    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Erro na Análise"

# Example usage (for testing)
if __name__ == "__main__":
    test_text_positive = "Hoje foi um dia maravilhoso, me senti muito feliz e produtivo."
    test_text_negative = "Estou me sentindo muito para baixo e sem energia hoje."
    test_text_neutral = "O dia foi normal, sem grandes acontecimentos."

    print(f"Texto: {test_text_positive}")
    print(f"Sentimento: {analyze_sentiment(test_text_positive)}\n")

    print(f"Texto: {test_text_negative}")
    print(f"Sentimento: {analyze_sentiment(test_text_negative)}\n")

    print(f"Texto: {test_text_neutral}")
    print(f"Sentimento: {analyze_sentiment(test_text_neutral)}\n")

    # Test without API Key (if GOOGLE_API_KEY is not set)
    # if not GOOGLE_API_KEY:
    #     print("Testing placeholder functionality:")
    #     print(f"Texto: {test_text_positive}")
    #     print(f"Sentimento: {analyze_sentiment(test_text_positive)}\n")

