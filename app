import streamlit as st
import json
import math

# 1. Configuração da Página
st.set_page_config(
    page_title="Helipê Ateliê Lúdico - Guia de Desenvolvimento",
    page_icon="🌱",
    layout="centered"
)

# 2. Estilização CSS Customizada (Cores e tipografia limpas)
st.markdown("""
    <style>
    .titulo-principal {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .subtitulo {
        color: #7f8c8d;
        text-align: center;
        font-size: 1.1em;
        margin-bottom: 2rem;
    }
    .disclaimer-montessori {
        background-color: #f9f6f0;
        border-left: 4px solid #d4a373;
        padding: 15px;
        margin-top: 30px;
        font-size: 0.9em;
        color: #555;
        border-radius: 4px;
    }
    .link-loja {
        text-decoration: none;
        background-color: #d4a373;
        color: white !important;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
    .link-loja:hover {
        background-color: #bc8f5b;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Carregamento dos Dados JSON
@st.cache_data
def carregar_dados():
    try:
        with open("dados_brinquedos.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Erro: O arquivo 'dados_brinquedos.json' não foi encontrado. Certifique-se de que ele está na mesma pasta do app.py.")
        return None

# 4. Interface Principal
def main():
    st.markdown("<h1 class='titulo-principal'>🌱 Helipê Ateliê Lúdico</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo'>Descubra o material ideal para nutrir a Mente Absorvente do seu bebê.</p>", unsafe_allow_html=True)

    dados = carregar_dados()
    if not dados:
        return

    # Formulário de Entrada
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            idade_input = st.number_input("Idade do bebê", min_value=0, max_value=52, value=3, step=1)
        with col2:
            unidade = st.selectbox("Medida", ["Meses", "Semanas"])

    # Botão de Busca
    if st.button("Buscar Sugestões"):
        # 5. Lógica de Conversão (Semanas para Meses)
        if unidade == "Semanas":
            meses_calculados = math.floor(idade_input / 4.345) # Média de semanas num mês
        else:
            meses_calculados = idade_input

        if meses_calculados > 12:
            st.warning("Este guia foca no primeiro ano de vida (0 a 12 meses), o período mais intenso da mente absorvente inconsciente.")
            return

        # 6. Busca no JSON
        recomendacoes = []
        for faixa in dados.get("faixas_etarias", []):
            if faixa["idade_min_meses"] <= meses_calculados <= faixa["idade_max_meses"]:
                recomendacoes = faixa["recomendacoes"]
                break

        # 7. Renderização dos Resultados
        if recomendacoes:
            st.success(f"Idade calculada: aproximadamente {meses_calculados} meses. Veja os materiais adequados para este momento:")
            
            for item in recomendacoes:
                st.markdown("---")
                st.subheader(item["titulo"])
                
                col_img, col_texto = st.columns([1, 2])
                
                with col_img:
                    # Tenta carregar a imagem, se falhar mostra um aviso amigável
                    try:
                        st.image(item["imagem_caminho"], use_container_width=True)
                    except:
                        st.info("Imagem do material")
                
                with col_texto:
                    st.write("**Apresentação Pedagógica:**")
                    st.write(item["atividade_descricao"])
                    st.write(f"⏱️ **Tempo de concentração esperado:** {item['tempo_duracao']}")
                    
                    st.markdown(f"<a href='{item['link_produto']}' target='_blank' class='link-loja'>Ver na loja online</a>", unsafe_allow_html=True)
            
            # 8. Disclaimer Baseado em "A Mente Absorvente"
            st.markdown("""
            <div class='disclaimer-montessori'>
                <strong>O Papel do Adulto Preparado:</strong><br>
                Segundo Maria Montessori em <em>"A Mente Absorvente"</em>, o bebê de 0 a 3 anos possui uma forma de inteligência inconsciente que absorve o ambiente como uma esponja. 
                A mão é o principal instrumento dessa inteligência. Nossa recomendação é que você prepare um ambiente seguro e ofereça o material para que o bebê o explore livremente. 
                Observe sem interromper: a verdadeira aprendizagem acontece no esforço contínuo e na repetição no ritmo único de cada criança.
            </div>
            """, unsafe_allow_html=True)
            
            # Botão de Nova Consulta
            if st.button("Fazer Nova Consulta"):
                st.rerun()
                
        else:
            st.info("Ainda estamos preparando os materiais perfeitos para esta exata fase no nosso catálogo.")

if __name__ == "__main__":
    main()
