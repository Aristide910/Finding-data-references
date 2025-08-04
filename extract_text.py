import os
import json
import pandas as pd
import xml.etree.ElementTree as ET
from docx import Document
import PyPDF2

def extract_text_from_pdf(path):
    text = ""
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ''
    return text

def extract_text_from_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return ET.tostring(root, encoding='unicode')

def extract_text_from_docx(path):
    doc = Document(path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_csv(path):
    df = pd.read_csv(path)
    return df.to_string()

def extract_text_from_xlsx(path):
    df = pd.read_excel(path)
    return df.to_string()

def extract_text_from_txt(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def extract_text_from_file(path):
    ext = os.path.splitext(path)[-1].lower()
    try:
        if ext == '.txt':
            return extract_text_from_txt(path)
        elif ext == '.pdf':
            return extract_text_from_pdf(path)
        elif ext == '.docx':
            return extract_text_from_docx(path)
        elif ext == '.csv':
            return extract_text_from_csv(path)
        elif ext == '.xlsx':
            return extract_text_from_xlsx(path)
        elif ext == '.json':
            return extract_text_from_json(path)
        elif ext == '.xml':
            return extract_text_from_xml(path)
        else:
            return f"[!] Format non supporté: {ext}"
    except Exception as e:
        return f"[!] Erreur avec {path} : {e}"

def extract_text_from_folder(folder_path):
    results = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            print(f"Lecture de: {file}")
            text = extract_text_from_file(full_path)
            results[file] = text
    return results

# Test avec un dossier local
if __name__ == "__main__":
    dossier = "make-data-count/train/PDF"
    extraits = extract_text_from_folder(dossier)

    # Sauvegarde dans un fichier texte (facultatif)
    with open("extraits_resultats.txt", "w", encoding="utf-8") as out:
        for nom_fichier, contenu in extraits.items():
            out.write(f"=== {nom_fichier} ===\n{contenu}\n\n")
