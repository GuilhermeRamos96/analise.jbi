import streamlit as st
import json
import os
from modules import pdf_utils, export_utils # Removido checklist_utils

st.set_page_config(page_title="Avaliação Crítica JBI", layout="wide")

st.title("📄 Sistema de Avaliação Crítica de Artigos Científicos")
st.markdown("Carregue um **artigo em PDF**, escolha o **delineamento metodológico** e preencha o **checklist interativo**.")

# Caminho para o arquivo JSON de checklists
CHECKLIST_JSON_PATH = os.path.join('data', 'checklists.json')

# Função para carregar checklists do JSON
@st.cache_data # Cache para evitar recarregar a cada interação
def load_checklists(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Erro: Arquivo de checklists '{json_path}' não encontrado.")
        return {}
    except json.JSONDecodeError:
        st.error(f"Erro: Falha ao decodificar o arquivo JSON '{json_path}'. Verifique o formato.")
        return {}

# Carrega os dados dos checklists
all_checklists_data = load_checklists(CHECKLIST_JSON_PATH)

if 'selected_snippets' not in st.session_state:
    st.session_state.selected_snippets = {}

pdf_file = st.file_uploader("➡️ Carregar artigo PDF", type=["pdf"])

if pdf_file:
    try:
        pages, num_pages = pdf_utils.extract_text_from_pdf(pdf_file)
        page = st.slider("📄 Página para visualização:", 1, num_pages, 1)
        
        with st.expander("🔍 Visualizar página selecionada"):
            st.text_area("Texto da Página:", pages[page - 1], height=300)

        selected_text = st.text_area("✂️ Selecione e copie aqui o trecho relevante do artigo:", "")
    except Exception as e:
        st.error(f"Erro ao processar o PDF: {e}")
        st.stop()

st.subheader("✅ Seleção do delineamento metodológico")

# Usa os tipos de estudo carregados do JSON como opções
study_types = list(all_checklists_data.keys())

if not study_types:
    st.warning("Nenhum checklist encontrado. Verifique o arquivo 'data/checklists.json'.")
else:
    option = st.selectbox("Escolha o tipo de estudo:", study_types)

    if option:
        # Obtém o checklist selecionado do dicionário carregado
        checklist = all_checklists_data.get(option, [])
        
        if not checklist:
             st.warning(f"Checklist para '{option}' está vazio ou não foi carregado corretamente.")
        else:
            st.write(f"**Checklist para {option}:**")
            
            responses = []

            for i, question in enumerate(checklist):
                st.write(f"**{i + 1}. {question}**")
                # Usar colunas pode não ser ideal em todas as larguras, mas mantém o layout original
                cols = st.columns([1, 3]) 
                
                with cols[0]:
                    # Usar um ID único para cada widget é crucial no Streamlit
                    answer = st.radio("Resposta:", ["Sim", "Não", "Incerteza", "Não aplicável"], key=f"resp_{option}_{i}") 
                with cols[1]:
                    # Usar um valor padrão vazio ou o texto selecionado se disponível
                    default_snippet = selected_text if 'selected_text' in locals() else ""
                    snippet = st.text_area("Trecho associado:", value=default_snippet, key=f"snip_{option}_{i}")

                responses.append({
                    "question": question,
                    "answer": answer,
                    "snippet": snippet
                })

            if st.button("📤 Exportar resumo em PDF"):
                try:
                    # Passa o tipo de estudo para a função de exportação
                    pdf_bytes = export_utils.export_summary_to_pdf(option, responses)
                    st.download_button(
                        label="📥 Baixar Resumo PDF",
                        data=pdf_bytes,
                        file_name=f"resumo_avaliacao_{option.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                    st.success("✅ Resumo gerado com sucesso. Clique no botão acima para baixar.")
                except Exception as e:
                    st.error(f"Erro ao gerar o PDF: {e}")

