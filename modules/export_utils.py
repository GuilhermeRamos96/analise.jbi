from fpdf import FPDF
import io

class CustomPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "", 8)
        self.set_text_color(100)
        self.cell(0, 10, "Baseado nas ferramentas JBI: https://jbi.global/critical-appraisal-tools", 0, 0, "C")

def export_summary_to_pdf(study_type, responses, info):
    pdf = CustomPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(left=20, top=20, right=20)
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0)
    pdf.cell(0, 12, "Resumo da Avaliacao Critica", ln=True, align="C")
    pdf.ln(8)
    
    # Study type
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Tipo de Estudo:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, study_type, align="L")
    pdf.ln(5)
    
    # Article information
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Informacoes do Artigo:", ln=True)
    pdf.set_font("Arial", "", 11)
    
    info_labels = {
        'nome_examinador': 'Examinador',
        'data_avaliacao': 'Data da Avaliacao',
        'titulo_artigo': 'Titulo do Artigo', 
        'autor_artigo': 'Autor do Artigo',
        'ano_artigo': 'Ano do Artigo'
    }
    
    for key, label in info_labels.items():
        value = info.get(key, '')
        pdf.multi_cell(0, 6, f"{label}: {value}", align="L")
    
    pdf.ln(8)
    
    # Checklist responses
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Checklist:", ln=True)
    pdf.ln(4)
    
    indent = 10
    usable_width = pdf.w - pdf.r_margin - pdf.l_margin - indent
    
    for i, item in enumerate(responses):
        # Pergunta
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 6, f"{i + 1}. {item['question']}", align="L")
        
        # Resposta
        pdf.set_font("Arial", "", 11)
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(usable_width, 6, f"Resposta: {item['answer']}", align="L")
        
        # Comentário
        snippet_text = item.get('snippet', '').strip() or 'Sem comentario.'
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(usable_width, 6, f"Comentario: {snippet_text}", align="L")
        
        pdf.ln(4)
        
        # Linha divisória
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.2)
        x_start = pdf.l_margin
        x_end = pdf.w - pdf.r_margin
        y = pdf.get_y()
        pdf.line(x_start, y, x_end, y)
        pdf.ln(4)
    
    # Gerar PDF em buffer
    pdf_buffer = io.BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    pdf_buffer.write(pdf_output)
    pdf_buffer.seek(0)
    
    return pdf_buffer

# Função alternativa para salvar diretamente em arquivo
def save_pdf_to_file(study_type, responses, info, filename="relatorio.pdf"):
    pdf = CustomPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(left=20, top=20, right=20)
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0)
    pdf.cell(0, 12, "Resumo da Avaliacao Critica", ln=True, align="C")
    pdf.ln(8)
    
    # Study type
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Tipo de Estudo:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, study_type, align="L")
    pdf.ln(5)
    
    # Article information
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Informacoes do Artigo:", ln=True)
    pdf.set_font("Arial", "", 11)
    
    info_labels = {
        'nome_examinador': 'Examinador',
        'data_avaliacao': 'Data da Avaliacao',
        'titulo_artigo': 'Titulo do Artigo', 
        'autor_artigo': 'Autor do Artigo',
        'ano_artigo': 'Ano do Artigo'
    }
    
    for key, label in info_labels.items():
        value = info.get(key, '')
        pdf.multi_cell(0, 6, f"{label}: {value}", align="L")
    
    pdf.ln(8)
    
    # Checklist responses
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Checklist:", ln=True)
    pdf.ln(4)
    
    indent = 10
    usable_width = pdf.w - pdf.r_margin - pdf.l_margin - indent
    
    for i, item in enumerate(responses):
        # Pergunta
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 6, f"{i + 1}. {item['question']}", align="L")
        
        # Resposta
        pdf.set_font("Arial", "", 11)
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(usable_width, 6, f"Resposta: {item['answer']}", align="L")
        
        # Comentário
        snippet_text = item.get('snippet', '').strip() or 'Sem comentario.'
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(usable_width, 6, f"Comentario: {snippet_text}", align="L")
        
        pdf.ln(4)
        
        # Linha divisória
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.2)
        x_start = pdf.l_margin
        x_end = pdf.w - pdf.r_margin
        y = pdf.get_y()
        pdf.line(x_start, y, x_end, y)
        pdf.ln(4)
    
    # Salvar arquivo
    pdf.output(filename)
    print(f"PDF salvo como: {filename}")

# Exemplo de uso:
"""
# Para usar em Flask/Django (retorna buffer):
pdf_buffer = export_summary_to_pdf(study_type, responses, info)

# Para download em Flask:
from flask import send_file
return send_file(pdf_buffer, 
                 as_attachment=True, 
                 download_name='relatorio.pdf',
                 mimetype='application/pdf')

# Para salvar arquivo local:
save_pdf_to_file(study_type, responses, info, "meu_relatorio.pdf")
"""
