"""
CALENDÁRIO RENDA MAIS - INTERFACE 100% IDÊNTICA À VERSÃO DESKTOP
================================================================
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
# AUTENTICAÇÃO
# ============================================

SENHA_CORRETA = "Rendamais2025@"

def verificar_senha():
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        st.markdown("""
        <style>
            .stApp {
                background: white;
            }
            .login-box {
                max-width: 400px;
                margin: 150px auto;
                padding: 40px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div style='text-align: center;'><h1 style='font-size: 60px;'>🌳</h1><h2>Calendário Renda Mais</h2><h3 style='color: #7dcea0;'>TAUARI INVESTIMENTOS</h3></div>", unsafe_allow_html=True)
            senha = st.text_input("Digite a senha:", type="password", placeholder="Senha")
            if st.button("🔓 Entrar", use_container_width=True):
                if senha == SENHA_CORRETA:
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
    /* RESET COMPLETO */
    .stApp {
        background: white !important;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Esconder elementos do Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* CABEÇALHO VERDE */
    .header-verde {
        background: #1e4d2b;
        padding: 20px 40px;
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
    
    /* BARRA DE SELEÇÃO */
    .barra-selecao {
        background: #ecf0f1;
        padding: 15px 40px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .barra-selecao label {
        font-weight: bold;
        color: #1e4d2b;
        font-size: 12px;
        display: block;
        margin-bottom: 5px;
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
    }
    
    /* CARDS DE FUNDOS */
    .fundo-card {
        background: white;
        border: 1px solid #ddd;
        border-left: 6px solid #27ae60;
        border-radius: 4px;
        padding: 12px;
        margin-bottom: 8px;
        font-family: 'Segoe UI', sans-serif;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .fundo-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transform: translateX(3px);
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
    
    /* TESE */
    .tese-texto {
        padding: 15px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 12px;
        line-height: 1.6;
        color: #2c3e50;
    }
    
    .tese-texto h4 {
        font-size: 13px;
        font-weight: bold;
        color: #1e4d2b;
        margin: 15px 0 8px 0;
    }
    
    .tese-texto ul {
        margin: 8px 0;
        padding-left: 20px;
    }
    
    .tese-texto li {
        margin: 4px 0;
    }
    
    /* CALENDÁRIO */
    .calendario-nav {
        background: #f8f9fa;
        padding: 10px 15px;
        border-bottom: 2px solid #e0e0e0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .calendario-mes {
        font-size: 16px;
        font-weight: bold;
        color: #1e4d2b;
        font-family: 'Segoe UI', sans-serif;
    }
    
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
    
    /* SELECTBOX */
    .stSelectbox [data-baseweb="select"] {
        background: white;
        border: 2px solid #27ae60 !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
    }
    
    /* SCROLLBAR */
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
        condicoes = f"• Emissor: Gestora especializada em FII\n• Prazo: Indeterminado (cotização diária ou semanal)\n• Taxa: Taxa de administração: 0,5% a 1,0% a.a. | Performance: Pode haver\n• Liquidez: D+30 (típico)\n• Aplicação mínima: R$ 1.000,00\n• Pagamento: {dia_util_int}º dia útil"
        perfil = "Ideal para: investidores que buscam renda mensal passiva, isenta de IR para PF, com exposição ao mercado imobiliário sem precisar comprar imóveis diretamente"
        speech = "Destaque a isenção de IR, diversificação imobiliária, liquidez em bolsa (D+3) e distribuição mensal. Enfatize que o cliente pode começar com valores acessíveis e construir um portfólio imobiliário robusto. Compare com aluguel de imóveis próprios mostrando vantagens de não ter vacância, manutenção ou inadimplência."
    elif 'CRI' in nome_ativo or 'Renda' in nome_ativo:
        resumo = "Fundo de renda fixa que investe predominantemente em Certificados de Recebíveis Imobiliários (CRI), títulos públicos e crédito privado de primeira linha, com estratégia conservadora e foco em previsibilidade."
        condicoes = f"• Emissor: Gestora com expertise em renda fixa\n• Prazo: Indeterminado (cotização diária ou semanal)\n• Taxa: Taxa de administração: 0,5% a 1,0% a.a. | Performance: Pode haver\n• Liquidez: D+30 (típico)\n• Aplicação mínima: R$ 1.000,00\n• Pagamento: {dia_util_int}º dia útil"
        perfil = "Conservadores e moderados que buscam rentabilidade acima do CDI com baixa volatilidade. Excelente para reserva de emergência de médio prazo e alocação tática"
        speech = "Posicione como alternativa superior à poupança e CDB tradicional. Mostre histórico de rentabilidade consistente, benefícios da diversificação do fundo vs título único, e gestão ativa. Use simulações comparativas mostrando diferença acumulada ao longo de 3-5 anos. Ideal para complementar renda fixa de clientes conservadores."
    else:
        resumo = "Fundo de investimento com gestão profissional ativa, estratégia macro diversificada e foco em gerar retornos consistentes através de alocação tática em múltiplas classes de ativos conforme cenário econômico."
        condicoes = f"• Emissor: Casa de gestão independente\n• Prazo: Variável conforme estratégia\n• Taxa: Taxa de administração: 1,0% a 2,0% a.a. | Performance: conforme mandato\n• Liquidez: D+30 (típico)\n• Aplicação mínima: R$ 1.000,00\n• Pagamento: {dia_util_int}º dia útil"
        perfil = "Investidores com perfil moderado que buscam diversificação e gestão ativa. Patrimônio mínimo sugerido: R$ 100 mil"
        speech = "Posicione como 'core' do portfólio diversificado. Enfatize gestão profissional, rebalanceamento tático, e histórico do gestor. Use para clientes que não têm tempo ou conhecimento para gerir investimentos ativamente. Mostre como o fundo se comportou em diferentes cenários (alta de juros, crise, etc). Compare custo-benefício vs consultoria independente."
    
    return {
        'resumo': resumo,
        'condicoes': condicoes,
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
    df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses = carregar_dados()
    
    if df_base is None:
        st.stop()
    
    # CABEÇALHO
    st.markdown("""
    <div class="header-verde">
        <div class="logo">🌳</div>
        <div class="texto">
            <h1>📅 CALENDÁRIO DE PAGAMENTOS - RENDA MAIS</h1>
            <h2>TAUARI INVESTIMENTOS</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # BARRA DE SELEÇÃO
    st.markdown('<div class="barra-selecao"><label>👤 SELECIONE O CLIENTE:</label></div>', unsafe_allow_html=True)
    
    clientes = sorted(df_base['Cliente'].unique())
    cliente_selecionado = st.selectbox("", [""] + list(clientes), label_visibility="collapsed")
    
    if not cliente_selecionado:
        st.stop()
    
    fundos_cliente = df_base[df_base['Cliente'] == cliente_selecionado]
    
    # CONTAINER PRINCIPAL
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    # COLUNA 1: FUNDOS
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            posicao = float(fundo['Financeiro'])
            info = buscar_info_fundo(ativo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            
            dia_texto = f"{info['dia_util']}º dia útil" if info['dia_util'] else "Não definido"
            
            st.markdown(f"""
            <div class="fundo-card" style="border-left-color: {info['cor']}">
                <div class="nome">{ativo}</div>
                <div class="info">
                    💰 Posição: <span class="valor">R$ {posicao:,.2f}</span> | 📅 {dia_texto}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # COLUNA 2: TESE
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        if len(fundos_cliente) > 0:
            primeiro_fundo = fundos_cliente.iloc[0]
            info = buscar_info_fundo(primeiro_fundo['Ativo'], mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            tese = info['tese']
            
            st.markdown(f"""
            <div class="tese-texto">
                <strong style="color: {info['cor']}; font-size: 13px;">{primeiro_fundo['Ativo']}</strong>
                <p style="margin: 10px 0;">{tese.get('resumo', '')}</p>
                
                <h4>📋 Resumo de Condições</h4>
                <p style="white-space: pre-line; font-size: 11px;">{tese.get('condicoes', '')}</p>
                
                <h4>🎯 Perfil do Cliente</h4>
                <p>{tese.get('perfil', '')}</p>
                
                <h4>💡 Speech de Venda</h4>
                <p>{tese.get('speech', '')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # COLUNA 3: CALENDÁRIO
    with col3:
        st.markdown('<div class="box"><div class="box-titulo">📅 CALENDÁRIO</div>', unsafe_allow_html=True)
        
        # Navegação
        if 'mes_atual' not in st.session_state:
            st.session_state.mes_atual = datetime.now().month
            st.session_state.ano_atual = datetime.now().year
        
        col_p1, col_p2, col_p3 = st.columns([1, 3, 1])
        
        with col_p1:
            if st.button("◀ Mês Anterior"):
                st.session_state.mes_atual -= 1
                if st.session_state.mes_atual < 1:
                    st.session_state.mes_atual = 12
                    st.session_state.ano_atual -= 1
                st.rerun()
        
        with col_p2:
            st.markdown(f'<div class="calendario-mes" style="text-align: center; padding: 8px 0;">{MESES_PT[st.session_state.mes_atual-1]} {st.session_state.ano_atual}</div>', unsafe_allow_html=True)
        
        with col_p3:
            if st.button("Próximo Mês ▶"):
                st.session_state.mes_atual += 1
                if st.session_state.mes_atual > 12:
                    st.session_state.mes_atual = 1
                    st.session_state.ano_atual += 1
                st.rerun()
        
        # Grid do calendário
        cal = calendar.monthcalendar(st.session_state.ano_atual, st.session_state.mes_atual)
        
        # Headers
        dias_semana = ['seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.', 'dom.']
        html_cal = '<div class="calendario-grid">'
        
        for dia in dias_semana:
            html_cal += f'<div class="cal-header">{dia}</div>'
        
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
        
        # Renderizar dias
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
