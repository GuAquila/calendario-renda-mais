"""
CALENDÁRIO RENDA MAIS - VERSÃO STREAMLIT CLOUD
===============================================
Interface web moderna com autenticação simples
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar

# Configuração da página
st.set_page_config(
    page_title="Calendário Renda Mais - TAUARI",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# AUTENTICAÇÃO SIMPLES POR SENHA
# ============================================

SENHA_CORRETA = "Rendamais2025@"

def verificar_senha():
    """Exibe campo de senha e verifica"""
    
    # Verificar se já está autenticado
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        # Estilo da página de login
        st.markdown("""
        <style>
            .login-container {
                max-width: 500px;
                margin: 100px auto;
                padding: 40px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            .login-header {
                text-align: center;
                color: #1e4d2b;
                margin-bottom: 30px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Container de login
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="login-header">
                <h1>🌳</h1>
                <h2>Calendário Renda Mais</h2>
                <h3>TAUARI INVESTIMENTOS</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Campo de senha
            senha_digitada = st.text_input(
                "Digite a senha de acesso:",
                type="password",
                placeholder="Senha",
                key="senha_input"
            )
            
            # Botão de entrar
            if st.button("🔓 Entrar", use_container_width=True):
                if senha_digitada == SENHA_CORRETA:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("❌ Senha incorreta! Tente novamente.")
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.info("💡 Entre em contato com o administrador se não tiver a senha")
        
        st.stop()

# Verificar autenticação
verificar_senha()

# ============================================
# CÓDIGO DO APLICATIVO (após autenticação)
# ============================================

# CSS customizado
st.markdown("""
<style>
    /* Cabeçalho verde */
    .main-header {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    
    /* Botão de logout */
    .logout-btn {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 999;
    }
    
    /* Cards de fundos */
    .fundo-card {
        background: white;
        border-left: 6px solid #27ae60;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Calendário */
    .calendario-dia {
        border: 1px solid #e0e0e0;
        padding: 10px;
        min-height: 80px;
        border-radius: 5px;
        background: white;
    }
    
    .evento-badge {
        background: #27ae60;
        color: white;
        padding: 3px 8px;
        border-radius: 3px;
        font-size: 11px;
        margin: 2px 0;
        display: inline-block;
        font-weight: bold;
    }
    
    .block-container {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Paleta de cores
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
    """Carrega dados do Excel (com cache)"""
    try:
        NOME_ARQUIVO = 'calendario_Renda_mais.xlsx'
        
        df_base = pd.read_excel(NOME_ARQUIVO, sheet_name='Base')
        df_base.columns = df_base.columns.str.strip()
        
        df_suporte = pd.read_excel(NOME_ARQUIVO, sheet_name='Suporte')
        
        # Feriados
        try:
            df_feriados = pd.read_excel(NOME_ARQUIVO, sheet_name='Feriados')
            feriados = set()
            for col in df_feriados.columns:
                for val in df_feriados[col]:
                    if pd.notna(val) and isinstance(val, datetime):
                        feriados.add(val.date())
        except:
            feriados = set()
        
        # Criar mapas
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
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None, None, None, None, None, None


def criar_tese(nome_ativo, dia_util_int):
    """Cria tese do fundo"""
    if 'FII' in nome_ativo or 'Imobiliário' in nome_ativo:
        resumo = "Fundo de Investimento Imobiliário focado em imóveis comerciais e CRI."
        emissor = "Gestora especializada em FII"
        perfil = "Investidores que buscam renda mensal isenta de IR"
        speech = "Destaque isenção de IR, diversificação imobiliária e distribuição mensal."
    elif 'CRI' in nome_ativo or 'Renda' in nome_ativo:
        resumo = "Fundo de renda fixa com CRI, títulos públicos e crédito privado."
        emissor = "Gestora com expertise em renda fixa"
        perfil = "Conservadores que buscam rentabilidade acima do CDI"
        speech = "Alternativa superior à poupança com rentabilidade consistente."
    else:
        resumo = "Fundo com gestão ativa e estratégia diversificada."
        emissor = "Casa de gestão independente"
        perfil = "Investidores com perfil moderado"
        speech = "Gestão profissional e rebalanceamento tático."
    
    return {
        'resumo': resumo,
        'emissor': emissor,
        'perfil': perfil,
        'speech': speech,
        'dia_util': dia_util_int
    }


def buscar_info_fundo(nome_ativo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses):
    """Busca informações de um fundo"""
    for nome_fundo in mapa_pagamentos.keys():
        if nome_fundo.lower() in nome_ativo.lower() or nome_ativo.lower() in nome_fundo.lower():
            return {
                'dia_util': mapa_pagamentos.get(nome_fundo),
                'cor': mapa_cores.get(nome_fundo, '#95a5a6'),
                'sigla': mapa_siglas.get(nome_fundo, nome_ativo[:10]),
                'tese': mapa_teses.get(nome_fundo, {})
            }
    
    return {
        'dia_util': None,
        'cor': '#95a5a6',
        'sigla': nome_ativo[:10],
        'tese': {}
    }


def calcular_dia_util(ano, mes, numero_dia_util, feriados):
    """Calcula a data do Nº dia útil do mês"""
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


def main():
    """Função principal do app"""
    
    # Botão de logout no canto
    col_logout = st.columns([10, 1])
    with col_logout[1]:
        if st.button("🚪 Sair"):
            st.session_state.autenticado = False
            st.rerun()
    
    # Cabeçalho
    st.markdown("""
    <div class="main-header">
        <h1>🌳 CALENDÁRIO DE PAGAMENTOS - RENDA MAIS 🌳</h1>
        <h2>TAUARI INVESTIMENTOS</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses = carregar_dados()
    
    if df_base is None:
        st.stop()
    
    # Seletor de cliente
    st.sidebar.markdown("### 👤 SELECIONE O CLIENTE")
    clientes = sorted(df_base['Cliente'].unique())
    cliente_selecionado = st.sidebar.selectbox(
        "",
        ["Selecione..."] + list(clientes),
        key="cliente_select"
    )
    
    if cliente_selecionado == "Selecione...":
        st.info("👆 Selecione um cliente na barra lateral para começar")
        st.stop()
    
    # Filtrar fundos
    fundos_cliente = df_base[df_base['Cliente'] == cliente_selecionado]
    
    # Layout em 3 colunas
    col1, col2, col3 = st.columns([1, 1, 2])
    
    # COLUNA 1: FUNDOS
    with col1:
        st.markdown("### 📊 FUNDOS DO CLIENTE")
        
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            posicao = float(fundo['Financeiro'])
            
            info = buscar_info_fundo(ativo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            dia_util = info['dia_util']
            cor = info['cor']
            
            dia_texto = f"{dia_util}º dia útil" if dia_util else "Não definido"
            
            with st.container():
                st.markdown(f"""
                <div class="fundo-card" style="border-left-color: {cor}">
                    <strong>{ativo[:50]}</strong><br>
                    <small>💰 R$ {posicao:,.2f} | 📅 {dia_texto}</small>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Ver detalhes"):
                    tese = info['tese']
                    if tese:
                        st.markdown(f"**Resumo:** {tese.get('resumo', 'N/A')}")
                        st.markdown(f"**Emissor:** {tese.get('emissor', 'N/A')}")
                        st.markdown(f"**Perfil:** {tese.get('perfil', 'N/A')}")
                        st.markdown(f"**Speech:** {tese.get('speech', 'N/A')}")
    
    # COLUNA 2: RESUMO
    with col2:
        st.markdown("### 📈 RESUMO")
        
        total_fundos = len(fundos_cliente)
        total_posicao = fundos_cliente['Financeiro'].sum()
        
        st.metric("Total de Fundos", total_fundos)
        st.metric("Posição Total", f"R$ {total_posicao:,.2f}")
        
        st.markdown("#### 📅 Próximos Pagamentos")
        
        hoje = date.today()
        mes_atual = hoje.month
        ano_atual = hoje.year
        
        eventos_proximos = []
        
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            info = buscar_info_fundo(ativo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            
            if info['dia_util']:
                data_pagamento = calcular_dia_util(ano_atual, mes_atual, info['dia_util'], feriados)
                if data_pagamento and data_pagamento >= hoje:
                    dias_faltam = (data_pagamento - hoje).days
                    eventos_proximos.append({
                        'data': data_pagamento,
                        'dias': dias_faltam,
                        'sigla': info['sigla'],
                        'cor': info['cor']
                    })
        
        eventos_proximos.sort(key=lambda x: x['data'])
        
        for evento in eventos_proximos[:5]:
            st.markdown(f"""
            <span class="evento-badge" style="background: {evento['cor']}">
                {evento['sigla']} - {evento['data'].strftime('%d/%m')} ({evento['dias']} dias)
            </span>
            """, unsafe_allow_html=True)
    
    # COLUNA 3: CALENDÁRIO
    with col3:
        st.markdown("### 📅 CALENDÁRIO")
        
        # Controles
        col_prev, col_mes, col_next = st.columns([1, 3, 1])
        
        if 'mes_atual' not in st.session_state:
            st.session_state.mes_atual = datetime.now().month
            st.session_state.ano_atual = datetime.now().year
        
        with col_prev:
            if st.button("◀"):
                st.session_state.mes_atual -= 1
                if st.session_state.mes_atual < 1:
                    st.session_state.mes_atual = 12
                    st.session_state.ano_atual -= 1
        
        with col_mes:
            st.markdown(f"<h3 style='text-align: center; color: #1e4d2b;'>{MESES_PT[st.session_state.mes_atual-1]} {st.session_state.ano_atual}</h3>", unsafe_allow_html=True)
        
        with col_next:
            if st.button("▶"):
                st.session_state.mes_atual += 1
                if st.session_state.mes_atual > 12:
                    st.session_state.mes_atual = 1
                    st.session_state.ano_atual += 1
        
        # Calendário
        cal = calendar.monthcalendar(st.session_state.ano_atual, st.session_state.mes_atual)
        
        dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        cols_header = st.columns(7)
        for i, dia in enumerate(dias_semana):
            cols_header[i].markdown(f"<div style='text-align: center; font-weight: bold; background: #27ae60; color: white; padding: 5px; border-radius: 3px;'>{dia}</div>", unsafe_allow_html=True)
        
        # Eventos
        eventos_mes = {}
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            info = buscar_info_fundo(ativo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            
            if info['dia_util']:
                data_pagamento = calcular_dia_util(st.session_state.ano_atual, st.session_state.mes_atual, info['dia_util'], feriados)
                if data_pagamento:
                    dia = data_pagamento.day
                    if dia not in eventos_mes:
                        eventos_mes[dia] = []
                    eventos_mes[dia].append({
                        'sigla': info['sigla'],
                        'cor': info['cor'],
                        'ativo': ativo
                    })
        
        # Renderizar
        for semana in cal:
            cols = st.columns(7)
            for i, dia in enumerate(semana):
                if dia == 0:
                    cols[i].markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
                else:
                    eventos_html = ""
                    if dia in eventos_mes:
                        for evento in eventos_mes[dia]:
                            eventos_html += f"<span class='evento-badge' style='background: {evento['cor']}' title='{evento['ativo']}'>{evento['sigla']}</span><br>"
                    
                    cols[i].markdown(f"""
                    <div class="calendario-dia">
                        <strong style="font-size: 16px;">{dia}</strong><br>
                        {eventos_html}
                    </div>
                    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
