from fpdf import FPDF
import io
import textwrap

class CustomPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "", 8)
        self.set_text_color(100)
        self.cell(0, 10, "Baseado nas ferramentas JBI: https://jbi.global/critical-appraisal-tools", 0, 0, "C")

def smart_text_wrap(pdf, text, max_width, font_family="Arial", font_style="", font_size=11):
    """
    Quebra inteligente de texto baseada na largura real da fonte
    """
    if not text:
        return [""]
    
    # Configurar fonte temporariamente para medir
    pdf.set_font(font_family, font_style, font_size)
    
    # Limpar e preparar texto
    text = str(text).strip()
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    lines = []
    paragraphs = text.split('\n')
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            lines.append("")
            continue
            
        # Quebrar por palavras se for muito longo
        words = paragraph.split()
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            
            # Verificar se a linha cabe na largura
            if pdf.get_string_width(test_line) <= max_width:
                current_line = test_line
            else:
                # Se a linha atual não está vazia, adicionar e começar nova
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Palavra muito longa, forçar quebra
                    if len(word) > 50:  # Palavra muito longa
                        chars_per_line = int(max_width / (font_size * 0.6))  # Estimativa
                        word_parts = textwrap.wrap(word, width=chars_per_line)
                        lines.extend(word_parts[:-1])
                        current_line = word_parts[-1] if word_parts else ""
                    else:
                        current_line = word
        
        # Adicionar última linha do parágrafo
        if current_line:
            lines.append(current_line)
    
    return lines if lines else [""]

def add_wrapped_text(pdf, text, x, y, max_width, line_height=6, font_family="Arial", font_style="", font_size=11):
    """
    Adiciona texto com quebra automática na posição especificada
    """
    pdf.set_font(font_family, font_style, font_size)
    
    lines = smart_text_wrap(pdf, text, max_width, font_family, font_style, font_size)
    current_y = y
    
    for line in lines:
        pdf.set_xy(x, current_y)
        pdf.cell(max_width, line_height, line, ln=True)
        current_y += line_height
    
    return current_y

def export_summary_to_pdf(study_type, responses, info):
    pdf = CustomPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.set_margins(left=25, top=25, right=25)
    pdf.add_page()
    
    # Larguras disponíveis
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    indent = 15
    content_width = page_width - indent
    
    current_y = pdf.get_y()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0)
    pdf.cell(0, 12, "Resumo da Avaliacao Critica", ln=True, align="C")
    current_y = pdf.get_y() + 8
    
    # Study type
    pdf.set_xy(pdf.l_margin, current_y)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Tipo de Estudo:", ln=True)
    current_y = pdf.get_y()
    
    current_y = add_wrapped_text(pdf, str(study_type), pdf.l_margin, current_y, 
                               page_width, 7, "Arial", "", 11)
    current_y += 8
    
    # Article information
    pdf.set_xy(pdf.l_margin, current_y)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Informacoes do Artigo:", ln=True)
    current_y = pdf.get_y()
    
    info_labels = {
        'nome_examinador': 'Examinador',
        'data_avaliacao': 'Data da Avaliacao',
        'titulo_artigo': 'Titulo do Artigo', 
        'autor_artigo': 'Autor do Artigo',
        'ano_artigo': 'Ano do Artigo'
    }
    
    for key, label in info_labels.items():
        value = str(info.get(key, ''))
        text_line = f"{label}: {value}"
        current_y = add_wrapped_text(pdf, text_line, pdf.l_margin, current_y, 
                                   page_width, 6, "Arial", "", 11)
    
    current_y += 10
    
    # Checklist responses
    pdf.set_xy(pdf.l_margin, current_y)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Checklist:", ln=True)
    current_y = pdf.get_y() + 4
    
    for i, item in enumerate(responses):
        # Verificar se precisa de nova página
        if current_y > pdf.h - 60:  # Se estiver muito perto do fim
            pdf.add_page()
            current_y = pdf.get_y()
        
        # Pergunta (negrito, sem recuo)
        question_text = str(item.get('question', f'Pergunta {i+1}'))
        question_full = f"{i + 1}. {question_text}"
        current_y = add_wrapped_text(pdf, question_full, pdf.l_margin, current_y, 
                                   page_width, 6, "Arial", "B", 11)
        current_y += 2
        
        # Resposta (com recuo)
        answer_text = str(item.get('answer', 'Sem resposta'))
        answer_full = f"Resposta: {answer_text}"
        current_y = add_wrapped_text(pdf, answer_full, pdf.l_margin + indent, current_y, 
                                   content_width, 6, "Arial", "", 11)
        current_y += 2
        
        # Comentário (com recuo)
        snippet_text = str(item.get('snippet', '')).strip() or 'Sem comentario.'
        comment_full = f"Comentario: {snippet_text}"
        current_y = add_wrapped_text(pdf, comment_full, pdf.l_margin + indent, current_y, 
                                   content_width, 6, "Arial", "", 11)
        current_y += 6
        
        # Linha divisória
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.2)
        pdf.line(pdf.l_margin, current_y, pdf.w - pdf.r_margin, current_y)
        current_y += 8
    
    # Gerar PDF
    try:
        pdf_output = pdf.output(dest='S').encode('latin1')
        pdf_buffer = io.BytesIO(pdf_output)
        return pdf_buffer
    except Exception as e:
        print(f"Erro na geração do PDF: {e}")
        return None

