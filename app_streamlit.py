"""
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
======================================================
Sistema multi-assessor com senhas individuais
VERSÃO CORRIGIDA E COMENTADA - Novembro 2025
Usa APENAS aba "Base" do Excel

ESTE CÓDIGO FOI COMENTADO DETALHADAMENTE PARA INICIANTES!
Cada parte importante tem explicações claras.
"""

# ==============================================================================
# PASSO 1: IMPORTAR AS BIBLIOTECAS NECESSÁRIAS
# ==============================================================================
# Estas são as "ferramentas" que vamos usar no programa

import streamlit as st  # Para criar a interface web
import pandas as pd     # Para trabalhar com Excel/dados
from datetime import datetime, date, timedelta  # Para trabalhar com datas
import calendar        # Para criar calendários
import os             # Para trabalhar com arquivos do sistema

# ==============================================================================
# PASSO 2: CONFIGURAR A PÁGINA DO STREAMLIT
# ==============================================================================
# Define como a página web vai aparecer para o usuário

st.set_page_config(
    page_title="Calendário Renda Mais - TAUARI",  # Título na aba do navegador
    page_icon="🌳",                                # Ícone na aba do navegador
    layout="wide",                                 # Layout largo (usa toda a tela)
    initial_sidebar_state="collapsed"              # Esconde a barra lateral
)

# ==============================================================================
# PASSO 3: DEFINIR OS ASSESSORES E SUAS SENHAS
# ==============================================================================
# Dicionário com código do assessor: (nome, senha)

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

# ==============================================================================
# FUNÇÃO: VALIDAR SENHA DO ASSESSOR
# ==============================================================================
def validar_senha_assessor(codigo_assessor, senha):
    """
    Esta função verifica se o código e senha do assessor estão corretos.
    
    O que ela faz:
    1. Verifica se o código do assessor existe no dicionário ASSESSORES
    2. Se existir, compara a senha digitada com a senha correta
    3. Retorna True/False e o nome do assessor
    
    Parâmetros:
        codigo_assessor: código digitado pelo usuário (ex: '46857')
        senha: senha digitada pelo usuário (ex: 'GA2025')
    
    Retorna:
        (True, 'Nome do Assessor') se a senha estiver correta
        (False, None) se a senha estiver errada
    """
    
    # Verifica se o código existe no dicionário
    if codigo_assessor not in ASSESSORES:
        return False, None  # Código não existe
    
    # Pega o nome e senha esperada do dicionário
    nome_assessor, senha_esperada = ASSESSORES[codigo_assessor]
    
    # Compara a senha digitada com a senha esperada
    if senha == senha_esperada:
        return True, nome_assessor  # Senha correta!
    
    return False, None  # Senha incorreta

# ==============================================================================
# FUNÇÃO: VERIFICAR AUTENTICAÇÃO (TELA DE LOGIN)
# ==============================================================================
def verificar_autenticacao(df_base):
    """
    Esta função cria a tela de login e verifica se o assessor pode acessar.
    
    O que ela faz:
    1. Mostra uma tela de login bonita
    2. Pede código e senha do assessor
    3. Verifica se estão corretos
    4. Se corretos, libera o acesso ao sistema
    
    Parâmetro:
        df_base: dados do Excel carregados
    """
    
    # ===== INICIALIZAR VARIÁVEIS DE SESSÃO =====
    # session_state guarda informações enquanto o usuário usa o sistema
    
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False  # Usuário ainda não entrou
    
    if 'assessor_logado' not in st.session_state:
        st.session_state.assessor_logado = None  # Nenhum assessor logado
    
    if 'nome_assessor' not in st.session_state:
        st.session_state.nome_assessor = None  # Nome do assessor
    
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'  # Começa na tela de login
    
    # ===== SE NÃO ESTÁ AUTENTICADO, MOSTRAR TELA DE LOGIN =====
    if not st.session_state.autenticado:
        
        # CSS: código que deixa a tela bonita
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
        
        # Criar 3 colunas para centralizar o formulário
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:  # Usar apenas a coluna do meio
            
            # Título da página
            st.markdown("""
            <div class="login-titulo">
                <h2 style='margin: 10px 0; font-size: 24px;'>Calendário Renda Mais - Tauari Investimentos</h2>
                <p style='color: #7f8c8d; font-size: 14px; margin-top: 15px;'>Acesso restrito por Assessor (uso interno) - Última atualização 24/10</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Criar formulário de login
            with st.form("login_form"):
                
                # Campo para digitar o código do assessor
                codigo_assessor = st.text_input(
                    "👤 Código do Assessor:",
                    placeholder="Coloque seu código, exemplo: 46857",
                    max_chars=10,
                    key="codigo_input"
                )
                
                # Campo para digitar a senha (oculta os caracteres)
                senha_assessor = st.text_input(
                    "🔐 Senha do Assessor:",
                    type="password",  # Esconde a senha com asteriscos
                    placeholder="Digite sua senha",
                    max_chars=20,
                    key="senha_input"
                )
                
                # Botão para enviar o formulário
                submitted = st.form_submit_button("🔓 Entrar", use_container_width=True)
                
                # ===== QUANDO O USUÁRIO CLICA EM "ENTRAR" =====
                if submitted:
                    
                    # Verificar se os campos foram preenchidos
                    if not codigo_assessor or not senha_assessor:
                        st.error("❌ Preencha todos os campos!")
                    
                    else:
                        # Validar o código e senha
                        valido, nome_assessor = validar_senha_assessor(codigo_assessor, senha_assessor)
                        
                        if valido:  # Se a senha estiver correta
                            
                            if df_base is not None:
                                # Limpar a coluna Assessor (remover 'A' do início)
                                df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip().str.replace('A', '', 1)
                                
                                # Filtrar apenas os clientes deste assessor
                                clientes_assessor = df_base[df_base['Assessor'] == str(codigo_assessor)]
                                
                                if clientes_assessor.empty:
                                    st.error(f"❌ Nenhum cliente encontrado para o Assessor {codigo_assessor}")
                                
                                else:
                                    # SUCESSO! Salvar informações e liberar acesso
                                    st.session_state.autenticado = True
                                    st.session_state.assessor_logado = codigo_assessor
                                    st.session_state.nome_assessor = nome_assessor
                                    st.session_state.pagina_atual = 'sistema'
                                    st.success(f"✅ Bem-vindo, {nome_assessor}!")
                                    st.rerun()  # Recarrega a página
                            
                            else:
                                st.error("❌ Erro ao carregar a base de dados!")
                        
                        else:
                            st.error("❌ Código ou senha incorretos!")
            
            # Botão para ver os fundos sem fazer login
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
                • Em caso de dúvidas: <strong>gustavo.aquila@tauariinvestimentos.com.br</strong>
            </div>
            """, unsafe_allow_html=True)
        
        st.stop()  # Para aqui se não estiver autenticado

