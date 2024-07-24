from flask import Flask, request, render_template
import fitz  # PyMuPDF
import requests

app = Flask(__name__)

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
    response = query_gemini_api(pdf_text, question)

    return response

def process_pdf(file):
    # Using PyMuPDF to extract text from the PDF
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    pdf_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pdf_text += page.get_text()
    return pdf_text

def query_gemini_api(pdf_text, question):
    headers = {
        'Authorization': 'Bearer AIzaSyAFt3EOfTkY5eZXF3k-9IDowvUTL6lBPJo',  # Your Gemini API key
        'Content-Type': 'application/json'
    }
    data = {
        'documents': [pdf_text],
        'question': question
    }
    response = requests.post('https://api.gemini.com/query', headers=headers, json=data)
    return response.json().get('answers', ['No answer found'])[0]

if __name__ == '__main__':
    app.run(debug=True)
