import streamlit as st
import json
import math

# 1. Configurações Iniciais da Página
st.set_page_config(
    page_title="Guia Sensorial - Helipê Ateliê Lúdico",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Conexão PWA, Customização CSS e Banner de Instalação
st.markdown("""
    <link rel="manifest" href="manifest.json">
    <style>
    /* Esconde o menu do Streamlit e o rodapé para parecer app nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ajuste para remover espaços desnecessários e ficar em tela cheia */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }

    /* Estilo dos Botões */
    .stButton>button {
        background-color: #A3B18A;
        color: white;
        border-radius: 8px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #588157;
        color: white;
    }
    
    /* Estilo do Disclaimer */
    .disclaimer-box {
        background-color: #F4F1DE;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #E07A5F;
        margin-bottom: 20px;
    }
    
    /* Banner de Instalação (Visível apenas em telas menores/celulares) */
    .install-banner {
        display: none;
        background-color: #E07A5F;
        color: white;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 0.9em;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    @media (max-width: 768px) {
        .install-banner {
            display: block;
        }
    }
    </style>
    
    <div class="install-banner">
        📲 Dica: Tenha o Guia sempre à mão! Toque em 'Compartilhar' no navegador e escolha 'Adicionar à Tela de Início'.
    </div>
""", unsafe_allow_html=True)

# 3. Carregamento dos Dados JSON
@st.cache_data
def carregar_dados():
    try:
        with open('dados_brinquedos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Arquivo dados_brinquedos.json não encontrado. Verifique o diretório.")
        return None

dados = carregar_dados()

# 4. Cabeçalho
try:
    st.image("assets/img/logo_helipe.png", use_container_width=True)
except:
    st.warning("Logo em carregamento...")

st.title("52 Semanas de Descobertas")
st.markdown("O Guia Sensorial da Mente Absorvente para o primeiro ano do seu bebê.")
st.divider()

# 5. Inputs do Usuário
col1, col2 = st.columns(2)

with col1:
    idade_input = st.number_input("Idade do bebê:", min_value=1, max_value=52, value=1, step=1)

with col2:
    unidade_input = st.selectbox("Medida em:", ["Semanas", "Meses"])

# 6. Lógica de Conversão (Meses para Semanas)
semana_calculada = idade_input

if unidade_input == "Meses":
    # 1 mês tem em média 4.34 semanas. Limitamos a 52 semanas (1 ano).
    semana_calculada = math.ceil(idade_input * 4.34)
    if semana_calculada > 52:
        semana_calculada = 52
    st.caption(f"💡 {idade_input} meses correspondem aproximadamente à semana {semana_calculada}.")

# 7. Lógica de Busca no JSON e Renderização
if dados:
    faixa_encontrada = None
    
    # Localiza o bloco do mês correspondente
    for faixa in dados.get("faixas_etarias", []):
        if faixa["semana_min"] <= semana_calculada <= faixa["semana_max"]:
            faixa_encontrada = faixa
            break

    if faixa_encontrada:
        st.subheader(f"✨ Fase Atual: {faixa_encontrada['tema_fase']}")
        st.write(f"Recomendações baseadas no **{faixa_encontrada['mes_referencia']}** (Semanas {faixa_encontrada['semana_min']} a {faixa_encontrada['semana_max']}).")
        
        # Filtra atividades da semana exata ou traz todas do período se não houver especificidade
        atividades_semana = [
            rec for rec in faixa_encontrada.get("recomendacoes", []) 
            if rec.get("semana_especifica") == semana_calculada or rec.get("semana_especifica") is None
        ]

        if not atividades_semana:
            # Fallback: exibe todas do mês se não tiver uma específica para a semana
            atividades_semana = faixa_encontrada.get("recomendacoes", [])

        st.divider()

        # Renderiza os cards de atividades
        for item in atividades_semana:
            col_img, col_txt = st.columns([1, 2])
            
            with col_img:
                try:
                    st.image(item["imagem_caminho"], use_container_width=True)
                except:
                    # Imagem de fallback caso a original não esteja na pasta
                    st.image("https://via.placeholder.com/300x300.png?text=Em+Breve", use_container_width=True)
            
            with col_txt:
                st.markdown(f"### {item['titulo']}")
                st.markdown(f"**Como fazer:** {item['atividade_descricao']}")
                st.markdown(f"⏱️ **Tempo sugerido:** {item['tempo_duracao']}")
                
                # Botão de Compra se houver link de produto
                if item.get("link_produto"):
                    st.link_button("Ver Produto no Ateliê", item["link_produto"])
                
            st.divider()

        # Selo de Qualidade e Disclaimer
        st.markdown("""
        <div class="disclaimer-box">
            <strong>Qualidade Helipê:</strong> Nossos materiais são artesanais, finalizados com óleo de tungue puro e fios 100% algodão, garantindo total segurança para a exploração tátil e oral do seu bebê.
        </div>
        """, unsafe_allow_html=True)

        st.info("🌱 Lembrete Pedagógico: Cada bebê possui um ritmo único de desenvolvimento. A Mente Absorvente floresce na repetição e sem pressão. Observe seu filho e siga o tempo dele.")

    else:
        st.warning("Ops! Não encontramos atividades cadastradas para essa idade. O guia cobre de 1 a 52 semanas.")

# 8. Rodapé com Link pra Loja Geral
st.markdown("<center>Quer conhecer a linha completa?</center>", unsafe_allow_html=True)
st.link_button("Visitar www.helipe.com.br", "https://www.helipe.com.br?utm_source=app_brinde&utm_medium=referral&utm_campaign=rodape")
