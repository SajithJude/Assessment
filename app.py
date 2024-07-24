from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)


import os
from flask import Flask, request, render_template
import llamaindex
import requests

app = Flask(__name__)


gemini_api_key = os.getenv("GEMINI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, render_template
import llamaindex
import requests

app = Flask(__name__)

# Load the API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query-pdf', methods=['POST'])
def query_pdf():
    if 'pdf_file' not in request.files:
        return 'No file part'
    file = request.files['pdf_file']
    question = request.form['question']

    # Process the PDF file and prepare it for querying
    pdf_text = process_pdf(file)

    # Query using Gemini API
    response = query_gemini(pdf_text, question)

    return response['answers'][0]

def process_pdf(file):
    # Example using PyMuPDF (fitz) for PDF processing
    import fitz  # Install using `pip install PyMuPDF`
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def query_gemini(pdf_text, question):
    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "documents": [pdf_text],
        "question": question
    }
    response = requests.post("https://api.gemini.com/query", headers=headers, json=data)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
