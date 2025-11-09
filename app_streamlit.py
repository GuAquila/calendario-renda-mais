"""
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
======================================================
Sistema multi-assessor com senhas individuais
VERSÃO FINAL LIMPA - 25/10/2025
Usa APENAS aba "Base" do Excel

MODIFICAÇÃO: Página "Conheça os Fundos" agora destaca o fundo selecionado no topo
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
    """Valida a senha do assessor"""
    if codigo_assessor not in ASSESSORES:
        return False, None
    
    nome_assessor, senha_esperada = ASSESSORES[codigo_assessor]
    if senha == senha_esperada:
        return True, nome_assessor
    return False, None

def verificar_autenticacao(df_base):
    """Tela de login por assessor"""
    
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
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="login-titulo">
                <h2 style='margin: 10px 0; font-size: 24px;'>Calendário Renda Mais - Tauari Investimentos</h2>
                <p style='color: #7f8c8d; font-size: 14px; margin-top: 15px;'>Acesso restrito por Assessor (uso interno) - Última atualização 24/10</p>
            </div>
            """, unsafe_allow_html=True)
            
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
                    if not codigo_assessor or not senha_assessor:
                        st.error("❌ Preencha todos os campos!")
                    else:
                        valido, nome_assessor = validar_senha_assessor(codigo_assessor, senha_assessor)
                        if valido:
                            if df_base is not None:
                                df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip().str.replace('A', '', 1)
                                clientes_assessor = df_base[df_base['Assessor'] == str(codigo_assessor)]
                                
                                if clientes_assessor.empty:
                                    st.error(f"❌ Nenhum cliente encontrado para o Assessor {codigo_assessor}")
                                else:
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
# CSS
# ============================================

