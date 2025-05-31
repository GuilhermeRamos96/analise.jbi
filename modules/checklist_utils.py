
from docx import Document

def extract_checklist_from_docx(docx_path):
    document = Document(docx_path)
    checklist = []
    for para in document.paragraphs:
        if para.text.strip().startswith(tuple(['Were', 'Was', 'Did', 'Is', 'Are'])):
            checklist.append(para.text.strip())
    return checklist
