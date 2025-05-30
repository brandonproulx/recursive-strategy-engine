# recursive-strategy-engine
A lightweight agentic framework that uses GPT-4o, recursive micro-agents, and retrieval-augmented context to simulate and evaluate multiple decision paths in parallel.  Built to model strategic thinking, project long-term outcomes, and recommend the most thoughtful path forward—modular by design, and easy to expand.



> ⚠️ This is not a production tool—this is a flexible skeleton built for experimentation and extension.

---

## 🔍 What It Does

- Accepts a strategic question from the user  
- Retrieves relevant personalized context from a local vector store (ChromaDB)
- Uses a parent GPT-4o agent to generate 7–10 viable decision paths
- Spawns parallel GPT-4o micro-agents to simulate long-term outcomes for each path
- Synthesizes the simulations to recommend the most compelling strategy

---

## 🧠 Why It’s Modular

Each script is intentionally separate:
- So you can modify individual components easily
- So the system can scale or adapt to new goals or domains
- So it stays beginner-friendly while still being powerful

---

## 🧰 Tech Stack

- [x] Python 3.11+
- [x] OpenAI GPT-4o (via API)
- [x] LangChain + LangChain Community + LangChain OpenAI
- [x] ChromaDB (vector store)
- [x] `dotenv` for local config
- [x] `ThreadPoolExecutor` for parallel agent execution

---

## 🛠️ Setup & Usage

1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/recursive-strategy-engine.git
   cd recursive-strategy-engine

   .
├── build_vector_store.py         # Load personal data into vector store
├── parent_agent.py               # Generates high-level decision paths
├── recursive_micro_agent.py      # Simulates each path in parallel
├── run_strategic_engine.py       # Orchestrates everything
├── requirements.txt
├── .env.example                  # For safe environment config
├── LICENSE
└── README.md


