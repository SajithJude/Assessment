from flask import Flask, request, render_template, redirect, url_for, session
import fitz  # PyMuPDF
import os
# from google.colab import userdata
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure Google API Key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the uploaded PDF file
        pdf_file = request.files['pdf_file']
        if pdf_file:
            pdf_text = process_pdf(pdf_file)
            session['pdf_text'] = pdf_text  # Store extracted text in session for chat reference
            return redirect(url_for('chat'))
    return render_template('upload.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'pdf_text' not in session:
        return redirect(url_for('index'))  # Redirect to upload if no PDF text is stored

    if request.method == 'POST':
        user_input = request.form['message']
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat_session = model.start_chat(history=[])  # Start a new chat session
        response = chat_session.send_message(session['pdf_text'] + "\n\n" + user_input)
        session['history'].append({'role': 'user', 'text': user_input})
        session['history'].append({'role': 'model', 'text': response.text})
    else:
        session['history'] = []

    history_display = '\n\n'.join(f"**{item['role']}**: {item['text']}" for item in session['history'])
    return render_template('chat.html', history=history_display)

def process_pdf(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pdf_text = ''
    for page in pdf_document:
        pdf_text += page.get_text()
    pdf_document.close()
    return pdf_text

if __name__ == '__main__':
    app.run(debug=True)
