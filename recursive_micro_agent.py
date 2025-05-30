from openai import OpenAI
from dotenv import load_dotenv
import os

# === Load API Key ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
def simulate_path(path: str, context: str) -> str:
    """Simulates a single decision path step-by-step with user's context."""
messages = [
        {
            "role": "system",
            "content": (
                "You are a recursive simulation agent. Your job is to simulate a decision path step-by-step "
                "based on the user's personal context. Think long-term, reason deeply, and reflect on the outcome."
            )
        },
        {
            "role": "user",
            "content": f"USER CONTEXT:\n{context}"
        }
    ]
steps = [
        f"Step 1: What does this decision involve?\n{path}",
        "Step 2: What are the short- and long-term consequences of this choice?",
        "Step 3: What are the major risks and benefits of this choice?",
        "Step 4: How well does this choice align with the user's values and goals?",
        "Step 5: Play out the timeline of this choice over 1, 3, and 5 years.",
        "Step 6: Now that this path has played out, reflect-was this ultimately a good decision?"
    ]
transcript = [f"🧠 Decision Path: {path}\n"]
    for i, step in enumerate(steps, 1):
        messages.append({"role": "user", "content": step})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": content})
        transcript.append(f"🔄 Step {i}:\n{content}\n")
return "\n".join(transcript)
