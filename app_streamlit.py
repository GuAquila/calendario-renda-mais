"""
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
======================================================
Sistema multi-assessor com senhas individuais
VERSÃO CORRIGIDA - 25/10/2025
Usa APENAS aba "Base" do Excel

CÓDIGO EXPLICADO PARA INICIANTES:
- Este código cria um sistema web usando Streamlit
- Cada assessor tem seu login e senha
- Mostra os fundos e valores aplicados de cada cliente
"""

# ============================================
# PARTE 1: IMPORTAR BIBLIOTECAS
# ============================================
# Aqui importamos as ferramentas que vamos usar

import streamlit as st  # Para criar a interface web
import pandas as pd  # Para trabalhar com Excel e tabelas
from datetime import datetime, date, timedelta  # Para trabalhar com datas
import calendar  # Para criar calendários
import os  # Para verificar se arquivos existem

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
# Aqui configuramos como a página vai aparecer

st.set_page_config(
    page_title="Calendário Renda Mais - TAUARI",  # Título da aba do navegador
    page_icon="🌳",  # Ícone que aparece na aba
    layout="wide",  # Página larga (usa toda a tela)
    initial_sidebar_state="collapsed"  # Barra lateral fechada
)

# ============================================
# PARTE 2: LISTA DE ASSESSORES E SENHAS
# ============================================
# Cada assessor tem um código (chave) e um nome + senha (valor)

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

# ============================================
# PARTE 3: FUNÇÃO PARA VALIDAR SENHA
# ============================================
def validar_senha_assessor(codigo_assessor, senha):
    """
    Esta função verifica se o código e senha do assessor estão corretos
    
    PARÂMETROS:
    - codigo_assessor: o código que o assessor digitou (exemplo: '46857')
    - senha: a senha que o assessor digitou (exemplo: 'GA2025')
    
    RETORNA:
    - True/False: se a senha está correta
    - nome_assessor: o nome do assessor (ou None se errado)
    """
    
    # Verifica se o código existe na lista
    if codigo_assessor not in ASSESSORES:
        return False, None  # Código não existe
    
    # Pega o nome e senha esperada deste assessor
    nome_assessor, senha_esperada = ASSESSORES[codigo_assessor]
    
    # Verifica se a senha digitada está correta
    if senha == senha_esperada:
        return True, nome_assessor  # Senha correta!
    
    return False, None  # Senha errada

# ============================================
# PARTE 4: FUNÇÃO PARA CARREGAR O EXCEL
# ============================================
def carregar_dados_excel():
    """
    Esta função carrega os dados do arquivo Excel
    
    IMPORTANTE: O arquivo 'calendario_Renda_mais.xlsx' deve estar
    na MESMA PASTA que este código!
    
    RETORNA:
    - df_base: tabela com todos os dados (ou None se der erro)
    """
    
    # Nome do arquivo Excel
    nome_arquivo = 'calendario_Renda_mais.xlsx'
    nome_aba = 'Base'  # Nome da aba que queremos usar
    
    # PASSO 1: Verificar se o arquivo existe
    if not os.path.exists(nome_arquivo):
        st.error(f"""
        ❌ ERRO: Arquivo Excel não encontrado!
        
        O arquivo '{nome_arquivo}' não está na mesma pasta do código.
        
        📁 Certifique-se de que o arquivo está no lugar correto:
        - No GitHub: deve estar na raiz do repositório
        - No computador: deve estar na mesma pasta do app_streamlit.py
        """)
        return None
    
    # PASSO 2: Tentar carregar o arquivo
    try:
        # Lê o arquivo Excel, especificamente a aba "Base"
        df_base = pd.read_excel(nome_arquivo, sheet_name=nome_aba)
        
        # Mostra mensagem de sucesso (só para debug)
        st.success(f"✅ Dados carregados com sucesso! Total de registros: {len(df_base)}")
        
        # PASSO 3: Verificar se as colunas necessárias existem
        colunas_necessarias = ['Assessor', 'Cliente', 'Ativo', 'Aplicação', 'Rendimento %']
        colunas_faltando = [col for col in colunas_necessarias if col not in df_base.columns]
        
        if colunas_faltando:
            st.error(f"""
            ❌ ERRO: Colunas faltando no Excel!
            
            As seguintes colunas não foram encontradas na aba '{nome_aba}':
            {', '.join(colunas_faltando)}
            
            Colunas encontradas: {', '.join(df_base.columns.tolist())}
            """)
            return None
        
        # PASSO 4: Garantir que os tipos de dados estão corretos
        # Converte a coluna Aplicação para número (float)
        df_base['Aplicação'] = pd.to_numeric(df_base['Aplicação'], errors='coerce')
        
        # Converte a coluna Rendimento % para número (float)
        df_base['Rendimento %'] = pd.to_numeric(df_base['Rendimento %'], errors='coerce')
        
        # Remove linhas onde Aplicação é nulo ou zero
        df_base = df_base[df_base['Aplicação'].notna()]
        df_base = df_base[df_base['Aplicação'] > 0]
        
        return df_base
        
    except Exception as e:
        # Se der qualquer erro, mostra mensagem clara
        st.error(f"""
        ❌ ERRO ao carregar o arquivo Excel!
        
        Detalhes do erro: {str(e)}
        
        Verifique se:
        1. O arquivo está no lugar correto
        2. A aba '{nome_aba}' existe no Excel
        3. O arquivo não está aberto em outro programa
        """)
        return None

