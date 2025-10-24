"""
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
======================================================
Sistema multi-assessor com senhas individuais
VERSÃO ATUALIZADA - 24/10/2025
CORREÇÕES IMPLEMENTADAS:
1. Links dos fundos adicionados na tela "Conheça nossos Fundos"
2. Barra de seleção de clientes com tamanho reduzido
3. Valor Aplicado corrigido da aba "Base" do Excel
4. Seleção de fundo ao passar o mouse (sem botão verde)
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
    """Valida a senha do assessor"""
    if codigo_assessor not in ASSESSORES:
        return False, None
    
    nome_assessor, senha_esperada = ASSESSORES[codigo_assessor]
    if senha == senha_esperada:
        return True, nome_assessor
    return False, None

def verificar_autenticacao(df_base):
    """Tela de login por assessor - ATUALIZADA COM ENTER"""
    
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
                                df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
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
# CSS - ATUALIZADO COM HOVER PARA SELEÇÃO
# ============================================

st.markdown("""
<style>
    /* RESET E BASE */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    }
    
    .container-principal {
        padding: 20px;
        max-width: 2200px;
        margin: 0 auto;
    }
    
    /* CABEÇALHO */
    .header {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }
    
    .header h1 {
        font-size: 32px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-info {
        text-align: right;
    }
    
    .header-info div {
        font-size: 14px;
        margin: 5px 0;
        opacity: 0.95;
    }
    
    /* SELETOR DE CLIENTE - TAMANHO REDUZIDO */
    .stSelectbox {
        max-width: 400px !important;
        margin: 0 auto 25px auto;
    }
    
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #27ae60;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        color: #1e4d2b;
    }
    
    /* BOXES */
    .box {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        height: 100%;
    }
    
    .box-titulo {
        font-size: 20px;
        font-weight: bold;
        color: #1e4d2b;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 3px solid #27ae60;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .box-conteudo {
        overflow-y: auto;
        max-height: 750px;
        padding-right: 10px;
    }
    
    /* CARDS DE FUNDOS - COM HOVER */
    .fundo-card-container {
        margin-bottom: 15px;
    }
    
    .fundo-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-left: 5px solid #27ae60;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .fundo-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
        background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%);
    }
    
    .fundo-card-selecionado {
        background: linear-gradient(135deg, #c8e6c9 0%, #e8f5e9 100%);
        border-left-width: 8px;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4);
        transform: translateX(5px);
    }
    
    .fundo-card .nome {
        font-weight: bold;
        font-size: 15px;
        color: #1e4d2b;
        margin-bottom: 10px;
        line-height: 1.4;
    }
    
    .fundo-card .info {
        font-size: 13px;
        color: #34495e;
        line-height: 1.6;
    }
    
    .fundo-card .valor {
        color: #27ae60;
        font-weight: bold;
    }
    
    /* ESCONDER BOTÃO (NÃO É MAIS NECESSÁRIO) */
    .fundo-card-container button {
        display: none !important;
    }
    
    /* TESE */
    .tese-texto {
        font-size: 15px;
        line-height: 1.8;
        color: #2c3e50;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 10px;
        max-height: 750px;
        overflow-y: auto;
    }
    
    .tese-texto h4 {
        color: #1e4d2b;
        margin-top: 20px;
        margin-bottom: 10px;
        font-size: 16px;
    }
    
    .tese-texto p {
        margin-bottom: 15px;
        text-align: justify;
    }
    
    /* CALENDÁRIO */
    .calendario-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        margin-top: 15px;
    }
    
    .cal-header {
        background: #1e4d2b;
        color: white;
        padding: 12px 5px;
        text-align: center;
        font-weight: bold;
        font-size: 13px;
        border-radius: 5px;
    }
    
    .cal-dia {
        background: white;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 8px;
        min-height: 90px;
        position: relative;
        transition: all 0.2s ease;
    }
    
    .cal-dia:hover {
        background: #f0f0f0;
        transform: scale(1.02);
    }
    
    .cal-dia.fim-semana {
        background: #f8f9fa;
    }
    
    .cal-dia .numero {
        font-weight: bold;
        font-size: 14px;
        color: #2c3e50;
        margin-bottom: 5px;
    }
    
    .cal-evento {
        background: #27ae60;
        color: white;
        padding: 3px 6px;
        border-radius: 4px;
        font-size: 11px;
        margin-top: 3px;
        font-weight: 600;
        text-align: center;
    }
    
    /* BOTÕES */
    .stButton button {
        background: #27ae60;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: #1e8449;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.4);
    }
    
    /* PÁGINA DE FUNDOS */
    .fundo-info-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 6px solid #27ae60;
        transition: all 0.3s ease;
    }
    
    .fundo-info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(39, 174, 96, 0.2);
    }
    
    .fundo-nome {
        font-size: 22px;
        font-weight: bold;
        color: #1e4d2b;
        margin-bottom: 15px;
    }
    
    .fundo-link {
        display: inline-block;
        background: #27ae60;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        margin: 10px 10px 10px 0;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .fundo-link:hover {
        background: #1e8449;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.4);
        text-decoration: none;
        color: white;
    }
    
    /* SCROLLBAR */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #27ae60;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1e8449;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# JAVASCRIPT PARA SELEÇÃO POR HOVER