# Versão simplificada para casos extremos
def export_simple_pdf_with_wrap(study_type, responses, info):
    """
    Versão mais simples mas com quebra de texto garantida
    """
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    page_width = pdf.w - 40  # Margens de 20 de cada lado
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, "Relatorio de Avaliacao", ln=True, align="C")
    pdf.ln(10)
    
    # Usar quebra de texto para todo conteúdo
    current_y = pdf.get_y()
    
    # Tipo de estudo
    current_y = add_wrapped_text(pdf, f"Tipo de Estudo: {study_type}", 
                               20, current_y, page_width, 8, "Arial", "B", 12)
    current_y += 8
    
    # Informações
    for key, value in info.items():
        text = f"{key}: {value}"
        current_y = add_wrapped_text(pdf, text, 20, current_y, page_width, 6)
        current_y += 2
    
    current_y += 10
    
    # Respostas
    for i, item in enumerate(responses):
        if current_y > pdf.h - 40:
            pdf.add_page()
            current_y = 20
        
        # Pergunta
        current_y = add_wrapped_text(pdf, f"Pergunta {i+1}: {item.get('question', '')}", 
                                   20, current_y, page_width, 6, "Arial", "B", 11)
        current_y += 2
        
        # Resposta
        current_y = add_wrapped_text(pdf, f"Resposta: {item.get('answer', '')}", 
                                   25, current_y, page_width-5, 6)
        current_y += 2
        
        # Comentário
        current_y = add_wrapped_text(pdf, f"Comentario: {item.get('snippet', '')}", 
                                   25, current_y, page_width-5, 6)
        current_y += 10
    
    try:
        pdf_output = pdf.output(dest='S').encode('latin1')
        return io.BytesIO(pdf_output)
    except Exception as e:
        print(f"Erro: {e}")
        return None

# Função para salvar arquivo
def save_pdf_to_file(study_type, responses, info, filename="relatorio.pdf"):
    try:
        pdf_buffer = export_summary_to_pdf(study_type, responses, info)
        if pdf_buffer:
            with open(filename, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            print(f"PDF salvo como: {filename}")
            return True
        else:
            # Tentar versão simples
            pdf_buffer = export_simple_pdf_with_wrap(study_type, responses, info)
            if pdf_buffer:
                with open(filename, 'wb') as f:
                    f.write(pdf_buffer.getvalue())
                print(f"PDF salvo como: {filename} (versão simplificada)")
                return True
            else:
                print("Erro ao gerar PDF")
                return False
    except Exception as e:
        print(f"Erro ao salvar PDF: {e}")
        return False

# Exemplo de uso:
"""
try:
    pdf_buffer = export_summary_to_pdf(study_type, responses, info)
    
    # Para Flask:
    from flask import send_file
    return send_file(pdf_buffer, 
                     as_attachment=True, 
                     download_name='relatorio.pdf',
                     mimetype='application/pdf')
                     
    # Para salvar arquivo:
    save_pdf_to_file(study_type, responses, info, "meu_relatorio.pdf")
    
except Exception as e:
    print(f"Erro: {e}")
"""