# ============================================
# PARTE 5: CONFIGURAÇÃO DOS FUNDOS
# ============================================
# Aqui definimos as cores, siglas e informações de cada fundo

# Cores para cada tipo de fundo
MAPA_CORES = {
    'ARX FII Portfólio Renda CDI+ RL': '#3498db',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': '#e74c3c',
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': '#9b59b6',
    'Maua Lajes Corporativas Feeder FII RL - Senior': '#1abc9c',
    'Versa Capital Tech FIP-IE': '#f39c12',
}

# Siglas curtas para aparecer no calendário
MAPA_SIGLAS = {
    'ARX FII Portfólio Renda CDI+ RL': 'ARX',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 'AZ INFRA',
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 'AZ PAN',
    'Maua Lajes Corporativas Feeder FII RL - Senior': 'MAUA',
    'Versa Capital Tech FIP-IE': 'VERSA',
}

# Dias úteis de pagamento de cada fundo
MAPA_PAGAMENTOS = {
    'ARX FII Portfólio Renda CDI+ RL': 15,
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 7,
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 7,
    'Maua Lajes Corporativas Feeder FII RL - Senior': 21,
    'Versa Capital Tech FIP-IE': 10,
}

# Informações detalhadas de cada fundo
MAPA_TESES = {
    'ARX FII Portfólio Renda CDI+ RL': {
        'resumo': 'Fundo de renda com portfólio diversificado',
        'condicoes': 'Liquidez: 30 dias\nTaxa: 0,5% a.a.\nImposto: Isento',
        'venda_1min': 'Fundo conservador com rendimento superior ao CDI',
        'perfil': 'Investidores conservadores que buscam renda estável'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'resumo': 'Fundo de infraestrutura com foco em yield',
        'condicoes': 'Liquidez: 90 dias\nTaxa: 2% a.a.\nImposto: 15%',
        'venda_1min': 'Investe em projetos de infraestrutura com retorno atrativo',
        'perfil': 'Investidores moderados com horizonte de longo prazo'
    },
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': {
        'resumo': 'Fundo de renda com estratégia diversificada',
        'condicoes': 'Liquidez: 30 dias\nTaxa: 1% a.a.\nImposto: Regressivo',
        'venda_1min': 'Busca retorno acima do CDI com baixo risco',
        'perfil': 'Investidores conservadores a moderados'
    },
    'Maua Lajes Corporativas Feeder FII RL - Senior': {
        'resumo': 'Fundo imobiliário focado em lajes corporativas',
        'condicoes': 'Liquidez: D+0 (bolsa)\nTaxa: 0% a.a.\nImposto: Isento',
        'venda_1min': 'Renda mensal com imóveis de alto padrão',
        'perfil': 'Investidores que buscam renda passiva'
    },
    'Versa Capital Tech FIP-IE': {
        'resumo': 'Fundo de participações em empresas de tecnologia',
        'condicoes': 'Liquidez: Baixa\nTaxa: 2,5% a.a.\nImposto: 15%',
        'venda_1min': 'Investe em startups e scale-ups de tecnologia',
        'perfil': 'Investidores arrojados com perfil de venture capital'
    },
}

