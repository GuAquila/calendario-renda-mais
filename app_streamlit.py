"""
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
======================================================
Sistema multi-assessor com senhas individuais
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import os

st.set_page_config(
    page_title="Calendário Renda Mais - TAUARI",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# AUTENTICAÇÃO POR ASSESSOR
# ============================================

# Dicionário com os dados dos assessores: código -> (nome, senha)
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
    '29871': ('Jonathan Francesco Barletta', 'JFB2025'),
    '97495': ('Luana Peres Ribeiro', 'LPR2025'),
    '90410': ('Marta Maria Acquisti Guarido', 'MMAG2025'),
    '46604': ('Roberto da Silva Junior', 'RSJ2025'),
    '51594': ('Bruna Rafaela Teixeira Mateos', 'BRTM2025'),
    '91796': ('Jose Dy Carlos Bueno Chiroza', 'JDCBC2025'),
    '47104': ('Kamila Munhoz Adario', 'KMA2025'),
    '21635': ('Lucas Chede Garcia', 'LCG2025'),
    '24931': ('Paula Pellegrini Reimao', 'PPR2025'),
    '91476': ('Rafael Iran Gomes Januario', 'RIGJ2025'),
    '42596': ('Ricardo Salles de Godoy', 'RSG2025'),
    '94296': ('Vanessa Alves Mattar Calfat', 'VAMC2025'),
    '67756': ('Vinicius Nunes Palacios', 'VNP2025'),
}

def validar_senha_assessor(codigo_assessor, senha):
    """
    Valida a senha do assessor usando o dicionário ASSESSORES
    A senha é formada pelas iniciais dos nomes + 2025
    Exemplo: Andre Miyada → AM2025
    """
    if codigo_assessor not in ASSESSORES:
        return False, None
    
    nome_assessor, senha_esperada = ASSESSORES[codigo_assessor]
    if senha == senha_esperada:
        return True, nome_assessor
    return False, None

def verificar_autenticacao(df_base):
    """Tela de login por assessor"""
    
    # Inicializar session_state se não existir
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    if 'assessor_logado' not in st.session_state:
        st.session_state.assessor_logado = None
    if 'nome_assessor' not in st.session_state:
        st.session_state.nome_assessor = None
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'
    
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
            .btn-conhecer-fundos {
                background: #3498db !important;
                color: white !important;
                border: none !important;
                padding: 10px 20px !important;
                border-radius: 5px !important;
                font-weight: 600 !important;
                font-size: 13px !important;
                cursor: pointer !important;
                width: 100% !important;
                margin-top: 15px !important;
                text-align: center !important;
            }
            .btn-conhecer-fundos:hover {
                background: #2980b9 !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="login-titulo">
                <h1 style='font-size: 60px; margin: 0;'>🌳</h1>
                <h2 style='margin: 10px 0;'>Calendário Renda Mais</h2>
                <h3 style='color: #7dcea0; margin: 0;'>TAUARI INVESTIMENTOS</h3>
                <p style='color: #7f8c8d; font-size: 14px; margin-top: 15px;'>Acesso Restrito por Assessor</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Campos de login
            codigo_assessor = st.text_input(
                "👤 Código do Assessor:",
                placeholder="Coloque seu código, exemplo: 46857",
                max_chars=10
            )
            
            senha_assessor = st.text_input(
                "🔐 Senha do Assessor:",
                type="password",
                placeholder="Digite sua senha",
                max_chars=20
            )
            
            if st.button("🔓 Entrar", use_container_width=True):
                if not codigo_assessor or not senha_assessor:
                    st.error("❌ Preencha todos os campos!")
                else:
                    valido, nome_assessor = validar_senha_assessor(codigo_assessor, senha_assessor)
                    if valido:
                        # Verificar se o assessor tem clientes na base ANTES de autenticar
                        if df_base is not None:
                            df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
                            clientes_assessor = df_base[df_base['Assessor'] == str(codigo_assessor)]
                            
                            if clientes_assessor.empty:
                                st.error(f"❌ Nenhum cliente encontrado para o Assessor {codigo_assessor}")
                                st.info("💡 Verifique se há clientes vinculados ao seu código na planilha")
                            else:
                                # Só autentica se tiver clientes
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
            
            # Botão para conhecer os fundos
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📚 Conheça os Fundos", key="btn_conhecer_fundos", use_container_width=True):
                st.session_state.pagina_atual = 'fundos'
                st.rerun()
            
            # Informações de ajuda
            st.markdown("""
            <div class="login-info">
                <strong>ℹ️ Como acessar:</strong><br>
                • Digite seu código de assessor (apenas números)<br>
                • Digite sua senha pessoal<br>
                • Em caso de dúvidas, entre em contato com o suporte
            </div>
            """, unsafe_allow_html=True)
        
        st.stop()

# ============================================
# CSS
# ============================================

st.markdown("""
<style>
    .stApp {
        background: white !important;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* CABEÇALHO */
    .header-verde {
        background: #1e4d2b;
        padding: 20px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .header-content {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .header-verde .logo {
        font-size: 50px;
    }
    
    .header-verde .texto h1 {
        color: white;
        font-size: 18px;
        font-weight: bold;
        margin: 0 0 5px 0;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .header-verde .texto h2 {
        color: #7dcea0;
        font-size: 15px;
        font-weight: 600;
        margin: 0;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .assessor-info {
        color: white;
        font-size: 13px;
        background: rgba(255,255,255,0.1);
        padding: 8px 15px;
        border-radius: 5px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* BARRA DE SELEÇÃO */
    .barra-selecao {
        background: #ecf0f1;
        padding: 8px 40px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .barra-selecao label {
        font-weight: bold;
        color: #000000;
        font-size: 12px;
        display: block;
        margin-bottom: 4px;
    }

    /* SELECTBOX */
    .stSelectbox {
        margin: 0 !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        min-height: 32px !important;
        height: 32px !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div:first-child {
        background: white !important;
        border: 2px solid #27ae60 !important;
        color: #000000 !important;
        box-shadow: none !important;
        min-height: 32px !important;
        height: 32px !important;
        padding: 4px 10px !important;
        display: flex !important;
        align-items: center !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        line-height: 24px !important;
        overflow: visible !important;
        text-overflow: clip !important;
        white-space: nowrap !important;
    }
    
    .stSelectbox svg {
        fill: #27ae60 !important;
        width: 18px !important;
        height: 18px !important;
    }
    
    [data-baseweb="popover"] {
        background: white !important;
        border: 1px solid #27ae60 !important;
    }
    
    [data-baseweb="popover"] ul li {
        color: #000000 !important;
        background: white !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
    }
    
    [data-baseweb="popover"] ul li:hover {
        background: #e8f5e9 !important;
        color: #1e4d2b !important;
    }
    
    /* CONTAINER PRINCIPAL */
    .container-principal {
        padding: 20px 40px;
        background: white;
    }
    
    /* BOXES */
    .box {
        background: white;
        border: 1px solid #ddd;
        border-radius: 5px;
        overflow: hidden;
        height: 100%;
    }
    
    .box-titulo {
        background: #f8f9fa;
        padding: 10px 15px;
        border-bottom: 2px solid #e0e0e0;
        font-weight: bold;
        color: #2c3e50;
        font-size: 13px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .box-conteudo {
        padding: 10px;
        overflow-y: auto;
        max-height: 600px;
        background: #fafafa;
    }
    
    /* CARDS DE FUNDOS */
    .fundo-card-container {
        position: relative; 
        margin-bottom: 8px;
    }
    
    .fundo-card {
        background: white;
        border: 1px solid #ddd;
        border-left: 6px solid #27ae60;
        border-radius: 4px;
        padding: 12px;
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.2s;
    }
    
    .fundo-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transform: translateX(3px);
    }

    .fundo-card.fundo-card-selecionado {
        border-right: 2px solid #3498db;
        border-top: 1px solid #3498db;
        border-bottom: 1px solid #3498db;
        box-shadow: 0 0 5px rgba(52, 152, 219, 0.5); 
    }
    
    .fundo-card .nome {
        font-weight: bold;
        font-size: 12px;
        color: #2c3e50;
        margin-bottom: 8px;
        line-height: 1.3;
    }
    
    .fundo-card .info {
        font-size: 11px;
        color: #7f8c8d;
    }
    
    .fundo-card .info .valor {
        color: #27ae60;
        font-weight: 600;
    }

    .fundo-card-container .stButton button {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: transparent !important; 
        border: none !important;
        color: transparent !important;
        cursor: pointer;
        z-index: 10;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .fundo-card-container .stButton button:hover {
        background: rgba(0, 0, 0, 0.02) !important;
    }

    /* TESE */
    .tese-texto {
        padding: 15px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 12px;
        line-height: 1.6;
        color: #2c3e50;
        background: white;
    }
    
    .tese-texto strong {
        font-size: 13px;
        font-weight: bold;
        display: block;
        margin-bottom: 10px;
    }
    
    .tese-texto h4 {
        font-size: 13px;
        font-weight: bold;
        color: #1e4d2b;
        margin: 15px 0 8px 0;
        background: #f0f8f4;
        padding: 6px 10px;
        border-left: 4px solid #27ae60;
    }
    
    .tese-texto p {
        margin: 0 0 12px 0;
        color: #34495e;
        line-height: 1.7;
    }
    
    /* CALENDÁRIO */
    .calendario-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 0;
        border: 1px solid #ddd;
    }
    
    .cal-header {
        background: #27ae60;
        color: white;
        padding: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 11px;
        border: 1px solid #1e8449;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .cal-dia {
        border: 1px solid #ddd;
        padding: 8px;
        min-height: 90px;
        background: white;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .cal-dia.fim-semana {
        background: #f8f9fa;
    }
    
    .cal-dia .numero {
        font-size: 14px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    
    .cal-evento {
        background: #27ae60;
        color: white;
        padding: 3px 6px;
        border-radius: 3px;
        font-size: 10px;
        font-weight: bold;
        margin: 2px 0;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* BOTÕES */
    .stButton button {
        background: #27ae60 !important;
        color: white !important;
        border: none !important;
        padding: 8px 15px !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        font-size: 11px !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    .stButton button:hover {
        background: #1e8449 !important;
    }
    
    /* BOTÃO SAIR ESPECÍFICO */
    div[data-testid="column"]:last-child .stButton button {
        background: #e74c3c !important;
        color: white !important;
        padding: 10px 20px !important;
        font-size: 13px !important;
    }
    
    div[data-testid="column"]:last-child .stButton button:hover {
        background: #c0392b !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #27ae60;
        border-radius: 4px;
    }
    
    /* PÁGINA DE FUNDOS */
    .fundos-header {
        background: #1e4d2b;
        padding: 30px 40px;
        color: white;
        text-align: center;
    }
    
    .fundos-header h1 {
        font-size: 32px;
        margin: 0 0 10px 0;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .fundos-header p {
        font-size: 16px;
        margin: 0;
        color: #7dcea0;
    }
    
    .fundo-card-full {
        background: white;
        border: 1px solid #ddd;
        border-left: 6px solid #27ae60;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .fundo-card-full h3 {
        color: #1e4d2b;
        font-size: 18px;
        margin: 0 0 15px 0;
        font-weight: bold;
    }
    
    .fundo-card-full .info-section {
        margin-bottom: 15px;
    }
    
    .fundo-card-full .info-section h4 {
        color: #27ae60;
        font-size: 14px;
        margin: 0 0 8px 0;
        font-weight: 600;
    }
    
    .fundo-card-full .info-section p {
        color: #2c3e50;
        font-size: 13px;
        line-height: 1.6;
        margin: 0;
    }
    
    .fundo-card-full .links-section {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #e0e0e0;
    }
    
</style>
""", unsafe_allow_html=True)

# ============================================
# DADOS
# ============================================

CORES_FUNDOS = [
    '#27ae60', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c',
    '#2ecc71', '#e67e22', '#16a085', '#c0392b', '#2980b9', '#52be80'
]

MESES_PT = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

def criar_tese(nome_ativo, dia_util_int):
    if 'FII' in nome_ativo or 'Imobiliário' in nome_ativo:
        resumo = "Fundo de Investimento Imobiliário que investe em imóveis comerciais de alto padrão, galpões logísticos em regiões estratégicas e Certificados de Recebíveis Imobiliários (CRI) de emissores sólidos."
        condicoes = f"• Emissor: Gestora especializada em FII\n• Prazo: Indeterminado\n• Taxa: 0,5% a 1,0% a.a.\n• Liquidez: D+30\n• Aplicação mínima: R$ 1.000,00\n• Pagamento: {dia_util_int}º dia útil"
        perfil = "Ideal para investidores que buscam renda mensal passiva, isenta de IR para PF"
        speech = "Destaque a isenção de IR, diversificação imobiliária e distribuição mensal."
        venda_1min = "Este FII oferece renda mensal isenta de IR para pessoa física, investindo em imóveis de alta qualidade com inquilinos sólidos. Ideal para quem busca diversificação e rendimentos previsíveis acima da poupança."
        links = {
            'expert': 'https://exemplo.com/expert-fii',
            'lamina': 'https://exemplo.com/lamina-fii',
            'material': 'https://exemplo.com/material-fii'
        }
    elif 'CRI' in nome_ativo or 'Renda' in nome_ativo:
        resumo = "Fundo de renda fixa que investe em CRI, títulos públicos e crédito privado de primeira linha."
        condicoes = f"• Emissor: Gestora com expertise em renda fixa\n• Prazo: Indeterminado\n• Taxa: 0,5% a 1,0% a.a.\n• Liquidez: D+30\n• Aplicação mínima: R$ 1.000,00\n• Pagamento: {dia_util_int}º dia útil"
        perfil = "Conservadores que buscam rentabilidade acima do CDI"
        speech = "Alternativa superior à poupança com rentabilidade consistente."
        venda_1min = "Fundo de renda fixa que busca rentabilidade superior ao CDI através de uma carteira diversificada de CRI e crédito privado. Gestão profissional com foco em segurança e liquidez, perfeito para o investidor conservador que quer mais do que a poupança oferece."
        links = {
            'expert': 'https://exemplo.com/expert-cri',
            'lamina': 'https://exemplo.com/lamina-cri',
            'material': 'https://exemplo.com/material-cri'
        }
    else:
        resumo = "Fundo com gestão ativa e estratégia diversificada."
        condicoes = f"• Emissor: Casa de gestão independente\n• Prazo: Variável\n• Taxa: 1,0% a 2,0% a.a.\n• Liquidez: D+30\n• Aplicação mínima: R$ 1.000,00\n• Pagamento: {dia_util_int}º dia útil"
        perfil = "Investidores com perfil moderado"
        speech = "Gestão profissional e rebalanceamento tático."
        venda_1min = "Fundo com gestão ativa que busca as melhores oportunidades do mercado através de análise criteriosa e rebalanceamento constante. Diversificação automática com equipe especializada cuidando do seu patrimônio."
        links = {
            'expert': 'https://exemplo.com/expert-fundo',
            'lamina': 'https://exemplo.com/lamina-fundo',
            'material': 'https://exemplo.com/material-fundo'
        }
    
    return {
        'resumo': resumo,
        'condicoes': condicoes,
        'perfil': perfil,
        'speech': speech,
        'venda_1min': venda_1min,
        'links': links
    }

def buscar_info_fundo(nome_ativo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses):
    for nome_fundo in mapa_pagamentos.keys():
        if nome_fundo.lower() in nome_ativo.lower() or nome_ativo.lower() in nome_fundo.lower():
            return {
                'dia_util': mapa_pagamentos.get(nome_fundo),
                'cor': mapa_cores.get(nome_fundo, '#95a5a6'),
                'sigla': mapa_siglas.get(nome_fundo, nome_ativo[:10]),
                'tese': mapa_teses.get(nome_fundo, {})
            }
    return {'dia_util': None, 'cor': '#95a5a6', 'sigla': nome_ativo[:10], 'tese': {}}

def calcular_dia_util(ano, mes, numero_dia_util, feriados):
    if not numero_dia_util or numero_dia_util <= 0:
        return None
    
    try:
        dia_atual = date(ano, mes, 1)
        contador_dias_uteis = 0
        
        while dia_atual.month == mes:
            eh_fim_de_semana = dia_atual.weekday() >= 5
            eh_feriado = dia_atual in feriados
            
            if not eh_fim_de_semana and not eh_feriado:
                contador_dias_uteis += 1
                
                if contador_dias_uteis == numero_dia_util:
                    return dia_atual
            
            dia_atual += timedelta(days=1)
        
        return None
    except:
        return None

# ============================================
# CARREGAR DADOS ANTES DA AUTENTICAÇÃO
# ============================================

# Carregar dados primeiro para poder validar na tela de login
@st.cache_data
def carregar_dados():
    try:
        NOME_ARQUIVO = 'calendario_Renda_mais.xlsx'
        
        if not os.path.exists(NOME_ARQUIVO):
            st.error(f"❌ Erro: O arquivo '{NOME_ARQUIVO}' não foi encontrado.")
            return None, None, None, None, None, None

        df_base = pd.read_excel(NOME_ARQUIVO, sheet_name='Base')
        df_base.columns = df_base.columns.str.strip()
        
        df_suporte = pd.read_excel(NOME_ARQUIVO, sheet_name='Suporte')
        
        try:
            df_feriados = pd.read_excel(NOME_ARQUIVO, sheet_name='Feriados')
            feriados = set()
            for col in df_feriados.columns:
                for val in df_feriados[col]:
                    if pd.notna(val) and isinstance(val, datetime):
                        feriados.add(val.date())
        except:
            feriados = set()
        
        mapa_pagamentos = {}
        mapa_cores = {}
        mapa_siglas = {}
        mapa_teses = {}
        
        colunas = list(df_suporte.columns)
        col_ativo = colunas[7] if len(colunas) > 7 else None
        col_dia_util = colunas[8] if len(colunas) > 8 else None
        col_sigla = colunas[6] if len(colunas) > 6 else None
        
        cor_index = 0
        
        for index, row in df_suporte.iterrows():
            if col_ativo and col_dia_util:
                nome_ativo = str(row[col_ativo]).strip()
                dia_util = row[col_dia_util]
                
                if pd.isna(nome_ativo) or nome_ativo == '' or nome_ativo == 'nan':
                    continue
                
                try:
                    dia_util_int = int(float(dia_util))
                    mapa_pagamentos[nome_ativo] = dia_util_int
                    mapa_cores[nome_ativo] = CORES_FUNDOS[cor_index % len(CORES_FUNDOS)]
                    
                    if col_sigla:
                        sigla = str(row[col_sigla]).strip() if pd.notna(row[col_sigla]) else nome_ativo[:10]
                    else:
                        palavras = nome_ativo.split()
                        sigla = ''.join([p[0].upper() for p in palavras[:3]])
                    mapa_siglas[nome_ativo] = sigla.upper()
                    
                    tese = criar_tese(nome_ativo, dia_util_int)
                    mapa_teses[nome_ativo] = tese
                    
                    cor_index += 1
                except:
                    pass
        
        return df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None, None, None, None, None, None

# Carregar dados primeiro
df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses = carregar_dados()

# ============================================
# PÁGINA DE FUNDOS
# ============================================

def pagina_conheca_fundos():
    """Página pública com informações de todos os fundos"""
    
    st.markdown("""
    <div class="fundos-header">
        <h1>🌳 Conheça Nossos Fundos</h1>
        <p>Todos os fundos disponíveis na Tauari Investimentos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão voltar
    col_voltar = st.columns([6, 1])
    with col_voltar[1]:
        st.markdown('<div style="margin: 20px 40px 0 0;">', unsafe_allow_html=True)
        if st.button("🔙 Voltar ao Login", key="btn_voltar_login"):
            st.session_state.pagina_atual = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="padding: 20px 40px;">', unsafe_allow_html=True)
    
    if mapa_pagamentos:
        # Listar todos os fundos
        for idx, (nome_fundo, dia_util) in enumerate(mapa_pagamentos.items()):
            cor = mapa_cores.get(nome_fundo, '#27ae60')
            tese = mapa_teses.get(nome_fundo, {})
            
            st.markdown(f"""
            <div class="fundo-card-full" style="border-left-color: {cor}">
                <h3>📊 {nome_fundo}</h3>
                
                <div class="info-section">
                    <h4>📝 Sobre o Fundo</h4>
                    <p>{tese.get('resumo', 'Informações não disponíveis')}</p>
                </div>
                
                <div class="info-section">
                    <h4>📋 Resumo de Condições</h4>
                    <p style="white-space: pre-line;">{tese.get('condicoes', 'Informações não disponíveis')}</p>
                </div>
                
                <div class="info-section">
                    <h4>⚡ Venda em 1 Minuto</h4>
                    <p>{tese.get('venda_1min', 'Informações não disponíveis')}</p>
                </div>
                
                <div class="links-section">
                    <h4 style="color: #2c3e50; font-size: 14px; margin-bottom: 12px; font-weight: bold;">📎 Materiais e Conteúdos</h4>
            """, unsafe_allow_html=True)
            
            # Links do fundo
            if 'links' in tese and isinstance(tese['links'], dict):
                col1, col2, col3 = st.columns(3)
                with col1:
                    expert_url = tese['links'].get('expert', '#')
                    st.markdown(f'<a href="{expert_url}" target="_blank" style="display: block; background: #e74c3c; color: white; padding: 12px; border-radius: 6px; text-decoration: none; text-align: center; font-weight: 600; font-size: 13px; margin-bottom: 10px;">🎯 Expert</a>', unsafe_allow_html=True)
                with col2:
                    lamina_url = tese['links'].get('lamina', '#')
                    st.markdown(f'<a href="{lamina_url}" target="_blank" style="display: block; background: #27ae60; color: white; padding: 12px; border-radius: 6px; text-decoration: none; text-align: center; font-weight: 600; font-size: 13px; margin-bottom: 10px;">📄 Lâmina</a>', unsafe_allow_html=True)
                with col3:
                    material_url = tese['links'].get('material', '#')
                    st.markdown(f'<a href="{material_url}" target="_blank" style="display: block; background: #3498db; color: white; padding: 12px; border-radius: 6px; text-decoration: none; text-align: center; font-weight: 600; font-size: 13px; margin-bottom: 10px;">📢 Material Publicitário</a>', unsafe_allow_html=True)
            
            st.markdown("""
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Nenhum fundo disponível no momento")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Verificar qual página mostrar
if st.session_state.get('pagina_atual') == 'fundos':
    pagina_conheca_fundos()
else:
    # Verificar autenticação passando df_base
    verificar_autenticacao(df_base)

# ============================================
# INTERFACE PRINCIPAL
# ============================================

def main():
    # Os dados já foram carregados globalmente
    global df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses
    
    if df_base is None:
        st.stop()
    
    # Verificar se está autenticado
    if not st.session_state.get('autenticado', False) or not st.session_state.get('assessor_logado'):
        st.error("❌ Sessão expirada. Faça login novamente.")
        st.session_state.autenticado = False
        st.session_state.assessor_logado = None
        st.rerun()
    
    # FILTRAR CLIENTES DO ASSESSOR LOGADO
    assessor_logado = st.session_state.assessor_logado
    
    # Converter coluna Assessor para string para comparação
    df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
    
    df_base_filtrado = df_base[df_base['Assessor'] == str(assessor_logado)]
    
    # CABEÇALHO COM INFO DO ASSESSOR
    assessor_nome = st.session_state.get('nome_assessor', 'Assessor')
    st.markdown(f"""
    <div class="header-verde">
        <div class="header-content">
            <div class="logo">🌳</div>
            <div class="texto">
                <h1>📅 CALENDÁRIO DE PAGAMENTOS - RENDA MAIS</h1>
                <h2>TAUARI INVESTIMENTOS</h2>
            </div>
        </div>
        <div class="assessor-info">
            👤 Assessor: <strong>{assessor_nome}</strong> ({assessor_logado})
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # BARRA DE SAUDAÇÃO E BOTÃO SAIR
    st.markdown('<div style="background: white; padding: 5px 0;">', unsafe_allow_html=True)
    col_saudacao, col_btn_sair = st.columns([5, 1])
    
    with col_saudacao:
        nome_assessor = st.session_state.get('nome_assessor', 'Assessor')
        st.markdown(f'<p style="font-size: 22px; color: #1e4d2b; margin: 15px 0 15px 40px; font-weight: 700;">👋 Olá, {nome_assessor}!</p>', unsafe_allow_html=True)
    
    with col_btn_sair:
        st.markdown('<div style="margin-top: 10px; margin-right: 40px;">', unsafe_allow_html=True)
        if st.button("🚪 Sair", key="btn_sair"):
            # Limpar session_state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # BARRA DE SELEÇÃO
    st.markdown('<div class="barra-selecao">', unsafe_allow_html=True)
    st.markdown(f'<label>👤 SELECIONE O CLIENTE ({len(df_base_filtrado)} clientes):</label>', unsafe_allow_html=True)
    
    clientes = sorted(df_base_filtrado['Cliente'].unique())
    cliente_selecionado = st.selectbox("Selecione o Cliente", [""] + list(clientes), label_visibility="collapsed", key="cliente_select")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not cliente_selecionado:
        st.stop()
    
    fundos_cliente = df_base_filtrado[df_base_filtrado['Cliente'] == cliente_selecionado]

    if 'fundo_selecionado' not in st.session_state or st.session_state.fundo_selecionado not in fundos_cliente['Ativo'].values:
        if not fundos_cliente.empty:
            st.session_state.fundo_selecionado = fundos_cliente['Ativo'].iloc[0]
        else:
            st.session_state.fundo_selecionado = None
    
    # CONTAINER PRINCIPAL
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    # COLUNA 1: FUNDOS
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            try:
                posicao = float(fundo['Financeiro'])
            except:
                posicao = 0.0
                
            info = buscar_info_fundo(ativo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            
            dia_texto = f"{info['dia_util']}º dia útil" if info['dia_util'] else "Não definido"
            
            classe_selecao = 'fundo-card-selecionado' if ativo == st.session_state.fundo_selecionado else ''
            
            st.markdown(f"""
            <div class="fundo-card-container">
                <div class="fundo-card {classe_selecao}" style="border-left-color: {info['cor']}">
                    <div class="nome">{ativo}</div>
                    <div class="info">
                        💰 Posição: <span class="valor">R$ {posicao:,.2f}</span> | 📅 {dia_texto}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(" ", key=f"select_{ativo}", help=f"Ver tese: {ativo}"):
                st.session_state.fundo_selecionado = ativo
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # COLUNA 2: TESE
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        fundo_para_tese = st.session_state.fundo_selecionado
        
        if fundo_para_tese:
            info = buscar_info_fundo(fundo_para_tese, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            tese = info['tese']
            
            st.markdown(f"""
            <div class="tese-texto">
                <strong style="color: {info['cor']};">{fundo_para_tese}</strong>
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
    
    # COLUNA 3: CALENDÁRIO
    with col3:
        st.markdown('<div class="box"><div class="box-titulo">📅 CALENDÁRIO</div>', unsafe_allow_html=True)
        
        if 'mes_atual' not in st.session_state:
            st.session_state.mes_atual = datetime.now().month
            st.session_state.ano_atual = datetime.now().year
        
        col_p1, col_p2, col_p3 = st.columns([1, 3, 1])
        
        with col_p1:
            if st.button("◀ Mês Anterior", key="prev_mes"):
                st.session_state.mes_atual -= 1
                if st.session_state.mes_atual < 1:
                    st.session_state.mes_atual = 12
                    st.session_state.ano_atual -= 1
                st.rerun()
        
        with col_p2:
            st.markdown(f'<div style="text-align: center; padding: 8px; font-size: 16px; font-weight: bold; color: #1e4d2b;">{MESES_PT[st.session_state.mes_atual-1]} {st.session_state.ano_atual}</div>', unsafe_allow_html=True)
        
        with col_p3:
            if st.button("Próximo Mês ▶", key="next_mes"):
                st.session_state.mes_atual += 1
                if st.session_state.mes_atual > 12:
                    st.session_state.mes_atual = 1
                    st.session_state.ano_atual += 1
                st.rerun()
        
        cal = calendar.monthcalendar(st.session_state.ano_atual, st.session_state.mes_atual)
        
        dias_semana = ['seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.', 'dom.']
        html_cal = '<div class="calendario-grid">'
        
        for dia in dias_semana:
            html_cal += f'<div class="cal-header">{dia}</div>'
        
        eventos_mes = {}
        for _, fundo in fundos_cliente.iterrows():
            info = buscar_info_fundo(fundo['Ativo'], mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            if info['dia_util']:
                data_pagamento = calcular_dia_util(st.session_state.ano_atual, st.session_state.mes_atual, info['dia_util'], feriados)
                if data_pagamento:
                    dia = data_pagamento.day
                    if dia not in eventos_mes:
                        eventos_mes[dia] = []
                    eventos_mes[dia].append({'sigla': info['sigla'], 'cor': info['cor']})
        
        for semana in cal:
            for dia in semana:
                if dia == 0:
                    html_cal += '<div class="cal-dia" style="background: #f8f9fa;"></div>'
                else:
                    data = date(st.session_state.ano_atual, st.session_state.mes_atual, dia)
                    classe = "cal-dia fim-semana" if data.weekday() >= 5 else "cal-dia" 
                    
                    eventos_html = ""
                    if dia in eventos_mes:
                        for evento in eventos_mes[dia]:
                            eventos_html += f'<div class="cal-evento" style="background: {evento["cor"]}">{evento["sigla"]}</div>'
                    
                    html_cal += f'<div class="{classe}"><div class="numero">{dia}</div>{eventos_html}</div>'
        
        html_cal += '</div>'
        st.markdown(html_cal, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
