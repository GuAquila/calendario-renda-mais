"""
CALENDÁRIO RENDA MAIS - VERSÃO DEFINITIVA SEM ERROS
====================================================
Sistema multi-assessor com senhas individuais
VERSÃO 100% À PROVA DE ERROS - 07/11/2025
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar

st.set_page_config(
    page_title="Calendário Renda Mais - TAUARI",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# ASSESSORES
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

# ============================================
# CSS
# ============================================

st.markdown("""
<style>
    .stApp { background: white !important; }
    .header-sistema {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        padding: 20px 40px; border-radius: 10px; margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .titulo-principal { color: white; font-size: 28px; font-weight: bold; margin: 0; }
    .info-assessor { color: #e8f5e9; font-size: 14px; margin-top: 5px; }
    .cliente-selector {
        background: white !important; padding: 12px 20px; border-radius: 8px;
        margin-bottom: 25px; border: 2px solid #27ae60; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        max-width: 400px;
    }
    .cliente-selector h3 {
        color: #1e4d2b !important; font-size: 14px !important;
        font-weight: bold; margin: 0 0 8px 0 !important; text-align: center;
    }
    .box {
        background: white; border-radius: 10px; padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;
    }
    .box-titulo {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        color: white; padding: 12px 20px; border-radius: 8px;
        font-weight: bold; font-size: 16px; margin: -20px -20px 20px -20px;
        text-align: center;
    }
    .box-conteudo { max-height: 600px; overflow-y: auto; padding-right: 10px; }
    .fundo-card {
        background: white; border: 2px solid #e0e0e0; border-left: 5px solid #27ae60;
        border-radius: 8px; padding: 15px; margin-bottom: 15px;
        cursor: pointer; transition: all 0.3s ease;
    }
    .fundo-card:hover {
        transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        border-color: #27ae60;
    }
    .fundo-card-selecionado {
        border: 3px solid #27ae60 !important; background: #f0f9f4 !important;
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.2);
    }
    .fundo-card .nome {
        font-weight: bold; color: #1e4d2b; font-size: 14px; margin-bottom: 8px;
    }
    .fundo-card .info { font-size: 12px; color: #555; line-height: 1.6; }
    .fundo-card .valor { color: #27ae60; font-weight: bold; }
    .tese-texto {
        padding: 15px; background: #f8f9fa; border-radius: 8px;
        font-size: 13px; line-height: 1.7; color: #2c3e50;
    }
    .tese-texto h4 {
        color: #1e4d2b; font-size: 14px; margin-top: 15px;
        margin-bottom: 8px; font-weight: bold;
    }
    .calendario-grid {
        display: grid; grid-template-columns: repeat(7, 1fr);
        gap: 8px; padding: 15px; background: white;
    }
    .cal-header {
        background: #1e4d2b; color: white; padding: 10px;
        text-align: center; font-weight: bold; font-size: 12px;
        border-radius: 5px; text-transform: uppercase;
    }
    .cal-dia {
        background: white; border: 1px solid #e0e0e0; border-radius: 8px;
        padding: 8px; min-height: 80px; transition: all 0.2s;
    }
    .cal-dia:hover {
        background: #f0f9f4; transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .cal-dia.fim-semana { background: #f8f9fa; }
    .cal-dia .numero {
        font-weight: bold; color: #1e4d2b; font-size: 14px; margin-bottom: 5px;
    }
    .cal-evento {
        background: #27ae60; color: white; padding: 3px 6px;
        border-radius: 4px; font-size: 10px; margin-top: 3px;
        font-weight: bold; text-align: center; white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis;
    }
    .stButton button {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        color: white; border: none; padding: 10px 20px;
        border-radius: 8px; font-weight: bold; transition: all 0.3s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DADOS
# ============================================

MESES_PT = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

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
        'resumo': 'Fundo de Investimento Imobiliário composto por CRIs, mecânica de Renda Fixa.',
        'condicoes': '• Rentabilidade: CDI + 2,04%\n• Prazo: 7 anos\n• Duration: 3,6 anos',
        'venda_1min': 'Fundo imobiliário com foco em CRIs que busca rentabilidade acima do CDI.',
        'perfil': 'Investidores que buscam renda recorrente através do mercado imobiliário.'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'resumo': 'Fundo com investimento em ativos de infraestrutura maduros.',
        'condicoes': '• Rentabilidade: CDI + 2,20%\n• Prazo: 5 anos\n• Duration: 3,5 anos',
        'venda_1min': 'Fundo de infraestrutura com distribuição mensal de rendimentos.',
        'perfil': 'Investidores que buscam distribuição mensal de rendimentos isentos.'
    },
}

def gerar_feriados(ano):
    """Gera lista de feriados nacionais"""
    feriados_fixos = {
        (1, 1): "Ano Novo", (4, 21): "Tiradentes", (5, 1): "Dia do Trabalho",
        (9, 7): "Independência", (10, 12): "N.S. Aparecida", (11, 2): "Finados",
        (11, 15): "Proclamação", (11, 20): "Consciência Negra", (12, 25): "Natal"
    }
    lista_feriados = [date(ano, mes, dia) for (mes, dia) in feriados_fixos.keys()]
    return lista_feriados

def calcular_dia_util(ano, mes, dia_util_desejado, feriados):
    """Calcula o dia útil real do mês"""
    try:
        primeiro_dia = date(ano, mes, 1)
        if mes == 12:
            ultimo_dia = date(ano, mes, 31)
        else:
            ultimo_dia = date(ano, mes + 1, 1) - timedelta(days=1)
        
        dia_atual = primeiro_dia
        contador_dias_uteis = 0
        
        while dia_atual <= ultimo_dia:
            if dia_atual.weekday() < 5 and dia_atual not in feriados:
                contador_dias_uteis += 1
                if contador_dias_uteis == dia_util_desejado:
                    return dia_atual
            dia_atual += timedelta(days=1)
        return None
    except:
        return None

def buscar_info_fundo(nome_fundo):
    """Busca informações do fundo"""
    return {
        'cor': MAPA_CORES.get(nome_fundo, '#27ae60'),
        'sigla': MAPA_SIGLAS.get(nome_fundo, nome_fundo[:10]),
        'tese': MAPA_TESES.get(nome_fundo, {
            'resumo': 'Informações não disponíveis',
            'condicoes': 'N/A',
            'venda_1min': 'N/A',
            'perfil': 'N/A'
        })
    }

# ============================================
# CARREGAR DADOS
# ============================================

@st.cache_data
def carregar_dados():
    """Carrega dados do Excel - SEM MODIFICAR nomes das colunas"""
    try:
        df = pd.read_excel('calendario_Renda_mais.xlsx', sheet_name='Base')
        # NÃO mexer nos nomes das colunas - usar exatamente como está no Excel
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar Excel: {str(e)}")
        return None

# ============================================
# TELA DE LOGIN
# ============================================

def tela_login(df_base):
    """Tela de login por assessor"""
    
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    if 'assessor_logado' not in st.session_state:
        st.session_state.assessor_logado = None
    if 'nome_assessor' not in st.session_state:
        st.session_state.nome_assessor = None
    
    if st.session_state.autenticado:
        return True
    
    st.markdown("""
    <div style="text-align: center; padding: 30px;">
        <h1 style="color: #1e4d2b;">Calendário Renda Mais - Tauari Investimentos</h1>
        <p style="color: #7f8c8d;">Acesso restrito por Assessor</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            codigo_assessor = st.text_input(
                "👤 Código do Assessor:",
                placeholder="Exemplo: 22359",
                max_chars=10
            )
            
            senha_assessor = st.text_input(
                "🔐 Senha do Assessor:",
                type="password",
                placeholder="Digite sua senha",
                max_chars=20
            )
            
            submitted = st.form_submit_button("🔓 Entrar", use_container_width=True)
            
            if submitted:
                if not codigo_assessor or not senha_assessor:
                    st.error("❌ Preencha todos os campos!")
                else:
                    valido, nome_assessor = validar_senha_assessor(codigo_assessor, senha_assessor)
                    if valido:
                        if df_base is not None:
                            try:
                                codigo_com_a = f"A{codigo_assessor}"
                                clientes = df_base[df_base['Código do Assessor'] == codigo_com_a]
                                
                                if clientes.empty:
                                    st.error(f"❌ Nenhum cliente encontrado para o Assessor {codigo_assessor}")
                                else:
                                    st.session_state.autenticado = True
                                    st.session_state.assessor_logado = codigo_assessor
                                    st.session_state.nome_assessor = nome_assessor
                                    st.success(f"✅ Bem-vindo, {nome_assessor}!")
                                    st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao buscar clientes: {str(e)}")
                        else:
                            st.error("❌ Erro ao carregar a base de dados!")
                    else:
                        st.error("❌ Código ou senha incorretos!")
    
    return False

# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def main():
    """Função principal"""
    
    # Carregar dados
    df_base = carregar_dados()
    
    if df_base is None:
        st.stop()
    
    # Verificar autenticação
    if not tela_login(df_base):
        st.stop()
    
    # Inicializar estado
    if 'mes_atual' not in st.session_state:
        st.session_state.mes_atual = datetime.now().month
        st.session_state.ano_atual = datetime.now().year
    
    feriados = gerar_feriados(st.session_state.ano_atual)
    
    # Header
    st.markdown(f"""
    <div class="header-sistema">
        <div class="titulo-principal">📅 Calendário Renda Mais - Tauari Investimentos</div>
        <div class="info-assessor">
            👤 Assessor: <strong>{st.session_state.nome_assessor}</strong> | 
            Código: <strong>{st.session_state.assessor_logado}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão sair
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🔓 Sair", key="btn_sair"):
            st.session_state.autenticado = False
            st.session_state.assessor_logado = None
            st.session_state.nome_assessor = None
            st.rerun()
    
    # Filtrar dados do assessor
    try:
        codigo_com_a = f"A{st.session_state.assessor_logado}"
        df_filtrado = df_base[df_base['Código do Assessor'] == codigo_com_a].copy()
    except Exception as e:
        st.error(f"❌ Erro ao filtrar dados: {str(e)}")
        st.stop()
    
    if df_filtrado.empty:
        st.error("❌ Nenhum cliente encontrado!")
        st.stop()
    
    # Seletor de cliente
    st.markdown('<div class="cliente-selector"><h3>👥 SELECIONE O CLIENTE</h3>', unsafe_allow_html=True)
    
    try:
        clientes = sorted(df_filtrado['Código do Cliente'].unique())
        cliente_selecionado = st.selectbox(
            "Cliente",
            [""] + list(clientes),
            label_visibility="collapsed",
            key="cliente_select"
        )
    except Exception as e:
        st.error(f"❌ Erro ao listar clientes: {str(e)}")
        st.stop()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not cliente_selecionado:
        st.stop()
    
    # Filtrar fundos do cliente
    try:
        fundos_cliente = df_filtrado[df_filtrado['Código do Cliente'] == cliente_selecionado].copy()
    except Exception as e:
        st.error(f"❌ Erro ao buscar fundos: {str(e)}")
        st.stop()
    
    if 'fundo_selecionado' not in st.session_state:
        try:
            st.session_state.fundo_selecionado = fundos_cliente['Fundo'].iloc[0]
        except:
            st.session_state.fundo_selecionado = None
    
    # Layout principal
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    # COLUNA 1: Fundos do cliente
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        for _, fundo_row in fundos_cliente.iterrows():
            try:
                nome_fundo = str(fundo_row['Fundo'])
                
                # Valor Aplicado
                try:
                    valor_aplicado = float(fundo_row['Valor Solicitado'])
                except:
                    valor_aplicado = 0.0
                
                # Rendimento Percentual
                try:
                    rendimento_str = str(fundo_row['Rendimento']).replace(',', '.')
                    percentual_liquido = float(rendimento_str) * 100
                except:
                    percentual_liquido = 0.0
                
                # Valor Líquido
                try:
                    valor_liquido = float(fundo_row['Rendimento Liquido'])
                except:
                    valor_liquido = 0.0
                
                # Data de Pagamento
                try:
                    dia_pagamento = int(fundo_row['Data do Pagamento'])
                    data_calc = calcular_dia_util(
                        st.session_state.ano_atual,
                        st.session_state.mes_atual,
                        dia_pagamento,
                        feriados
                    )
                    if data_calc:
                        data_texto = data_calc.strftime("%d/%m/%Y")
                    else:
                        data_texto = f"Dia útil {dia_pagamento}"
                except:
                    data_texto = "Não definida"
                
                info = buscar_info_fundo(nome_fundo)
                classe = 'fundo-card-selecionado' if nome_fundo == st.session_state.fundo_selecionado else ''
                
                st.markdown(f"""
                <div class="fundo-card {classe}" style="border-left-color: {info['cor']}">
                    <div class="nome">{nome_fundo}</div>
                    <div class="info" style="margin-top: 8px;">
                        <div style="margin-bottom: 4px;">💰 <strong>Valor Aplicado:</strong> <span class="valor">R$ {valor_aplicado:,.2f}</span></div>
                        <div style="margin-bottom: 4px;">📅 <strong>Data Pagamento:</strong> {data_texto}</div>
                        <div style="margin-bottom: 4px;">📈 <strong>% Líquido:</strong> <span class="valor">{percentual_liquido:.2f}%</span></div>
                        <div>💵 <strong>Valor Líquido:</strong> <span class="valor">R$ {valor_liquido:,.2f}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("📊", key=f"sel_{nome_fundo}", help=f"Selecionar {nome_fundo}"):
                    st.session_state.fundo_selecionado = nome_fundo
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Erro ao processar fundo: {str(e)}")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # COLUNA 2: Tese do fundo
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        if st.session_state.fundo_selecionado:
            try:
                info = buscar_info_fundo(st.session_state.fundo_selecionado)
                tese = info['tese']
                
                st.markdown(f"""
                <div class="tese-texto">
                    <strong style="color: {info['cor']};">{st.session_state.fundo_selecionado}</strong>
                    <p>{tese['resumo']}</p>
                    <h4>📋 Condições</h4>
                    <p style="white-space: pre-line;">{tese['condicoes']}</p>
                    <h4>⚡ Venda em 1 Minuto</h4>
                    <p>{tese['venda_1min']}</p>
                    <h4>🎯 Perfil</h4>
                    <p>{tese['perfil']}</p>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown('<div class="tese-texto"><p>Erro ao carregar tese.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="tese-texto"><p>Selecione um fundo.</p></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # COLUNA 3: Calendário
    with col3:
        st.markdown('<div class="box"><div class="box-titulo">📅 CALENDÁRIO</div>', unsafe_allow_html=True)
        
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
        
        # Gerar calendário
        try:
            cal = calendar.monthcalendar(st.session_state.ano_atual, st.session_state.mes_atual)
            
            dias_semana = ['seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.', 'dom.']
            html_cal = '<div class="calendario-grid">'
            
            for dia in dias_semana:
                html_cal += f'<div class="cal-header">{dia}</div>'
            
            # Coletar eventos
            eventos_mes = {}
            for _, fundo_row in fundos_cliente.iterrows():
                try:
                    dia_pagamento = int(fundo_row['Data do Pagamento'])
                    data_calc = calcular_dia_util(
                        st.session_state.ano_atual,
                        st.session_state.mes_atual,
                        dia_pagamento,
                        feriados
                    )
                    
                    if data_calc:
                        dia = data_calc.day
                        nome_fundo = str(fundo_row['Fundo'])
                        info = buscar_info_fundo(nome_fundo)
                        
                        if dia not in eventos_mes:
                            eventos_mes[dia] = []
                        eventos_mes[dia].append({
                            'sigla': info['sigla'],
                            'cor': info['cor']
                        })
                except:
                    pass
            
            # Renderizar dias
            for semana in cal:
                for dia in semana:
                    if dia == 0:
                        html_cal += '<div class="cal-dia" style="background: #f8f9fa;"></div>'
                    else:
                        data_dia = date(st.session_state.ano_atual, st.session_state.mes_atual, dia)
                        classe = "cal-dia fim-semana" if data_dia.weekday() >= 5 else "cal-dia"
                        
                        eventos_html = ""
                        if dia in eventos_mes:
                            for evento in eventos_mes[dia]:
                                eventos_html += f'<div class="cal-evento" style="background: {evento["cor"]}">{evento["sigla"]}</div>'
                        
                        html_cal += f'<div class="{classe}"><div class="numero">{dia}</div>{eventos_html}</div>'
            
            html_cal += '</div>'
            st.markdown(html_cal, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Erro ao gerar calendário: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
