"""
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
======================================================
Sistema multi-assessor com senhas individuais
VERSÃO ATUALIZADA - 24/10/2025
Usa APENAS aba "Base" do Excel

MELHORIAS DESTA VERSÃO:
- Selectbox para escolher fundo (texto em preto)
- Fundo selecionado aparece primeiro na lista com borda em destaque
- Valores aplicados vêm da coluna "Aplicação" do Excel
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import os

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Calendário Renda Mais - TAUARI",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# AUTENTICAÇÃO POR ASSESSOR
# ============================================

# Dicionário com os códigos e senhas dos assessores
ASSESSORES = {
    '21743': ('Andre Miyada', 'AM2025'),
    '22359': ('Giuliano Hissnauer Vieira', 'GHV2025'),
    '21685': ('Rudney Vicente de Araujo', 'RVA2025'),
    '31321': ('Adriana Ourique Giraldelli Miranda', 'AOGM2025'),
    '23496': ('Ana Carolina Falcao Nagoshi', 'ACFN2025'),
    '73735': ('Jeferson de Carvalho', 'JC2025'),
    '72197': ('Jose Eduardo Monteiro de Vasconcelos', 'JEMV2025'),
    '74644': ('Marcelo Fontes de Almeida', 'MFA2025'),
    '39586': ('Marco Antonio de Moraes', 'MAM2025'),
    '46857': ('Gustavo Aquila', 'GA2025'),
    '51594': ('Bruna Rafaela Teixeira Mateos', 'BRTM2025'),
    '91796': ('Jose Dy Carlos Bueno Chiroza', 'JDCBC2025'),
    '47104': ('Kamila Munhoz Adario', 'KMA2025'),
    '21635': ('Lucas Chede Garcia', 'LCG2025'),
    '24931': ('Paula Pellegrini Reimao', 'PPR2025'),
    '91476': ('Rafael Iran Gomes Januario', 'RIGJ2025'),
    '42596': ('Ricardo Salles de Godoy', 'RSG2025'),
    '67756': ('Vinicius Nunes Palacios', 'VNP2025'),
}

def validar_senha_assessor(codigo_assessor, senha):
    """
    Valida a senha do assessor
    
    Parâmetros:
    - codigo_assessor: código do assessor (string)
    - senha: senha informada (string)
    
    Retorna:
    - (True, nome_assessor) se válido
    - (False, None) se inválido
    """
    # Verifica se o código existe no dicionário
    if codigo_assessor not in ASSESSORES:
        return False, None
    
    # Pega o nome e senha esperada
    nome_assessor, senha_esperada = ASSESSORES[codigo_assessor]
    
    # Compara a senha
    if senha == senha_esperada:
        return True, nome_assessor
    return False, None

def verificar_autenticacao(df_base):
    """
    Tela de login por assessor
    Só permite acesso se o assessor tiver senha válida
    """
    
    # Inicializa as variáveis de sessão
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    if 'assessor_logado' not in st.session_state:
        st.session_state.assessor_logado = None
    if 'nome_assessor' not in st.session_state:
        st.session_state.nome_assessor = None
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'
    
    # Se não está autenticado, mostra a tela de login
    if not st.session_state.autenticado:
        st.markdown("""
        <style>
            .stApp {
                background: white;
            }
            .login-box {
                max-width: 450px;
                margin: 120px auto;
                padding: 40px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            }
            .login-titulo {
                text-align: center;
                color: #1e4d2b;
                margin-bottom: 30px;
            }
            .login-info {
                background: #e8f5e9;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #27ae60;
                margin-top: 20px;
                font-size: 12px;
                color: #2c3e50;
            }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Tenta carregar a logo (se existir)
            try:
                st.image("logo_tauari.png", width=350)
            except:
                st.markdown("<div style='text-align: center; padding: 20px;'><div style='background: #2d5a3d; color: white; padding: 40px; border-radius: 10px; font-size: 14px;'>📁 Salve a logo como 'logo_tauari.png'<br>na mesma pasta do código</div></div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="login-titulo">
                <h2 style='margin: 10px 0; font-size: 24px;'>Calendário Renda Mais - Tauari Investimentos</h2>
                <p style='color: #7f8c8d; font-size: 14px; margin-top: 15px;'>Acesso restrito por Assessor (uso interno) - Última atualização 24/10</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Formulário de login
            with st.form("login_form"):
                codigo_assessor = st.text_input(
                    "👤 Código do Assessor:",
                    placeholder="Coloque seu código, exemplo: 46857",
                    max_chars=10,
                    key="codigo_input"
                )
                
                senha_assessor = st.text_input(
                    "🔐 Senha do Assessor:",
                    type="password",
                    placeholder="Digite sua senha",
                    max_chars=20,
                    key="senha_input"
                )
                
                submitted = st.form_submit_button("🔓 Entrar", use_container_width=True)
                
                if submitted:
                    # Valida se os campos foram preenchidos
                    if not codigo_assessor or not senha_assessor:
                        st.error("❌ Preencha todos os campos!")
                    else:
                        # Valida a senha
                        valido, nome_assessor = validar_senha_assessor(codigo_assessor, senha_assessor)
                        if valido:
                            if df_base is not None:
                                # Prepara a coluna Assessor
                                df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
                                clientes_assessor = df_base[df_base['Assessor'] == str(codigo_assessor)]
                                
                                # Verifica se tem clientes
                                if clientes_assessor.empty:
                                    st.error(f"❌ Nenhum cliente encontrado para o Assessor {codigo_assessor}")
                                else:
                                    # Login bem-sucedido!
                                    st.session_state.autenticado = True
                                    st.session_state.assessor_logado = codigo_assessor
                                    st.session_state.nome_assessor = nome_assessor
                                    st.session_state.pagina_atual = 'sistema'
                                    st.success(f"✅ Bem-vindo, {nome_assessor}!")
                                    st.rerun()
                            else:
                                st.error("❌ Erro ao carregar a base de dados!")
                        else:
                            st.error("❌ Código ou senha incorretos!")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Botão para conhecer os fundos (sem login)
            if st.button("📚 Conheça os Fundos", key="btn_conhecer_fundos", use_container_width=True):
                st.session_state.pagina_atual = 'fundos'
                st.rerun()
            
            st.markdown("""
            <div class="login-info">
                <strong>ℹ️ Como acessar:</strong><br>
                • Digite seu código de assessor (apenas números)<br>
                • Digite sua senha pessoal<br>
                • Em caso de dúvidas: <strong>gustavo.aquila@tauariinvestimentos.com.br</strong>
            </div>
            """, unsafe_allow_html=True)
        
        st.stop()

# ============================================
# CSS - ESTILOS DA APLICAÇÃO
# ============================================

st.markdown("""
<style>
    /* Fundo branco da aplicação */
    .stApp {
        background: white !important;
    }
    
    /* Cabeçalho do sistema */
    .header-sistema {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        padding: 20px 40px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .titulo-principal {
        color: white;
        font-size: 28px;
        font-weight: bold;
        margin: 0;
        text-align: left;
    }
    
    .info-assessor {
        color: #e8f5e9;
        font-size: 14px;
        margin-top: 5px;
    }
    
    /* ESTILO DO SELECTBOX DE FUNDOS - TEXTO EM PRETO */
    .stSelectbox label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    /* Placeholder do selectbox em preto */
    .stSelectbox [data-baseweb="select"] > div {
        color: #000000 !important;
    }
    
    /* Texto selecionado em preto */
    .stSelectbox [data-baseweb="select"] > div > div {
        color: #000000 !important;
    }
    
    /* Seletor de cliente */
    .cliente-selector {
        background: white !important;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        border: 2px solid #27ae60;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        max-width: 400px;
    }
    
    .cliente-selector h3 {
        color: #1e4d2b !important;
        font-size: 14px !important;
        font-weight: bold;
        margin: 0 0 8px 0 !important;
        text-align: center;
    }
    
    /* Seletor de fundos */
    .fundo-selector {
        background: white !important;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        border: 2px solid #27ae60;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        max-width: 500px;
    }
    
    .fundo-selector h3 {
        color: #1e4d2b !important;
        font-size: 14px !important;
        font-weight: bold;
        margin: 0 0 8px 0 !important;
        text-align: center;
    }
    
    /* Altura mínima do selectbox */
    [data-baseweb="select"] {
        min-height: 40px !important;
    }
    
    /* Container principal */
    .container-principal {
        display: flex;
        gap: 20px;
        margin-top: 20px;
    }
    
    /* Caixas (boxes) */
    .box {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .box-titulo {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        margin: -20px -20px 20px -20px;
        text-align: center;
    }
    
    .box-conteudo {
        max-height: 600px;
        overflow-y: auto;
        padding-right: 10px;
    }
    
    /* Cards dos fundos */
    .fundo-card-container {
        margin-bottom: 15px;
    }
    
    .fundo-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-left: 5px solid #27ae60;
        border-radius: 8px;
        padding: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .fundo-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        border-color: #27ae60;
    }
    
    /* CARD DO FUNDO SELECIONADO - COM BORDA EM DESTAQUE */
    .fundo-card-selecionado {
        border: 4px solid #27ae60 !important;
        background: #f0f9f4 !important;
        box-shadow: 0 6px 20px rgba(39, 174, 96, 0.3) !important;
        transform: scale(1.02);
    }
    
    .fundo-card .nome {
        font-weight: bold;
        color: #1e4d2b;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .fundo-card .info {
        font-size: 12px;
        color: #555;
        line-height: 1.6;
    }
    
    .fundo-card .valor {
        color: #27ae60;
        font-weight: bold;
    }
    
    /* Texto da tese do fundo */
    .tese-texto {
        padding: 15px;
        background: #f8f9fa;
        border-radius: 8px;
        font-size: 13px;
        line-height: 1.7;
        color: #2c3e50;
    }
    
    .tese-texto h4 {
        color: #1e4d2b;
        font-size: 14px;
        margin-top: 15px;
        margin-bottom: 8px;
        font-weight: bold;
    }
    
    .tese-texto strong {
        font-size: 15px;
        display: block;
        margin-bottom: 10px;
    }
    
    /* Calendário */
    .calendario-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 8px;
        padding: 15px;
        background: white;
    }
    
    .cal-header {
        background: #1e4d2b;
        color: white;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 12px;
        border-radius: 5px;
        text-transform: uppercase;
    }
    
    .cal-dia {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 8px;
        min-height: 80px;
        transition: all 0.2s;
    }
    
    .cal-dia:hover {
        background: #f0f9f4;
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .cal-dia.fim-semana {
        background: #f8f9fa;
    }
    
    .cal-dia .numero {
        font-weight: bold;
        color: #1e4d2b;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    .cal-evento {
        background: #27ae60;
        color: white;
        padding: 3px 6px;
        border-radius: 4px;
        font-size: 10px;
        margin-top: 3px;
        font-weight: bold;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Botões */
    .stButton button {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
    }
    
    /* Scrollbar personalizada */
    .box-conteudo::-webkit-scrollbar {
        width: 8px;
    }
    
    .box-conteudo::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .box-conteudo::-webkit-scrollbar-thumb {
        background: #27ae60;
        border-radius: 10px;
    }
    
    .box-conteudo::-webkit-scrollbar-thumb:hover {
        background: #1e4d2b;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FERIADOS NACIONAIS
# ============================================

def gerar_feriados(ano):
    """
    Gera lista de feriados nacionais do Brasil para um ano específico
    """
    feriados = [
        date(ano, 1, 1),   # Ano Novo
        date(ano, 4, 21),  # Tiradentes
        date(ano, 5, 1),   # Dia do Trabalho
        date(ano, 9, 7),   # Independência
        date(ano, 10, 12), # Nossa Senhora Aparecida
        date(ano, 11, 2),  # Finados
        date(ano, 11, 15), # Proclamação da República
        date(ano, 12, 25), # Natal
    ]
    return feriados

# ============================================
# CÁLCULO DE DIA ÚTIL
# ============================================

def calcular_dia_util(ano, mes, dia_util_alvo, feriados):
    """
    Calcula qual é a data do N-ésimo dia útil do mês
    
    Exemplo: dia_util_alvo = 5 significa o 5º dia útil do mês
    """
    # Primeiro dia do mês
    data_atual = date(ano, mes, 1)
    dias_uteis_contados = 0
    
    # Enquanto não encontrar o dia útil desejado
    while dias_uteis_contados < dia_util_alvo:
        # Se for dia da semana (seg-sex) e não for feriado
        if data_atual.weekday() < 5 and data_atual not in feriados:
            dias_uteis_contados += 1
            # Se chegou no dia útil desejado, retorna a data
            if dias_uteis_contados == dia_util_alvo:
                return data_atual
        
        # Avança para o próximo dia
        data_atual += timedelta(days=1)
        
        # Se passar para o próximo mês, retorna None
        if data_atual.month != mes:
            return None
    
    return None

# ============================================
# MESES EM PORTUGUÊS
# ============================================

MESES_PT = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

# ============================================
# MAPAS DE INFORMAÇÕES DOS FUNDOS
# ============================================

# Mapa de dias úteis de pagamento (qual dia útil do mês o fundo paga)
MAPA_PAGAMENTOS = {
    'ARX FII Portfólio Renda CDI+ RL': 5,
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 5,
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 5,
    'AZ Quest Panorama Renda CDI FI RL': 5,
    'BGR Galpões Logísticos - Cota Sênior': 7,
    'BGR Galpões Logísticos - Cota Subordinada': 7,
    'Maua Lajes Corporativas Feeder FII RL - Senior': 7,
    'SPX CRI Portfolio Renda Mais': 5,
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': 5,
    'XP Renda Imobiliária Feeder FII RL': 5,
    'XP Habitat Renda Imobiliária Feeder FII': 5,
    'Valora CRI CDI Renda+ FII RL': 5,
}

# Mapa de cores dos fundos (para identificação visual)
MAPA_CORES = {
    'ARX FII Portfólio Renda CDI+ RL': '#e74c3c',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': '#3498db',
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': '#9b59b6',
    'AZ Quest Panorama Renda CDI FI RL': '#9b59b6',
    'BGR Galpões Logísticos - Cota Sênior': '#f39c12',
    'BGR Galpões Logísticos - Cota Subordinada': '#d35400',
    'Maua Lajes Corporativas Feeder FII RL - Senior': '#1abc9c',
    'SPX CRI Portfolio Renda Mais': '#34495e',
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': '#16a085',
    'XP Renda Imobiliária Feeder FII RL': '#27ae60',
    'XP Habitat Renda Imobiliária Feeder FII': '#2ecc71',
    'Valora CRI CDI Renda+ FII RL': '#e67e22',
}

# Mapa de siglas dos fundos (para o calendário)
MAPA_SIGLAS = {
    'ARX FII Portfólio Renda CDI+ RL': 'ARX',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 'AZ Infra',
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 'AZ Pan',
    'AZ Quest Panorama Renda CDI FI RL': 'AZ Pan',
    'BGR Galpões Logísticos - Cota Sênior': 'BGR Sr',
    'BGR Galpões Logísticos - Cota Subordinada': 'BGR Sub',
    'Maua Lajes Corporativas Feeder FII RL - Senior': 'Maua',
    'SPX CRI Portfolio Renda Mais': 'SPX',
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': 'Solis',
    'XP Renda Imobiliária Feeder FII RL': 'XP Renda',
    'XP Habitat Renda Imobiliária Feeder FII': 'XP Hab',
    'Valora CRI CDI Renda+ FII RL': 'Valora',
}

# Mapa de teses de investimento dos fundos
MAPA_TESES = {
    'ARX FII Portfólio Renda CDI+ RL': {
        'resumo': 'Fundo focado em CRIs com rentabilidade atrelada ao CDI, gestão da ARX.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio/Longo prazo
• Liquidez: D+30
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Fundo de CRIs que busca rentabilidade acima do CDI com baixa volatilidade.',
        'perfil': 'Investidores que buscam renda passiva com proteção do CDI.'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'resumo': 'Fundo de infraestrutura com foco em ativos reais e renda previsível.',
        'condicoes': '''• Rentabilidade: IPCA + spread
• Prazo: Longo prazo (5-7 anos)
• Liquidez: Baixa (prazo determinado)
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Investe em infraestrutura brasileira gerando renda atrelada à inflação.',
        'perfil': 'Investidores de longo prazo que buscam proteção inflacionária.'
    },
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': {
        'resumo': 'Fundo imobiliário com estratégia diversificada e rentabilidade atrelada ao CDI.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio prazo
• Liquidez: D+30 a D+60
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Fundo de tijolo e papel que busca rentabilidade superior ao CDI.',
        'perfil': 'Investidores que buscam diversificação imobiliária com renda CDI+.'
    },
    'AZ Quest Panorama Renda CDI FI RL': {
        'resumo': 'Fundo imobiliário com estratégia diversificada e rentabilidade atrelada ao CDI.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio prazo
• Liquidez: D+30 a D+60
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Fundo de tijolo e papel que busca rentabilidade superior ao CDI.',
        'perfil': 'Investidores que buscam diversificação imobiliária com renda CDI+.'
    },
    'BGR Galpões Logísticos - Cota Sênior': {
        'resumo': 'Fundo focado em galpões logísticos com estrutura sênior.',
        'condicoes': '''• Rentabilidade: IPCA + spread
• Prazo: Médio/Longo prazo
• Liquidez: D+60
• Público-alvo: Investidores qualificados
• Prioridade no recebimento''',
        'venda_1min': 'Investe em galpões logísticos com preferência no recebimento de rendimentos.',
        'perfil': 'Investidores conservadores que buscam renda com segurança.'
    },
    'BGR Galpões Logísticos - Cota Subordinada': {
        'resumo': 'Fundo focado em galpões logísticos com estrutura subordinada.',
        'condicoes': '''• Rentabilidade: IPCA + spread maior
• Prazo: Médio/Longo prazo
• Liquidez: D+60
• Público-alvo: Investidores qualificados
• Maior risco e retorno''',
        'venda_1min': 'Investe em galpões logísticos com potencial de retorno superior.',
        'perfil': 'Investidores que aceitam maior risco para buscar maior retorno.'
    },
    'Maua Lajes Corporativas Feeder FII RL - Senior': {
        'resumo': 'Fundo focado em lajes corporativas com estrutura sênior.',
        'condicoes': '''• Rentabilidade: IPCA + spread
• Prazo: Médio/Longo prazo
• Liquidez: D+60
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Investe em lajes corporativas AAA com prioridade no recebimento.',
        'perfil': 'Investidores que buscam renda previsível em imóveis corporativos.'
    },
    'SPX CRI Portfolio Renda Mais': {
        'resumo': 'Fundo de CRIs com gestão SPX Capital focado em renda.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio prazo
• Liquidez: D+30
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Portfolio de CRIs selecionados pela SPX Capital.',
        'perfil': 'Investidores que buscam renda através de crédito imobiliário.'
    },
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': {
        'resumo': 'Fundo de crédito com rentabilidade atrelada ao CDI.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Curto/Médio prazo
• Liquidez: D+30
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Fundo de crédito diversificado que busca rentabilidade acima do CDI.',
        'perfil': 'Investidores que buscam renda em crédito privado.'
    },
    'XP Renda Imobiliária Feeder FII RL': {
        'resumo': 'Fundo feeder que investe em fundos imobiliários de renda.',
        'condicoes': '''• Rentabilidade: Renda variável
• Prazo: Médio/Longo prazo
• Liquidez: D+30
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Acesso a portfolio diversificado de fundos imobiliários.',
        'perfil': 'Investidores que buscam diversificação em FIIs.'
    },
    'XP Habitat Renda Imobiliária Feeder FII': {
        'resumo': 'Fundo feeder focado em imóveis residenciais para renda.',
        'condicoes': '''• Rentabilidade: Renda variável
• Prazo: Médio/Longo prazo
• Liquidez: D+30
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Investe em fundos imobiliários focados no setor residencial.',
        'perfil': 'Investidores que buscam exposição ao mercado residencial.'
    },
    'Valora CRI CDI Renda+ FII RL': {
        'resumo': 'Fundo imobiliário focado em CRIs com rentabilidade atrelada ao CDI.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio/Longo prazo
• Liquidez: D+30 a D+60
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Fundo de CRIs que busca rentabilidade acima do CDI com gestão profissional.',
        'perfil': 'Investidores que buscam renda através de CRIs com retornos superiores ao CDI.'
    }
}

# Mapa de links dos fundos (Expert XP e Material Publicitário)
MAPA_LINKS = {
    'ARX FII Portfólio Renda CDI+ RL': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/dezembro-24-arx-fii-portfolio-renda-cdi-rl/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2024/11/Material-Publicitario-1a-Emissao-ARX-Portfolio-Renda-CDI_vf.pdf'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/marco-25-az-quest-renda-mais/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/03/AZQI-RENDA_Material-Publicitario-vf-26_03.pdf'
    },
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/agosto-25-1a-emissao-az-quest-panorama-renda-cdi-fii-portfolio-renda-mais-fii-prazo-determinado/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2021/01/AZ-Quest-Panorama_MP-VF-1.pdf'
    },
    'AZ Quest Panorama Renda CDI FI RL': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/agosto-25-1a-emissao-az-quest-panorama-renda-cdi-fii-portfolio-renda-mais-fii-prazo-determinado/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2021/01/AZ-Quest-Panorama_MP-VF-1.pdf'
    },
    'BGR Galpões Logísticos - Cota Sênior': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/outubro-25-1a-emissao-bgr-galpoes-logisticos-cota-senior-fii/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/10/MP-FII-BGR-GL-FEEDER-17.10.pdf'
    },
    'BGR Galpões Logísticos - Cota Subordinada': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/outubro-25-1a-emissao-bgr-galpoes-logisticos-cota-subordinada-fii/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/10/MP-FII-BGR-GL-MASTER.pdf'
    },
    'Maua Lajes Corporativas Feeder FII RL - Senior': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/agosto-25-2a-emissao-aaaaa-fundo-de-investimento-imobiliario-responsabilidade-limitada-subclasse-a-e-b-prazo-determinado/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2021/01/MP_MAUA_LAJES_SENIOR_MCLC-2.pdf'
    },
    'SPX CRI Portfolio Renda Mais': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/janeiro-25-spx-capital-portfolio-renda/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/01/Apresentacao-SPX-Capital-FII-Portfolio-Renda-I-Final.pdf'
    },
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/fevereiro-25-solis-portfolio-credito/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/01/Material-Publicitario_FIC-FIDC-SOLIS_v.divulgacao.pdf'
    },
    'XP Renda Imobiliária Feeder FII RL': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/julho-25-1a-emissao-fundo-de-investimento-imobiliario-xp-renda-imobiliaria-feeder-fii-portfolio-renda/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/07/IPO-XP-Renda-Imobiliaria-vf-07.07.pdf'
    },
    'XP Habitat Renda Imobiliária Feeder FII': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/agosto-25-1a-emissao-xp-habitat-renda-imobiliaria-feeder-fii-portfolio-renda/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2021/01/MP-XP-Habitat-Renda-Imobiliaria-FII_vf-2.pdf'
    },
    'Valora CRI CDI Renda+ FII RL': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/junho-25-1a-emissao-valora-cri-cdi-renda-mais-fundo-de-investimento-imobiliario-fii-portfolio-renda/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/05/Material-Publicitario-1a-Emissao-Valora-CRI-CDI-Renda-Mais-FII-10_06.pdf'
    }
}

def buscar_info_fundo(nome_fundo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses):
    """
    Busca todas as informações de um fundo nos mapas
    
    Retorna um dicionário com:
    - dia_util: dia útil de pagamento
    - cor: cor do fundo
    - sigla: sigla abreviada
    - tese: tese de investimento
    - links: links do Expert XP e Material
    """
    return {
        'dia_util': mapa_pagamentos.get(nome_fundo, 0),
        'cor': mapa_cores.get(nome_fundo, '#27ae60'),
        'sigla': mapa_siglas.get(nome_fundo, nome_fundo[:10]),
        'tese': mapa_teses.get(nome_fundo, {
            'resumo': 'Informações não disponíveis',
            'condicoes': 'N/A',
            'venda_1min': 'N/A',
            'perfil': 'N/A'
        }),
        'links': MAPA_LINKS.get(nome_fundo, {'expert': '', 'material': ''})
    }

# ============================================
# TELA DE FUNDOS (PÚBLICA)
# ============================================

def tela_fundos():
    """
    Tela de apresentação dos fundos (pode ser acessada sem login)
    """
    
    st.markdown("""
    <div style="text-align: center; padding: 30px;">
        <h1 style="color: #1e4d2b; font-size: 36px; margin-bottom: 10px;">
            📚 Materiais e Conteúdos
        </h1>
        <p style="color: #7f8c8d; font-size: 16px;">
            Conheça nossos fundos e acesse materiais exclusivos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("🔙 Voltar ao Login", use_container_width=True):
            st.session_state.pagina_atual = 'login'
            st.rerun()
    
    with col2:
        # Selectbox para navegar rapidamente aos fundos
        fundos_lista = sorted(MAPA_TESES.keys())
        fundo_selecionado = st.selectbox(
            "🎯 Ir para o fundo:",
            ["Selecione um fundo..."] + fundos_lista,
            key="nav_fundo"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Lista todos os fundos
    for fundo_nome in sorted(MAPA_TESES.keys()):
        info = buscar_info_fundo(fundo_nome, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
        tese = info['tese']
        links = info['links']
        
        fundo_id = fundo_nome.replace(" ", "_")
        
        st.markdown(f"""
        <div id="{fundo_id}" style="background: white; border: 2px solid {info['cor']}; border-left: 6px solid {info['cor']}; 
                    border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
            <h3 style="color: {info['cor']}; margin-bottom: 15px; font-size: 20px;">
                {fundo_nome}
            </h3>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <p style="margin-bottom: 10px; color: #000000;"><strong style="color: #000000;">📝 Resumo:</strong> {tese['resumo']}</p>
                <p style="margin-bottom: 10px; color: #000000;"><strong style="color: #000000;">📋 Condições:</strong></p>
                <p style="white-space: pre-line; margin-left: 15px; font-size: 14px; color: #000000;">{tese['condicoes']}</p>
                <p style="margin-bottom: 10px; color: #000000;"><strong style="color: #000000;">⚡ Venda em 1 Minuto:</strong> {tese['venda_1min']}</p>
                <p style="margin-bottom: 0; color: #000000;"><strong style="color: #000000;">🎯 Perfil do Cliente:</strong> {tese['perfil']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if links['material']:
                st.markdown(f"""
                <a href="{links['material']}" target="_blank" style="text-decoration: none;">
                    <button style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                                   color: white; border: none; padding: 12px 20px; border-radius: 8px; 
                                   font-weight: bold; cursor: pointer; width: 100%; font-size: 14px;">
                        📄 Material Publicitário
                    </button>
                </a>
                """, unsafe_allow_html=True)
        
        with col2:
            if links['expert']:
                st.markdown(f"""
                <a href="{links['expert']}" target="_blank" style="text-decoration: none;">
                    <button style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                                   color: white; border: none; padding: 12px 20px; border-radius: 8px; 
                                   font-weight: bold; cursor: pointer; width: 100%; font-size: 14px;">
                        🎓 Expert XP
                    </button>
                </a>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# CARREGAR DADOS - APENAS ABA BASE
# ============================================

@st.cache_data
def carregar_dados():
    """
    Carrega dados APENAS da aba Base do Excel
    
    A aba "Base" contém:
    - Assessor: código do assessor
    - Cliente: código do cliente
    - Ativo: nome do fundo
    - Aplicação: valor aplicado (usado como "Valor Aplicado")
    - Rendimento %: percentual de rendimento líquido
    """
    try:
        # Lê o arquivo Excel (certifique-se que está na mesma pasta)
        df_base = pd.read_excel('calendario_Renda_mais.xlsx', sheet_name='Base')
        return df_base
    except Exception as e:
        st.error(f"❌ Erro ao carregar Excel: {str(e)}")
        st.stop()

# ============================================
# FUNÇÃO PRINCIPAL DO SISTEMA
# ============================================

def main():
    """
    Função principal que controla o fluxo do sistema
    """
    
    # Carrega os dados do Excel
    df_base = carregar_dados()
    
    # Inicializa a variável de página atual
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'
    
    # Se está na página de fundos, mostra essa página
    if st.session_state.pagina_atual == 'fundos':
        tela_fundos()
        return
    
    # Verifica se o usuário está autenticado
    verificar_autenticacao(df_base)
    
    # Gera feriados do ano atual
    feriados = gerar_feriados(datetime.now().year)
    
    # ============================================
    # CABEÇALHO DO SISTEMA
    # ============================================
    
    st.markdown(f"""
    <div class="header-sistema">
        <div class="titulo-principal">📅 Calendário Renda Mais - Tauari Investimentos</div>
        <div class="info-assessor">
            👤 Assessor: <strong>{st.session_state.nome_assessor}</strong> | 
            Código: <strong>{st.session_state.assessor_logado}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botões de ação
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        if st.button("🔓 Sair", key="btn_sair"):
            st.session_state.autenticado = False
            st.session_state.assessor_logado = None
            st.session_state.nome_assessor = None
            st.session_state.pagina_atual = 'login'
            st.rerun()
    
    with col2:
        if st.button("📚 Ver Fundos", key="btn_ver_fundos"):
            st.session_state.pagina_atual = 'fundos'
            st.rerun()
    
    # ============================================
    # FILTRAR DADOS DO ASSESSOR
    # ============================================
    
    # Prepara a coluna Assessor (remove espaços)
    df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
    
    # Filtra apenas os clientes deste assessor
    df_base_filtrado = df_base[df_base['Assessor'] == str(st.session_state.assessor_logado)]
    
    if df_base_filtrado.empty:
        st.error("❌ Nenhum cliente encontrado!")
        st.stop()
    
    # ============================================
    # SELETOR DE CLIENTE
    # ============================================
    
    st.markdown('<div class="cliente-selector"><h3>👥 SELECIONE O CLIENTE</h3>', unsafe_allow_html=True)
    
    # Lista de clientes (ordenada)
    clientes = sorted(df_base_filtrado['Cliente'].unique())
    cliente_selecionado = st.selectbox(
        "Cliente", 
        [""] + list(clientes),  # Opção vazia no início
        label_visibility="collapsed", 
        key="cliente_select"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Se nenhum cliente foi selecionado, para aqui
    if not cliente_selecionado:
        st.stop()
    
    # Filtra os fundos deste cliente
    fundos_cliente = df_base_filtrado[df_base_filtrado['Cliente'] == cliente_selecionado]

    # ============================================
    # SELETOR DE FUNDO (NOVO!)
    # ============================================
    
    # Inicializa o fundo selecionado
    if 'fundo_selecionado' not in st.session_state:
        st.session_state.fundo_selecionado = fundos_cliente['Ativo'].iloc[0] if not fundos_cliente.empty else None
    
    st.markdown('<div class="fundo-selector"><h3>🎯 ESCOLHA SEU FUNDO</h3>', unsafe_allow_html=True)
    
    # Lista de fundos do cliente (ordenada)
    fundos_disponiveis = sorted(fundos_cliente['Ativo'].unique())
    
    # Selectbox para escolher o fundo (com texto em preto via CSS)
    fundo_escolhido = st.selectbox(
        "Escolha seu fundo",  # Este texto ficará em preto pelo CSS
        ["Escolha seu fundo"] + fundos_disponiveis,
        label_visibility="collapsed",
        key="fundo_select"
    )
    
    # Se um fundo foi escolhido, atualiza a seleção
    if fundo_escolhido != "Escolha seu fundo":
        st.session_state.fundo_selecionado = fundo_escolhido
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # LAYOUT PRINCIPAL (3 COLUNAS)
    # ============================================
    
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    # ============================================
    # COLUNA 1: FUNDOS DO CLIENTE
    # ============================================
    
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        # ORDENAR FUNDOS: SELECIONADO PRIMEIRO
        fundos_ordenados = []
        fundo_selecionado_atual = st.session_state.fundo_selecionado
        
        # Primeiro, adiciona o fundo selecionado (se houver)
        if fundo_selecionado_atual:
            fundo_sel = fundos_cliente[fundos_cliente['Ativo'] == fundo_selecionado_atual]
            if not fundo_sel.empty:
                fundos_ordenados.append(fundo_sel.iloc[0])
        
        # Depois, adiciona os outros fundos
        for _, fundo in fundos_cliente.iterrows():
            if fundo['Ativo'] != fundo_selecionado_atual:
                fundos_ordenados.append(fundo)
        
        # Mostra cada fundo
        for fundo in fundos_ordenados:
            ativo = fundo['Ativo']
            
            # PEGA O VALOR APLICADO DA COLUNA "Aplicação" DO EXCEL
            try:
                valor_aplicado = float(fundo['Aplicação'])
            except:
                valor_aplicado = 0.0
            
            # Pega o percentual de rendimento
            try:
                percentual_liquido = float(fundo['Rendimento %'])
            except:
                percentual_liquido = 0.0
            
            # Calcula o valor líquido do cupom
            valor_liquido_cupom = valor_aplicado * percentual_liquido
            
            # Busca informações do fundo
            info = buscar_info_fundo(ativo, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
            
            # Calcula a data de pagamento
            data_pagamento = None
            dia_util = info.get('dia_util')
            
            if dia_util and dia_util > 0:
                try:
                    data_pagamento = calcular_dia_util(
                        st.session_state.ano_atual, 
                        st.session_state.mes_atual, 
                        dia_util, 
                        feriados
                    )
                except:
                    pass
            
            data_texto = data_pagamento.strftime("%d/%m/%Y") if data_pagamento else "Não definida"
            
            # Define a classe CSS (se está selecionado)
            classe_selecao = 'fundo-card-selecionado' if ativo == st.session_state.fundo_selecionado else ''
            
            # Mostra o card do fundo
            st.markdown(f"""
            <div class="fundo-card-container">
                <div class="fundo-card {classe_selecao}" style="border-left-color: {info.get('cor', '#27ae60')}">
                    <div class="nome">{ativo}</div>
                    <div class="info" style="margin-top: 8px;">
                        <div style="margin-bottom: 4px;">💰 <strong>Valor Aplicado:</strong> <span class="valor">R$ {valor_aplicado:,.2f}</span></div>
                        <div style="margin-bottom: 4px;">📅 <strong>Data Pagamento:</strong> {data_texto}</div>
                        <div style="margin-bottom: 4px;">📈 <strong>% Líquido:</strong> <span class="valor">{percentual_liquido:.2f}%</span></div>
                        <div>💵 <strong>Valor Líquido:</strong> <span class="valor">R$ {valor_liquido_cupom:,.2f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Botão para selecionar o fundo
            if st.button("📊", key=f"sel_{ativo}", help=f"Selecionar {ativo}"):
                st.session_state.fundo_selecionado = ativo
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ============================================
    # COLUNA 2: TESE DO FUNDO
    # ============================================
    
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        if st.session_state.fundo_selecionado:
            # Busca a tese do fundo selecionado
            info = buscar_info_fundo(st.session_state.fundo_selecionado, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
            tese = info.get('tese', {})
            
            # Mostra a tese
            st.markdown(f"""
            <div class="tese-texto">
                <strong style="color: {info.get('cor', '#27ae60')};">{st.session_state.fundo_selecionado}</strong>
                <p>{tese.get('resumo', '')}</p>
                <h4>📋 Resumo de Condições</h4>
                <p style="white-space: pre-line;">{tese.get('condicoes', '')}</p>
                <h4>⚡ Venda em 1 Minuto</h4>
                <p>{tese.get('venda_1min', '')}</p>
                <h4>🎯 Perfil do Cliente</h4>
                <p>{tese.get('perfil', '')}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="tese-texto"><p>Selecione um fundo.</p></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # COLUNA 3: CALENDÁRIO
    # ============================================
    
    with col3:
        st.markdown('<div class="box"><div class="box-titulo">📅 CALENDÁRIO</div>', unsafe_allow_html=True)
        
        # Inicializa mês e ano atual
        if 'mes_atual' not in st.session_state:
            st.session_state.mes_atual = datetime.now().month
            st.session_state.ano_atual = datetime.now().year
        
        # Botões de navegação do calendário
        col_p1, col_p2, col_p3 = st.columns([1, 3, 1])
        
        with col_p1:
            if st.button("◀ Anterior", key="prev_mes"):
                st.session_state.mes_atual -= 1
                if st.session_state.mes_atual < 1:
                    st.session_state.mes_atual = 12
                    st.session_state.ano_atual -= 1
                st.rerun()
        
        with col_p2:
            st.markdown(f'<div style="text-align: center; padding: 8px; font-size: 18px; font-weight: bold; color: #1e4d2b;">{MESES_PT[st.session_state.mes_atual-1]} {st.session_state.ano_atual}</div>', unsafe_allow_html=True)
        
        with col_p3:
            if st.button("Próximo ▶", key="next_mes"):
                st.session_state.mes_atual += 1
                if st.session_state.mes_atual > 12:
                    st.session_state.mes_atual = 1
                    st.session_state.ano_atual += 1
                st.rerun()
        
        # Gera o calendário do mês
        cal = calendar.monthcalendar(st.session_state.ano_atual, st.session_state.mes_atual)
        
        # Cabeçalho dos dias da semana
        dias_semana = ['seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.', 'dom.']
        html_cal = '<div class="calendario-grid">'
        
        for dia in dias_semana:
            html_cal += f'<div class="cal-header">{dia}</div>'
        
        # Coleta eventos do mês (datas de pagamento dos fundos)
        eventos_mes = {}
        for _, fundo in fundos_cliente.iterrows():
            info = buscar_info_fundo(fundo['Ativo'], MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
            
            dia_util = info.get('dia_util')
            if dia_util and dia_util > 0:
                try:
                    data_pagamento = calcular_dia_util(st.session_state.ano_atual, st.session_state.mes_atual, dia_util, feriados)
                    if data_pagamento:
                        dia = data_pagamento.day
                        if dia not in eventos_mes:
                            eventos_mes[dia] = []
                        eventos_mes[dia].append({
                            'sigla': info.get('sigla', fundo['Ativo'][:10]), 
                            'cor': info.get('cor', '#27ae60')
                        })
                except:
                    pass
        
        # Gera os dias do calendário
        for semana in cal:
            for dia in semana:
                if dia == 0:
                    # Dia vazio (fora do mês)
                    html_cal += '<div class="cal-dia" style="background: #f8f9fa;"></div>'
                else:
                    # Dia válido
                    data = date(st.session_state.ano_atual, st.session_state.mes_atual, dia)
                    classe = "cal-dia fim-semana" if data.weekday() >= 5 else "cal-dia" 
                    
                    # Eventos deste dia
                    eventos_html = ""
                    if dia in eventos_mes:
                        for evento in eventos_mes[dia]:
                            eventos_html += f'<div class="cal-evento" style="background: {evento["cor"]}">{evento["sigla"]}</div>'
                    
                    html_cal += f'<div class="{classe}"><div class="numero">{dia}</div>{eventos_html}</div>'
        
        html_cal += '</div>'
        st.markdown(html_cal, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# EXECUÇÃO DO PROGRAMA
# ============================================

if __name__ == "__main__":
    main()
