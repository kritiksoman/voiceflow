import chromadb
from google import genai as embed_client
import subprocess
import os


embed_client = embed_client.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Reconnect to the stored database
client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), 'local_chroma_db'))
collection = client.get_collection(name="text_vectors")

# Perform a search query
# Generate embeddings for all texts

def window_tool(window_name, top_k=1):
    """Search for a window name in the database and return the results."""
    result = embed_client.models.embed_content(
            model="gemini-embedding-exp-03-07",
            contents=window_name)
    embeddings = [result.embeddings[0].values]
    results = collection.query(query_embeddings=embeddings, n_results=top_k)
    print("Search Results:", results)
    print( )
    return results


if __name__ == "__main__":
    print("Welcome to the window search tool!")

