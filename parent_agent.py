from openai import OpenAI
from dotenv import load_dotenv
import os

# === Load API Key ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
def generate_paths(prompt: str, context: str) -> list[str]:
    """Generates 5–10 strategic decision paths based on a prompt and context."""
messages = [
        {
            "role": "system",
            "content": (
                "You are a strategic thinking assistant. The user will give you a personal or professional question.\n"
                "Your job is to generate a list of 7–10 realistic and mutually exclusive DECISION PATHS they could pursue.\n"
                "Each decision should represent a full, specific course of action (e.g., 'stay in current job and pursue promotion', "
                "'go full-time into consulting', 'start consulting part-time', etc.).\n"
                "\n"
                "Do NOT give reflective questions, journaling advice, or suggestions for how to decide.\n"
                "Just list concrete paths the person could follow - as if you're Doctor Strange running 10 alternate timelines.\n"
                "\n"
                "Output ONLY the list. No explanations, no markdown, no extra formatting."
            )
        },
        {
            "role": "user",
            "content": f"""
USER QUESTION:
{prompt}
USER CONTEXT:
{context}
"""
        }
    ]
response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )
raw_output = response.choices[0].message.content.strip()
# Parse bullet points into list
    paths = []
    for line in raw_output.splitlines():
        if "-" in line:
            _, option = line.split("-", 1)
            paths.append(option.strip())
        elif line.strip():
            paths.append(line.strip())
return paths
