# export_utils.py - Arquivo completo com página final de referência JBI

from fpdf import FPDF
import io
import textwrap

class CustomPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "", 8)
        self.set_text_color(100)
        self.cell(0, 10, "Baseado nas ferramentas JBI: https://jbi.global/critical-appraisal-tools", 0, 0, "C")

def export_summary_to_pdf(study_type, responses, info):
    """
    Função principal para gerar PDF - VERSÃO ROBUSTA
    """
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Configurações básicas
    pdf.set_font("Arial", "", 12)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, "Resumo da Avaliação Crítica - Baseado na JBI", ln=True, align="C")
    pdf.ln(10)

    # Função para adicionar texto com quebra segura
    def add_text_safe(text, bold=False, indent=0):
        style = "B" if bold else ""
        pdf.set_font("Arial", style, 11)

        clean_text = str(text).strip()
        if not clean_text:
            return

        max_chars = 90 - indent
        if len(clean_text) > max_chars:
            lines = textwrap.wrap(clean_text, width=max_chars)
        else:
            lines = [clean_text]

        for line in lines:
            if indent > 0:
                line = " " * indent + line
            pdf.cell(0, 7, line, ln=True)
        pdf.ln(2)

    # Tipo de estudo
    add_text_safe("Tipo de Estudo:", bold=True)
    add_text_safe(study_type)
    pdf.ln(5)

    # Informações do artigo
    add_text_safe("Informações do Artigo:", bold=True)

    info_labels = {
        'nome_examinador': 'Examinador',
        'data_avaliacao': 'Data da Avaliacao',
        'titulo_artigo': 'Titulo do Artigo',
        'autor_artigo': 'Autor do Artigo',
        'ano_artigo': 'Ano do Artigo'
    }

    for key, label in info_labels.items():
        value = info.get(key, '')
        add_text_safe(f"{label}: {value}")

    pdf.ln(8)

    # Checklist
    add_text_safe("Checklist:", bold=True)
    pdf.ln(3)

    for i, item in enumerate(responses):
        if pdf.get_y() > 250:
            pdf.add_page()

        question = item.get('question', f'Pergunta {i+1}')
        add_text_safe(f"{i+1}. {question}", bold=True)

        answer = item.get('answer', 'Sem resposta')
        add_text_safe(f"Resposta: {answer}", indent=4)

        snippet = item.get('snippet', '') or 'Sem comentario'
        add_text_safe(f"Comentario: {snippet}", indent=4)

        pdf.ln(5)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(5)

    # Adicionar página final com referência JBI
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 8, "Referência Metodológica", align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)
    texto_referencia = (
        "Este documento foi elaborado pelo 'avaliacriticajbi' com base nas Ferramentas de Avaliação Crítica da "
        "Joanna Briggs Institute (JBI).\n\n"
        "Para mais informações, acesse: https://jbi.global/critical-appraisal-tools"
        "APP, acesse: https://avaliacriticajbi.streamlit.app/"
    )
    pdf.multi_cell(0, 7, texto_referencia)

    # Gerar PDF com fallback
    try:
        pdf_content = pdf.output(dest='S')
        pdf_buffer = io.BytesIO()
        if isinstance(pdf_content, str):
            pdf_buffer.write(pdf_content.encode('latin1'))
        else:
            pdf_buffer.write(pdf_content)
        pdf_buffer.seek(0)
        return pdf_buffer
    except Exception as e1:
        try:
            pdf_buffer = io.BytesIO()
            pdf.output(pdf_buffer)
            pdf_buffer.seek(0)
            return pdf_buffer
        except Exception as e2:
            try:
                import tempfile
                import os
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    pdf.output(tmp_file.name)
                    with open(tmp_file.name, 'rb') as f:
                        pdf_data = f.read()
                    os.unlink(tmp_file.name)
                    return io.BytesIO(pdf_data)
            except Exception as e3:
                print(f"Erro método 1: {e1}")
                print(f"Erro método 2: {e2}")
                print(f"Erro método 3: {e3}")
                return None

def save_pdf_to_file(study_type, responses, info, filename="relatorio.pdf"):
    try:
        pdf_buffer = export_summary_to_pdf(study_type, responses, info)
        if pdf_buffer:
            with open(filename, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            print(f"PDF salvo como: {filename}")
            return True
        else:
            print("Erro ao gerar PDF")
            return False
    except Exception as e:
        print(f"Erro ao salvar PDF: {e}")
        return False

def get_pdf_data(study_type, responses, info):
    pdf_buffer = export_summary_to_pdf(study_type, responses, info)
    if pdf_buffer:
        return pdf_buffer.getvalue()
    return None

def get_pdf_response(study_type, responses, info, filename="relatorio.pdf"):
    try:
        from flask import send_file
        pdf_buffer = export_summary_to_pdf(study_type, responses, info)
        if pdf_buffer:
            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=filename,
                mimetype='application/pdf'
            )
        return None
    except ImportError:
        print("Flask não disponível")
        return None
    except Exception as e:
        print(f"Erro no Flask response: {e}")
        return None
