"""
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
======================================================
Sistema multi-assessor com senhas individuais
VERSÃO FINAL COMPLETA - ATUALIZADA 24/10/2025
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
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .header-verde {
        background: #1e4d2b;
        padding: 20px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .assessor-info {
        color: white;
        font-size: 16px;
        background: rgba(255,255,255,0.1);
        padding: 10px 18px;
        border-radius: 5px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .barra-selecao {
        background: #ecf0f1;
        padding: 8px 40px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .stSelectbox [data-baseweb="select"] > div:first-child {
        background: white !important;
        border: 2px solid #27ae60 !important;
        color: #000000 !important;
    }
    
    .container-principal {
        padding: 20px 40px;
        background: white;
    }
    
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
        font-size: 15px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .box-conteudo {
        padding: 10px;
        overflow-y: auto;
        max-height: 600px;
        background: #fafafa;
    }
    
    .fundo-card-container {
        position: relative; 
        margin-bottom: 12px;
    }
    
    .fundo-card {
        background: white;
        border: 1px solid #ddd;
        border-left: 6px solid #27ae60;
        border-radius: 4px;
        padding: 14px;
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.2s;
        min-height: 140px;
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
        font-size: 14px;
        color: #2c3e50;
        margin-bottom: 10px;
        line-height: 1.3;
        border-bottom: 1px solid #e0e0e0;
        padding-bottom: 8px;
    }
    
    .fundo-card .info {
        font-size: 12px;
        color: #34495e;
        line-height: 1.6;
    }
    
    .fundo-card .info strong {
        color: #2c3e50;
        font-weight: 600;
    }
    
    .fundo-card .info .valor {
        color: #27ae60;
        font-weight: 700;
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
    }

    .tese-texto {
        padding: 15px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        line-height: 1.6;
        color: #2c3e50;
        background: white;
    }
    
    .tese-texto h4 {
        font-size: 14px;
        font-weight: bold;
        color: #1e4d2b;
        margin: 15px 0 8px 0;
        background: #f0f8f4;
        padding: 6px 10px;
        border-left: 4px solid #27ae60;
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
        font-size: 12px;
        border: 1px solid #1e8449;
    }
    
    .cal-dia {
        border: 1px solid #ddd;
        padding: 8px;
        min-height: 90px;
        background: white;
    }
    
    .cal-dia.fim-semana {
        background: #f8f9fa;
    }
    
    .cal-dia .numero {
        font-size: 15px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    
    .cal-evento {
        background: #27ae60;
        color: white;
        padding: 3px 6px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: bold;
        margin: 2px 0;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .stButton button {
        background: #27ae60 !important;
        color: white !important;
        border: none !important;
        padding: 10px 18px !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
    }
    
    .stButton button:hover {
        background: #1e8449 !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
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

def criar_tese(nome_ativo, dia_util_int, df_fundos=None):
    """Cria tese lendo do Excel ou usando padrão"""
    
    resumo = "Informações não disponíveis"
    condicoes = f"• Pagamento: {dia_util_int}º dia útil"
    perfil = "Não especificado"
    venda_1min = "Informações não disponíveis"
    
    # Tentar ler do Excel
    if df_fundos is not None and len(df_fundos) > 0:
        for idx, row in df_fundos.iterrows():
            nome_col = None
            for col in df_fundos.columns:
                if 'fundo' in col.lower() or 'nome' in col.lower() or 'ativo' in col.lower():
                    nome_col = col
                    break
            
            if nome_col:
                nome_excel = str(row[nome_col]).strip() if pd.notna(row[nome_col]) else ''
                
                if nome_excel and (nome_excel.lower() in nome_ativo.lower() or nome_ativo.lower() in nome_excel.lower()):
                    for col in df_fundos.columns:
                        col_lower = col.lower()
                        
                        if 'resumo' in col_lower or 'sobre' in col_lower or 'descri' in col_lower:
                            if pd.notna(row[col]) and str(row[col]).strip() != '':
                                resumo = str(row[col]).strip()
                        
                        if 'condi' in col_lower or 'taxa' in col_lower or 'emissor' in col_lower:
                            if pd.notna(row[col]) and str(row[col]).strip() != '':
                                condicoes = str(row[col]).strip()
                                if f"Pagamento: {dia_util_int}º dia útil" not in condicoes:
                                    condicoes += f"\n• Pagamento: {dia_util_int}º dia útil"
                        
                        if 'perfil' in col_lower:
                            if pd.notna(row[col]) and str(row[col]).strip() != '':
                                perfil = str(row[col]).strip()
                        
                        if 'venda' in col_lower or '1 minuto' in col_lower or 'pitch' in col_lower:
                            if pd.notna(row[col]) and str(row[col]).strip() != '':
                                venda_1min = str(row[col]).strip()
                    break
    
    # Usar teses padrão se não encontrou no Excel
    if resumo == "Informações não disponíveis":
        if 'FII' in nome_ativo or 'Imobiliário' in nome_ativo:
            resumo = "Fundo de Investimento Imobiliário que investe em imóveis comerciais de alto padrão, galpões logísticos em regiões estratégicas e Certificados de Recebíveis Imobiliários (CRI) de emissores sólidos."
            condicoes = f"• Emissor: Gestora especializada em FII\n• Prazo: Indeterminado\n• Taxa: 0,5% a 1,0% a.a.\n• Liquidez: D+30\n• Aplicação mínima: R$ 1.000,00\n• Pagamento: {dia_util_int}º dia útil"
            perfil = "Ideal para investidores que buscam renda mensal passiva, isenta de IR para PF"
            venda_1min = "Este FII oferece renda mensal isenta de IR para pessoa física, investindo em imóveis de alta qualidade com inquilinos sólidos. Ideal para quem busca diversificação e rendimentos previsíveis acima da poupança."
        elif 'CRI' in nome_ativo or 'Renda' in nome_ativo:
            resumo = "Fundo de renda fixa que investe em CRI, títulos públicos e crédito privado de primeira linha."
            condicoes = f"• Emissor: Gestora com expertise em renda fixa\n• Prazo: Indeterminado\n• Taxa: 0,5% a 1,0% a.a.\n• Liquidez: D+30\n• Aplicação mínima: R$ 1.000,00\n• Pagamento: {dia_util_int}º dia útil"
            perfil = "Conservadores que buscam rentabilidade acima do CDI"
            venda_1min = "Fundo de renda fixa que busca rentabilidade superior ao CDI através de uma carteira diversificada de CRI e crédito privado. Gestão profissional com foco em segurança e liquidez, perfeito para o investidor conservador que quer mais do que a poupança oferece."
        else:
            resumo = "Fundo com gestão ativa e estratégia diversificada."
            condicoes = f"• Emissor: Casa de gestão independente\n• Prazo: Variável\n• Taxa: 1,0% a 2,0% a.a.\n• Liquidez: D+30\n• Aplicação mínima: R$ 1.000,00\n• Pagamento: {dia_util_int}º dia útil"
            perfil = "Investidores com perfil moderado"
            venda_1min = "Fundo com gestão ativa que busca as melhores oportunidades do mercado através de análise criteriosa e rebalanceamento constante. Diversificação automática com equipe especializada cuidando do seu patrimônio."
    
    return {
        'resumo': resumo,
        'condicoes': condicoes,
        'perfil': perfil,
        'venda_1min': venda_1min
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
    return {'dia_util': None, 'cor': '#95a5a6', 'sigla': nome_ativo[:10], 'tese': {}}

def calcular_dia_util(ano, mes, numero_dia_util, feriados):
    """Calcula a data do N-ésimo dia útil"""
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
# CARREGAR DADOS
# ============================================

@st.cache_data(ttl=60)
def carregar_dados(force_reload=False):
    """Carrega dados do Excel incluindo links"""
    try:
        NOME_ARQUIVO = 'calendario_Renda_mais.xlsx'
        
        if not os.path.exists(NOME_ARQUIVO):
            st.error(f"❌ Erro: O arquivo '{NOME_ARQUIVO}' não foi encontrado.")
            return None, None, None, None, None, None, None

        df_base = pd.read_excel(NOME_ARQUIVO, sheet_name='Base')
        df_base.columns = df_base.columns.str.strip()
        
        print(f"\n{'='*60}")
        print(f"✅ Aba 'Base' carregada com sucesso!")
        print(f"   Total de linhas: {len(df_base)}")
        print(f"   Colunas encontradas: {list(df_base.columns)}")
        print(f"{'='*60}\n")
        
        df_suporte = pd.read_excel(NOME_ARQUIVO, sheet_name='Suporte')
        
        # Carregar aba Fundos
        df_fundos = None
        try:
            df_fundos = pd.read_excel(NOME_ARQUIVO, sheet_name='Fundos')
            df_fundos.columns = df_fundos.columns.str.strip()
            print(f"\n{'='*60}")
            print(f"✅ Aba 'Fundos' carregada com sucesso!")
            print(f"   Total de linhas: {len(df_fundos)}")
            print(f"   Colunas encontradas: {list(df_fundos.columns)}")
            print(f"{'='*60}\n")
            
            # Mostrar primeiras linhas para debug
            print("📋 Primeiras 3 linhas da aba Fundos:")
            for idx, row in df_fundos.head(3).iterrows():
                print(f"  Linha {idx + 1}:")
                for col in df_fundos.columns:
                    valor = row[col]
                    if pd.notna(valor):
                        print(f"    {col}: {str(valor)[:50]}")
            print()
            
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"⚠️ Erro ao carregar aba 'Fundos': {e}")
            print(f"   Certifique-se que existe uma aba chamada 'Fundos' no Excel")
            print(f"{'='*60}\n")
        
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
        mapa_links = {}
        
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
                    
                    # Criar tese passando df_fundos
                    tese = criar_tese(nome_ativo, dia_util_int, df_fundos)
                    mapa_teses[nome_ativo] = tese
                    
                    # Buscar links
                    link_expert = ''
                    link_material = ''
                    
                    if df_fundos is not None and len(df_fundos) > 0:
                        col_fundo = None
                        col_expert = None
                        col_material = None
                        
                        # Identificar colunas com busca mais flexível
                        for col in df_fundos.columns:
                            col_lower = col.lower().strip()
                            col_clean = col_lower.replace(' ', '').replace('_', '')
                            
                            if any(x in col_clean for x in ['fundo', 'nome', 'ativo']):
                                col_fundo = col
                                print(f"  Coluna do fundo identificada: '{col}'")
                            elif 'expert' in col_clean:
                                col_expert = col
                                print(f"  Coluna Expert identificada: '{col}'")
                            elif any(x in col_clean for x in ['material', 'publicitario', 'publicitário']):
                                col_material = col
                                print(f"  Coluna Material identificada: '{col}'")
                        
                        if col_fundo:
                            print(f"\n🔍 Buscando links para: {nome_ativo}")
                            for idx_f, row_f in df_fundos.iterrows():
                                nome_fundo_excel = str(row_f[col_fundo]).strip() if pd.notna(row_f[col_fundo]) else ''
                                
                                # Comparação mais flexível - remover espaços extras e comparar
                                nome_ativo_clean = ' '.join(nome_ativo.lower().split())
                                nome_excel_clean = ' '.join(nome_fundo_excel.lower().split())
                                
                                # Várias formas de comparação
                                match = False
                                if nome_excel_clean and nome_ativo_clean:
                                    # Exata
                                    if nome_excel_clean == nome_ativo_clean:
                                        match = True
                                        print(f"  ✅ Match exato: '{nome_fundo_excel}'")
                                    # Contém
                                    elif nome_excel_clean in nome_ativo_clean or nome_ativo_clean in nome_excel_clean:
                                        match = True
                                        print(f"  ✅ Match parcial: '{nome_fundo_excel}'")
                                    # Primeiras palavras
                                    elif nome_excel_clean.split()[0] in nome_ativo_clean or nome_ativo_clean.split()[0] in nome_excel_clean:
                                        match = True
                                        print(f"  ✅ Match por palavra: '{nome_fundo_excel}'")
                                
                                if match:
                                    if col_expert and pd.notna(row_f[col_expert]):
                                        link_expert = str(row_f[col_expert]).strip()
                                        # Validar URL
                                        if link_expert and link_expert.lower() != 'nan' and ('http://' in link_expert.lower() or 'https://' in link_expert.lower()):
                                            print(f"  📎 Expert encontrado: {link_expert[:50]}...")
                                        else:
                                            print(f"  ⚠️ Expert inválido: '{link_expert}'")
                                            link_expert = ''
                                    
                                    if col_material and pd.notna(row_f[col_material]):
                                        link_material = str(row_f[col_material]).strip()
                                        # Validar URL
                                        if link_material and link_material.lower() != 'nan' and ('http://' in link_material.lower() or 'https://' in link_material.lower()):
                                            print(f"  📎 Material encontrado: {link_material[:50]}...")
                                        else:
                                            print(f"  ⚠️ Material inválido: '{link_material}'")
                                            link_material = ''
                                    
                                    if link_expert or link_material:
                                        print(f"  ✅ Total de links válidos: {1 if link_expert else 0} Expert + {1 if link_material else 0} Material")
                                    else:
                                        print(f"  ⚠️ Nenhum link válido encontrado para este fundo")
                                    break
                            
                            if not link_expert and not link_material:
                                print(f"  ❌ Nenhum match encontrado na aba Fundos para: {nome_ativo}")
                        
                        mapa_links[nome_ativo] = {
                            'expert': link_expert,
                            'material': link_material
                        }
                    else:
                        mapa_links[nome_ativo] = {'expert': '', 'material': ''}
                    
                    cor_index += 1
                except Exception as e:
                    print(f"❌ Erro ao processar {nome_ativo}: {e}")
                    continue
        
        print(f"\n{'='*60}")
        print(f"📊 RESUMO DO CARREGAMENTO:")
        print(f"   Total de fundos carregados: {len(mapa_pagamentos)}")
        print(f"   Total de links processados: {len(mapa_links)}")
        
        # Contar fundos com e sem links
        fundos_com_expert = sum(1 for links in mapa_links.values() if links.get('expert'))
        fundos_com_material = sum(1 for links in mapa_links.values() if links.get('material'))
        fundos_com_ambos = sum(1 for links in mapa_links.values() if links.get('expert') and links.get('material'))
        fundos_sem_links = sum(1 for links in mapa_links.values() if not links.get('expert') and not links.get('material'))
        
        print(f"\n📎 ESTATÍSTICAS DE LINKS:")
        print(f"   ✅ Fundos com link Expert: {fundos_com_expert}")
        print(f"   ✅ Fundos com link Material: {fundos_com_material}")
        print(f"   ✅ Fundos com ambos os links: {fundos_com_ambos}")
        print(f"   ⚠️  Fundos SEM links: {fundos_sem_links}")
        
        if fundos_sem_links > 0:
            print(f"\n⚠️ FUNDOS SEM LINKS CADASTRADOS:")
            for nome, links in mapa_links.items():
                if not links.get('expert') and not links.get('material'):
                    print(f"   - {nome}")
            print(f"\n💡 DICA: Adicione esses fundos na aba 'Fundos' do Excel")
            print(f"   Estrutura esperada:")
            print(f"   | Fundo | Link Expert | Link Material |")
        
        print(f"{'='*60}\n")
        
        return df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses, mapa_links
        
    except Exception as e:
        st.error(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None, None, None, None

if 'reload_count' not in st.session_state:
    st.session_state.reload_count = 0

df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses, mapa_links = carregar_dados(st.session_state.reload_count)

if mapa_links is None:
    mapa_links = {}

# Debug mais completo
print(f"\n{'='*60}")
print(f"🔍 VERIFICAÇÃO FINAL DOS LINKS:")
if mapa_links:
    fundos_com_links = sum(1 for links in mapa_links.values() if links.get('expert') or links.get('material'))
    print(f"   Total de fundos no sistema: {len(mapa_links)}")
    print(f"   Fundos com pelo menos 1 link: {fundos_com_links}")
    
    if fundos_com_links > 0:
        print(f"\n   ✅ Links encontrados para:")
        for nome, links in mapa_links.items():
            if links.get('expert') or links.get('material'):
                expert_status = "✓" if links.get('expert') else "✗"
                material_status = "✓" if links.get('material') else "✗"
                print(f"      {nome[:40]:40} [Expert:{expert_status}] [Material:{material_status}]")
    else:
        print(f"\n   ⚠️ NENHUM LINK FOI ENCONTRADO!")
        print(f"   Verifique:")
        print(f"   1. A aba 'Fundos' existe no Excel")
        print(f"   2. Os nomes dos fundos na aba 'Fundos' correspondem aos da aba 'Base'")
        print(f"   3. As URLs começam com http:// ou https://")
else:
    print(f"   ❌ mapa_links está vazio!")
print(f"{'='*60}\n")

# ============================================
# PÁGINA DE FUNDOS
# ============================================

def pagina_conheca_fundos():
    """Página pública com informações dos fundos"""
    
    st.markdown("""
    <div style="background: white; padding: 30px 40px; text-align: center; border-bottom: 3px solid #1e4d2b;">
        <h1 style="font-size: 36px; margin: 10px 0 5px 0; font-family: 'Segoe UI', sans-serif; color: #1e4d2b; font-weight: 700;">
            Conheça nossos Fundos Renda Mais
        </h1>
        <h2 style="font-size: 28px; margin: 5px 0 20px 0; font-family: 'Segoe UI', sans-serif; color: #27ae60; font-weight: 600;">
            Tauari Investimentos
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col_space, col_btn = st.columns([6, 1])
    with col_btn:
        if st.button("🔙 Voltar ao Login", key="btn_voltar_login_fundos"):
            st.session_state.pagina_atual = 'login'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not mapa_pagamentos:
        st.warning("⚠️ Nenhum fundo disponível")
        st.stop()
    
    st.markdown("""
    <div style="background: #f8f9fa; padding: 20px 40px; border-radius: 8px; margin-bottom: 20px; border: 2px solid #27ae60;">
        <p style="color: #000000; font-weight: bold; font-size: 18px; margin: 0 0 15px 0;">🔍 Ir para o Fundo:</p>
    """, unsafe_allow_html=True)
    
    fundos_ordenados = sorted(list(mapa_pagamentos.keys()))
    lista_fundos = ["📋 Todos os Fundos"] + fundos_ordenados
    
    fundo_nav = st.selectbox(
        "Selecione:",
        lista_fundos,
        key="filtro_fundos_conheca",
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if fundo_nav != "📋 Todos os Fundos":
        st.success(f"🎯 Mostrando: **{fundo_nav}**")
        fundos_para_exibir = [fundo_nav] + [f for f in fundos_ordenados if f != fundo_nav]
    else:
        fundos_para_exibir = fundos_ordenados
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    for nome_fundo in fundos_para_exibir:
        dia_util = mapa_pagamentos[nome_fundo]
        cor = mapa_cores.get(nome_fundo, '#27ae60')
        tese = mapa_teses.get(nome_fundo, {})
        
        destaque = ""
        if fundo_nav != "📋 Todos os Fundos" and nome_fundo == fundo_nav:
            destaque = "border: 3px solid #f39c12; box-shadow: 0 0 20px rgba(243, 156, 18, 0.4);"
        
        resumo = tese.get("resumo", "Informações não disponíveis")
        condicoes = tese.get('condicoes', 'Informações não disponíveis')
        venda = tese.get("venda_1min", "Informações não disponíveis")
        perfil = tese.get("perfil", "Não especificado")
        
        with st.container():
            st.markdown(f"""
            <div style="background: white; border: 1px solid #ddd; border-left: 6px solid {cor}; 
                 border-radius: 8px; padding: 20px; margin-bottom: 10px; 
                 box-shadow: 0 2px 4px rgba(0,0,0,0.1); {destaque}">
                <h3 style="color: #1e4d2b; font-size: 20px; margin: 0 0 20px 0; font-weight: bold;">
                    📊 {nome_fundo}
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<p style="color: #000000; font-weight: bold; font-size: 16px; margin-bottom: 8px;">📝 Sobre o Fundo</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #000000; font-size: 14px; line-height: 1.7;">{resumo}</p>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<p style="color: #000000; font-weight: bold; font-size: 16px; margin-bottom: 8px;">📋 Resumo de Condições</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="color: #000000; font-size: 14px; line-height: 1.7; white-space: pre-line;">{condicoes}</p>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<p style="color: #000000; font-weight: bold; font-size: 16px; margin-bottom: 8px;">⚡ Venda em 1 Minuto</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="color: #000000; font-size: 14px; line-height: 1.7;">{venda}</p>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown('<p style="color: #000000; font-weight: bold; font-size: 16px; margin-bottom: 8px;">🎯 Perfil do Cliente</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #000000; font-size: 14px; line-height: 1.7;">{perfil}</p>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown('<p style="color: #000000; font-weight: bold; font-size: 16px; margin-bottom: 15px;">📎 Materiais e Conteúdos</p>', unsafe_allow_html=True)
            
            links_fundo = {}
            if mapa_links and isinstance(mapa_links, dict) and nome_fundo in mapa_links:
                links_fundo = mapa_links.get(nome_fundo, {})
            
            expert_url = links_fundo.get('expert', '') if isinstance(links_fundo, dict) else ''
            material_url = links_fundo.get('material', '') if isinstance(links_fundo, dict) else ''
            
            if not expert_url or not expert_url.startswith('http'):
                expert_url = ''
            if not material_url or not material_url.startswith('http'):
                material_url = ''
            
            botoes_ativos = []
            if expert_url:
                botoes_ativos.append(('expert', expert_url))
            if material_url:
                botoes_ativos.append(('material', material_url))
            
            if not botoes_ativos:
                st.markdown('''
                <div style="background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107;">
                    <p style="color: #856404; margin: 0; font-size: 13px;">
                        ⚠️ <strong>Links não cadastrados</strong><br>
                        Configure a aba "Fundos" no Excel: Fundo, Link Expert, Link Material
                    </p>
                </div>
                ''', unsafe_allow_html=True)
            else:
                if len(botoes_ativos) == 2:
                    col_links = st.columns([1, 1, 2])
                else:
                    col_links = st.columns([1, 3])
                
                for idx, (tipo, url) in enumerate(botoes_ativos):
                    with col_links[idx]:
                        if tipo == 'expert':
                            st.markdown(f'''
                            <a href="{url}" target="_blank" style="
                                display: block; background: #e74c3c; color: white;
                                padding: 18px 30px; border-radius: 8px; text-decoration: none;
                                font-weight: 700; font-size: 16px; text-align: center;
                                box-shadow: 0 3px 8px rgba(0,0,0,0.2);">🎯 Expert</a>
                            ''', unsafe_allow_html=True)
                        elif tipo == 'material':
                            st.markdown(f'''
                            <a href="{url}" target="_blank" style="
                                display: block; background: #3498db; color: white;
                                padding: 18px 30px; border-radius: 8px; text-decoration: none;
                                font-weight: 700; font-size: 16px; text-align: center;
                                box-shadow: 0 3px 8px rgba(0,0,0,0.2);">📢 Material Publicitário</a>
                            ''', unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 40px 0; border: none; border-top: 2px solid #e0e0e0;'>", unsafe_allow_html=True)
    
    st.stop()

if st.session_state.get('pagina_atual') == 'fundos':
    pagina_conheca_fundos()
else:
    verificar_autenticacao(df_base)

# ============================================
# INTERFACE PRINCIPAL
# ============================================

def main():
    global df_base, feriados, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses, mapa_links
    
    if df_base is None:
        st.stop()
    
    if mapa_links is None:
        mapa_links = {}
    
    if not st.session_state.get('autenticado', False) or not st.session_state.get('assessor_logado'):
        st.error("❌ Sessão expirada. Faça login novamente.")
        st.session_state.autenticado = False
        st.session_state.assessor_logado = None
        st.rerun()
    
    assessor_logado = st.session_state.assessor_logado
    df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
    df_base_filtrado = df_base[df_base['Assessor'] == str(assessor_logado)]
    
    assessor_nome = st.session_state.get('nome_assessor', 'Assessor')
    
    st.markdown(f"""
    <div style="background: #1e4d2b; padding: 20px 40px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <div style="font-size: 60px;">🌳</div>
                <div>
                    <h1 style="color: white; font-size: 22px; font-weight: bold; margin: 0 0 5px 0;">
                        📅 CALENDÁRIO DE PAGAMENTOS - RENDA MAIS
                    </h1>
                    <h2 style="color: #7dcea0; font-size: 18px; font-weight: 600; margin: 0;">
                        TAUARI INVESTIMENTOS
                    </h2>
                </div>
            </div>
            <div class="assessor-info">
                👤 Assessor: <strong>{assessor_nome}</strong> ({assessor_logado})
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="background: white; padding: 5px 0;">', unsafe_allow_html=True)
    col_saudacao, col_btns = st.columns([5, 1])
    
    with col_saudacao:
        nome_assessor = st.session_state.get('nome_assessor', 'Assessor')
        st.markdown(f'<p style="font-size: 26px; color: #1e4d2b; margin: 15px 0 15px 40px; font-weight: 700;">👋 Olá, {nome_assessor}!</p>', unsafe_allow_html=True)
    
    with col_btns:
        st.markdown('<div style="margin-top: 10px; margin-right: 40px;">', unsafe_allow_html=True)
        if st.button("🚪 Sair", key="btn_sair"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="barra-selecao">', unsafe_allow_html=True)
    
    num_clientes_unicos = df_base_filtrado['Cliente'].nunique()
    st.markdown(f'<label style="font-weight: bold; color: #000000; font-size: 16px; display: block; margin-bottom: 6px;">👤 SELECIONE O CLIENTE ({num_clientes_unicos} clientes):</label>', unsafe_allow_html=True)
    
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
            
            # CORRIGIDO: Buscar da coluna "Aplicação" (não "Financeiro")
            try:
                # Tentar primeiro "Aplicação", depois "Financeiro", depois "Valor"
                if 'Aplicação' in fundo.index:
                    valor_aplicado = float(str(fundo['Aplicação']).replace('R
    
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        fundo_para_tese = st.session_state.fundo_selecionado
        
        if fundo_para_tese:
            info = buscar_info_fundo(fundo_para_tese, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
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
            info = buscar_info_fundo(fundo['Ativo'], mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            
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
, '').replace('.', '').replace(',', '.').strip())
                elif 'Financeiro' in fundo.index:
                    valor_aplicado = float(fundo['Financeiro'])
                elif 'Valor' in fundo.index:
                    valor_aplicado = float(fundo['Valor'])
                else:
                    valor_aplicado = 0.0
            except Exception as e:
                print(f"Erro ao ler valor aplicado: {e}")
                valor_aplicado = 0.0
            
            # CORRIGIDO: Buscar da coluna "Rendimento" (não "Rendimento %")
            try:
                # Tentar primeiro "Rendimento", depois "Rendimento %", depois "% Líquido"
                if 'Rendimento' in fundo.index:
                    percentual_str = str(fundo['Rendimento']).replace('%', '').replace(',', '.').strip()
                    percentual_liquido = float(percentual_str)
                elif 'Rendimento %' in fundo.index:
                    percentual_liquido = float(fundo['Rendimento %'])
                elif '% Líquido' in fundo.index:
                    percentual_liquido = float(fundo['% Líquido'])
                else:
                    percentual_liquido = 0.0
            except Exception as e:
                print(f"Erro ao ler percentual: {e}")
                percentual_liquido = 0.0
            
            # Valor Líquido do Cupom
            valor_liquido_cupom = valor_aplicado * (percentual_liquido / 100)
            
            info = buscar_info_fundo(ativo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            
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
            
            if st.button(" ", key=f"select_{ativo}", help=f"Ver tese: {ativo}"):
                st.session_state.fundo_selecionado = ativo
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        fundo_para_tese = st.session_state.fundo_selecionado
        
        if fundo_para_tese:
            info = buscar_info_fundo(fundo_para_tese, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
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
            info = buscar_info_fundo(fundo['Ativo'], mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses)
            
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