def buscar_info_fundo(nome_fundo, mapa_pag, mapa_cor, mapa_sig, mapa_tese):
    """
    Busca informações de um fundo específico
    
    PARÂMETROS:
    - nome_fundo: nome do fundo para buscar
    - mapa_pag: dicionário com dias de pagamento
    - mapa_cor: dicionário com cores
    - mapa_sig: dicionário com siglas
    - mapa_tese: dicionário com informações detalhadas
    
    RETORNA:
    - Dicionário com todas as informações do fundo
    """
    return {
        'dia_util': mapa_pag.get(nome_fundo, 0),
        'cor': mapa_cor.get(nome_fundo, '#27ae60'),
        'sigla': mapa_sig.get(nome_fundo, nome_fundo[:10]),
        'tese': mapa_tese.get(nome_fundo, {
            'resumo': 'Informação não disponível',
            'condicoes': 'Consultar gestor',
            'venda_1min': 'Consultar gestor',
            'perfil': 'Consultar gestor'
        })
    }

# ============================================
# PARTE 6: FUNÇÕES PARA CÁLCULO DE DATAS
# ============================================

# Lista de feriados nacionais de 2025
feriados = [
    date(2025, 1, 1),   # Ano Novo
    date(2025, 4, 18),  # Sexta-feira Santa
    date(2025, 4, 21),  # Tiradentes
    date(2025, 5, 1),   # Dia do Trabalho
    date(2025, 6, 19),  # Corpus Christi
    date(2025, 9, 7),   # Independência
    date(2025, 10, 12), # Nossa Senhora Aparecida
    date(2025, 11, 2),  # Finados
    date(2025, 11, 15), # Proclamação da República
    date(2025, 12, 25), # Natal
]

def eh_dia_util(data, lista_feriados):
    """
    Verifica se uma data é dia útil (não é fim de semana nem feriado)
    
    PARÂMETROS:
    - data: a data para verificar
    - lista_feriados: lista com todos os feriados
    
    RETORNA:
    - True se for dia útil, False se não for
    """
    # weekday() retorna: 0=segunda, 1=terça, ..., 5=sábado, 6=domingo
    # Se for >= 5, é fim de semana
    if data.weekday() >= 5:
        return False
    
    # Se estiver na lista de feriados, não é dia útil
    if data in lista_feriados:
        return False
    
    return True

def calcular_dia_util(ano, mes, numero_dia_util, lista_feriados):
    """
    Calcula qual é o Xº dia útil do mês
    
    Exemplo: Se numero_dia_util = 5, retorna o 5º dia útil do mês
    
    PARÂMETROS:
    - ano: ano desejado (ex: 2025)
    - mes: mês desejado (ex: 10 para outubro)
    - numero_dia_util: qual dia útil queremos (ex: 5 = 5º dia útil)
    - lista_feriados: lista com todos os feriados
    
    RETORNA:
    - A data do Xº dia útil do mês
    """
    # Começa no primeiro dia do mês
    data_atual = date(ano, mes, 1)
    dias_uteis_contados = 0
    
    # Continua contando até encontrar o dia útil desejado
    while dias_uteis_contados < numero_dia_util:
        # Se for dia útil, aumenta o contador
        if eh_dia_util(data_atual, lista_feriados):
            dias_uteis_contados += 1
            
            # Se chegou no dia útil desejado, retorna
            if dias_uteis_contados == numero_dia_util:
                return data_atual
        
        # Passa para o próximo dia
        data_atual += timedelta(days=1)
        
        # Se passou para o próximo mês, algo deu errado
        if data_atual.month != mes:
            return None
    
    return data_atual

