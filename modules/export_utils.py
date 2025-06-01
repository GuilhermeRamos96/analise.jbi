from fpdf import FPDF
import io

def test_pdf_generation():
    """
    Função para testar se o ambiente suporta geração de PDF
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(40, 10, "Teste")
        
        # Testar método 1
        try:
            buffer1 = io.BytesIO()
            pdf.output(buffer1)
            buffer1.seek(0)
            print("✅ Método 1 (output direto) funciona")
            return "metodo1"
        except Exception as e:
            print(f"❌ Método 1 falhou: {e}")
        
        # Testar método 2
        try:
            content = pdf.output(dest='S')
            if content:
                if isinstance(content, str):
                    buffer2 = io.BytesIO(content.encode('latin1'))
                else:
                    buffer2 = io.BytesIO(content)
                print("✅ Método 2 (dest='S') funciona")
                return "metodo2"
        except Exception as e:
            print(f"❌ Método 2 falhou: {e}")
        
        # Testar método 3 (arquivo temporário)
        try:
            import tempfile
            import os
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            pdf.output(temp_file.name)
            with open(temp_file.name, 'rb') as f:
                content = f.read()
            os.unlink(temp_file.name)
            buffer3 = io.BytesIO(content)
            print("✅ Método 3 (arquivo temporário) funciona")
            return "metodo3"
        except Exception as e:
            print(f"❌ Método 3 falhou: {e}")
        
        return None
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return None

def export_guaranteed_pdf(study_type, responses, info):
    """
    Versão que se adapta ao seu ambiente
    """
    # Descobrir qual método funciona
    working_method = test_pdf_generation()
    
    if not working_method:
        print("❌ ERRO: Nenhum método de PDF funciona no seu ambiente")
        return None
    
    print(f"🔧 Usando {working_method} para gerar PDF")
    
    # Criar PDF principal
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Função para texto seguro (sem quebra de linha)
    def safe_text(text, max_chars=80):
        if not text:
            return ""
        text = str(text).replace('\n', ' ').replace('\r', ' ')
        if len(text) > max_chars:
            return text[:max_chars-3] + "..."
        return text
    
    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, "Relatorio de Avaliacao", ln=True, align="C")
    pdf.ln(10)
    
    # Tipo de estudo
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Tipo de Estudo:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, safe_text(study_type), ln=True)
    pdf.ln(5)
    
    # Informações do artigo
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Informacoes do Artigo:", ln=True)
    pdf.set_font("Arial", "", 11)
    
    info_map = {
        'nome_examinador': 'Examinador',
        'data_avaliacao': 'Data',
        'titulo_artigo': 'Titulo',
        'autor_artigo': 'Autor',
        'ano_artigo': 'Ano'
    }
    
    for key, label in info_map.items():
        value = safe_text(info.get(key, ''), 60)
        pdf.cell(0, 6, f"{label}: {value}", ln=True)
    
    pdf.ln(8)
    
    # Checklist
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Checklist:", ln=True)
    pdf.ln(5)
    
    for i, item in enumerate(responses):
        # Verificar espaço na página
        if pdf.get_y() > 250:
            pdf.add_page()
        
        # Pergunta
        pdf.set_font("Arial", "B", 11)
        question = safe_text(item.get('question', ''), 70)
        pdf.cell(0, 7, f"{i+1}. {question}", ln=True)
        
        # Resposta
        pdf.set_font("Arial", "", 10)
        answer = safe_text(item.get('answer', ''), 60)
        pdf.cell(0, 6, f"    Resposta: {answer}", ln=True)
        
        # Comentário
        snippet = safe_text(item.get('snippet', ''), 60)
        pdf.cell(0, 6, f"    Comentario: {snippet}", ln=True)
        pdf.ln(3)
        
        # Linha divisória
        pdf.set_draw_color(200)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(5)
    
    # Gerar usando o método que funciona
    try:
        if working_method == "metodo1":
            buffer = io.BytesIO()
            pdf.output(buffer)
            buffer.seek(0)
            return buffer
            
        elif working_method == "metodo2":
            content = pdf.output(dest='S')
            if isinstance(content, str):
                return io.BytesIO(content.encode('latin1'))
            else:
                return io.BytesIO(content)
                
        elif working_method == "metodo3":
            import tempfile
            import os
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            pdf.output(temp_file.name)
            with open(temp_file.name, 'rb') as f:
                content = f.read()
            os.unlink(temp_file.name)
            return io.BytesIO(content)
            
    except Exception as e:
        print(f"❌ Erro na geração final: {e}")
        return None

# Função de teste completa
def test_complete_flow(study_type="Teste", responses=None, info=None):
    """
    Testa o fluxo completo
    """
    if responses is None:
        responses = [
            {
                'question': 'Esta é uma pergunta de teste?',
                'answer': 'Sim',
                'snippet': 'Este é um comentário de teste'
            }
        ]
    
    if info is None:
        info = {
            'nome_examinador': 'Teste',
            'data_avaliacao': '2024-01-01',
            'titulo_artigo': 'Artigo de Teste',
            'autor_artigo': 'Autor Teste',
            'ano_artigo': '2024'
        }
    
    print("🧪 Testando geração completa de PDF...")
    buffer = export_guaranteed_pdf(study_type, responses, info)
    
    if buffer:
        print("✅ PDF gerado com sucesso!")
        print(f"📊 Tamanho: {len(buffer.getvalue())} bytes")
        
        # Salvar arquivo de teste
        try:
            with open("teste_pdf.pdf", "wb") as f:
                f.write(buffer.getvalue())
            print("💾 PDF salvo como 'teste_pdf.pdf'")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False
    else:
        print("❌ Falha na geração do PDF")
        return False

# Para usar:
if __name__ == "__main__":
    # Rodar teste
    success = test_complete_flow()
    
    if success:
        print("\n🎉 SUCESSO! O código está funcionando.")
        print("Agora você pode usar export_guaranteed_pdf() com seus dados reais.")
    else:
        print("\n💔 FALHA! Há um problema no seu ambiente.")
        print("Tente instalar: pip install fpdf2")