# ==============================================================================
# CSS: ESTILOS DA PÁGINA
# ==============================================================================
# Este código CSS deixa a página bonita com cores, sombras, etc.

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
    
    .fundo-destaque {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 35px;
        border-radius: 15px;
        margin-bottom: 40px;
        box-shadow: 0 8px 25px rgba(39, 174, 96, 0.25);
        border: 3px solid #27ae60;
        animation: fadeIn 0.5s ease-in;
    }
    
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
    
    .fundo-destaque h2 {
        color: #1e4d2b;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 3px solid #27ae60;
    }
    
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
    
    .fundo-destaque-conteudo {
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DADOS E CONFIGURAÇÕES
# ==============================================================================

# Nomes dos meses em português
MESES_PT = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

# ==============================================================================
# FUNÇÃO: GERAR FERIADOS
# ==============================================================================
def gerar_feriados(ano):
    """
    Esta função cria uma lista com todos os feriados do ano.
    
    Por que isso é importante?
    - Feriados não são dias úteis
    - Pagamentos não acontecem em feriados
    - Precisamos pular os feriados ao calcular datas de pagamento
    
    Parâmetro:
        ano: ano para gerar os feriados (ex: 2025)
    
    Retorna:
        lista com objetos date de cada feriado
    """
    
    # Feriados fixos (acontecem todo ano na mesma data)
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
    
    # Feriados móveis (mudam de data todo ano - como Carnaval e Páscoa)
    feriados_moveis = {
        2025: [(2, 28), (3, 3), (3, 4), (4, 18), (5, 29)],
        2026: [(2, 13), (2, 16), (2, 17), (4, 3), (5, 14)],
        2027: [(2, 5), (2, 8), (2, 9), (3, 26), (5, 6)],
    }
    
    # Criar lista vazia para guardar os feriados
    lista_feriados = []
    
    # Adicionar feriados fixos
    for (mes, dia), nome in feriados_fixos.items():
        lista_feriados.append(date(ano, mes, dia))
    
    # Adicionar feriados móveis (se existirem para este ano)
    if ano in feriados_moveis:
        for (mes, dia) in feriados_moveis[ano]:
            lista_feriados.append(date(ano, mes, dia))
    
    return lista_feriados

# ==============================================================================
# FUNÇÃO: CALCULAR DIA ÚTIL
# ==============================================================================
def calcular_dia_util(ano, mes, dia_util_desejado, feriados):
    """
    Esta função encontra qual é a DATA do Nº dia útil do mês.
    
    Exemplo: "Quero o 5º dia útil de novembro de 2025"
    A função vai contar os dias úteis e retornar a data exata.
    
    O que é dia útil?
    - Segunda a sexta-feira
    - Que NÃO seja feriado
    
    Parâmetros:
        ano: ano desejado (ex: 2025)
        mes: mês desejado (ex: 11 para novembro)
        dia_util_desejado: qual dia útil queremos (ex: 5 = quinto dia útil)
        feriados: lista com os feriados do ano
    
    Retorna:
        objeto date com a data encontrada
        ou None se não encontrar
    """
    
    # Pegar o primeiro dia do mês
    primeiro_dia = date(ano, mes, 1)
    
    # Calcular o último dia do mês
    if primeiro_dia.month == 12:
        ultimo_dia = date(ano, mes, 31)  # Dezembro tem 31 dias
    else:
        # Pega o dia antes do primeiro dia do próximo mês
        ultimo_dia = (date(ano, mes + 1, 1) - timedelta(days=1))
    
    # Começar a contar do primeiro dia
    dia_atual = primeiro_dia
    contador_dias_uteis = 0
    
    # Loop: percorrer todos os dias do mês
    while dia_atual <= ultimo_dia:
        
        # Verificar se é dia útil:
        # - weekday() < 5 significa segunda a sexta (0=segunda, 4=sexta)
        # - dia_atual not in feriados significa que não é feriado
        
        if dia_atual.weekday() < 5 and dia_atual not in feriados:
            # É um dia útil! Aumentar o contador
            contador_dias_uteis += 1
            
            # Verificar se chegamos no dia útil que queremos
            if contador_dias_uteis == dia_util_desejado:
                return dia_atual  # Encontramos! Retornar esta data
        
        # Avançar para o próximo dia
        dia_atual += timedelta(days=1)
    
    # Se chegou aqui, não encontrou (o mês não tem tantos dias úteis)
    return None

# ==============================================================================
# MAPEAMENTO DOS FUNDOS - DIA DE PAGAMENTO
# ==============================================================================
# Este dicionário define em qual DIA ÚTIL cada fundo paga
# Exemplo: 'ARX FII' paga no 15º dia útil do mês

MAPA_PAGAMENTOS = {
    'ARX FII Portfólio Renda CDI+ RL': 15,
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 5,
    'AZ Quest Panorama Renda Mais (1ª Emissão)': 5,
    'AZ Quest Panorama Renda Mais (2ª Emissão)': 5,
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

# ==============================================================================
# MAPEAMENTO DOS FUNDOS - CORES
# ==============================================================================
# Define a cor de cada fundo (para deixar o visual mais bonito)

MAPA_CORES = {
    'ARX FII Portfólio Renda CDI+ RL': '#e74c3c',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': '#3498db',
    'AZ Quest Panorama Renda Mais (1ª Emissão)': '#9b59b6',
    'AZ Quest Panorama Renda Mais (2ª Emissão)': '#8e44ad',
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

# ==============================================================================
# MAPEAMENTO DOS FUNDOS - SIGLAS
# ==============================================================================
# Nome curto de cada fundo (para mostrar no calendário)

MAPA_SIGLAS = {
    'ARX FII Portfólio Renda CDI+ RL': 'ARX',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 'AZ Quest',
    'AZ Quest Panorama Renda Mais (1ª Emissão)': 'AZ Panorama 1',
    'AZ Quest Panorama Renda Mais (2ª Emissão)': 'AZ Panorama 2',
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

# ==============================================================================
# MAPEAMENTO DOS FUNDOS - TESES DE INVESTIMENTO
# ==============================================================================
# Informações detalhadas sobre cada fundo

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
    'AZ Quest Panorama Renda Mais (1ª Emissão)': {
        'resumo': 'Fundo imobiliário de renda fixa com objetivo de superar o CDI através de uma carteira diversificada com um portfólio de crédito para incorporadoras de médio e alto padrão em São Paulo.',
        'condicoes': '''• Rentabilidade: CDI + 2,40% (Isento de IR para PF)
• Prazo: 5 anos (+ 1 prorrogável)
• Duration: 3,5 anos
• Público-alvo: Investidor em Geral''',
        'venda_1min': 'Fundo que busca retornos superiores ao CDI investindo em uma carteira diversificada de crédito privado com reinvestimento limitado a 3 anos, devolução integral do capital em até 5 anos. Além de garantias reais e um time com expertise de 24 anos no setor.',
        'perfil': 'Investidores conservadores que buscam retornos superiores ao CDI com gestão ativa.'
    },
    'AZ Quest Panorama Renda Mais (2ª Emissão)': {
        'resumo': 'Fundo imobiliário de renda fixa com objetivo de superar o CDI através de uma carteira diversificada com um portfólio de crédito para incorporadoras de médio e alto padrão em São Paulo.',
        'condicoes': '''• Rentabilidade: CDI + 2,40% (Isento de IR para PF)
• Prazo: 5 anos (+ 1 prorrogável)
• Duration: 3,5 anos
• Público-alvo: Investidor em Geral''',
        'venda_1min': 'Fundo que busca retornos superiores ao CDI investindo em uma carteira diversificada de crédito privado com reinvestimento limitado a 3 anos, devolução integral do capital em até 5 anos. Além de garantias reais e um time com expertise de 24 anos no setor.',
        'perfil': 'Investidores conservadores que buscam retornos superiores ao CDI com gestão ativa.'
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
        'venda_1min': 'Fundo de lajes corporativas com estrutura sênior, proporcionando renda estável do mercado corporativo com rendimentos mensais mais correção do IPCA na cota, sem volatilidade.',
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

# ==============================================================================
# MAPEAMENTO DOS FUNDOS - LINKS
# ==============================================================================
# Links para materiais e documentos de cada fundo

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

# ==============================================================================
# FUNÇÃO: BUSCAR INFORMAÇÕES DO FUNDO
# ==============================================================================
def buscar_info_fundo(nome_fundo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses, fundo_data=None):
    """
    Esta função busca todas as informações de um fundo.
    
    O que ela retorna:
    - Dia útil de pagamento
    - Cor para exibição
    - Sigla (nome curto)
    - Tese de investimento
    - Links para materiais
    
    Parâmetros:
        nome_fundo: nome completo do fundo
        mapa_pagamentos: dicionário com dias de pagamento
        mapa_cores: dicionário com cores
        mapa_siglas: dicionário com siglas
        mapa_teses: dicionário com teses
        fundo_data: dados do fundo do Excel (opcional)
    
    Retorna:
        dicionário com todas as informações
    """
    
    # ===== BUSCAR LINKS =====
    # Se temos dados do Excel, usar os links de lá
    # Senão, usar os links padrão do MAPA_LINKS
    
    if fundo_data is not None:
        try:
            # Tentar pegar os links do Excel
            link_expert = str(fundo_data.get('Link Expert', '')).strip()
            link_material = str(fundo_data.get('Material Publicitário', '')).strip()
            
            # Limpar valores vazios ou 'nan'
            if link_expert == 'nan' or link_expert == '':
                link_expert = ''
            if link_material == 'nan' or link_material == '':
                link_material = ''
            
            links = {'expert': link_expert, 'material': link_material}
        except:
            # Se der erro, usar os links padrão
            links = MAPA_LINKS.get(nome_fundo, {'expert': '', 'material': ''})
    else:
        # Usar os links padrão
        links = MAPA_LINKS.get(nome_fundo, {'expert': '', 'material': ''})
    
    # ===== MONTAR E RETORNAR O DICIONÁRIO COM TODAS AS INFORMAÇÕES =====
    return {
        'dia_util': mapa_pagamentos.get(nome_fundo, 0),           # Dia útil de pagamento
        'cor': mapa_cores.get(nome_fundo, '#27ae60'),             # Cor do fundo
        'sigla': mapa_siglas.get(nome_fundo, nome_fundo[:10]),   # Sigla (nome curto)
        'tese': mapa_teses.get(nome_fundo, {                     # Tese de investimento
            'resumo': 'Informações não disponíveis',
            'condicoes': 'N/A',
            'venda_1min': 'N/A',
            'perfil': 'N/A'
        }),
        'links': links  # Links para materiais
    }

# ==============================================================================
# TELA DE FUNDOS (COM DESTAQUE)
# ==============================================================================
def tela_fundos():
    """
    Esta função cria a tela onde o usuário pode ver todos os fundos
    disponíveis e suas informações detalhadas.
    
    Não precisa de login para acessar esta tela.
    """
    
    # Título da página
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
    
    # Criar 3 colunas para os botões
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Botão para voltar ao login
        if st.button("🔙 Voltar ao Login", use_container_width=True):
            st.session_state.pagina_atual = 'login'
            st.rerun()
    
    with col2:
        # Seletor para ir direto para um fundo
        fundos_lista = sorted(MAPA_TESES.keys())
        fundo_selecionado = st.selectbox(
            "🎯 Ir para o fundo:",
            ["Selecione um fundo..."] + fundos_lista,
            key="nav_fundo"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== SE SELECIONOU UM FUNDO, MOSTRAR EM DESTAQUE =====
    if fundo_selecionado and fundo_selecionado != "Selecione um fundo...":
        
        # Buscar informações do fundo
        info_destaque = buscar_info_fundo(
            fundo_selecionado,
            MAPA_PAGAMENTOS,
            MAPA_CORES,
            MAPA_SIGLAS,
            MAPA_TESES
        )
        
        tese_destaque = info_destaque['tese']
        links_destaque = info_destaque['links']
        
        # Mostrar fundo em destaque (box grande e colorido)
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
        
        # Botões para links
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
    
    # ===== MOSTRAR TODOS OS FUNDOS =====
    for fundo_nome in sorted(MAPA_TESES.keys()):
        
        # Buscar informações do fundo
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
        
        # Mostrar card do fundo
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
        
        # Botões de links
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

# ==============================================================================
# FUNÇÃO: CARREGAR DADOS DO EXCEL
# ==============================================================================
@st.cache_data
def carregar_dados():
    """
    Esta função carrega os dados do arquivo Excel.
    
    O que ela faz:
    1. Abre o arquivo Excel
    2. Lê a aba 'Base'
    3. Verifica se as colunas necessárias existem
    4. Retorna os dados para usar no sistema
    
    O @st.cache_data faz o Streamlit guardar os dados na memória,
    assim não precisa ler o Excel toda vez (fica mais rápido!)
    
    Retorna:
        DataFrame do pandas com os dados do Excel
    """
    
    try:
        # ===== PASSO 1: CARREGAR O EXCEL =====
        # Lê o arquivo e pega apenas a aba 'Base'
        df_base = pd.read_excel('calendario_Renda_mais.xlsx', sheet_name='Base')
        
        # ===== PASSO 2: LIMPAR NOMES DAS COLUNAS =====
        # Remove espaços extras que podem causar problemas
        df_base.columns = df_base.columns.str.strip()
        
        # ===== PASSO 3: VERIFICAR SE TEM DADOS =====
        if df_base.empty:
            st.error("❌ O arquivo Excel está vazio!")
            st.stop()
        
        # ===== PASSO 4: VALIDAR COLUNAS ESSENCIAIS =====
        # Estas colunas PRECISAM existir no Excel
        colunas_essenciais = ['Assessor', 'Cliente', 'Fundo', 'Aplicado']
        
        # Verificar quais colunas estão faltando
        colunas_faltando = [col for col in colunas_essenciais if col not in df_base.columns]
        
        if colunas_faltando:
            # Se alguma coluna essencial estiver faltando, mostrar erro
            st.error(f"❌ Colunas essenciais faltando: {', '.join(colunas_faltando)}")
            st.error(f"📋 Colunas disponíveis no Excel: {', '.join(df_base.columns.tolist())}")
            st.stop()
        
        # ===== SUCESSO! RETORNAR OS DADOS =====
        return df_base
        
    except FileNotFoundError:
        # Se o arquivo não foi encontrado
        st.error("❌ Arquivo 'calendario_Renda_mais.xlsx' não encontrado!")
        st.error("📁 Certifique-se de que o arquivo está na mesma pasta do código.")
        st.stop()
        
    except Exception as e:
        # Se deu algum outro erro
        st.error(f"❌ Erro ao carregar Excel: {str(e)}")
        st.error(f"🔍 Tipo do erro: {type(e).__name__}")
        st.stop()

# ==============================================================================
# FUNÇÃO PRINCIPAL DO SISTEMA
# ==============================================================================
def main():
    """
    Esta é a função PRINCIPAL do sistema!
    
    Ela coordena tudo:
    1. Carrega os dados do Excel
    2. Mostra a tela de login (se necessário)
    3. Mostra a tela principal do sistema (depois de logado)
    
    É aqui que o programa começa a rodar!
    """
    
    # ===== PASSO 1: CARREGAR DADOS DO EXCEL =====
    df_base = carregar_dados()
    
    # ===== PASSO 2: VERIFICAR QUAL PÁGINA MOSTRAR =====
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'  # Começa na tela de login
    
    # Se estiver na tela de fundos, mostrar ela e parar aqui
    if st.session_state.pagina_atual == 'fundos':
        tela_fundos()
        return
    
    # ===== PASSO 3: VERIFICAR AUTENTICAÇÃO =====
    # Se não estiver logado, para aqui
    verificar_autenticacao(df_base)
    
    # ===== A PARTIR DAQUI, O USUÁRIO ESTÁ LOGADO! =====
    
    # ===== PASSO 4: GERAR FERIADOS DO ANO =====
    feriados = gerar_feriados(datetime.now().year)
    
    # ===== PASSO 5: MOSTRAR CABEÇALHO DO SISTEMA =====
    st.markdown(f"""
    <div class="header-sistema">
        <div class="titulo-principal">📅 Calendário Renda Mais - Tauari Investimentos</div>
        <div class="info-assessor">
            👤 Assessor: <strong>{st.session_state.nome_assessor}</strong> | 
            Código: <strong>{st.session_state.assessor_logado}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== PASSO 6: BOTÕES DO TOPO =====
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        # Botão para sair (fazer logout)
        if st.button("🔓 Sair", key="btn_sair"):
            st.session_state.autenticado = False
            st.session_state.assessor_logado = None
            st.session_state.nome_assessor = None
            st.session_state.pagina_atual = 'login'
            st.rerun()
    
    with col2:
        # Botão para ver os fundos
        if st.button("📚 Ver Fundos", key="btn_ver_fundos"):
            st.session_state.pagina_atual = 'fundos'
            st.rerun()
    
    # ===== PASSO 7: FILTRAR DADOS DO ASSESSOR =====
    try:
        # Limpar a coluna Assessor (remover 'A' do início se tiver)
        df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip().str.replace('A', '', 1)
        
        # Filtrar apenas os clientes deste assessor
        df_base_filtrado = df_base[df_base['Assessor'] == str(st.session_state.assessor_logado)]
        
    except Exception as e:
        st.error(f"❌ Erro ao filtrar assessor: {str(e)}")
        st.error("🔍 Verifique se a coluna 'Assessor' existe no Excel")
        st.stop()
    
    # Verificar se tem clientes para este assessor
    if df_base_filtrado.empty:
        st.error("❌ Nenhum cliente encontrado para este assessor!")
        st.error(f"🔍 Assessor logado: {st.session_state.assessor_logado}")
        st.stop()
    
    # ===== PASSO 8: SELETOR DE CLIENTE =====
    st.markdown('<div class="cliente-selector"><h3>👥 SELECIONE O CLIENTE</h3>', unsafe_allow_html=True)
    
    try:
        # Pegar lista de clientes únicos
        clientes = sorted(df_base_filtrado['Cliente'].unique())
    except Exception as e:
        st.error(f"❌ Erro ao buscar clientes: {str(e)}")
        st.error("🔍 Verifique se a coluna 'Cliente' existe no Excel")
        st.stop()
    
    # Criar seletor de cliente
    cliente_selecionado = st.selectbox(
        "Cliente", 
        [""] + list(clientes),  # Lista começa vazia
        label_visibility="collapsed",  # Esconde o label (já tem no HTML acima)
        key="cliente_select"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Se não selecionou cliente, para aqui
    if not cliente_selecionado:
        st.stop()
    
    # ===== PASSO 9: FILTRAR FUNDOS DO CLIENTE =====
    try:
        # Pegar apenas os fundos deste cliente
        fundos_cliente = df_base_filtrado[df_base_filtrado['Cliente'] == cliente_selecionado]
    except Exception as e:
        st.error(f"❌ Erro ao filtrar fundos do cliente: {str(e)}")
        st.stop()
    
    # Verificar se o cliente tem fundos
    if fundos_cliente.empty:
        st.error("❌ Nenhum fundo encontrado para este cliente!")
        st.stop()
    
    # Verificar se a coluna Fundo existe
    if 'Fundo' not in fundos_cliente.columns:
        st.error("❌ Coluna 'Fundo' não encontrada no Excel!")
        st.stop()

    # ===== PASSO 10: INICIALIZAR FUNDO SELECIONADO =====
    # Guardar qual fundo está selecionado na tela
    if 'fundo_selecionado' not in st.session_state or st.session_state.fundo_selecionado is None:
        try:
            # Selecionar o primeiro fundo por padrão
            st.session_state.fundo_selecionado = fundos_cliente['Fundo'].iloc[0] if not fundos_cliente.empty else None
        except Exception as e:
            st.error(f"❌ Erro ao selecionar fundo inicial: {str(e)}")
            st.session_state.fundo_selecionado = None
    
    # Garantir que o fundo selecionado ainda existe na lista
    try:
        if st.session_state.fundo_selecionado is not None:
            if st.session_state.fundo_selecionado not in fundos_cliente['Fundo'].values:
                # Se o fundo não existe mais, selecionar o primeiro
                st.session_state.fundo_selecionado = fundos_cliente['Fundo'].iloc[0] if not fundos_cliente.empty else None
    except Exception as e:
        st.warning(f"⚠️ Aviso ao validar fundo selecionado: {str(e)}")
        st.session_state.fundo_selecionado = fundos_cliente['Fundo'].iloc[0] if not fundos_cliente.empty else None
    
    # ===== PASSO 11: CRIAR LAYOUT DE 3 COLUNAS =====
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    # Dividir a tela em 3 partes:
    # - col1: Lista de fundos (esquerda)
    # - col2: Tese do fundo (meio)
    # - col3: Calendário (direita)
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    # ===========================================================================
    # COLUNA 1: LISTA DE FUNDOS DO CLIENTE
    # ===========================================================================
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        # ===== LOOP: MOSTRAR CADA FUNDO =====
        for idx, (row_idx, fundo) in enumerate(fundos_cliente.iterrows()):
            try:
                # ------------------------------------------
                # 1. PEGAR O NOME DO FUNDO
                # ------------------------------------------
                nome_fundo = str(fundo.get('Fundo', 'Fundo Desconhecido'))
                
                # ------------------------------------------
                # 2. LER VALOR APLICADO DO EXCEL
                # ------------------------------------------
                # Coluna 'Aplicado' contém quanto o cliente investiu
                try:
                    valor_aplicado = float(fundo.get('Aplicado', 0))
                except (ValueError, TypeError):
                    valor_aplicado = 0.0
                
                # ------------------------------------------
                # 3. LER RENDIMENTO % DO EXCEL
                # ------------------------------------------
                # IMPORTANTE: A coluna '%' já vem em decimal (0.0115 = 1.15%)
                # Então multiplicamos por 100 para mostrar como porcentagem
                try:
                    rendimento_str = str(fundo.get('%', '0')).strip()
                    
                    # Verificar se está vazio ou é nan
                    if rendimento_str in ['-', '', 'nan', 'None', 'NaN']:
                        rendimento_percentual = 0.0
                    else:
                        # Converter para float e multiplicar por 100
                        # Exemplo: 0.0115 * 100 = 1.15%
                        rendimento_percentual = float(rendimento_str) * 100
                
                except (ValueError, TypeError):
                    rendimento_percentual = 0.0
                
                # ------------------------------------------
                # 4. BUSCAR INFORMAÇÕES DO FUNDO
                # ------------------------------------------
                # Esta função busca a cor, sigla, tese, etc.
                info = buscar_info_fundo(nome_fundo, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES, fundo)
                
                # ------------------------------------------
                # 5. CALCULAR DATA DE PAGAMENTO
                # ------------------------------------------
                # Primeiro tenta usar a coluna 'Data' do Excel
                # Se não tiver, usa o dia padrão do MAPA_PAGAMENTOS
                
                dia_pagamento = None
                
                # Tentar ler da coluna 'Data'
                try:
                    data_str = str(fundo.get('Data', '')).strip()
                    if data_str not in ['-', '', 'nan', 'None', 'NaN']:
                        dia_pagamento = int(float(data_str))
                except (ValueError, TypeError):
                    pass  # Se der erro, deixa None
                
                # Se não tem data no Excel, usar o padrão do mapa
                if not dia_pagamento or dia_pagamento == 0:
                    dia_pagamento = info.get('dia_util', None)
                
                # Calcular a data real de pagamento
                data_pagamento = None
                if dia_pagamento and dia_pagamento > 0:
                    try:
                        # Calcular qual será o dia do pagamento
                        data_pagamento = calcular_dia_util(
                            st.session_state.ano_atual,      # Ano atual
                            st.session_state.mes_atual,      # Mês atual
                            dia_pagamento,                    # Dia útil desejado
                            feriados                          # Lista de feriados
                        )
                    except Exception:
                        pass  # Se der erro, deixa None
                
                # Formatar data para mostrar ou colocar "Não definida"
                data_texto = data_pagamento.strftime("%d/%m/%Y") if data_pagamento else "Não definida"
                
                # ------------------------------------------
                # 6. VERIFICAR SE ESTE FUNDO ESTÁ SELECIONADO
                # ------------------------------------------
                classe_selecao = 'fundo-card-selecionado' if nome_fundo == st.session_state.fundo_selecionado else ''
                
                # ------------------------------------------
                # 7. MOSTRAR O CARD DO FUNDO
                # ------------------------------------------
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
                
                # ------------------------------------------
                # 8. BOTÃO PARA SELECIONAR ESTE FUNDO
                # ------------------------------------------
                # Quando clica, este fundo fica selecionado
                # CHAVE ÚNICA: usa índice + nome do fundo
                if st.button("📊", key=f"sel_{idx}_{row_idx}", help=f"Selecionar {nome_fundo}"):
                    st.session_state.fundo_selecionado = nome_fundo
                    st.rerun()  # Recarregar a página
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                # Se der erro em algum fundo, mostrar e continuar para o próximo
                st.error(f"❌ Erro ao processar fundo: {str(e)}")
                continue

        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ===========================================================================
    # COLUNA 2: TESE DO FUNDO SELECIONADO
    # ===========================================================================
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        # Verificar se tem um fundo selecionado
        if st.session_state.fundo_selecionado:
            
            # Buscar dados do fundo selecionado no Excel
            fundo_selecionado_data = fundos_cliente[fundos_cliente['Fundo'] == st.session_state.fundo_selecionado]
            fundo_data = fundo_selecionado_data.iloc[0] if not fundo_selecionado_data.empty else None
            
            # Buscar informações do fundo (tese, cor, etc.)
            info = buscar_info_fundo(
                st.session_state.fundo_selecionado, 
                MAPA_PAGAMENTOS, 
                MAPA_CORES, 
                MAPA_SIGLAS, 
                MAPA_TESES, 
                fundo_data
            )
            tese = info.get('tese', {})
            
            # Mostrar a tese formatada
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
            # Se não tem fundo selecionado
            st.markdown('<div class="tese-texto"><p>Selecione um fundo.</p></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===========================================================================
    # COLUNA 3: CALENDÁRIO
    # ===========================================================================
    with col3:
        st.markdown('<div class="box"><div class="box-titulo">📅 CALENDÁRIO</div>', unsafe_allow_html=True)
        
        # ===== INICIALIZAR MÊS E ANO =====
        if 'mes_atual' not in st.session_state:
            st.session_state.mes_atual = datetime.now().month  # Mês atual
            st.session_state.ano_atual = datetime.now().year   # Ano atual
        
        # ===== BOTÕES DE NAVEGAÇÃO DO CALENDÁRIO =====
        col_p1, col_p2, col_p3 = st.columns([1, 3, 1])
        
        with col_p1:
            # Botão para mês anterior
            if st.button("◀️ Anterior", key="prev_mes"):
                st.session_state.mes_atual -= 1
                if st.session_state.mes_atual < 1:  # Se passou de janeiro
                    st.session_state.mes_atual = 12   # Volta para dezembro
                    st.session_state.ano_atual -= 1   # Do ano anterior
                st.rerun()
        
        with col_p2:
            # Mostrar mês e ano atual
            st.markdown(f'<div style="text-align: center; padding: 8px; font-size: 18px; font-weight: bold; color: #1e4d2b;">{MESES_PT[st.session_state.mes_atual-1]} {st.session_state.ano_atual}</div>', unsafe_allow_html=True)
        
        with col_p3:
            # Botão para próximo mês
            if st.button("Próximo ▶️", key="next_mes"):
                st.session_state.mes_atual += 1
                if st.session_state.mes_atual > 12:  # Se passou de dezembro
                    st.session_state.mes_atual = 1     # Volta para janeiro
                    st.session_state.ano_atual += 1    # Do ano seguinte
                st.rerun()
        
        # ===== GERAR CALENDÁRIO DO MÊS =====
        # calendar.monthcalendar retorna uma matriz com as semanas do mês
        cal = calendar.monthcalendar(st.session_state.ano_atual, st.session_state.mes_atual)
        
        # Dias da semana
        dias_semana = ['seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.', 'dom.']
        
        # Começar HTML do calendário
        html_cal = '<div class="calendario-grid">'
        
        # Adicionar cabeçalho (seg, ter, qua, ...)
        for dia in dias_semana:
            html_cal += f'<div class="cal-header">{dia}</div>'
        
        # ===== CALCULAR EVENTOS (PAGAMENTOS) DO MÊS =====
        # Dicionário: {dia: [lista de fundos que pagam neste dia]}
        eventos_mes = {}
        
        # Para cada fundo do cliente
        for _, fundo in fundos_cliente.iterrows():
            try:
                # Buscar info do fundo
                info = buscar_info_fundo(
                    fundo.get('Fundo', ''), 
                    MAPA_PAGAMENTOS, 
                    MAPA_CORES, 
                    MAPA_SIGLAS, 
                    MAPA_TESES, 
                    fundo
                )
                
                # Pegar dia útil de pagamento da coluna 'Data' do Excel
                try:
                    data_str = str(fundo.get('Data', '')).strip()
                    if data_str not in ['-', '', 'nan', 'None']:
                        dia_util = int(float(data_str))
                    else:
                        dia_util = None
                except (ValueError, TypeError):
                    dia_util = None
                
                # Se tem dia útil definido
                if dia_util and dia_util > 0:
                    try:
                        # Calcular a data real de pagamento
                        data_pagamento = calcular_dia_util(
                            st.session_state.ano_atual, 
                            st.session_state.mes_atual, 
                            dia_util, 
                            feriados
                        )
                        
                        if data_pagamento:
                            dia = data_pagamento.day
                            
                            # Adicionar este fundo na lista de eventos deste dia
                            if dia not in eventos_mes:
                                eventos_mes[dia] = []
                            
                            eventos_mes[dia].append({
                                'sigla': info.get('sigla', str(fundo.get('Fundo', 'N/A'))[:10]), 
                                'cor': info.get('cor', '#27ae60')
                            })
                    except Exception:
                        pass  # Se der erro, apenas pula
            
            except Exception as e:
                continue  # Se houver erro, pula este fundo
        
        # ===== CRIAR GRID DO CALENDÁRIO =====
        # Para cada semana do mês
        for semana in cal:
            # Para cada dia da semana
            for dia in semana:
                
                if dia == 0:
                    # Dia vazio (antes do início ou depois do fim do mês)
                    html_cal += '<div class="cal-dia" style="background: #f8f9fa;"></div>'
                
                else:
                    # Criar objeto date para este dia
                    data = date(st.session_state.ano_atual, st.session_state.mes_atual, dia)
                    
                    # Definir classe CSS (fim de semana tem cor diferente)
                    classe = "cal-dia fim-semana" if data.weekday() >= 5 else "cal-dia" 
                    
                    # Ver se tem eventos (pagamentos) neste dia
                    eventos_html = ""
                    if dia in eventos_mes:
                        # Para cada fundo que paga neste dia
                        for evento in eventos_mes[dia]:
                            # Adicionar um "chip" colorido com a sigla do fundo
                            eventos_html += f'<div class="cal-evento" style="background: {evento["cor"]}">{evento["sigla"]}</div>'
                    
                    # Adicionar este dia ao HTML
                    html_cal += f'<div class="{classe}"><div class="numero">{dia}</div>{eventos_html}</div>'
        
        # Fechar HTML do calendário
        html_cal += '</div>'
        
        # Mostrar o calendário na tela
        st.markdown(html_cal, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# PONTO DE ENTRADA DO PROGRAMA
# ==============================================================================
# Esta parte é executada quando o programa inicia
if __name__ == "__main__":
    main()  # Chama a função principal
