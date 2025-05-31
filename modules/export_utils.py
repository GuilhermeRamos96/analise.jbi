from fpdf import FPDF
import io

def export_summary_to_pdf(study_type, responses):
    pdf = FPDF()
    pdf.add_page()
    # Add UTF-8 font support
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)
    
    pdf.multi_cell(0, 10, f"Resumo da Avaliação Crítica\nTipo de Estudo: {study_type}\n\n")

    for i, item in enumerate(responses):
        pdf.set_font("DejaVu", "B", size=10) # Bold for question
        pdf.multi_cell(0, 8, f"{i + 1}. {item["question"]}")
        pdf.set_font("DejaVu", "", size=10) # Regular for answer/snippet
        pdf.multi_cell(0, 8, f"   Resposta: {item["answer"]}")
        pdf.multi_cell(0, 8, f"   Trecho: {item["snippet"]}")
        pdf.ln(3) # Add a bit more space between items

    # Output PDF to a byte string
    pdf_output = pdf.output(dest=\"S\").encode("latin-1") # Use latin-1 encoding as FPDF output bytes
    return pdf_output