# ============================================

st.markdown("""
<script>
// Adicionar evento de hover para seleção de fundos
document.addEventListener('DOMContentLoaded', function() {
    // Observar mudanças no DOM
    const observer = new MutationObserver(function(mutations) {
        const fundoCards = document.querySelectorAll('.fundo-card');
        fundoCards.forEach(card => {
            if (!card.hasAttribute('data-hover-enabled')) {
                card.setAttribute('data-hover-enabled', 'true');
                card.addEventListener('mouseenter', function() {
                    // Encontrar o botão escondido dentro do card
                    const container = this.closest('.fundo-card-container');
                    const button = container.querySelector('button');
                    if (button) {
                        button.click();
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
</script>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURAÇÕES DE DADOS
# ============================================

MESES_PT = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

FERIADOS_NACIONAIS_2025 = [
    date(2025, 1, 1),   # Confraternização Universal
    date(2025, 3, 4),   # Carnaval
    date(2025, 4, 18),  # Paixão de Cristo
    date(2025, 4, 21),  # Tiradentes
    date(2025, 5, 1),   # Dia do Trabalho
    date(2025, 6, 19),  # Corpus Christi
    date(2025, 9, 7),   # Independência
    date(2025, 10, 12), # Nossa Senhora Aparecida
    date(2025, 11, 2),  # Finados
    date(2025, 11, 15), # Proclamação da República
    date(2025, 11, 20), # Consciência Negra
    date(2025, 12, 25), # Natal
]

# Mapas de configuração dos fundos
MAPA_PAGAMENTOS = {
    'ARX FII Portfólio Renda CDI+ RL': 4,
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 8,
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 5,
    'AZ Quest Panorama Renda CDI FI RL': 5,
    'Maua Lajes Corporativas Feeder FII RL - Senior': 5,
    'SPX CRI Portfolio Renda Mais': 5,
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': 5,
    'XP Renda Imobiliária Feeder FII RL': 5,
    'XP Habitat Renda Imobiliária Feeder FII': 5,
    'Valora CRI CDI Renda+ FII RL': 5,
}

MAPA_CORES = {
    'ARX FII Portfólio Renda CDI+ RL': '#27ae60',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': '#3498db',
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': '#9b59b6',
    'AZ Quest Panorama Renda CDI FI RL': '#9b59b6',
    'Maua Lajes Corporativas Feeder FII RL - Senior': '#e74c3c',
    'SPX CRI Portfolio Renda Mais': '#f39c12',
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': '#1abc9c',
    'XP Renda Imobiliária Feeder FII RL': '#e67e22',
    'XP Habitat Renda Imobiliária Feeder FII': '#34495e',
    'Valora CRI CDI Renda+ FII RL': '#c0392b',
}

MAPA_SIGLAS = {
    'ARX FII Portfólio Renda CDI+ RL': 'ARX',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 'AZ Infra',
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 'AZ Panorama',
    'AZ Quest Panorama Renda CDI FI RL': 'AZ Panorama',
    'Maua Lajes Corporativas Feeder FII RL - Senior': 'Maua',
    'SPX CRI Portfolio Renda Mais': 'SPX',
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': 'Solis',
    'XP Renda Imobiliária Feeder FII RL': 'XP Renda',
    'XP Habitat Renda Imobiliária Feeder FII': 'XP Habitat',
    'Valora CRI CDI Renda+ FII RL': 'Valora',
}

MAPA_TESES = {
    'ARX FII Portfólio Renda CDI+ RL': {
        'resumo': 'Fundo de investimento imobiliário focado em ativos de renda com proteção CDI+.',
        'condicoes': '''Taxa de administração: 0,50% a.a.
Taxa de performance: Não há
Prazo: Indeterminado
Liquidez: D+30 após conversão (D+60 total)
Rendimento alvo: CDI + 1,15% a.a.''',
        'venda_1min': 'Invista em imóveis com renda garantida acima do CDI, diversificação automática e liquidez em 60 dias.',
        'perfil': 'Investidores que buscam renda passiva com segurança e querem exposição imobiliária sem gestão direta.'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'resumo': 'Fundo de investimento em participações focado em infraestrutura com rendimentos atrativos.',
        'condicoes': '''Taxa de administração: 1,00% a.a.
Taxa de performance: 20% sobre CDI + 4%
Prazo: 5 anos
Liquidez: Baixa (prazo determinado)
Rendimento alvo: CDI + 4,50% a.a.''',
        'venda_1min': 'Invista em projetos de infraestrutura rentáveis com proteção inflacionária e alta previsibilidade de rendimentos.',
        'perfil': 'Investidores arrojados que buscam altos rendimentos e podem abrir mão de liquidez no médio prazo.'
    },
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': {
        'resumo': 'Fundo multimercado focado em renda fixa com estratégia conservadora.',
        'condicoes': '''Taxa de administração: 0,70% a.a.
Taxa de performance: Não há
Prazo: Indeterminado
Liquidez: D+30
Rendimento alvo: CDI + 0,50% a.a.''',
        'venda_1min': 'Fundo de renda fixa que busca superar o CDI com baixo risco e boa liquidez.',
        'perfil': 'Investidores conservadores que buscam rentabilidade acima da poupança com segurança.'
    },
    'AZ Quest Panorama Renda CDI FI RL': {
        'resumo': 'Fundo multimercado focado em renda fixa com estratégia conservadora.',
        'condicoes': '''Taxa de administração: 0,70% a.a.
Taxa de performance: Não há
Prazo: Indeterminado
Liquidez: D+30
Rendimento alvo: CDI + 0,50% a.a.''',
        'venda_1min': 'Fundo de renda fixa que busca superar o CDI com baixo risco e boa liquidez.',
        'perfil': 'Investidores conservadores que buscam rentabilidade acima da poupança com segurança.'
    },
    'Maua Lajes Corporativas Feeder FII RL - Senior': {
        'resumo': 'Fundo imobiliário focado em lajes corporativas AAA com contratos de longo prazo.',
        'condicoes': '''Taxa de administração: 0,60% a.a.
Taxa de performance: Não há
Prazo: 5 anos
Liquidez: Baixa (prazo determinado)
Rendimento alvo: IPCA + 7,50% a.a.''',
        'venda_1min': 'Invista em escritórios premium com inquilinos de primeira linha e rendimentos corrigidos pela inflação.',
        'perfil': 'Investidores que buscam proteção inflacionária e renda de longo prazo em ativos de qualidade.'
    },
    'SPX CRI Portfolio Renda Mais': {
        'resumo': 'Fundo de CRI diversificado com foco em crédito imobiliário de qualidade.',
        'condicoes': '''Taxa de administração: 0,60% a.a.
Taxa de performance: Não há
Prazo: Indeterminado
Liquidez: D+90
Rendimento alvo: CDI + 2,00% a.a.''',
        'venda_1min': 'Diversifique em crédito imobiliário com garantias reais e rendimentos superiores ao CDI.',
        'perfil': 'Investidores moderados que buscam renda com garantia imobiliária e boa rentabilidade.'
    },
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': {
        'resumo': 'Fundo de crédito privado diversificado com foco em segurança e rentabilidade.',
        'condicoes': '''Taxa de administração: 0,80% a.a.
Taxa de performance: Não há
Prazo: Indeterminado
Liquidez: D+60
Rendimento alvo: CDI + 1,80% a.a.''',
        'venda_1min': 'Invista em uma carteira diversificada de crédito privado com análise criteriosa de risco.',
        'perfil': 'Investidores que buscam rentabilidade acima do CDI com gestão profissional de crédito.'
    },
    'XP Renda Imobiliária Feeder FII RL': {
        'resumo': 'Fundo de fundos imobiliários com diversificação automática em FIIs de qualidade.',
        'condicoes': '''Taxa de administração: 0,50% a.a.
Taxa de performance: Não há
Prazo: Indeterminado
Liquidez: D+30
Rendimento alvo: CDI + 1,50% a.a.''',
        'venda_1min': 'Diversifique em vários FIIs de uma vez com gestão especializada e boa liquidez.',
        'perfil': 'Investidores que querem exposição ao mercado imobiliário sem escolher fundos individualmente.'
    },
    'XP Habitat Renda Imobiliária Feeder FII': {
        'resumo': 'Fundo de fundos imobiliários focado em imóveis residenciais e comerciais.',
        'condicoes': '''Taxa de administração: 0,50% a.a.
Taxa de performance: Não há
Prazo: Indeterminado
Liquidez: D+30
Rendimento alvo: CDI + 1,40% a.a.''',
        'venda_1min': 'Invista no mercado imobiliário brasileiro de forma diversificada e profissional.',
        'perfil': 'Investidores que buscam renda passiva com diversificação no setor imobiliário.'
    },
    'Valora CRI CDI Renda+ FII RL': {
        'resumo': 'Fundo de CRI com foco em crédito imobiliário selecionado e rentabilidade acima do CDI.',
        'condicoes': '''Taxa de administração: 0,60% a.a.
Taxa de performance: Não há
Prazo: Indeterminado
Liquidez: D+60
Rendimento alvo: CDI + 2,20% a.a.''',
        'venda_1min': 'Acesse crédito imobiliário de qualidade com garantias e rendimentos atrativos.',
        'perfil': 'Investidores que buscam renda previsível com lastro imobiliário e boa rentabilidade.'
    },
}

def buscar_info_fundo(nome_fundo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses):
    """Busca informações do fundo nos mapas"""
    return {
        'dia_util': mapa_pagamentos.get(nome_fundo, 5),
        'cor': mapa_cores.get(nome_fundo, '#27ae60'),
        'sigla': mapa_siglas.get(nome_fundo, nome_fundo[:10]),
        'tese': mapa_teses.get(nome_fundo, {
            'resumo': 'Informações do fundo não disponíveis.',
            'condicoes': '',
            'venda_1min': '',
            'perfil': ''
        })
    }

def calcular_dia_util(ano, mes, dia_util_alvo, feriados):
    """Calcula o dia útil do mês considerando feriados"""
    try:
        primeiro_dia = date(ano, mes, 1)
        ultimo_dia = date(ano, mes, calendar.monthrange(ano, mes)[1])
        
        data_atual = primeiro_dia
        dias_uteis_contados = 0
        
        while data_atual <= ultimo_dia:
            eh_fim_semana = data_atual.weekday() >= 5
            eh_feriado = data_atual in feriados
            
            if not eh_fim_semana and not eh_feriado:
                dias_uteis_contados += 1
                if dias_uteis_contados == dia_util_alvo:
                    return data_atual
            
            data_atual += timedelta(days=1)
        
        return None
    except:
        return None

@st.cache_data
def carregar_dados_excel():
    """Carrega os dados do Excel - ATUALIZADO"""
    try:
        # Nome do arquivo Excel
        excel_file = 'calendario_Renda_mais.xlsx'
        
        # Carregar a aba Base
        df_base = pd.read_excel(excel_file, sheet_name='Base')
        
        # Converter colunas para o tipo correto
        df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
        df_base['Cliente'] = df_base['Cliente'].astype(str).str.strip()
        df_base['Ativo'] = df_base['Ativo'].astype(str).str.strip()
        
        # CORREÇÃO: Renomear coluna para 'Financeiro' para manter compatibilidade
        if 'Aplicação' in df_base.columns:
            df_base['Financeiro'] = df_base['Aplicação']
        
        # Carregar a aba Fundos para os links
        df_fundos = pd.read_excel(excel_file, sheet_name='Fundos', header=None)
        
        # Processar os links dos fundos (linha 1 tem os cabeçalhos)
        links_fundos = {}
        for idx in range(2, len(df_fundos)):  # Começa da linha 2 (índice 2)
            fundo = df_fundos.iloc[idx, 1]  # Coluna 1: Nome do Fundo
            link_expert = df_fundos.iloc[idx, 2]  # Coluna 2: Link Expert
            link_material = df_fundos.iloc[idx, 3]  # Coluna 3: Link Material
            
            if pd.notna(fundo):
                links_fundos[str(fundo).strip()] = {
                    'expert': str(link_expert) if pd.notna(link_expert) else '',
                    'material': str(link_material) if pd.notna(link_material) else ''
                }
        
        return df_base, links_fundos
        
    except FileNotFoundError:
        st.error("❌ Arquivo 'calendario_Renda_mais.xlsx' não encontrado!")
        st.info("📁 Certifique-se de que o arquivo está na mesma pasta do código.")
        return None, None
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return None, None

def pagina_fundos(links_fundos):
    """Página de informações dos fundos - ATUALIZADA COM LINKS"""
    st.markdown('<div class="header"><div class="header-content">', unsafe_allow_html=True)
    st.markdown('<h1>📚 Conheça nossos Fundos Renda Mais</h1>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Verificar se há links cadastrados
    if not links_fundos or len(links_fundos) == 0:
        st.warning("⚠️ Links não cadastrados")
        st.info("📋 Configure a aba 'Fundos' no Excel: Fundo, Link Expert, Link Material")
        
        if st.button("← Voltar para Login"):
            st.session_state.pagina_atual = 'login'
            st.rerun()
        st.stop()
    
    # Mostrar cada fundo com seus links
    for fundo_nome, links in links_fundos.items():
        st.markdown(f"""
        <div class="fundo-info-card">
            <div class="fundo-nome">{fundo_nome}</div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if links['expert']:
                st.markdown(f'''
                <a href="{links['expert']}" target="_blank" class="fundo-link">
                    🎓 Expert XP
                </a>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('<span style="color: #999;">Link Expert não disponível</span>', unsafe_allow_html=True)
        
        with col2:
            if links['material']:
                st.markdown(f'''
                <a href="{links['material']}" target="_blank" class="fundo-link">
                    📄 Material Publicitário
                </a>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('<span style="color: #999;">Link Material não disponível</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("← Voltar para Login", key="btn_voltar"):
        st.session_state.pagina_atual = 'login'
        st.rerun()

def main():
    """Função principal do aplicativo"""
    
    # Carregar dados do Excel
    df_base, links_fundos = carregar_dados_excel()
    
    if df_base is None:
        st.stop()
    
    # Inicializar feriados
    feriados = FERIADOS_NACIONAIS_2025
    
    # Verificar qual página mostrar
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'
    
    if st.session_state.pagina_atual == 'fundos':
        pagina_fundos(links_fundos)
        return
    
    # Verificar autenticação
    verificar_autenticacao(df_base)
    
    # Filtrar base por assessor logado
    assessor_codigo = st.session_state.assessor_logado
    assessor_nome = st.session_state.nome_assessor
    
    df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
    df_base_filtrado = df_base[df_base['Assessor'] == str(assessor_codigo)].copy()
    
    if df_base_filtrado.empty:
        st.error(f"❌ Nenhum cliente encontrado para o Assessor {assessor_codigo}")
        st.stop()
    
    # Cabeçalho do sistema
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.markdown('<div class="header-content">', unsafe_allow_html=True)
    
    col_h1, col_h2 = st.columns([3, 1])
    
    with col_h1:
        st.markdown(f'<h1>🌳 Calendário Renda Mais - Tauari Investimentos</h1>', unsafe_allow_html=True)
    
    with col_h2:
        st.markdown(f'''
        <div class="header-info">
            <div>👤 <strong>{assessor_nome}</strong></div>
            <div>🏢 Assessor: {assessor_codigo}</div>
            <div>👥 {len(df_base_filtrado['Cliente'].unique())} clientes</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    if st.button("🚪 Sair", key="btn_sair"):
        st.session_state.autenticado = False
        st.session_state.assessor_logado = None
        st.session_state.nome_assessor = None
        st.session_state.pagina_atual = 'login'
        st.rerun()
    
    # SELETOR DE CLIENTE - TAMANHO REDUZIDO
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    clientes_unicos = sorted(df_base_filtrado['Cliente'].unique())
    
    if 'cliente_selecionado' not in st.session_state or st.session_state.cliente_selecionado not in clientes_unicos:
        st.session_state.cliente_selecionado = clientes_unicos[0] if clientes_unicos else None
    
    # CORREÇÃO 2: Seletor com tamanho reduzido (via CSS)
    cliente_selecionado = st.selectbox(
        "🔍 Selecione o Cliente:",
        clientes_unicos,
        index=clientes_unicos.index(st.session_state.cliente_selecionado) if st.session_state.cliente_selecionado in clientes_unicos else 0,
        key="select_cliente"
    )
    
    st.session_state.cliente_selecionado = cliente_selecionado
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not cliente_selecionado:
        st.stop()
    
    fundos_cliente = df_base_filtrado[df_base_filtrado['Cliente'] == cliente_selecionado]

    if 'fundo_selecionado' not in st.session_state or st.session_state.fundo_selecionado not in fundos_cliente['Ativo'].values:
        if not fundos_cliente.empty:
            st.session_state.fundo_selecionado = fundos_cliente['Ativo'].iloc[0]
        else:
            st.session_state.fundo_selecionado = None
    
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            
            # CORREÇÃO 3: Pegar valor correto da coluna 'Financeiro' (que vem de 'Aplicação')
            try:
                valor_aplicado = float(fundo['Financeiro'])
            except:
                valor_aplicado = 0.0
            
            try:
                percentual_liquido = float(fundo.get('Rendimento %', 0))
            except:
                percentual_liquido = 0.0
            
            valor_liquido_cupom = valor_aplicado * (percentual_liquido / 100)
            
            info = buscar_info_fundo(ativo, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
            
            data_pagamento = None
            dia_util = info.get('dia_util')
            
            if dia_util and dia_util > 0:
                try:
                    data_pagamento = calcular_dia_util(
                        st.session_state.ano_atual if 'ano_atual' in st.session_state else datetime.now().year, 
                        st.session_state.mes_atual if 'mes_atual' in st.session_state else datetime.now().month, 
                        dia_util, 
                        feriados
                    )
                except:
                    pass
            
            data_texto = data_pagamento.strftime("%d/%m/%Y") if data_pagamento else "Não definida"
            
            classe_selecao = 'fundo-card-selecionado' if ativo == st.session_state.fundo_selecionado else ''
            
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
            
            # CORREÇÃO 4: Botão escondido (CSS) que será acionado pelo hover
            if st.button(" ", key=f"select_{ativo}", help=f"Ver tese: {ativo}"):
                st.session_state.fundo_selecionado = ativo
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        fundo_para_tese = st.session_state.fundo_selecionado
        
        if fundo_para_tese:
            info = buscar_info_fundo(fundo_para_tese, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
            tese = info.get('tese', {})
            
            st.markdown(f"""
            <div class="tese-texto">
                <strong style="color: {info.get('cor', '#27ae60')};">{fundo_para_tese}</strong>
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
            if st.button("◀ Mês Anterior", key="prev_mes"):
                st.session_state.mes_atual -= 1
                if st.session_state.mes_atual < 1:
                    st.session_state.mes_atual = 12
                    st.session_state.ano_atual -= 1
                st.rerun()
        
        with col_p2:
            st.markdown(f'<div style="text-align: center; padding: 8px; font-size: 18px; font-weight: bold; color: #1e4d2b;">{MESES_PT[st.session_state.mes_atual-1]} {st.session_state.ano_atual}</div>', unsafe_allow_html=True)
        
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
