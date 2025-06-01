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
    pdf.set_margins(left=20, top=20, right=20)
    pdf.add_page()

    # Add UTF-8 font support
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", uni=True)

    # Title
    pdf.set_font("DejaVu", "B", 16)
    pdf.set_text_color(0)
    pdf.cell(0, 12, "Resumo da Avaliação Crítica", ln=True, align="C")
    pdf.ln(8)

    # Study type
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 8, "Tipo de Estudo:", ln=True)
    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 7, study_type, align="L")
    pdf.ln(5)

    # Article information
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 8, "Informações do Artigo:", ln=True)
    pdf.set_font("DejaVu", "", 11)
    for key, label in [('nome_examinador', 'Examinador'),
                       ('data_avaliacao', 'Data da Avaliação'),
                       ('titulo_artigo', 'Título do Artigo'),
                       ('autor_artigo', 'Autor do Artigo'),
                       ('ano_artigo', 'Ano do Artigo')]:
        value = info.get(key, '')
        pdf.multi_cell(0, 6, f"{label}: {value}", align="L")
    pdf.ln(8)

    # Checklist responses
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 8, "Checklist:", ln=True)
    pdf.ln(4)

    indent = 10  # Recuo para respostas e comentários

    for i, item in enumerate(responses):
        # Pergunta
        pdf.set_font("DejaVu", "B", 11)
        pdf.multi_cell(0, 6, f"{i + 1}. {item['question']}", align="L")

        # Resposta (indentada)
        pdf.set_font("DejaVu", "", 11)
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(0, 6, f"Resposta: {item['answer']}", align="L")

        # Comentário (indentado)
        snippet_text = item['snippet'].strip() or 'Sem comentário.'
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(0, 6, f"Comentário: {snippet_text}", align="L")
        
        pdf.ln(4)

        # Linha divisória suave
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.2)
        x_start = pdf.l_margin
        x_end = pdf.w - pdf.r_margin
        y = pdf.get_y()
        pdf.line(x_start, y, x_end, y)
        pdf.ln(4)

    # Output
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer.getvalue()
