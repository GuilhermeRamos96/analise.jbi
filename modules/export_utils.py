from fpdf import FPDF
import io
import textwrap

class CustomPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(100)
        self.cell(0, 10, "Baseado nas ferramentas JBI: https://jbi.global/critical-appraisal-tools", 0, 0, "C")

def wrap_text(text, width=120):
    return "\n".join(textwrap.wrap(text, width=width))

def export_summary_to_pdf(study_type, responses, info):
    pdf = CustomPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(left=15, top=20, right=15)
    pdf.add_page()

    # Add UTF-8 font support once
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", uni=True)

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin

    # Title
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Resumo da Avaliação Crítica", ln=True, align="C")
    pdf.ln(5)

    # Study type
    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(usable_width, 10, wrap_text(f"Tipo de Estudo: {study_type}"))
    pdf.ln(3)

    # Article information
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 8, "Informações do Artigo:", ln=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(usable_width, 8, wrap_text(f"Examinador: {info.get('nome_examinador', '')}"))
    pdf.multi_cell(usable_width, 8, wrap_text(f"Data da avaliação: {info.get('data_avaliacao', '')}"))
    pdf.multi_cell(usable_width, 8, wrap_text(f"Título do artigo: {info.get('titulo_artigo', '')}"))
    pdf.multi_cell(usable_width, 8, wrap_text(f"Autor do artigo: {info.get('autor_artigo', '')}"))
    pdf.multi_cell(usable_width, 8, wrap_text(f"Ano do artigo: {info.get('ano_artigo', '')}"))
    pdf.ln(5)

    # Checklist responses
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 8, "Checklist:", ln=True)
    pdf.ln(2)

    for i, item in enumerate(responses):
        pdf.set_font("DejaVu", "B", 10)
        pdf.multi_cell(usable_width, 7, wrap_text(f"{i + 1}. {item['question']}"))
        pdf.set_font("DejaVu", "", 10)
        pdf.multi_cell(usable_width, 7, wrap_text(f"Resposta: {item['answer']}"))
        snippet_text = item['snippet'].strip() if item['snippet'].strip() else 'Sem comentário.'
        pdf.multi_cell(usable_width, 7, wrap_text(f"Comentário: {snippet_text}"))
        pdf.ln(3)

    # Output
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer.getvalue()
