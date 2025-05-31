import chromadb
import google.generativeai as genai
from google import genai as embed_client
import subprocess
import os
import time

import os
os.environ["GEMINI_API_KEY"] = "" #TODO: enter your API key here

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
embed_client = embed_client.Client(api_key=os.getenv("GEMINI_API_KEY"))


# Initialize ChromaDB with persistent storage
client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), 'local_chroma_db'))


# Run the mdfind command
result = subprocess.run(["mdfind", "kMDItemKind == 'Application'"], capture_output=True, text=True)

stime = time.time()

# Split output into a list
applications = result.stdout.strip().split("\n")
model = genai.GenerativeModel("gemini-2.0-flash")
responses = []
unique_apps = []
for i, application in enumerate(applications):
      app = application.split("/")[-1]
      if app not in unique_apps:
        unique_apps.append(app)
        des = model.generate_content("Create a textual description of the application in few words. It should follow the format: Application name: purpose of the application. \n" + app) 
        responses.append(des)
        print(f"Processed {i+1}/{len(applications)}: {application.split('/')[-1]}")

# Create a collection
collection = client.get_or_create_collection(name="text_vectors")

states = []
for application, response in zip(applications, responses):
    # Create a state for each application
    state = {
            "tool": "os", 
            # "action": "open", 
            "window_name": application, 
            "description": response.text,
            "start_state": "any",
            "end_state": application,
            }
    states.append(state)
        

# Generate embeddings for all texts
result = []
skip_id = []
for i, text in enumerate(states):
        try:
                result.append(embed_client.models.embed_content(
                        model="gemini-embedding-exp-03-07",
                        contents=text['description']))
                print(f"Embedded {i+1}/{len(states)}: {text['description']}")
        except:
                wait_time = 10
                time.sleep(wait_time)
                skip_id.append(i)
# embed_model = genai.GenerativeModel("gemini-embedding-exp-03-07")
# responses = [embed_model.embed_content(text['description']) for text in states]
# Extract embeddings from responses
embeddings = [resp.embeddings[0].values for resp in result]

# Index data
ids=[x['description'] for i, x in enumerate(states) if i not in skip_id]
metadatas = [x for i, x in enumerate(states) if i not in skip_id]
collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

# The database is automatically saved to disk at `./local_chroma_db`
print("Vector database saved locally at 'local_chroma_db'.")
print("Time taken to create the database:", time.time() - stime)


