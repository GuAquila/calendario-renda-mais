"""
CALENDÁRIO RENDA MAIS - INTERFACE IDÊNTICA À VERSÃO DESKTOP
===========================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar

st.set_page_config(
    page_title="Calendário Renda Mais - TAUARI",
    page_icon="🌳",
    layout="wide"
)

# ============================================
# AUTENTICAÇÃO
# ============================================

SENHA_CORRETA = "Rendamais2025@"

def verificar_senha():
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        st.markdown("""
        <style>
            .login-container {
                max-width: 400px;
                margin: 150px auto;
                padding: 40px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            }
            .login-header {
                text-align: center;
                color: #1e4d2b;
                margin-bottom: 30px;
            }
            .stTextInput input {
                padding: 12px !important;
                font-size: 14px !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="login-header">
                <h1 style="font-size: 60px; margin: 0;">🌳</h1>
                <h2 style="margin: 10px 0;">Calendário Renda Mais</h2>
                <h3 style="color: #7dcea0; margin: 0;">TAUARI INVESTIMENTOS</h3>
            </div>
            """, unsafe_allow_html=True)
            
            senha_digitada = st.text_input(
                "Digite a senha de acesso:",
                type="password",
                placeholder="Senha"
            )
            
            if st.button("🔓 Entrar", use_container_width=True):
                if senha_digitada == SENHA_CORRETA:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("❌ Senha incorreta!")
        
        st.stop()

verificar_senha()

# ============================================
# CSS IDÊNTICO À VERSÃO DESKTOP
# ============================================

st.markdown("""
<style>
    /* Remover padding padrão */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Esconder menu e footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Cabeçalho verde IDÊNTICO */
    .header-tauari {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        padding: 25px 40px;
        color: white;
        margin: 0;
    }
    
    .header-content {
        display: flex;
        align-items: center;
        gap: 25px;
    }
    
    .header-logo {
        font-size: 50px;
    }
    
    .header-text h1 {
        font-size: 20px;
        margin: 0 0 5px 0;
        font-weight: bold;
    }
    
    .header-text h2 {
        font-size: 16px;
        margin: 0;
        color: #7dcea0;
        font-weight: 600;
    }
    
    /* Seletor de cliente */
    .cliente-bar {
        background: #ecf0f1;
        padding: 15px 40px;
        margin: 0;
    }
    
    .cliente-label {
        font-weight: bold;
        color: #1e4d2b;
        font-size: 13px;
        margin-bottom: 5px;
    }
    
    /* Container principal */
    .main-content {
        display: flex;
        gap: 15px;
        padding: 20px 40px;
        background: #f5f5f5;
    }
    
    /* Colunas */
    .column-box {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        overflow: hidden;
    }
    
    .column-title {
        background: #f8f9fa;
        padding: 12px 20px;
        font-weight: bold;
        color: #2c3e50;
        font-size: 14px;
        border-bottom: 2px solid #e0e0e0;
    }
    
    /* Cards de fundos IDÊNTICOS */
    .fundo-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-left: 6px solid #27ae60;
        border-radius: 4px;
        padding: 12px 15px;
        margin: 8px;
        transition: all 0.2s;
        cursor: pointer;
    }
    
    .fundo-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transform: translateX(3px);
    }
    
    .fundo-nome {
        font-weight: bold;
        color: #2c3e50;
        font-size: 12px;
        margin-bottom: 6px;
        line-height: 1.4;
    }
    
    .fundo-info {
        font-size: 11px;
        color: #7f8c8d;
    }
    
    .fundo-posicao {
        color: #27ae60;
        font-weight: 600;
    }
    
    /* Tese */
    .tese-content {
        padding: 15px 20px;
        max-height: 580px;
        overflow-y: auto;
        font-size: 12px;
        line-height: 1.6;
    }
    
    /* Calendário */
    .calendario-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 20px;
        background: #f8f9fa;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .mes-ano-display {
        font-size: 16px;
        font-weight: bold;
        color: #1e4d2b;
        text-align: center;
        flex: 1;
    }
    
    .calendario-grid {
        padding: 0;
    }
    
    .dia-header {
        background: #27ae60;
        color: white;
        padding: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 11px;
    }
    
    .dia-celula {
        border: 1px solid #e0e0e0;
        padding: 8px;
        min-height: 85px;
        background: white;
        position: relative;
    }
    
    .dia-celula.fim-semana {
        background: #ecf0f1;
    }
    
    .dia-numero {
        font-size: 14px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    
    .evento {
        background: #27ae60;
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 10px;
        font-weight: bold;
        margin: 2px 0;
        display: block;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #27ae60;
        border-radius: 4px;
    }
    
    /* Botões */
    .stButton button {
        background: #27ae60 !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }
    
    .stButton button:hover {
        background: #1e8449 !important;
    }
    
    /* Selectbox */
    .stSelectbox {
        margin: 0 !important;
    }
    
    .stSelectbox > div > div {
        background: white !important;
        border: 2px solid #27ae60 !important;
        border-radius: 5px !important;
        font-size: 13px !important;
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

@st.cache_data
def carregar_dados():
    try:
        NOME_ARQUIVO = 'calendario_Renda_mais.xlsx'
        
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
                    mapa_siglas[nome_ativo] = sigla
                    
                    tese = criar_tese(nome_ativo, dia_util_int)
                    mapa_teses[nome_ativo] = tese
                    
                    cor_index += 1
                except:
                    pass
        
        return df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses
        
    except Exception as e:
        st.error(f"❌ Erro: {e}")
        return None, None, None, None, None, None

def criar_tese(nome_ativo, dia_util_int):
    if 'FII' in nome_ativo or 'Imobiliário' in nome_ativo:
        resumo = "Fundo de Investimento Imobiliário que investe em imóveis comerciais de alto padrão, galpões logísticos em regiões estratégicas e Certificados de Recebíveis Imobiliários (CRI) de emissores sólidos."
        emissor = "Gestora especializada em FII"
        perfil = "Ideal para investidores que buscam renda mensal passiva, isenta de IR para PF"
        speech = "Destaque a isenção de IR, diversificação imobiliária, liquidez em bolsa (D+3) e distribuição mensal."
    elif 'CRI' in nome_ativo or 'Renda' in nome_ativo:
        resumo = "Fundo de renda fixa que investe predominantemente em Certificados de Recebíveis Imobiliários (CRI), títulos públicos e crédito privado de primeira linha."
        emissor = "Gestora com expertise em renda fixa"
        perfil = "Conservadores e moderados que buscam rentabilidade acima do CDI"
        speech = "Posicione como alternativa superior à poupança e CDB tradicional."
    else:
        resumo = "Fundo de investimento com gestão profissional ativa e estratégia macro diversificada."
        emissor = "Casa de gestão independente"
        perfil = "Investidores com perfil moderado"
        speech = "Gestão profissional e rebalanceamento tático."
    
    return {
        'resumo': resumo,
        'emissor': emissor,
        'perfil': perfil,
        'speech': speech
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
        dias_no_mes = 0
        
        while dia_atual.month == mes and dias_no_mes < 35:
            dias_no_mes += 1
            
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
# INTERFACE PRINCIPAL
# ============================================

def main():
    # Carregar dados
    df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses = carregar_dados()
    
    if df_base is None:
        st.stop()
    
    # CABEÇALHO VERDE
    st.markdown("""
    <div class="header-tauari">
        <div class="header-content">
            <div class="header-logo">🌳</div>
            <div class="header-text">
                <h1>📅 CALENDÁRIO DE PAGAMENTOS - RENDA MAIS</h1>
                <h2>TAUARI INVESTIMENTOS</h2>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # BARRA DE SELEÇÃO
    st.markdown('<div class="cliente-bar">', unsafe_allow_html=True)
    st.markdown('<div class="cliente-label">👤 SELECIONE O CLIENTE:</div>', unsafe_allow_html=True)
    
    clientes = sorted(df_base['Cliente'].unique())
    cliente_selecionado = st.selectbox("", [""] + list(clientes), label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not cliente_selecionado:
        st.stop()
    
    fundos_cliente = df_base[df_base['Cliente'] == cliente_selecionado]
    
    # LAYOUT 3 COLUNAS
    col1, col2, col3 = st.columns([25, 25, 50])
    
    # COLUNA 1: FUNDOS
    with col1:
        st.markdown('<div class="column-box">', unsafe_allow_html=True)
        st.markdown('<div class="column-title">📊 FUNDOS DO CLIENTE</div>', unsafe_allow_html=True)
        
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            posicao = float(fundo['Financeiro'])
            info = buscar_info_fundo(ativo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            
            dia_texto = f"{info['dia_util']}º dia útil" if info['dia_util'] else "Não definido"
            
            st.markdown(f"""
            <div class="fundo-card" style="border-left-color: {info['cor']}">
                <div class="fundo-nome">{ativo}</div>
                <div class="fundo-info">
                    <span class="fundo-posicao">💰 R$ {posicao:,.2f}</span> | 📅 {dia_texto}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # COLUNA 2: TESE
    with col2:
        st.markdown('<div class="column-box">', unsafe_allow_html=True)
        st.markdown('<div class="column-title">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        st.markdown('<div class="tese-content">Passe o mouse sobre um fundo</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # COLUNA 3: CALENDÁRIO
    with col3:
        st.markdown('<div class="column-box">', unsafe_allow_html=True)
        st.markdown('<div class="column-title">📅 CALENDÁRIO</div>', unsafe_allow_html=True)
        
        # Navegação
        if 'mes_atual' not in st.session_state:
            st.session_state.mes_atual = datetime.now().month
            st.session_state.ano_atual = datetime.now().year
        
        col_prev, col_mes, col_next = st.columns([15, 70, 15])
        
        with col_prev:
            if st.button("◀ Mês Anterior"):
                st.session_state.mes_atual -= 1
                if st.session_state.mes_atual < 1:
                    st.session_state.mes_atual = 12
                    st.session_state.ano_atual -= 1
        
        with col_mes:
            st.markdown(f'<div class="mes-ano-display">{MESES_PT[st.session_state.mes_atual-1]} {st.session_state.ano_atual}</div>', unsafe_allow_html=True)
        
        with col_next:
            if st.button("Próximo Mês ▶"):
                st.session_state.mes_atual += 1
                if st.session_state.mes_atual > 12:
                    st.session_state.mes_atual = 1
                    st.session_state.ano_atual += 1
        
        # Calendário
        cal = calendar.monthcalendar(st.session_state.ano_atual, st.session_state.mes_atual)
        
        # Headers
        dias_semana = ['seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.', 'dom.']
        cols_header = st.columns(7)
        for i, dia in enumerate(dias_semana):
            cols_header[i].markdown(f'<div class="dia-header">{dia}</div>', unsafe_allow_html=True)
        
        # Eventos
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
        
        # Renderizar
        for semana in cal:
            cols = st.columns(7)
            for i, dia in enumerate(semana):
                if dia == 0:
                    cols[i].markdown('<div style="height: 85px;"></div>', unsafe_allow_html=True)
                else:
                    data = date(st.session_state.ano_atual, st.session_state.mes_atual, dia)
                    classe_extra = " fim-semana" if data.weekday() >= 5 else ""
                    
                    eventos_html = ""
                    if dia in eventos_mes:
                        for evento in eventos_mes[dia]:
                            eventos_html += f'<div class="evento" style="background: {evento["cor"]}">{evento["sigla"]}</div>'
                    
                    cols[i].markdown(f'''
                    <div class="dia-celula{classe_extra}">
                        <div class="dia-numero">{dia}</div>
                        {eventos_html}
                    </div>
                    ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
