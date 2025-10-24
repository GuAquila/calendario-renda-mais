"""
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
======================================================
Sistema multi-assessor com senhas individuais
VERSÃO ATUALIZADA - 24/10/2025
Melhorias:
- Botões de Material e Expert na tela de Fundos
- Barra de seleção de cliente ajustada (fundo branco, menor)
- Valores aplicados atualizados do Excel
- Hover no nome do fundo para ver a tese (removido botão verde)
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
            
            # TÍTULO ATUALIZADO
            st.markdown("""
            <div class="login-titulo">
                <h2 style='margin: 10px 0; font-size: 24px;'>Calendário Renda Mais - Tauari Investimentos</h2>
                <p style='color: #7f8c8d; font-size: 14px; margin-top: 15px;'>Acesso restrito por Assessor (uso interno) - Última atualização 24/10</p>
            </div>
            """, unsafe_allow_html=True)
            
            # FORM PARA PERMITIR ENTER
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
# CSS
# ============================================

st.markdown("""
<style>
    .stApp {
        background: white !important;
    }
    
    /* Header do sistema */
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
    
    /* AJUSTE DA BARRA DE SELEÇÃO - MUDANÇA 2 */
    .cliente-selector {
        background: white !important;  /* Fundo branco */
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 25px;
        border: 2px solid #27ae60;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        max-width: 400px;  /* Diminuindo o tamanho */
    }
    
    .cliente-selector h3 {
        color: #1e4d2b !important;  /* Texto em preto/verde escuro */
        font-size: 16px !important;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
    }
    
    /* Ajustando o selectbox */
    .stSelectbox > div > div {
        background: white !important;
        color: #000000 !important;  /* Texto preto */
    }
    
    /* Container principal */
    .container-principal {
        display: flex;
        gap: 20px;
        margin-top: 20px;
    }
    
    /* Boxes padrão */
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
    
    /* Cards dos fundos - COM HOVER PARA TESE (MUDANÇA 4) */
    .fundo-card-container {
        margin-bottom: 15px;
        position: relative;
    }
    
    .fundo-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-left: 5px solid #27ae60;
        border-radius: 8px;
        padding: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .fundo-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        border-color: #27ae60;
    }
    
    /* TOOLTIP PARA TESE - MUDANÇA 4 */
    .fundo-card:hover::after {
        content: "🔍 Passe o mouse no nome para ver a tese";
        position: absolute;
        bottom: -25px;
        left: 0;
        background: #27ae60;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 11px;
        white-space: nowrap;
        z-index: 1000;
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
        position: relative;
        cursor: help;  /* Cursor de ajuda ao passar o mouse */
    }
    
    /* TOOLTIP DA TESE - MUDANÇA 4 */
    .fundo-card .nome::before {
        content: attr(data-tese);
        position: absolute;
        bottom: 100%;
        left: 0;
        background: #2c3e50;
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: normal;
        width: 350px;
        max-width: 350px;
        white-space: pre-wrap;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s, visibility 0.3s;
        z-index: 2000;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        line-height: 1.5;
        margin-bottom: 10px;
    }
    
    .fundo-card .nome:hover::before {
        opacity: 1;
        visibility: visible;
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
    
    /* Tese do fundo */
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
        position: relative;
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
# DADOS E CONFIGURAÇÕES
# ============================================

MESES_PT = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

# FERIADOS NACIONAIS
def gerar_feriados(ano):
    """Gera lista de feriados nacionais para o ano"""
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
    """Calcula o dia útil real do mês, pulando fins de semana e feriados"""
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

# DIAS DE PAGAMENTO (dia útil do mês)
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

# CORES DOS FUNDOS
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

# SIGLAS DOS FUNDOS (para o calendário)
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

# TESES DOS FUNDOS
MAPA_TESES = {
    'ARX FII Portfólio Renda CDI+ RL': {
        'resumo': 'Fundo de Investimento Imobiliário focado em CRIs com rentabilidade atrelada ao CDI+.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio/Longo prazo
• Liquidez: D+30 a D+60
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Fundo imobiliário com foco em CRIs que busca rentabilidade acima do CDI, oferecendo uma boa alternativa para renda passiva.',
        'perfil': 'Investidores que buscam renda recorrente com retornos superiores ao CDI através do mercado imobiliário.'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'resumo': 'Fundo de investimento em participações focado em infraestrutura com geração de renda.',
        'condicoes': '''• Rentabilidade: IPCA + spread
• Prazo: Longo prazo
• Liquidez: Baixa (prazo determinado)
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Fundo de infraestrutura que investe em ativos geradores de renda, protegidos contra inflação.',
        'perfil': 'Investidores que buscam proteção inflacionária e renda de longo prazo através de ativos de infraestrutura.'
    },
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': {
        'resumo': 'Fundo de renda fixa com objetivo de superar o CDI através de uma carteira diversificada.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio prazo
• Liquidez: D+30
• Público-alvo: Investidor geral''',
        'venda_1min': 'Fundo que busca retornos superiores ao CDI investindo em uma carteira diversificada de crédito privado.',
        'perfil': 'Investidores conservadores que buscam retornos superiores ao CDI com gestão ativa.'
    },
    'AZ Quest Panorama Renda CDI FI RL': {
        'resumo': 'Fundo de renda fixa com objetivo de superar o CDI através de uma carteira diversificada.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio prazo
• Liquidez: D+30
• Público-alvo: Investidor geral''',
        'venda_1min': 'Fundo que busca retornos superiores ao CDI investindo em uma carteira diversificada de crédito privado.',
        'perfil': 'Investidores conservadores que buscam retornos superiores ao CDI com gestão ativa.'
    },
    'BGR Galpões Logísticos - Cota Sênior': {
        'resumo': 'Fundo imobiliário focado em galpões logísticos com estrutura de cotas sênior.',
        'condicoes': '''• Rentabilidade: IPCA + spread
• Prazo: Médio/Longo prazo
• Liquidez: D+60
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Investimento em galpões logísticos com cota sênior, oferecendo menor risco e proteção inflacionária.',
        'perfil': 'Investidores que buscam renda no setor logístico com menor risco através da estrutura sênior.'
    },
    'BGR Galpões Logísticos - Cota Subordinada': {
        'resumo': 'Fundo imobiliário focado em galpões logísticos com estrutura de cotas subordinadas.',
        'condicoes': '''• Rentabilidade: Maior potencial de retorno
• Prazo: Médio/Longo prazo
• Liquidez: D+60
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Investimento em galpões logísticos com cota subordinada, oferecendo maior potencial de retorno.',
        'perfil': 'Investidores que aceitam maior risco em busca de retornos superiores no setor logístico.'
    },
    'Maua Lajes Corporativas Feeder FII RL - Senior': {
        'resumo': 'Fundo imobiliário focado em lajes corporativas com estrutura sênior.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio prazo
• Liquidez: D+30 a D+60
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Fundo de lajes corporativas com estrutura sênior, proporcionando renda estável do mercado corporativo.',
        'perfil': 'Investidores que buscam renda do mercado imobiliário corporativo com menor risco.'
    },
    'SPX CRI Portfolio Renda Mais': {
        'resumo': 'Fundo focado em Certificados de Recebíveis Imobiliários diversificado.',
        'condicoes': '''• Rentabilidade: IPCA/CDI + spread
• Prazo: Médio/Longo prazo
• Liquidez: D+30 a D+60
• Público-alvo: Investidores qualificados''',
        'venda_1min': 'Portfolio diversificado de CRIs que busca renda recorrente com proteção inflacionária.',
        'perfil': 'Investidores que buscam diversificação no mercado imobiliário através de CRIs.'
    },
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': {
        'resumo': 'Fundo de crédito privado que investe em direitos creditórios diversos.',
        'condicoes': '''• Rentabilidade: CDI + spread
• Prazo: Médio prazo
• Liquidez: D+30
• Público-alvo: Investidor geral''',
        'venda_1min': 'Fundo de crédito privado diversificado que busca retornos superiores ao CDI.',
        'perfil': 'Investidores moderados que buscam retornos atrativos através de crédito privado.'
    },
    'XP Renda Imobiliária Feeder FII RL': {
        'resumo': 'Fundo de fundos imobiliários que investe em FIIs geradores de renda.',
        'condicoes': '''• Rentabilidade: Distribuição mensal
• Prazo: Indeterminado
• Liquidez: D+30
• Público-alvo: Investidor geral''',
        'venda_1min': 'Fundo que investe em uma carteira diversificada de FIIs geradores de renda mensal.',
        'perfil': 'Investidores que buscam renda recorrente através de uma carteira diversificada de FIIs.'
    },
    'XP Habitat Renda Imobiliária Feeder FII': {
        'resumo': 'Fundo de fundos imobiliários focado em ativos residenciais.',
        'condicoes': '''• Rentabilidade: Distribuição mensal
• Prazo: Indeterminado
• Liquidez: D+30
• Público-alvo: Investidor geral''',
        'venda_1min': 'Fundo que investe em FIIs do setor residencial, oferecendo renda mensal.',
        'perfil': 'Investidores que buscam exposição ao mercado residencial através de FIIs.'
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

# LINKS DOS FUNDOS - MUDANÇA 1
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
    """Busca informações do fundo nos mapas"""
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
# TELA DE FUNDOS - COM BOTÕES DE LINKS (MUDANÇA 1)
# ============================================

def tela_fundos():
    """Tela de apresentação dos fundos com links"""
    
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
    
    # Botão para voltar ao login
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔙 Voltar ao Login", use_container_width=True):
            st.session_state.pagina_atual = 'login'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Lista de fundos com botões de links - MUDANÇA 1
    for fundo_nome in sorted(MAPA_TESES.keys()):
        info = buscar_info_fundo(fundo_nome, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
        tese = info['tese']
        links = info['links']
        
        # Card do fundo
        st.markdown(f"""
        <div style="background: white; border: 2px solid {info['cor']}; border-left: 6px solid {info['cor']}; 
                    border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
            <h3 style="color: {info['cor']}; margin-bottom: 15px; font-size: 20px;">
                {fundo_nome}
            </h3>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <p style="margin-bottom: 10px;"><strong>📝 Resumo:</strong> {tese['resumo']}</p>
                <p style="margin-bottom: 10px;"><strong>📋 Condições:</strong></p>
                <p style="white-space: pre-line; margin-left: 15px; font-size: 14px;">{tese['condicoes']}</p>
                <p style="margin-bottom: 10px;"><strong>⚡ Venda em 1 Minuto:</strong> {tese['venda_1min']}</p>
                <p style="margin-bottom: 0;"><strong>🎯 Perfil do Cliente:</strong> {tese['perfil']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # BOTÕES DE LINKS - MUDANÇA 1
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if links['material']:
                st.markdown(f"""
                <a href="{links['material']}" target="_blank" style="text-decoration: none;">
                    <button style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                                   color: white; border: none; padding: 12px 20px; border-radius: 8px; 
                                   font-weight: bold; cursor: pointer; width: 100%; font-size: 14px;
                                   transition: all 0.3s ease;">
                        📄 Material Publicitário
                    </button>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <button style="background: #95a5a6; color: white; border: none; padding: 12px 20px; 
                               border-radius: 8px; font-weight: bold; width: 100%; font-size: 14px; 
                               cursor: not-allowed;">
                    📄 Material Indisponível
                </button>
                """, unsafe_allow_html=True)
        
        with col2:
            if links['expert']:
                st.markdown(f"""
                <a href="{links['expert']}" target="_blank" style="text-decoration: none;">
                    <button style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                                   color: white; border: none; padding: 12px 20px; border-radius: 8px; 
                                   font-weight: bold; cursor: pointer; width: 100%; font-size: 14px;
                                   transition: all 0.3s ease;">
                        🎓 Expert XP
                    </button>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <button style="background: #95a5a6; color: white; border: none; padding: 12px 20px; 
                               border-radius: 8px; font-weight: bold; width: 100%; font-size: 14px; 
                               cursor: not-allowed;">
                    🎓 Expert Indisponível
                </button>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Aviso no final
    st.markdown("""
    <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #27ae60; margin-top: 30px;">
        <p style="color: #1e4d2b; font-weight: bold; margin-bottom: 10px;">⚠️ Links não cadastrados</p>
        <p style="color: #2c3e50; margin: 0;">
            Para configurar os links dos fundos, acesse o arquivo Excel na aba "Fundos" e preencha as colunas:
            <strong>Link Expert</strong> e <strong>Link Material</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# CARREGAR DADOS
# ============================================

@st.cache_data
def carregar_dados():
    """Carrega a base de dados do Excel - MUDANÇA 3"""
    try:
        # Carregar a aba Base
        df = pd.read_excel('calendario_Renda_mais.xlsx', sheet_name='Base')
        
        # Garantir que a coluna Aplicação seja tratada corretamente
        if 'Aplicação' in df.columns:
            # Renomear para Financeiro para compatibilidade com o código
            df = df.rename(columns={'Aplicação': 'Financeiro'})
        
        return df
    except FileNotFoundError:
        st.error("❌ Arquivo 'calendario_Renda_mais.xlsx' não encontrado!")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        st.stop()

# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def main():
    """Função principal do sistema"""
    
    # Carregar dados
    df_base = carregar_dados()
    
    # Verificar autenticação
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'
    
    # TELA DE FUNDOS
    if st.session_state.pagina_atual == 'fundos':
        tela_fundos()
        return
    
    # TELA DE LOGIN
    verificar_autenticacao(df_base)
    
    # SISTEMA PRINCIPAL (após autenticação)
    feriados = gerar_feriados(datetime.now().year)
    
    # Header do sistema
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
    
    # Filtrar apenas clientes do assessor logado - MUDANÇA 3
    df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
    df_base_filtrado = df_base[df_base['Assessor'] == str(st.session_state.assessor_logado)]
    
    if df_base_filtrado.empty:
        st.error("❌ Nenhum cliente encontrado para este assessor!")
        st.stop()
    
    # SELETOR DE CLIENTE - MUDANÇA 2 (ajustado CSS acima)
    st.markdown('<div class="cliente-selector"><h3>👥 SELECIONE O CLIENTE</h3>', unsafe_allow_html=True)
    
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
    
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            
            # MUDANÇA 3 - Usar coluna Financeiro (que foi renomeada de Aplicação)
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
            tese = info['tese']
            
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
            
            classe_selecao = 'fundo-card-selecionado' if ativo == st.session_state.fundo_selecionado else ''
            
            # MUDANÇA 4 - Criar tooltip com a tese para exibir ao passar o mouse
            tese_tooltip = f"{tese.get('resumo', '')}\\n\\n📋 Condições:\\n{tese.get('condicoes', '')}\\n\\n⚡ Venda em 1 Minuto:\\n{tese.get('venda_1min', '')}\\n\\n🎯 Perfil:\\n{tese.get('perfil', '')}"
            
            st.markdown(f"""
            <div class="fundo-card-container">
                <div class="fundo-card {classe_selecao}" style="border-left-color: {info.get('cor', '#27ae60')}">
                    <div class="nome" data-tese="{tese_tooltip}" title="Passe o mouse para ver a tese">{ativo}</div>
                    <div class="info" style="margin-top: 8px;">
                        <div style="margin-bottom: 4px;">💰 <strong>Valor Aplicado:</strong> <span class="valor">R$ {valor_aplicado:,.2f}</span></div>
                        <div style="margin-bottom: 4px;">📅 <strong>Data Pagamento:</strong> {data_texto}</div>
                        <div style="margin-bottom: 4px;">📈 <strong>% Líquido:</strong> <span class="valor">{percentual_liquido:.2f}%</span></div>
                        <div>💵 <strong>Valor Líquido:</strong> <span class="valor">R$ {valor_liquido_cupom:,.2f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # MUDANÇA 4 - Removido o botão verde que abria a tese
            # Agora a tese aparece ao passar o mouse sobre o nome do fundo
            if st.button("📊 Selecionar", key=f"select_{ativo}", help=f"Selecionar: {ativo}"):
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
