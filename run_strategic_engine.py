import os
import re
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from concurrent.futures import ThreadPoolExecutor, as_completed

from parent_agent import generate_paths
from recursive_micro_agent import simulate_path

# === Load API Key ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file.")
    exit()
client = OpenAI(api_key=api_key)

# === Ask for the strategic question ===
print("\n📌 What is your strategic decision-making question?")
prompt = input("> ").strip()
if not prompt:
    print("❌ No question provided.")
    exit()

# === Generate a session folder name ===
def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text[:40].strip("_")

slug = slugify(prompt)
timestamp = datetime.now().strftime("%Y-%m-%d")
session_folder = os.path.join("simulations", f"{timestamp}_{slug}")
os.makedirs(session_folder, exist_ok=True)

with open(os.path.join(session_folder, "prompt.txt"), "w", encoding="utf-8") as f:
    f.write(prompt)

# === Load context from vector store ===
embedding_function = OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name="text-embedding-3-large"
)
db = PersistentClient(path="./rag_db")
collection = db.get_or_create_collection("langchain", embedding_function=embedding_function)
results = collection.query(query_texts=[prompt], n_results=5)
context = "\n".join(results["documents"][0])

# === Generate decision paths ===
print("\n🤖 Generating decision paths...")
paths = generate_paths(prompt, context)

with open(os.path.join(session_folder, "paths.txt"), "w", encoding="utf-8") as f:
    for i, path in enumerate(paths, 1):
        f.write(f"{i}. {path}\n")

# === Simulate each decision path in parallel ===
print("\n🔁 Simulating each path in parallel...\n")

def simulate_with_index(index, path):
    print(f"🔄 Simulating Path {index}: {path}")
    simulation = simulate_path(path, context)
    return f"Path {index}: {path}\n\n{simulation}\n" + "="*80 + "\n"

timelines = []
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(simulate_with_index, i+1, path) for i, path in enumerate(paths)]
    for future in as_completed(futures):
        timelines.append(future.result())

with open(os.path.join(session_folder, "timelines.txt"), "w", encoding="utf-8") as f:
    f.writelines(timelines)

# === Ask GPT to synthesize all timelines ===
print("\n🧠 Analyzing all simulated paths to determine best outcome...")
messages = [
    {
        "role": "system",
        "content": (
            "You are a decision strategist. The user explored multiple decision paths through simulation. "
            "Compare and contrast each, and recommend the best one based on long-term value and alignment with goals."
        )
    },
    {
        "role": "user",
        "content": f"""QUESTION:
{prompt}

CONTEXT:
{context}

SIMULATED PATHS:
{''.join(timelines)}

What is your final recommendation and why?"""
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.7
)

final_answer = response.choices[0].message.content.strip()

print("\n📊 Final Strategic Recommendation:\n")
print(final_answer)

with open(os.path.join(session_folder, "final_recommendation.txt"), "w", encoding="utf-8") as f:
    f.write(final_answer)

print(f"\n✅ All outputs saved to: {session_folder}\n")
