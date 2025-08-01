import streamlit as st
import json
import os
import sys

# Adiciona a pasta 'modules' ao sys.path para permitir os imports
modules_path = os.path.join(os.path.dirname(__file__), 'modules')
if modules_path not in sys.path:
    sys.path.append(modules_path)

import export_utils

st.set_page_config(page_title="Avaliação Crítica JBI", layout="wide")

st.title("📄 Sistema de Avaliação Crítica de Artigos Científicos")
st.markdown("Escolha o **delineamento metodológico** e preencha o **checklist interativo** baseado na JBI.")

# Caminho para o arquivo JSON de checklists
CHECKLIST_JSON_PATH = os.path.join('data', 'checklists.json')

# Função para carregar checklists do JSON
@st.cache_data  # Cache para evitar recarregar a cada interação
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

# Informações do artigo e avaliador
st.subheader("📌 Informações do artigo")
nome_examinador = st.text_input("Nome do examinador:")
data_avaliacao = st.date_input("Data da avaliação:")
titulo_artigo = st.text_input("Título do artigo:")
autor_artigo = st.text_input("Autor do artigo:")
ano_artigo = st.text_input("Ano do artigo:")

st.subheader("✅ Seleção do delineamento metodológico")

# Usa os tipos de estudo carregados do JSON como opções
study_types = list(all_checklists_data.keys())

if not study_types:
    st.warning("Nenhum checklist encontrado. Verifique o arquivo 'data/checklists.json'.")
else:
    option = st.selectbox("Escolha o tipo de estudo:", study_types)

    if option:
        checklist = all_checklists_data.get(option, [])

        if not checklist:
            st.warning(f"Checklist para '{option}' está vazio ou não foi carregado corretamente.")
        else:
            st.write(f"**Checklist para {option}:**")

            responses = []

            for i, question in enumerate(checklist):
                st.write(f"**{i + 1}. {question}**")
                cols = st.columns([1, 3])

                with cols[0]:
                    answer = st.radio("Resposta:", ["Sim", "Não", "Incerteza", "Não aplicável"], key=f"resp_{option}_{i}")
                with cols[1]:
                    snippet = st.text_area("Comentário:", value="", key=f"snip_{option}_{i}")

                responses.append({
                    "question": question,
                    "answer": answer,
                    "snippet": snippet
                })

            if st.button("📤 Exportar resumo em PDF"):
                try:
                    pdf_bytes = export_utils.export_summary_to_pdf(option, responses, {
                        "nome_examinador": nome_examinador,
                        "data_avaliacao": str(data_avaliacao),
                        "titulo_artigo": titulo_artigo,
                        "autor_artigo": autor_artigo,
                        "ano_artigo": ano_artigo
                    })
                    st.download_button(
                        label="📥 Baixar Resumo PDF",
                        data=pdf_bytes,
                        file_name=f"resumo_avaliacao_{option.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                    st.success("✅ Resumo gerado com sucesso. Clique no botão acima para baixar.")
                except Exception as e:
                    st.error(f"Erro ao gerar o PDF: {e}")