# ============================================
# PARTE 7: NOMES DOS MESES EM PORTUGUÊS
# ============================================
MESES_PT = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 
    'Maio', 'Junho', 'Julho', 'Agosto',
    'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

# ============================================
# PARTE 8: TELA DE LOGIN
# ============================================
def verificar_autenticacao(df_base):
    """
    Mostra a tela de login para o assessor
    
    PARÂMETROS:
    - df_base: tabela com os dados do Excel
    """
    
    # Inicializar variáveis de sessão (memória do sistema)
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    if 'assessor_logado' not in st.session_state:
        st.session_state.assessor_logado = None
    if 'nome_assessor' not in st.session_state:
        st.session_state.nome_assessor = None
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'
    
    # Se não está autenticado, mostra tela de login
    if not st.session_state.autenticado:
        # CSS para deixar a página bonita
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
        
        # Cria 3 colunas para centralizar o conteúdo
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Tenta mostrar a logo
            try:
                st.image("logo_tauari.png", width=350)
            except:
                st.markdown("<div style='text-align: center; padding: 20px;'><div style='background: #2d5a3d; color: white; padding: 40px; border-radius: 10px; font-size: 14px;'>📁 Salve a logo como 'logo_tauari.png'<br>na mesma pasta do código</div></div>", unsafe_allow_html=True)
            
            # Título da página
            st.markdown("""
            <div class="login-titulo">
                <h2 style='margin: 10px 0; font-size: 24px;'>Calendário Renda Mais - Tauari Investimentos</h2>
                <p style='color: #7f8c8d; font-size: 14px; margin-top: 15px;'>Acesso restrito por Assessor - Última atualização 25/10/2025</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Formulário de login
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
                
                # Quando clicar em "Entrar"
                if submitted:
                    # Verifica se preencheu todos os campos
                    if not codigo_assessor or not senha_assessor:
                        st.error("❌ Preencha todos os campos!")
                    else:
                        # Valida a senha
                        valido, nome_assessor = validar_senha_assessor(codigo_assessor, senha_assessor)
                        
                        if valido:
                            # Senha correta! Agora verifica se tem clientes
                            if df_base is not None:
                                # Garante que a coluna Assessor é texto
                                df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
                                
                                # Filtra apenas os clientes deste assessor
                                clientes_assessor = df_base[df_base['Assessor'] == str(codigo_assessor)]
                                
                                if clientes_assessor.empty:
                                    st.error(f"❌ Nenhum cliente encontrado para o Assessor {codigo_assessor}")
                                else:
                                    # Tudo certo! Faz o login
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
            
            # Informações de ajuda
            st.markdown("""
            <div class="login-info">
                <strong>ℹ️ Como acessar:</strong><br>
                • Digite seu código de assessor (apenas números)<br>
                • Digite sua senha pessoal<br>
                • Em caso de dúvidas: <strong>gustavo.aquila@tauariinvestimentos.com.br</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Para a execução aqui (não mostra o resto do código)
        st.stop()

# ============================================
# PARTE 9: CSS PARA DEIXAR O SISTEMA BONITO
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
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    .header-titulo {
        color: white;
        font-size: 28px;
        font-weight: bold;
        margin: 0;
    }
    
    .info-assessor {
        color: white;
        font-size: 14px;
        margin-top: 8px;
    }
    
    .cliente-selector {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 25px;
        border-left: 5px solid #27ae60;
    }
    
    .cliente-selector h3 {
        margin: 0 0 15px 0;
        color: #1e4d2b;
    }
    
    .container-principal {
        display: flex;
        gap: 20px;
        margin-top: 20px;
    }
    
    .box {
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    .box-titulo {
        background: #1e4d2b;
        color: white;
        padding: 15px;
        font-weight: bold;
        font-size: 14px;
    }
    
    .box-conteudo {
        padding: 15px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .fundo-card-container {
        margin-bottom: 15px;
    }
    
    .fundo-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #27ae60;
        transition: all 0.3s;
    }
    
    .fundo-card:hover {
        background: #e9ecef;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .fundo-card-selecionado {
        background: #e8f5e9 !important;
        border-left-width: 6px !important;
    }
    
    .fundo-card .nome {
        font-weight: bold;
        color: #1e4d2b;
        margin-bottom: 8px;
    }
    
    .fundo-card .info {
        font-size: 13px;
        color: #495057;
    }
    
    .fundo-card .valor {
        color: #27ae60;
        font-weight: bold;
    }
    
    .tese-texto {
        padding: 20px;
        line-height: 1.6;
    }
    
    .tese-texto h4 {
        color: #1e4d2b;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    
    .calendario-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        padding: 15px;
    }
    
    .cal-header {
        text-align: center;
        font-weight: bold;
        padding: 8px;
        background: #1e4d2b;
        color: white;
        border-radius: 5px;
        font-size: 12px;
    }
    
    .cal-dia {
        min-height: 80px;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 5px;
        background: white;
    }
    
    .cal-dia.fim-semana {
        background: #f8f9fa;
    }
    
    .cal-dia .numero {
        font-weight: bold;
        color: #495057;
        margin-bottom: 3px;
    }
    
    .cal-evento {
        font-size: 10px;
        padding: 2px 4px;
        margin: 2px 0;
        border-radius: 3px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# PARTE 10: FUNÇÃO PRINCIPAL DO SISTEMA
# ============================================
def main():
    """
    Função principal que roda todo o sistema
    
    Esta é a função que executa quando o Streamlit inicia
    """
    
    # PASSO 1: Carregar dados do Excel
    df_base = carregar_dados_excel()
    
    # Se não conseguiu carregar, para aqui
    if df_base is None:
        st.stop()
    
    # PASSO 2: Verificar autenticação (login)
    verificar_autenticacao(df_base)
    
    # PASSO 3: Mostrar o cabeçalho do sistema
    st.markdown(f"""
    <div class="header-sistema">
        <div class="header-titulo">🌳 Calendário Renda Mais - Tauari Investimentos</div>
        <div class="info-assessor">
            👤 Assessor: <strong>{st.session_state.nome_assessor}</strong> | 
            Código: <strong>{st.session_state.assessor_logado}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # PASSO 4: Botões de ação
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        if st.button("🔓 Sair", key="btn_sair"):
            st.session_state.autenticado = False
            st.session_state.assessor_logado = None
            st.session_state.nome_assessor = None
            st.session_state.pagina_atual = 'login'
            st.rerun()
    
    # PASSO 5: Filtrar dados do assessor logado
    df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
    df_base_filtrado = df_base[df_base['Assessor'] == str(st.session_state.assessor_logado)]
    
    if df_base_filtrado.empty:
        st.error("❌ Nenhum cliente encontrado!")
        st.stop()
    
    # PASSO 6: Seletor de cliente
    st.markdown('<div class="cliente-selector"><h3>👥 SELECIONE O CLIENTE</h3>', unsafe_allow_html=True)
    
    clientes = sorted(df_base_filtrado['Cliente'].unique())
    cliente_selecionado = st.selectbox(
        "Cliente", 
        [""] + list(clientes), 
        label_visibility="collapsed", 
        key="cliente_select"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not cliente_selecionado:
        st.stop()
    
    # PASSO 7: Pegar todos os fundos do cliente selecionado
    fundos_cliente = df_base_filtrado[df_base_filtrado['Cliente'] == cliente_selecionado]

    # Inicializar o fundo selecionado
    if 'fundo_selecionado' not in st.session_state:
        st.session_state.fundo_selecionado = fundos_cliente['Ativo'].iloc[0] if not fundos_cliente.empty else None
    
    # PASSO 8: Criar as 3 colunas principais
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    # ===========================================
    # COLUNA 1: LISTA DE FUNDOS DO CLIENTE
    # ===========================================
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        # Para cada fundo do cliente
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            
            # IMPORTANTE: Aqui pegamos o valor aplicado da coluna "Aplicação"
            try:
                valor_aplicado = float(fundo['Aplicação'])
            except:
                valor_aplicado = 0.0
            
            # Pega o percentual de rendimento
            try:
                percentual_liquido = float(fundo['Rendimento %'])
            except:
                percentual_liquido = 0.0
            
            # Calcula o valor líquido que o cliente vai receber
            valor_liquido_cupom = valor_aplicado * percentual_liquido
            
            # Busca informações do fundo
            info = buscar_info_fundo(ativo, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
            
            # Calcula a data de pagamento
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
            
            # Define se este fundo está selecionado
            classe_selecao = 'fundo-card-selecionado' if ativo == st.session_state.fundo_selecionado else ''
            
            # Mostra o card do fundo
            st.markdown(f"""
            <div class="fundo-card-container">
                <div class="fundo-card {classe_selecao}" style="border-left-color: {info.get('cor', '#27ae60')}">
                    <div class="nome">{ativo}</div>
                    <div class="info" style="margin-top: 8px;">
                        <div style="margin-bottom: 4px;">💰 <strong>Valor Aplicado:</strong> <span class="valor">R$ {valor_aplicado:,.2f}</span></div>
                        <div style="margin-bottom: 4px;">📅 <strong>Data Pagamento:</strong> {data_texto}</div>
                        <div style="margin-bottom: 4px;">📈 <strong>% Líquido:</strong> <span class="valor">{percentual_liquido:.2%}</span></div>
                        <div>💵 <strong>Valor Líquido:</strong> <span class="valor">R$ {valor_liquido_cupom:,.2f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Botão para selecionar o fundo
            if st.button("📊", key=f"sel_{ativo}", help=f"Selecionar {ativo}"):
                st.session_state.fundo_selecionado = ativo
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ===========================================
    # COLUNA 2: INFORMAÇÕES DO FUNDO
    # ===========================================
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        if st.session_state.fundo_selecionado:
            info = buscar_info_fundo(st.session_state.fundo_selecionado, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
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
    
    # ===========================================
    # COLUNA 3: CALENDÁRIO
    # ===========================================
    with col3:
        st.markdown('<div class="box"><div class="box-titulo">📅 CALENDÁRIO</div>', unsafe_allow_html=True)
        
        # Inicializar mês e ano atual
        if 'mes_atual' not in st.session_state:
            st.session_state.mes_atual = datetime.now().month
            st.session_state.ano_atual = datetime.now().year
        
        # Botões para navegar entre meses
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
        
        # Gerar calendário do mês
        cal = calendar.monthcalendar(st.session_state.ano_atual, st.session_state.mes_atual)
        
        # Cabeçalho dos dias da semana
        dias_semana = ['seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.', 'dom.']
        html_cal = '<div class="calendario-grid">'
        
        for dia in dias_semana:
            html_cal += f'<div class="cal-header">{dia}</div>'
        
        # Calcular eventos (pagamentos) do mês
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
        
        # Gerar os dias do calendário
        for semana in cal:
            for dia in semana:
                if dia == 0:
                    # Dia vazio (de outro mês)
                    html_cal += '<div class="cal-dia" style="background: #f8f9fa;"></div>'
                else:
                    # Criar o objeto data
                    data = date(st.session_state.ano_atual, st.session_state.mes_atual, dia)
                    
                    # Definir classe (fim de semana ou não)
                    classe = "cal-dia fim-semana" if data.weekday() >= 5 else "cal-dia" 
                    
                    # Adicionar eventos (pagamentos) do dia
                    eventos_html = ""
                    if dia in eventos_mes:
                        for evento in eventos_mes[dia]:
                            eventos_html += f'<div class="cal-evento" style="background: {evento["cor"]}">{evento["sigla"]}</div>'
                    
                    html_cal += f'<div class="{classe}"><div class="numero">{dia}</div>{eventos_html}</div>'
        
        html_cal += '</div>'
        st.markdown(html_cal, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# EXECUTA O SISTEMA
# ============================================
if __name__ == "__main__":
    main()
