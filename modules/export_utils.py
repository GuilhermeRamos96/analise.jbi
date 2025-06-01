from fpdf import FPDF
import io

def export_summary_to_pdf(study_type, responses, info):
    pdf = FPDF()
    pdf.add_page()

    # Add UTF-8 font support once
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", uni=True)

    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, f"Resumo da Avaliação Crítica\nTipo de Estudo: {study_type}\n")

    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(0, 8, f"Examinador: {info.get('nome_examinador', '')}")
    pdf.multi_cell(0, 8, f"Data da avaliação: {info.get('data_avaliacao', '')}")
    pdf.multi_cell(0, 8, f"Título do artigo: {info.get('titulo_artigo', '')}")
    pdf.multi_cell(0, 8, f"Autor do artigo: {info.get('autor_artigo', '')}")
    pdf.multi_cell(0, 8, f"Ano do artigo: {info.get('ano_artigo', '')}")
    pdf.ln(5)

    for i, item in enumerate(responses):
        pdf.set_font("DejaVu", "B", size=10)  # Bold for question
        pdf.multi_cell(0, 8, f"{i + 1}. {item['question']}") 
        pdf.set_font("DejaVu", "", size=10)  # Regular for answer/snippet
        pdf.multi_cell(0, 8, f"   Resposta: {item['answer']}") 
        pdf.multi_cell(0, 8, f"   Comentário: {item['snippet']}") 
        pdf.ln(3)

    pdf_output = pdf.output(dest='S').encode("latin-1")
    return pdf_output