st.markdown("""
<style>
    .stApp {
        background: white !important;
    }
    
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
    
    /* BARRA DE SELEÇÃO - LIMPA */
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
    
    /* Selectbox styling */
    [data-baseweb="select"] {
        min-height: 40px !important;
    }
    
    .container-principal {
        display: flex;
        gap: 20px;
        margin-top: 20px;
    }
    
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
    
    .fundo-card-selecionado {
        border: 3px solid #27ae60 !important;
        background: #f0f9f4 !important;
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.2);
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
    
    /* ============================================
       NOVO CSS PARA FUNDO EM DESTAQUE
       ============================================ */
    
    /* Este é o estilo do box grande que aparece no topo quando um fundo é selecionado */
    .fundo-destaque {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 35px;
        border-radius: 15px;
        margin-bottom: 40px;
        box-shadow: 0 8px 25px rgba(39, 174, 96, 0.25);
        border: 3px solid #27ae60;
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Animação suave quando o fundo aparece em destaque */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Título do fundo em destaque - maior e mais chamativo */
    .fundo-destaque h2 {
        color: #1e4d2b;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 3px solid #27ae60;
    }
    
    /* Badge "SELECIONADO" que aparece no topo */
    .badge-selecionado {
        display: inline-block;
        background: #27ae60;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(39, 174, 96, 0.3);
    }
    
    /* Conteúdo do fundo em destaque */
    .fundo-destaque-conteudo {
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DADOS E CONFIGURAÇÕES
# ============================================

MESES_PT = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

def gerar_feriados(ano):
    """Gera lista de feriados nacionais"""
    feriados_fixos = {
        (1, 1): "Ano Novo",
        (4, 21): "Tiradentes",
        (5, 1): "Dia do Trabalho",
        (9, 7): "Independência",
        (10, 12): "Nossa Senhora Aparecida",
        (11, 2): "Finados",
        (11, 15): "Proclamação da República",
        (11, 20): "Dia da Consciência Negra",
        (12, 25): "Natal"
    }
    
    feriados_moveis = {
        2025: [(2, 28), (3, 3), (3, 4), (4, 18), (5, 29)],
        2026: [(2, 13), (2, 16), (2, 17), (4, 3), (5, 14)],
        2027: [(2, 5), (2, 8), (2, 9), (3, 26), (5, 6)],
    }
    
    lista_feriados = []
    for (mes, dia), nome in feriados_fixos.items():
        lista_feriados.append(date(ano, mes, dia))
    
    if ano in feriados_moveis:
        for (mes, dia) in feriados_moveis[ano]:
            lista_feriados.append(date(ano, mes, dia))
    
    return lista_feriados

def calcular_dia_util(ano, mes, dia_util_desejado, feriados):
    """Calcula o dia útil real do mês"""
    primeiro_dia = date(ano, mes, 1)
    
    if primeiro_dia.month == 12:
        ultimo_dia = date(ano, mes, 31)
    else:
        ultimo_dia = (date(ano, mes + 1, 1) - timedelta(days=1))
    
    dia_atual = primeiro_dia
    contador_dias_uteis = 0
    
    while dia_atual <= ultimo_dia:
        if dia_atual.weekday() < 5 and dia_atual not in feriados:
            contador_dias_uteis += 1
            if contador_dias_uteis == dia_util_desejado:
                return dia_atual
        dia_atual += timedelta(days=1)
    
    return None

# ============================================
# MAPEAMENTO DOS FUNDOS
# ============================================

MAPA_PAGAMENTOS = {
    'ARX FII Portfólio Renda CDI+ RL': 15,
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 5,
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 5,
    'AZ Quest Panorama Renda CDI FI RL': 5,
    'BGR Galpões Logísticos - Cota Sênior': 15,
    'BGR Galpões Logísticos - Cota Subordinada': 15,
    'Maua Lajes Corporativas Feeder FII RL - Senior': 15,
    'SPX CRI Portfolio Renda Mais': 15,
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': 5,
    'XP Renda Imobiliária Feeder FII RL': 15,
    'XP Habitat Renda Imobiliária Feeder FII': 15,
    'Valora CRI CDI Renda+ FII RL': 15,
}

MAPA_CORES = {
    'ARX FII Portfólio Renda CDI+ RL': '#e74c3c',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': '#3498db',
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': '#9b59b6',
    'AZ Quest Panorama Renda CDI FI RL': '#9b59b6',
    'BGR Galpões Logísticos - Cota Sênior': '#f39c12',
    'BGR Galpões Logísticos - Cota Subordinada': '#e67e22',
    'Maua Lajes Corporativas Feeder FII RL - Senior': '#1abc9c',
    'SPX CRI Portfolio Renda Mais': '#2ecc71',
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': '#34495e',
    'XP Renda Imobiliária Feeder FII RL': '#16a085',
    'XP Habitat Renda Imobiliária Feeder FII': '#27ae60',
    'Valora CRI CDI Renda+ FII RL': '#8e44ad',
}

MAPA_SIGLAS = {
    'ARX FII Portfólio Renda CDI+ RL': 'ARX',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 'AZ Quest',
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 'AZ Panorama',
    'AZ Quest Panorama Renda CDI FI RL': 'AZ Panorama',
    'BGR Galpões Logísticos - Cota Sênior': 'BGR Senior',
    'BGR Galpões Logísticos - Cota Subordinada': 'BGR Sub',
    'Maua Lajes Corporativas Feeder FII RL - Senior': 'Maua Senior',
    'SPX CRI Portfolio Renda Mais': 'SPX',
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': 'Solis',
    'XP Renda Imobiliária Feeder FII RL': 'XP Renda',
    'XP Habitat Renda Imobiliária Feeder FII': 'XP Habitat',
    'Valora CRI CDI Renda+ FII RL': 'Valora',
}

MAPA_TESES = {
    'ARX FII Portfólio Renda CDI+ RL': {
        'resumo': 'Fundo de Investimento Imobiliário é composto por CRIs, mecânica de Renda Fixa, distribuição mensal de rendimentos e amortizações periódicas, ambas isentas de IR.',
        'condicoes': '''• Rentabilidade: CDI + 2,04% (Isento de IR para PF)
• Prazo: 7 anos
• Duration: 3,6 anos
• Público-alvo: Investidores em Geral''',
        'venda_1min': 'Fundo imobiliário com foco em CRIs que busca rentabilidade acima do CDI, oferecendo uma boa alternativa para renda passiva. O fundo terá uma pulverização da carteira ao longo dos primeiros 24 meses, buscanto aproximadamente 20 operações em seu portfólio. O gestor é a ARX Investimentos, fundada em 2001, e controlada pelo grupo BNY Mellon, uma das mais tradicionais instituições financeiras do mundo.',
        'perfil': 'Investidores que buscam renda recorrente com retornos superiores ao CDI através do mercado imobiliário.'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'resumo': 'Fundo imoboliário com investimento em ativos de infraestrutura maduros, com distribuição de rendimentos mensais.',
        'condicoes': '''• Rentabilidade: CDI + 2,20% (Isento de IR para PF)
• Prazo: 5 anos (+ 2 prorrogáveis)
• Duration: 3,5 anos
• Público-alvo: Investidores Qualificados''',
        'venda_1min': 'O Fundo de infraestrutura faz parte de uma familía de fundos da AZ Quest que alcançou R$ 2 bilhões de reais. Além de parte relevante já em warehouse ou estruturação, permitindo uma alocação rápida e eficiente.',
        'perfil': 'Investidores que buscam distribuição mensal de rendimentos isentos e uma cota patrimonial que se mantém estável durante o processo.'
    },
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': {
        'resumo': 'Fundo imobiliário de renda fixa com objetivo de superar o CDI através de uma carteira diversificada com um portfólio de crédito para incorporadoras de médio e alto padrão em São Paulo.',
        'condicoes': '''• Rentabilidade: CDI + 2,40% (Isento de IR para PF)
• Prazo: 5 anos (+ 1 prorrogável)
• Duration: 3,5 anos
• Público-alvo: Investidor em Geral''',
        'venda_1min': 'Fundo que busca retornos superiores ao CDI investindo em uma carteira diversificada de crédito privado com reinvestimento limitado a 3 anos, devolução integral do capital em até 5 anos. Além de garantias reais e um time com expertise de 24 anos no setor.',
        'perfil': 'Investidores conservadores que buscam retornos superiores ao CDI com gestão ativa.'
    },
    'AZ Quest Panorama Renda CDI FI RL': {
        'resumo': 'Fundo imobiliário de renda fixa com objetivo de superar o CDI através de uma carteira diversificada com um portfólio de crédito para incorporadoras de médio e alto padrão em São Paulo.',
        'condicoes': '''• Rentabilidade: CDI + 2,40% (Isento de IR para PF)
• Prazo: 5 anos (+ 1 prorrogável)
• Duration: 3,5 anos
• Público-alvo: Investidor em Geral''',
        'venda_1min': 'Fundo que busca retornos superiores ao CDI investindo em uma carteira diversificada de crédito privado com reinvestimento limitado a 3 anos, devolução integral do capital em até 5 anos. Além de garantias reais e um time com expertise de 24 anos no setor.',
        'perfil': 'Investidores conservadores que buscam retornos superiores ao CDI com gestão ativa.'
    },
    'BGR Galpões Logísticos - Cota Sênior': {
        'resumo': 'Fundo imobiliário focado em galpões logísticos com estrutura de cotas sênior.',
        'condicoes': '''• Rentabilidade: IPCA + 9,50% (Isento de IR para PF)
• Prazo: 5 anos
• Duration: 3 anos
• Público-alvo: Investidores em Geral''',
        'venda_1min': 'Investimento em galpões logísticos com cota sênior, oferecendo menor risco e proteção inflacionária.',
        'perfil': 'Investidores que buscam renda no setor logístico com menor risco através da estrutura sênior.'
    },
    'BGR Galpões Logísticos - Cota Subordinada': {
        'resumo': 'Fundo imobiliário focado em galpões logísticos com estrutura de cotas subordinadas.',
        'condicoes': '''• Rentabilidade: IPCA + 29,20% (Isento de IR para PF)
• Prazo: 5 anos
• Duration: 3 anos
• Público-alvo: Investidores Profissionais''',
        'venda_1min': 'Investimento em galpões logísticos com cota subordinada, oferecendo maior potencial de retorno.',
        'perfil': 'Investidores que aceitam maior risco em busca de retornos superiores no setor logístico.'
    },
    'Maua Lajes Corporativas Feeder FII RL - Senior': {
        'resumo': 'Fundo imobiliário focado em lajes corporativas com estrutura sênior.',
        'condicoes': '''• Rentabilidade: IPCA + 9,20% (Isento de IR para PF)
• Prazo: 5 anos
• Duration: 4,1 anos
• Público-alvo: Investidores em Geral''',
        'venda_1min': 'Fundo de lajes corporativas com estrutura sênior, proporcionando renda estável do mercado corporativo com rendimentos mensais mais correção do IPCA na conta, sem volatilidade.',
        'perfil': 'Investidores que buscam renda do mercado imobiliário corporativo com menor volatilidade e remarcação na cota patrimonial.'
    },
    'SPX CRI Portfolio Renda Mais': {
        'resumo': 'Fundo imoboliário focado em CRIs, com indexador definido durante todo o período.',
        'condicoes': '''• Rentabilidade: CDI + 2,40% (Isento de IR para PF)
• Prazo: 6 anos
• Duration: 3,5 anos
• Público-alvo: Investidores em Geral''',
        'venda_1min': 'Portfolio diversificado de CRIs residenciais que busca renda recorrente com momento de alta taxa de Juros, além de uma taxa de administração inferior à média de mercado (0,90% a.a.).',
        'perfil': 'Investidores que buscam diversificação no mercado imobiliário através de CRIs.'
    },
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': {
        'resumo': 'Fundo que consiste na alocaçãõ diversificada em cotas seniores de FIDCs, com aquisições exclusivas priorizando um perfil conservador de investimento.',
        'condicoes': '''• Rentabilidade: CDI + 2,00% (Isento de IR para PF)
• Prazo: 6 anos
• Duration: 2,5 anos
• Público-alvo: Investidores em Geral''',
        'venda_1min': 'Fundo de crédito privado diversificado que busca retornos superiores ao CDI com aquisição exclusiva de cotas seniores de FIDCs, além de uma subordinação robusta (acima de 25,0%).',
        'perfil': 'Investidores conservadores que buscam retornos atrativos através de cotas seniores de outros FIDCs.'
    },
    'XP Renda Imobiliária Feeder FII RL': {
        'resumo': 'Fundo com objetivo de aquisição de 11 ativos imobiliários de alto padrão, com todos locados (vacância 0).',
        'condicoes': '''• Rentabilidade: IPCA + 9,00% (Isento de IR para PF)
• Prazo: 5 anos
• Duration: 3,5 anos
• Público-alvo: Investidores em Geral''',
        'venda_1min': 'Fundo que investe em uma carteira diversificada em ativos de alto padrão com estabilidade e mitigação de curva J.',
        'perfil': 'Investidores que buscam renda recorrente com ganhos acima da inflação em ativos diversificados e com alta qualidade de crédito.'
    },
    'XP Habitat Renda Imobiliária Feeder FII': {
        'resumo': 'Fundo imobiliário com dinâmica de cotas sênior e subordinada, composta majoritariamente por CRIs.',
        'condicoes': '''• Rentabilidade: IPCA + 10,00% (Isento de IR para PF)
• Prazo: 5 anos
• Duration: 4,5 anos
• Público-alvo: Investidores em Geral''',
        'venda_1min': 'Fundo que investe em CRIs com projeto de loteamento, incorporação, multipropriedade e crédito corporativo. Com um portfólio diversificado e rendimento desde o dia 1.',
        'perfil': 'Investidores que buscam exposição ao mercado imobiliário sem marcação a mercado.'
    },
    'Valora CRI CDI Renda+ FII RL': {
        'resumo': 'Fundo imobiliário focado em CRIs com rentabilidade atrelada ao CDI.',
        'condicoes': '''• Rentabilidade: CDI + 2,40% (Isento de IR para PF)
• Prazo: 6 anos
• Duration: 3,5 anos
• Público-alvo: Investidores em Geral''',
        'venda_1min': 'Fundo de CRIs que oferece rentabilidade superior ao CDI com distribuição mensal de rendimentos.',
        'perfil': 'Investidores que buscam renda passiva através do mercado imobiliário com baixa volatilidade.'
    }
}

MAPA_LINKS = {
    'ARX FII Portfólio Renda CDI+ RL': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/marco-25-1a-emissao-arx-fii-portfolio-renda-cdi-rl/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/02/Apresentacao-ARX-FII-Portfolio-Renda-CDIRL-2.pdf'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/fevereiro-25-az-quest-renda-mais-infra-yield-vi-fip-ie/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/01/AZ-Quest-Renda-Mais-Infra-Yield-VI-FIP-IE_vf.pdf'
    },
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/outubro-25-az-quest-panorama-renda-cdi-fi-responsabilidade-limitada-2/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2024/09/Apresentacao-AZ-Quest-Panorama-Renda-CDI-FI-Responsabilidade-Limitada-v3.pdf'
    },
    'AZ Quest Panorama Renda CDI FI RL': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/outubro-25-az-quest-panorama-renda-cdi-fi-responsabilidade-limitada-2/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2024/09/Apresentacao-AZ-Quest-Panorama-Renda-CDI-FI-Responsabilidade-Limitada-v3.pdf'
    },
    'BGR Galpões Logísticos - Cota Sênior': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/julho-25-bgr-galpoes-logisticos-cota-senior/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/06/BGR-Galpoes-Logisticos-Senior.pdf'
    },
    'BGR Galpões Logísticos - Cota Subordinada': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/julho-25-bgr-galpoes-logisticos-cota-subordinada/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/06/BGR-Galpoes-Logisticos-Subordinada.pdf'
    },
    'Maua Lajes Corporativas Feeder FII RL - Senior': {
        'expert': 'https://conteudos.xpi.com.br/assessor/fundos-alternativose/maio-25-maua-lajes-corporativas-feeder-fii-rl-senior/',
        'material': 'https://conteudos.xpi.com.br/wp-content/uploads/2025/04/Maua-Lajes-Corporativas-vf.pdf'
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

def buscar_info_fundo(nome_fundo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses, fundo_data=None):
    """Busca informações do fundo, com opção de usar links do Excel"""
    
    # Se temos dados do fundo do Excel, usar os links de lá
    if fundo_data is not None:
        try:
            link_expert = str(fundo_data.get('Link Expert', '')).strip()
            link_material = str(fundo_data.get('Material Publicitário', '')).strip()
            
            # Limpar valores 'nan'
            if link_expert == 'nan' or link_expert == '':
                link_expert = ''
            if link_material == 'nan' or link_material == '':
                link_material = ''
            
            links = {'expert': link_expert, 'material': link_material}
        except:
            links = MAPA_LINKS.get(nome_fundo, {'expert': '', 'material': ''})
    else:
        links = MAPA_LINKS.get(nome_fundo, {'expert': '', 'material': ''})
    
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
        'links': links
    }

# ============================================
# TELA DE FUNDOS - COM DESTAQUE
# ============================================

def tela_fundos():
    """Tela de apresentação dos fundos"""
    
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
        fundos_lista = sorted(MAPA_TESES.keys())
        fundo_selecionado = st.selectbox(
            "🎯 Ir para o fundo:",
            ["Selecione um fundo..."] + fundos_lista,
            key="nav_fundo"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if fundo_selecionado and fundo_selecionado != "Selecione um fundo...":
        info_destaque = buscar_info_fundo(
            fundo_selecionado,
            MAPA_PAGAMENTOS,
            MAPA_CORES,
            MAPA_SIGLAS,
            MAPA_TESES
        )
        
        tese_destaque = info_destaque['tese']
        links_destaque = info_destaque['links']
        
        st.markdown(f"""
<div class="fundo-destaque">
    <div class="badge-selecionado">
        ⭐ FUNDO SELECIONADO
    </div>
    <h2 style="color: {info_destaque['cor']};">
        {fundo_selecionado}
    </h2>
    <div class="fundo-destaque-conteudo">
        <p style="margin-bottom: 15px; color: #000000; font-size: 15px;">
            <strong style="color: #000000;">📝 Resumo:</strong> {tese_destaque['resumo']}
        </p>
        <p style="margin-bottom: 10px; color: #000000; font-size: 15px;">
            <strong style="color: #000000;">📋 Condições:</strong>
        </p>
        <p style="white-space: pre-line; margin-left: 15px; font-size: 14px; color: #000000; margin-bottom: 15px;">
            {tese_destaque['condicoes']}
        </p>
        <p style="margin-bottom: 10px; color: #000000; font-size: 15px;">
            <strong style="color: #000000;">⚡ Venda em 1 Minuto:</strong> {tese_destaque['venda_1min']}
        </p>
        <p style="margin-bottom: 0; color: #000000; font-size: 15px;">
            <strong style="color: #000000;">🎯 Perfil do Cliente:</strong> {tese_destaque['perfil']}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
        
        col_link1, col_link2, col_link3 = st.columns([1, 1, 2])
        
        with col_link1:
            if links_destaque['material']:
                st.markdown(f"""
<a href="{links_destaque['material']}" target="_blank" style="text-decoration: none;">
    <button style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 14px;">
        📄 Material Publicitário
    </button>
</a>
""", unsafe_allow_html=True)
        
        with col_link2:
            if links_destaque['expert']:
                st.markdown(f"""
<a href="{links_destaque['expert']}" target="_blank" style="text-decoration: none;">
    <button style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 14px;">
        🎓 Expert XP
    </button>
</a>
""", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
<div style="border-top: 2px solid #e0e0e0; margin: 30px 0;"></div>
""", unsafe_allow_html=True)
        
        st.markdown("""
<h3 style="color: #1e4d2b; text-align: center; margin-bottom: 30px;">
    📊 Todos os Fundos Disponíveis
</h3>
""", unsafe_allow_html=True)
    
    for fundo_nome in sorted(MAPA_TESES.keys()):
        info = buscar_info_fundo(
            fundo_nome,
            MAPA_PAGAMENTOS,
            MAPA_CORES,
            MAPA_SIGLAS,
            MAPA_TESES
        )
        
        tese = info['tese']
        links = info['links']
        fundo_id = fundo_nome.replace(" ", "_")
        
        st.markdown(f"""
<div id="{fundo_id}" style="background: white; border: 2px solid {info['cor']}; border-left: 6px solid {info['cor']}; border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
    <h3 style="color: {info['cor']}; margin-bottom: 15px; font-size: 20px;">
        {fundo_nome}
    </h3>
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
        <p style="margin-bottom: 10px; color: #000000;">
            <strong style="color: #000000;">📝 Resumo:</strong> {tese['resumo']}
        </p>
        <p style="margin-bottom: 10px; color: #000000;">
            <strong style="color: #000000;">📋 Condições:</strong>
        </p>
        <p style="white-space: pre-line; margin-left: 15px; font-size: 14px; color: #000000;">
            {tese['condicoes']}
        </p>
        <p style="margin-bottom: 10px; color: #000000;">
            <strong style="color: #000000;">⚡ Venda em 1 Minuto:</strong> {tese['venda_1min']}
        </p>
        <p style="margin-bottom: 0; color: #000000;">
            <strong style="color: #000000;">🎯 Perfil do Cliente:</strong> {tese['perfil']}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if links['material']:
                st.markdown(f"""
<a href="{links['material']}" target="_blank" style="text-decoration: none;">
    <button style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 14px;">
        📄 Material Publicitário
    </button>
</a>
""", unsafe_allow_html=True)
        
        with col2:
            if links['expert']:
                st.markdown(f"""
<a href="{links['expert']}" target="_blank" style="text-decoration: none;">
    <button style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 14px;">
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
    """Carrega dados APENAS da aba Base com validação completa"""
    try:
        # Carregar o Excel
        df_base = pd.read_excel('calendario_Renda_mais.xlsx', sheet_name='Base')
        
        # Limpar nomes das colunas (remover espaços extras)
        df_base.columns = df_base.columns.str.strip()
        
        # Validar se as colunas necessárias existem
        colunas_necessarias = ['Assessor', 'Cliente', 'Fundo', 'Aplicado', '%', 'Data']
        colunas_faltando = [col for col in colunas_necessarias if col not in df_base.columns]
        
        if colunas_faltando:
            st.error(f"❌ Colunas faltando no Excel: {', '.join(colunas_faltando)}")
            st.error(f"📋 Colunas encontradas: {', '.join(df_base.columns.tolist())}")
            st.info("""
            ✅ **Estrutura esperada do Excel:**
            - Coluna A: Assessor
            - Coluna B: Cliente  
            - Coluna C: Aplicado
            - Coluna D: Fundo
            - Coluna E: %
            - Coluna F: (pode ter outras colunas)
            - Coluna G: Data
            """)
            st.stop()
        
        # Verificar se há dados
        if df_base.empty:
            st.error("❌ O arquivo Excel está vazio!")
            st.stop()
        
        # Debug: mostrar primeiras linhas (apenas em desenvolvimento)
        # st.write("Debug - Primeiras linhas:", df_base.head())
        
        return df_base
        
    except FileNotFoundError:
        st.error("❌ Arquivo 'calendario_Renda_mais.xlsx' não encontrado!")
        st.error("📁 Certifique-se de que o arquivo está na mesma pasta do código.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro ao carregar Excel: {str(e)}")
        st.error(f"🔍 Tipo do erro: {type(e).__name__}")
        st.stop()

# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def main():
    """Função principal"""
    
    df_base = carregar_dados()
    
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'
    
    if st.session_state.pagina_atual == 'fundos':
        tela_fundos()
        return
    
    verificar_autenticacao(df_base)
    
    feriados = gerar_feriados(datetime.now().year)
    
    st.markdown(f"""
    <div class="header-sistema">
        <div class="titulo-principal">📅 Calendário Renda Mais - Tauari Investimentos</div>
        <div class="info-assessor">
            👤 Assessor: <strong>{st.session_state.nome_assessor}</strong> | 
            Código: <strong>{st.session_state.assessor_logado}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Validar se a coluna Assessor existe e processar
    try:
        df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip().str.replace('A', '', 1)
        df_base_filtrado = df_base[df_base['Assessor'] == str(st.session_state.assessor_logado)]
    except Exception as e:
        st.error(f"❌ Erro ao filtrar assessor: {str(e)}")
        st.error("🔍 Verifique se a coluna 'Assessor' existe no Excel")
        st.stop()
    
    if df_base_filtrado.empty:
        st.error("❌ Nenhum cliente encontrado para este assessor!")
        st.error(f"🔍 Assessor logado: {st.session_state.assessor_logado}")
        st.stop()
    
    st.markdown('<div class="cliente-selector"><h3>👥 SELECIONE O CLIENTE</h3>', unsafe_allow_html=True)
    
    # Validar se a coluna Cliente existe
    try:
        clientes = sorted(df_base_filtrado['Cliente'].unique())
    except Exception as e:
        st.error(f"❌ Erro ao buscar clientes: {str(e)}")
        st.error("🔍 Verifique se a coluna 'Cliente' existe no Excel")
        st.stop()
    
    cliente_selecionado = st.selectbox(
        "Cliente", 
        [""] + list(clientes), 
        label_visibility="collapsed", 
        key="cliente_select"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not cliente_selecionado:
        st.stop()
    
    # Filtrar fundos do cliente com validação
    try:
        fundos_cliente = df_base_filtrado[df_base_filtrado['Cliente'] == cliente_selecionado]
    except Exception as e:
        st.error(f"❌ Erro ao filtrar fundos do cliente: {str(e)}")
        st.stop()
    
    if fundos_cliente.empty:
        st.error("❌ Nenhum fundo encontrado para este cliente!")
        st.stop()
    
    # Validar se a coluna Fundo existe
    if 'Fundo' not in fundos_cliente.columns:
        st.error("❌ Coluna 'Fundo' não encontrada no Excel!")
        st.stop()

    # Inicializar fundo selecionado com segurança
    if 'fundo_selecionado' not in st.session_state:
        try:
            st.session_state.fundo_selecionado = fundos_cliente['Fundo'].iloc[0] if not fundos_cliente.empty else None
        except Exception as e:
            st.error(f"❌ Erro ao selecionar fundo inicial: {str(e)}")
            st.session_state.fundo_selecionado = None
    
    # Garantir que fundo_selecionado ainda existe na lista de fundos do cliente
    try:
        if st.session_state.fundo_selecionado is not None and st.session_state.fundo_selecionado not in fundos_cliente['Fundo'].values:
            st.session_state.fundo_selecionado = fundos_cliente['Fundo'].iloc[0] if not fundos_cliente.empty else None
    except Exception as e:
        st.warning(f"⚠️ Aviso ao validar fundo selecionado: {str(e)}")
        st.session_state.fundo_selecionado = fundos_cliente['Fundo'].iloc[0] if not fundos_cliente.empty else None
    
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        for _, fundo in fundos_cliente.iterrows():
            try:
                nome_fundo = str(fundo.get('Fundo', 'Fundo Desconhecido'))
                
                # Ler Valor Aplicado da Coluna C (Aplicado)
                try:
                    valor_aplicado = float(fundo.get('Aplicado', 0))
                except (ValueError, TypeError):
                    valor_aplicado = 0.0
                
                # Ler Rendimento % da Coluna E (%)
                try:
                    rendimento_str = str(fundo.get('%', '0')).strip()
                    if rendimento_str in ['-', '', 'nan', 'None']:
                        rendimento_percentual = 0.0
                    else:
                        rendimento_percentual = float(rendimento_str) * 100  # Converter para porcentagem
                except (ValueError, TypeError):
                    rendimento_percentual = 0.0
                
                # Ler Data da Coluna G (Data)
                try:
                    data_str = str(fundo.get('Data', '')).strip()
                    if data_str in ['-', '', 'nan', 'None']:
                        dia_pagamento = None
                    else:
                        dia_pagamento = int(float(data_str))
                except (ValueError, TypeError):
                    dia_pagamento = None
                
                info = buscar_info_fundo(nome_fundo, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES, fundo)
                
                # Calcular data de pagamento
                data_pagamento = None
                if dia_pagamento and dia_pagamento > 0:
                    try:
                        data_pagamento = calcular_dia_util(
                            st.session_state.ano_atual, 
                            st.session_state.mes_atual, 
                            dia_pagamento, 
                            feriados
                        )
                    except Exception:
                        pass
                
                data_texto = data_pagamento.strftime("%d/%m/%Y") if data_pagamento else "Não definida"
                
                classe_selecao = 'fundo-card-selecionado' if nome_fundo == st.session_state.fundo_selecionado else ''
                
                st.markdown(f"""
                <div class="fundo-card-container">
                    <div class="fundo-card {classe_selecao}" style="border-left-color: {info.get('cor', '#27ae60')}">
                        <div class="nome">{nome_fundo}</div>
                        <div class="info" style="margin-top: 8px;">
                            <div style="margin-bottom: 4px;">💰 <strong>Valor Aplicado:</strong> <span class="valor">R$ {valor_aplicado:,.2f}</span></div>
                            <div style="margin-bottom: 4px;">📅 <strong>Data Pagamento:</strong> {data_texto}</div>
                            <div>📈 <strong>Rendimento %:</strong> <span class="valor">{rendimento_percentual:.2f}%</span></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("📊", key=f"sel_{nome_fundo}", help=f"Selecionar {nome_fundo}"):
                    st.session_state.fundo_selecionado = nome_fundo
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Erro ao processar fundo: {str(e)}")
                continue

        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        if st.session_state.fundo_selecionado:
            # Buscar dados do fundo selecionado no dataframe
            fundo_selecionado_data = fundos_cliente[fundos_cliente['Fundo'] == st.session_state.fundo_selecionado]
            fundo_data = fundo_selecionado_data.iloc[0] if not fundo_selecionado_data.empty else None
            
            info = buscar_info_fundo(st.session_state.fundo_selecionado, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES, fundo_data)
            tese = info.get('tese', {})
            
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
    
    with col3:
        st.markdown('<div class="box"><div class="box-titulo">📅 CALENDÁRIO</div>', unsafe_allow_html=True)
        
        if 'mes_atual' not in st.session_state:
            st.session_state.mes_atual = datetime.now().month
            st.session_state.ano_atual = datetime.now().year
        
        col_p1, col_p2, col_p3 = st.columns([1, 3, 1])
        
        with col_p1:
            if st.button("◀️ Anterior", key="prev_mes"):
                st.session_state.mes_atual -= 1
                if st.session_state.mes_atual < 1:
                    st.session_state.mes_atual = 12
                    st.session_state.ano_atual -= 1
                st.rerun()
        
        with col_p2:
            st.markdown(f'<div style="text-align: center; padding: 8px; font-size: 18px; font-weight: bold; color: #1e4d2b;">{MESES_PT[st.session_state.mes_atual-1]} {st.session_state.ano_atual}</div>', unsafe_allow_html=True)
        
        with col_p3:
            if st.button("Próximo ▶️", key="next_mes"):
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
            try:
                info = buscar_info_fundo(fundo.get('Fundo', ''), MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES, fundo)
                
                # Usar a coluna Data do Excel
                try:
                    data_str = str(fundo.get('Data', '')).strip()
                    if data_str not in ['-', '', 'nan', 'None']:
                        dia_util = int(float(data_str))
                    else:
                        dia_util = None
                except (ValueError, TypeError):
                    dia_util = None
                
                if dia_util and dia_util > 0:
                    try:
                        data_pagamento = calcular_dia_util(st.session_state.ano_atual, st.session_state.mes_atual, dia_util, feriados)
                        if data_pagamento:
                            dia = data_pagamento.day
                            if dia not in eventos_mes:
                                eventos_mes[dia] = []
                            eventos_mes[dia].append({
                                'sigla': info.get('sigla', str(fundo.get('Fundo', 'N/A'))[:10]), 
                                'cor': info.get('cor', '#27ae60')
                            })
                    except Exception:
                        pass
            except Exception as e:
                continue  # Se houver erro, apenas pula esse fundo
        
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
