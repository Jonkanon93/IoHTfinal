from flask import Flask, request, render_template, send_from_directory
import os
import requests
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from patient_variations import patient_variations

app = Flask(__name__)
env = Environment(loader=FileSystemLoader('templates'))

app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/trigger_rpi', methods=['GET'])
def trigger_rpi():
  
    rpi_url = "http://192.168.36.196:5001/wait_for_trigger"

    response = requests.get(rpi_url)

    if response.status_code == 200:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'readings.txt')
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return {"message": "Trigger sent successfully, file saved at: " + file_path}
    else:
        return {"error": "Failed to trigger Raspberry Pi"}, 500

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def update_patient_file(patient, content):
    file_path = f"patient_files/{patient}.txt"
    new_content = {key: extract_content_after_keyword(content, key) for key in ["tilstand", "medicin", "note"]}

    existing_content = {"tilstand": "", "medicin": "", "note": ""}
    category = None

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip().endswith(':'):
                    category = line.strip().split(':')[0]
                elif category and category in new_content and line.strip():
                    existing_content[category] += line

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for key, value in new_content.items():
        if value:
            existing_content[key] += f"{timestamp}: {value}\n"

    with open(file_path, 'w') as file:
        for key in ["tilstand", "medicin", "note"]:
            if existing_content[key]:
                file.write(f"{key}:\n{existing_content[key]}")

    return existing_content

def extract_content_after_keyword(text, keyword):
    start_index = text.find(keyword)
    if start_index != -1:
        end_index = min([text.find(k, start_index + 1) for k in ["tilstand", "medicin", "note"] if text.find(k, start_index + 1) != -1] + [len(text)])
        return text[start_index + len(keyword):end_index].strip()
    return ""

def generate_html_file(patient, patient_content):
    template = env.get_template('template.html')
    html_output = template.render(patient_number=patient, patient_content=patient_content)

    with open(f'templates/{patient}.html', 'w') as html_file:
        html_file.write(html_output)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join("received_files", uploaded_file.filename)
        uploaded_file.save(file_path)

        with open(file_path, 'r') as file:
            content = file.read()

        if 'data' in content:
            trigger_rpi()  

        matched_patient = 'default'
        for patient, variations in patient_variations.items():
            for variation in variations:
                if content.startswith(variation):
                    matched_patient = patient
                    break

        updated_content = update_patient_file(matched_patient, content)
        generate_html_file(matched_patient, updated_content)

        return 'File received successfully', 200
    return 'No file found', 400


@app.route('/<patient>')
def view_text(patient):
    template_name = f"{patient}.html" if os.path.exists(f'templates/{patient}.html') else 'default.html'
    file_path = f"patient_files/{patient}.txt" if os.path.exists(f"patient_files/{patient}.txt") else f"patient_files/default.txt"
    patient_content = {"tilstand": "", "medicin": "", "note": ""}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                section = line.split(':')[0].strip()
                if section in patient_content:
                    patient_content[section] += line
    return render_template(template_name, patient_number=patient, patient_content=patient_content)

if __name__ == '__main__':
    os.makedirs("received_files", exist_ok=True)
    os.makedirs("patient_files", exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
