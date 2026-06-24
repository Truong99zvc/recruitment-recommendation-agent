# 🤖 Jobber - Autonomous Recruitment Recommendation Agent

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Sentient Framework](https://img.shields.io/badge/Powered%20by-Sentient-orange.svg)](https://github.com/sentient-engineering/sentient)

Jobber is an intelligent AI agent that searches and applies for jobs on your behalf by autonomously controlling your web browser. Simply provide your resume and preferences, and let the agent do the heavy lifting in the background.

This project is built upon the upcoming open-source framework [Sentient](https://github.com/sentient-engineering/sentient), which enables developers to instantly build fast & reliable AI agents capable of autonomous browser control.

> **Note:** Check out the beta `sentient` package on [PyPI](https://pypi.org/project/sentient/) and explore our experiments advancing OSS web-navigating agents in the [agent-q repository](https://github.com/sentient-engineering/agent-q).

---

## 🎥 Demo

Check out this [Loom Video](https://www.loom.com/share/2037ee751b4f491c8d2ffd472d8223bd?sid=53d08a9f-5a9b-4388-ae69-445032b31738) for a quick demonstration of Jobber in action!

---

## 🏗️ Architecture

The repository features two distinct implementations of the Jobber agent:

- **`jobber/` (Standard)**: A straightforward approach to implementing multi-agent conversation between a planner and a browser agent. It supports various OSS models and cost-effective alternatives like `gpt-4o-mini`.
- **`jobber_fsm/` (Finite State Machine)**: An advanced approach based on [Multi-Agent FSM](https://github.com/sentient-engineering/multi-agent-fsm). While highly scalable and robust, it currently relies on OpenAI's [Structured Outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/), making it less compatible with generic OSS models compared to the standard version.

Both approaches yield similar performance, but future scalability improvements will be focused primarily on the FSM implementation.

---

## 📂 Project Structure

```text
recruitment-recommendation-agent/
│
├── jobber/                             # Standard Agent Implementation
│   ├── core/                           # Core business logic
│   │   ├── agents/                     # Base, Planner, and Browser Navigation agents
│   │   ├── memory/                     # Long-term memory (LTM) & context management
│   │   ├── skills/                     # Actionable skills (e.g., getting screenshots, extracting URLs)
│   │   ├── playwright_manager.py       # Browser & Playwright session controller
│   │   ├── prompts.py                  # LLM Prompt templates for the standard agent
│   │   └── system_orchestrator.py      # Main loop orchestrating planner and browser agents
│   ├── user_preferences/               # Target job preferences and resume settings
│   ├── utils/                          # Helper functions (logging setup, path parsing)
│   ├── __main__.py                     # CLI entry point for the standard agent
│   └── config.py                       # Base configuration and path variables
│
├── jobber_fsm/                         # Finite State Machine Agent Implementation
│   ├── core/                           # FSM core logic
│   │   ├── agent/                      # State-specific agents (Planner, BrowserNav)
│   │   ├── memory/                     # FSM memory state and transition tracking
│   │   ├── models/                     # Pydantic schemas defining FSM states and IO models
│   │   ├── orchestrator/               # FSM orchestrator running the state machine loop
│   │   ├── prompts/                    # Advanced prompts using Structured Outputs
│   │   ├── skills/                     # FSM-specific skill utilities
│   │   └── web_driver/                 # Isolated Playwright manager for FSM
│   ├── config/                         # Configuration settings
│   ├── user_preferences/               # FSM-specific preferences and resume
│   ├── utils/                          # FSM helper scripts
│   └── __main__.py                     # FSM CLI entry point
│
├── test/                               # Evaluation and testing suite
│   ├── tests_processor.py              # Main test execution orchestrator
│   └── ...                             # Specific test cases and mocks
│
├── pyproject.toml                      # Poetry dependencies and metadata
├── requirements.txt                    # Fallback pip requirements
├── .pre-commit-config.yaml             # Pre-commit hooks configuration (Black, Flake8, isort)
├── .flake8                             # Linter rules configuration
├── .isort.cfg                          # Import sorter configuration
├── .gitignore                          # Standardized ignore rules
└── .env.example                        # Example environment variables (OpenAI, LangSmith keys)
```

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8+**
2. **Poetry**: We strongly recommend using Poetry for dependency management. Install it following [these instructions](https://python-poetry.org/docs/#installation).
3. **Google Chrome**: Ensure Chrome is installed on your machine.

### Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Truong99zvc/recruitment-recommendation-agent.git
cd recruitment-recommendation-agent
poetry install
```

### Browser Setup (Dev Mode)

To allow the agent to control your browser and reuse your active sessions (like logged-in states for LinkedIn or Wellfound), you need to start Chrome with remote debugging enabled on a separate terminal.

**macOS:**
```bash
sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

**Linux:**
```bash
google-chrome --remote-debugging-port=9222
```

**Windows:**
```powershell
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

### Environment Configuration

1. Copy the example `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your **OpenAI API Key** and **Langsmith API Key**. 
   > *Note: Langsmith tracing is required by default. If you prefer to run without it, comment out the line `litellm.success_callback = ["langsmith"]` inside `./jobber_fsm/core/agent/base.py`.*

### User Preferences

Update your job preferences and details inside the `user_preferences.txt` file located in the respective agent folder (`jobber/` or `jobber_fsm/`). 
Make sure to include the local, absolute file path to your resume within this file so the agent can upload it automatically during applications.

---

## 💻 Usage

You can run either the Standard or the FSM agent via the newly added CLI interface:

```bash
# Run the FSM Agent
python -m jobber_fsm --verbose

# OR Run the Standard Agent
python -m jobber --verbose
```

Once the orchestrator starts, enter your task prompt. For example:
> *"Apply for a backend engineer role based in Helsinki on LinkedIn."*

---

## 🧪 Evaluation

To run evaluations on the agent's performance, use the provided test processor scripts:

**For Standard Jobber:**
```bash
python -m test.tests_processor --orchestrator_type vanilla
```

**For Jobber FSM:**
```bash
python -m test.tests_processor --orchestrator_type fsm
```

---

## 📚 Acknowledgements & Citations

This project is deeply inspired by phenomenal work in the AI space. Please refer to [WebVoyager](https://arxiv.org/abs/2401.13919) and [Agent-E](https://arxiv.org/abs/2407.13032).

```bibtex
@article{he2024webvoyager,
  title={WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models},
  author={He, Hongliang and Yao, Wenlin and Ma, Kaixin and Yu, Wenhao and Dai, Yong and Zhang, Hongming and Lan, Zhenzhong and Yu, Dong},
  journal={arXiv preprint arXiv:2401.13919},
  year={2024}
}

@misc{abuelsaad2024-agente,
      title={Agent-E: From Autonomous Web Navigation to Foundational Design Principles in Agentic Systems},
      author={Tamer Abuelsaad and Deepak Akkil and Prasenjit Dey and Ashish Jagmohan and Aditya Vempaty and Ravi Kokku},
      year={2024},
      eprint={2407.13032},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2407.13032},
}
```

