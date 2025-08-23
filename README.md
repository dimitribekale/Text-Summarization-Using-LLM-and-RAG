# Text-Summarization-Using-Ollama-and-RAG
This simple project help summarizing a text or pdf document(supported formats: .txt and .pdf). You can also automatically summarize all the documents in a folder using a powerful model from the Ollama API for free.

# 📄 AI-Powered PDF Summarizer

This project is a simple AI-powered tool to summarize PDF documents.
It can process an entire folder of PDF files, extract their contents, and generate concise summaries.

✅ Handles multiple PDFs at once

✅ Outputs summaries either in the same folder or in a new output/ folder

✅ Supports Ollama as the AI inference engine

✅ Defaults to the deepseek-r1:7b model if no other Ollama model is specified

# 🚀 Features
Extracts text from all PDFs in a given folder.

Uses Ollama API models for natural language summarization.

Saves results in .txt format alongside the original PDFs or in an output/ folder.

Works on Windows, macOS, and Linux.

# 🔧 Installation Guide
1. Clone the Repository

bash
git clone https://github.com/dimitribekale/Text-Summarization-Using-LLM-and-RAG
.git
cd pdf-summarizer

2. Create a Python Virtual Environment

🟦 Windows (PowerShell)

powershell
python -m venv .venv
.venv\Scripts\activate

🍎 macOS

bash
python3 -m venv .venv
source .venv/bin/activate

🐧 Linux

bash
python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies

bash
pip install --upgrade pip
pip install -r requirements.txt

🧠 Setting up Ollama

This project uses Ollama for AI inference.

1. Install Ollama
macOS: Download from the official website.

Linux: Follow installation instructions from Ollama docs.

Windows: Use WSL2 (Ubuntu recommended) or the native Windows Ollama installer (if available).

2. Run the Ollama Service
bash
ollama serve
This runs the Ollama server in the background.

3. Pull Your Desired Model
By default, the tool uses:

bash
ollama pull deepseek-r1:7b
If you want to use another model (e.g., llama3:8b):

bash
ollama pull llama3:8b

# ▶️ Usage

Run the script:

bash
python main.py --input-folder path/to/pdf/folder

Options:

--input-folder → Path to folder containing PDFs.

--output-folder → Path to store summaries. If not provided, defaults to output/.

--model → Ollama model to use (default: deepseek-r1:7b).

Example:

bash
python summarize.py --input-folder ./pdfs --output-folder ./summaries --model llama3:8b
🗂 Project Structure

text
📂 src/
 ┣ 📜 main.py             # Main script
 ┣ 📜 rag.py              # Retrieval component script
 ┣ 📜 read_file.py        # File reader component script
 ┣ 📜 requirements.txt    # Python dependencies
 ┣ 📜 README.md           # Project documentation
 ┣ 📂 pdfs/               # (Example folder for input PDFs)
 ┗ 📂 output/             # Summarized results (auto-created)

⚡️ Troubleshooting
Ollama not running? → Ensure you started ollama serve.

Model not found? → Run ollama pull <model-name> before executing script.

PDF text not extracted correctly? → Some PDFs are images; you may need OCR (planned feature).

📌 Roadmap

 Support for batch summarization with progress tracking

👨💻 Contribution
Feel free to fork this repo, open issues, or submit PRs for improvements.

📜 License
MIT License – Free to use and modify.
