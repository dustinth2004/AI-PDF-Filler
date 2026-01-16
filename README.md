# AI PDF Filler

**Automate your form filling with AI.**

AI PDF Filler takes the grunt work out of filling PDFs. It intelligently detects empty fields and Q&A sections in your documents and fills them out using context you provide, powered by the Ollama AI engine.

## Section A: Introduction

### Features
*   **Automatic Field Detection**: Uses computer vision to find empty boxes and lines.
*   **Smart Q&A Processing**: Identifies "Q." and "A." sections and generates concise answers.
*   **Context-Aware**: Fills forms based on a simple text file you provide.
*   **Privacy-First**: Runs locally with Ollama (or connects to your private instance).
*   **GUI Included**: Easy-to-use interface for selecting files and monitoring progress.
*   **Multi-Platform**: Works on Windows, macOS, and Linux.

### Requirements
*   **Python 3.8+**
*   **Tesseract OCR**: The "eyes" of the operation.
*   **Ollama**: The "brain" of the operation (Running Llama 3.2 or similar).

---

## Section B: Install and Run (Main OS)

Follow these steps to get up and running on your main machine.

### 1. Install External Dependencies

**Tesseract OCR** must be installed on your system.
*   **Windows**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki) (Add to PATH during install!)
*   **macOS**: `brew install tesseract`
*   **Linux**: `sudo apt-get install tesseract-ocr`

**Ollama** must be installed and running.
1.  Download from [ollama.com](https://ollama.com).
2.  Run `ollama run llama3.2` in your terminal to pull the model and start the server.

### 2. Install the Application

Clone this repository and install the Python requirements.

```bash
git clone https://github.com/yourusername/ai-pdf-filler.git
cd ai-pdf-filler
python src/install.py
```

### 3. Run It

Launch the Graphical User Interface:

```bash
python src/gui.py
```

---

## Section B2: Alternative Configuration (Secondary OS / Remote AI)

You can run the lightweight GUI on one machine (e.g., a laptop or Raspberry Pi) and have the heavy AI lifting done on a powerful server on your network.

### Steps to Configure Remote Ollama:

1.  **On the Server (The "Brain"):**
    *   Ensure Ollama is running and accepting connections.
    *   Start Ollama with `OLLAMA_HOST=0.0.0.0 ollama serve` to allow network connections.

2.  **On the Client (The GUI):**
    *   Set the `OLLAMA_HOST` environment variable to your server's IP address before running the GUI.

    **Linux/Mac:**
    ```bash
    export OLLAMA_HOST=192.168.1.100  # Replace with your server IP
    python src/gui.py
    ```

    **Windows (PowerShell):**
    ```powershell
    $env:OLLAMA_HOST="192.168.1.100"
    python src/gui.py
    ```

---

## Section C: Crash Course

Here is how to use the tool once it's open:

1.  **Select PDF File**: Click "Browse" and pick the form you need to fill.
2.  **Select Context File**: Pick a `.txt` file that contains the data to use.
    *   *Tip*: The context file can be free-form text. e.g., "Name: John Doe, DOB: 01/01/1980, Address: 123 Main St..."
3.  **Select Output Directory**: Choose where to save the filled PDF.
4.  **Start Processing**: Click the big green button.
5.  **Wait**: The bar will fill up as it reads and writes each page.
6.  **Done**: Check your output folder for `marked_page_X.pdf`.

---

## Section D: Uh oh, I wrecked it... Now what?

**"Tesseract Not Found" Error**
*   Make sure Tesseract is installed.
*   On Windows, ensure you added it to your System PATH during installation.
*   If it's installed in a weird spot, you can set the path in your environment variables.

**"Connection Refused" (Ollama)**
*   Is Ollama running? Type `ollama list` in a terminal.
*   If running remotely, check your firewall and IP address.

**"The AI wrote nonsense"**
*   Check your **Context File**. Garbage in, garbage out. Make sure the info is clear.
*   Try a different model. The code defaults to `llama3.2`, but you can edit `src/pdf_processor.py` to change the model name if you have `mistral` or `llama2` preferred.

**"It didn't find the box"**
*   The PDF might be too blurry.
*   The tool looks for boxes with specific dimensions. If your form has tiny checkboxes or huge text areas, they might be missed.

---

## Section E: Suggestions?

Found a bug? Have a cool feature idea?

1.  **Fork** the repo.
2.  **Create a branch** (`git checkout -b feature/AmazingIdea`).
3.  **Commit** your changes.
4.  **Push** to the branch.
5.  **Open a Pull Request**.

We love feedback! Happy filling.
