from fpdf import FPDF
import io

class CustomPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(100)
        self.cell(0, 10, "Baseado nas ferramentas JBI: https://jbi.global/critical-appraisal-tools", 0, 0, "C")

def export_summary_to_pdf(study_type, responses, info):
    pdf = CustomPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(left=15, top=20, right=15)
    pdf.add_page()

    # Add UTF-8 font support once
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", uni=True)

    # Title
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Resumo da Avaliação Crítica", ln=True, align="C")
    pdf.ln(5)

    # Study type
    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 10, f"Tipo de Estudo: {study_type}", align="J")
    pdf.ln(3)

    # Article information
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 8, "Informações do Artigo:", ln=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(0, 8, f"Examinador: {info.get('nome_examinador', '')}", align="J")
    pdf.multi_cell(0, 8, f"Data da avaliação: {info.get('data_avaliacao', '')}", align="J")
    pdf.multi_cell(0, 8, f"Título do artigo: {info.get('titulo_artigo', '')}", align="J")
    pdf.multi_cell(0, 8, f"Autor do artigo: {info.get('autor_artigo', '')}", align="J")
    pdf.multi_cell(0, 8, f"Ano do artigo: {info.get('ano_artigo', '')}", align="J")
    pdf.ln(5)

    # Checklist responses
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 8, "Checklist:", ln=True)
    pdf.ln(2)

    for i, item in enumerate(responses):
        pdf.set_font("DejaVu", "B", 10)
        pdf.multi_cell(0, 7, f"{i + 1}. {item['question']}", align="J")
        pdf.set_font("DejaVu", "", 10)
        pdf.multi_cell(0, 7, f"Resposta: {item['answer']}", align="J")
        snippet_text = item['snippet'].strip() if item['snippet'].strip() else 'Sem comentário.'
        pdf.multi_cell(0, 7, f"Comentário: {snippet_text}", align="J")
        pdf.ln(3)

    # Output
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer.getvalue()

