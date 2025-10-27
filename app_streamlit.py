"""
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
======================================================
Sistema multi-assessor com senhas individuais
VERSÃO FINAL LIMPA - 26/10/2025
Usa APENAS aba "Base" do Excel

MODIFICAÇÃO: Página "Conheça os Fundos" agora destaca o fundo selecionado no topo
ATUALIZAÇÃO: Código ajustado para ler corretamente os dados do Excel
"""

# ============================================
# IMPORTAÇÃO DE BIBLIOTECAS
# ============================================
# Estas são as ferramentas que o Python vai usar
import streamlit as st  # Para criar a interface web
import pandas as pd  # Para trabalhar com planilhas/dados
from datetime import datetime, date, timedelta  # Para trabalhar com datas
import calendar  # Para criar calendários
import os  # Para trabalhar com arquivos do sistema

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
# Aqui configuramos como a página vai aparecer no navegador
st.set_page_config(
    page_title="Calendário Renda Mais - TAUARI",  # Título que aparece na aba do navegador
    page_icon="🌳",  # Ícone que aparece na aba
    layout="wide",  # Layout largo (usa toda a tela)
    initial_sidebar_state="collapsed"  # Barra lateral começa fechada
)

# ============================================
# AUTENTICAÇÃO POR ASSESSOR
# ============================================
# Dicionário com os assessores e suas senhas
# Formato: 'código': ('Nome Completo', 'Senha')
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
    """
    Função que valida se a senha do assessor está correta
    
    Parâmetros:
    - codigo_assessor: o código digitado pelo assessor
    - senha: a senha digitada
    
    Retorna:
    - True/False: se a senha está correta
    - nome_assessor: o nome do assessor (ou None se errado)
    """
    # Verifica se o código existe no dicionário
    if codigo_assessor not in ASSESSORES:
        return False, None
    
    # Pega o nome e senha esperada do assessor
    nome_assessor, senha_esperada = ASSESSORES[codigo_assessor]
    
    # Compara a senha digitada com a senha esperada
    if senha == senha_esperada:
        return True, nome_assessor
    return False, None

def verificar_autenticacao(df_base):
    """
    Função que cria a tela de login
    Só deixa o usuário entrar se a senha estiver correta
    """
    
    # Inicializa variáveis de controle na sessão
    # session_state guarda informações enquanto o programa está rodando
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    if 'assessor_logado' not in st.session_state:
        st.session_state.assessor_logado = None
    if 'nome_assessor' not in st.session_state:
        st.session_state.nome_assessor = None
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'login'
    
    # Se o usuário NÃO está autenticado, mostra a tela de login
    if not st.session_state.autenticado:
        # CSS para deixar a tela de login bonita
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
        
        # Cria 3 colunas, sendo a do meio maior
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Tenta mostrar o logo (se existir)
            try:
                st.image("logo_tauari.png", width=350)
            except:
                # Se não encontrar o logo, não faz nada
                st.markdown("<div style='text-align: center; padding: 20px;'><div style='background: #2d5a3d; color: white; padding: 40px; border-radius: 10px; font-size: 14px;'", unsafe_allow_html=True)
            
            # Título da página de login
            st.markdown("""
            <div class="login-titulo">
                <h2 style='margin: 10px 0; font-size: 24px;'>Calendário Renda Mais - Tauari Investimentos</h2>
                <p style='color: #7f8c8d; font-size: 14px; margin-top: 15px;'>Acesso restrito por Assessor (uso interno) - Última atualização 24/10</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Cria o formulário de login
            with st.form("login_form"):
                # Campo para digitar o código do assessor
                codigo_assessor = st.text_input(
                    "👤 Código do Assessor:",
                    placeholder="Coloque seu código, exemplo: 46857",
                    max_chars=10,
                    key="codigo_input"
                )
                
                # Campo para digitar a senha (fica oculta com asteriscos)
                senha_assessor = st.text_input(
                    "🔐 Senha do Assessor:",
                    type="password",
                    placeholder="Digite sua senha",
                    max_chars=20,
                    key="senha_input"
                )
                
                # Botão para enviar o formulário
                submitted = st.form_submit_button("🔓 Entrar", use_container_width=True)
                
                # Quando o botão é clicado
                if submitted:
                    # Verifica se os campos foram preenchidos
                    if not codigo_assessor or not senha_assessor:
                        st.error("❌ Preencha todos os campos!")
                    else:
                        # Valida a senha
                        valido, nome_assessor = validar_senha_assessor(codigo_assessor, senha_assessor)
                        
                        if valido:
                            # Se a senha está certa, verifica se tem clientes para este assessor
                            if df_base is not None:
                                # AJUSTE IMPORTANTE: Remove o "A" do código do assessor no Excel
                                # No Excel está como "A22359", mas no código precisa ser "22359"
                                df_base['Assessor_Limpo'] = df_base['Código do Assessor'].astype(str).str.replace('A', '').str.strip()
                                
                                # Busca clientes deste assessor
                                clientes_assessor = df_base[df_base['Assessor_Limpo'] == str(codigo_assessor)]
                                
                                if clientes_assessor.empty:
                                    st.error(f"❌ Nenhum cliente encontrado para o Assessor {codigo_assessor}")
                                else:
                                    # Tudo certo! Faz o login
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
            
            # Instruções de acesso
            st.markdown("""
            <div class="login-info">
                <strong>ℹ️ Como acessar:</strong><br>
                • Digite seu código de assessor (apenas números)<br>
                • Digite sua senha pessoal<br>
                • Em caso de dúvidas: <strong>gustavo.aquila@tauariinvestimentos.com.br</strong>
            </div>
            """, unsafe_allow_html=True)
        
        st.stop()  # Para a execução aqui se não estiver autenticado

# ============================================
# CSS - ESTILOS DA PÁGINA
# ============================================
# Este CSS deixa a página bonita e organizada
st.markdown("""
<style>
    .stApp {
        background: white !important;
    }
    
    .header-sistema {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .header-sistema h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
    }
    
    .header-sistema p {
        margin: 8px 0 0 0;
        font-size: 14px;
        opacity: 0.95;
    }
    
    .box {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        height: 100%;
    }
    
    .box-titulo {
        font-size: 16px;
        font-weight: 700;
        color: #1e4d2b;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e8f5e9;
    }
    
    .box-conteudo {
        overflow-y: auto;
        max-height: 550px;
    }
    
    .fundo-card-container {
        display: flex;
        align-items: stretch;
        margin-bottom: 12px;
    }
    
    .fundo-card {
        background: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid;
        flex: 1;
        transition: all 0.2s;
    }
    
    .fundo-card:hover {
        background: #e8f5e9;
        transform: translateX(3px);
    }
    
    .fundo-card-selecionado {
        background: #e8f5e9 !important;
        box-shadow: 0 2px 8px rgba(39, 174, 96, 0.2);
    }
    
    .fundo-card .nome {
        font-weight: 600;
        color: #2c3e50;
        font-size: 13px;
        line-height: 1.3;
    }
    
    .fundo-card .info {
        font-size: 11px;
        color: #7f8c8d;
        line-height: 1.5;
    }
    
    .fundo-card .valor {
        color: #27ae60;
        font-weight: 600;
    }
    
    .tese-texto {
        line-height: 1.7;
        color: #2c3e50;
        font-size: 13px;
    }
    
    .tese-texto h4 {
        color: #1e4d2b;
        font-size: 14px;
        margin-top: 15px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .tese-texto p {
        margin-bottom: 12px;
        text-align: justify;
    }
    
    .calendario-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 4px;
        margin-top: 15px;
    }
    
    .cal-header {
        background: #1e4d2b;
        color: white;
        padding: 8px;
        text-align: center;
        font-size: 11px;
        font-weight: 600;
        border-radius: 5px;
    }
    
    .cal-dia {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 6px;
        min-height: 70px;
        border-radius: 5px;
        transition: all 0.2s;
    }
    
    .cal-dia:hover {
        background: #f8f9fa;
        transform: scale(1.03);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .cal-dia.fim-semana {
        background: #f5f5f5;
    }
    
    .cal-dia .numero {
        font-weight: 600;
        color: #2c3e50;
        font-size: 12px;
        margin-bottom: 4px;
    }
    
    .cal-evento {
        background: #27ae60;
        color: white;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 9px;
        margin-top: 2px;
        text-align: center;
        font-weight: 600;
    }
    
    .container-principal {
        margin-top: 20px;
    }
    
    .info-cliente {
        background: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #27ae60;
    }
    
    .info-cliente strong {
        color: #1e4d2b;
    }
    
    .selecao-cliente {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    
    .titulo-selecao {
        color: #1e4d2b;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONSTANTES - INFORMAÇÕES FIXAS
# ============================================

# Nomes dos meses em português
MESES_PT = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

# Feriados nacionais (formato: mês/dia)
FERIADOS_NACIONAIS = [
    (1, 1),   # Ano Novo
    (4, 21),  # Tiradentes
    (5, 1),   # Dia do Trabalho
    (9, 7),   # Independência
    (10, 12), # Nossa Senhora Aparecida
    (11, 2),  # Finados
    (11, 15), # Proclamação da República
    (12, 25), # Natal
]

# Dias de pagamento de cada fundo (qual dia útil do mês)
MAPA_PAGAMENTOS = {
    'ARX FII Portfólio Renda CDI+ RL': 5,
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 10,
    'AZ Quest Panorama Renda Mais (1ª Emissão)': 10,
    'Maua Lajes Corporativas Feeder FII RL - Senior': 10,
    'AZ Quest Panorama Renda Mais (2ª Emissão)': 10,
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': 5,
    'SPX CRI Portfolio Renda Mais': 10,
    'Valora CRI CDI Renda+ FII RL': 10,
    'XP Habitat Renda Imobiliária Feeder FII': 10,
    'XP Renda Imobiliária Feeder FII RL': 10,
}

# Cores para cada fundo (para o calendário ficar colorido)
MAPA_CORES = {
    'ARX FII Portfólio Renda CDI+ RL': '#e74c3c',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': '#3498db',
    'AZ Quest Panorama Renda Mais (1ª Emissão)': '#9b59b6',
    'Maua Lajes Corporativas Feeder FII RL - Senior': '#f39c12',
    'AZ Quest Panorama Renda Mais (2ª Emissão)': '#1abc9c',
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': '#e67e22',
    'SPX CRI Portfolio Renda Mais': '#34495e',
    'Valora CRI CDI Renda+ FII RL': '#16a085',
    'XP Habitat Renda Imobiliária Feeder FII': '#27ae60',
    'XP Renda Imobiliária Feeder FII RL': '#2980b9',
}

# Siglas curtas para mostrar no calendário
MAPA_SIGLAS = {
    'ARX FII Portfólio Renda CDI+ RL': 'ARX',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 'AZ Infra',
    'AZ Quest Panorama Renda Mais (1ª Emissão)': 'AZ Pan 1',
    'Maua Lajes Corporativas Feeder FII RL - Senior': 'Maua',
    'AZ Quest Panorama Renda Mais (2ª Emissão)': 'AZ Pan 2',
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': 'Solis',
    'SPX CRI Portfolio Renda Mais': 'SPX',
    'Valora CRI CDI Renda+ FII RL': 'Valora',
    'XP Habitat Renda Imobiliária Feeder FII': 'XP Habitat',
    'XP Renda Imobiliária Feeder FII RL': 'XP Renda',
}

# Informações detalhadas sobre cada fundo
MAPA_TESES = {
    'ARX FII Portfólio Renda CDI+ RL': {
        'resumo': 'Fundo imobiliário com foco em ativos corporativos de alta qualidade. Rentabilidade atrelada ao CDI com pagamentos mensais.',
        'condicoes': 'Taxa de administração: 0,80% a.a.\nPagamento: 5º dia útil do mês\nRendimento: CDI + spread',
        'venda_1min': 'Fundo que investe em imóveis corporativos de qualidade, pagando rendimentos mensais atrelados ao CDI. Ideal para quem busca renda recorrente com baixa volatilidade.',
        'perfil': 'Investidor conservador a moderado que busca renda mensal com baixo risco.'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'resumo': 'Fundo de investimento em participações focado em infraestrutura, com rendimentos atrativos e gestão especializada.',
        'condicoes': 'Taxa de administração: 1,00% a.a.\nPagamento: 10º dia útil do mês\nRendimento: Distribuição de lucros',
        'venda_1min': 'Investe em empresas de infraestrutura com geração de caixa previsível. Oferece rendimentos mensais atrativos com diversificação em diferentes setores.',
        'perfil': 'Investidor moderado a arrojado que busca rentabilidade acima do CDI com renda mensal.'
    },
    'AZ Quest Panorama Renda Mais (1ª Emissão)': {
        'resumo': 'Fundo multiestratégia com foco em renda fixa e crédito privado, gerido pela AZ Quest.',
        'condicoes': 'Taxa de administração: 0,90% a.a.\nPagamento: 10º dia útil do mês\nRendimento: Pós-fixado',
        'venda_1min': 'Estratégia diversificada em renda fixa e crédito, buscando rentabilidade superior ao CDI com gestão ativa.',
        'perfil': 'Investidor moderado que busca diversificação e rendimentos consistentes.'
    },
    'Maua Lajes Corporativas Feeder FII RL - Senior': {
        'resumo': 'Fundo imobiliário focado em lajes corporativas de alto padrão em São Paulo.',
        'condicoes': 'Taxa de administração: 0,75% a.a.\nPagamento: 10º dia útil do mês\nRendimento: Aluguel + valorização',
        'venda_1min': 'Investe em lajes corporativas AAA em regiões nobres. Combina rendimentos de aluguel com potencial de valorização.',
        'perfil': 'Investidor moderado que busca exposição ao mercado imobiliário corporativo premium.'
    },
    'AZ Quest Panorama Renda Mais (2ª Emissão)': {
        'resumo': 'Segunda emissão do fundo multiestratégia AZ Quest, com estratégia aprimorada.',
        'condicoes': 'Taxa de administração: 0,90% a.a.\nPagamento: 10º dia útil do mês\nRendimento: Pós-fixado',
        'venda_1min': 'Evolução da estratégia Panorama, com foco em crédito privado e renda fixa de qualidade.',
        'perfil': 'Investidor moderado que busca rentabilidade consistente acima do CDI.'
    },
    'Solis Portfolio Crédito CDI+ FIC FIDC RL': {
        'resumo': 'Fundo de crédito privado com foco em operações estruturadas de alta qualidade.',
        'condicoes': 'Taxa de administração: 0,85% a.a.\nPagamento: 5º dia útil do mês\nRendimento: CDI + spread',
        'venda_1min': 'Estratégia focada em crédito privado selecionado, oferecendo prêmio sobre o CDI com risco controlado.',
        'perfil': 'Investidor moderado que aceita risco de crédito em troca de rentabilidade superior.'
    },
    'SPX CRI Portfolio Renda Mais': {
        'resumo': 'Portfólio de Certificados de Recebíveis Imobiliários com diversificação e qualidade.',
        'condicoes': 'Taxa de administração: 0,80% a.a.\nPagamento: 10º dia útil do mês\nRendimento: IPCA+ ou CDI+',
        'venda_1min': 'Diversificação em CRIs de qualidade, oferecendo rendimentos atrelados à inflação ou CDI.',
        'perfil': 'Investidor moderado que busca proteção inflacionária e renda recorrente.'
    },
    'Valora CRI CDI Renda+ FII RL': {
        'resumo': 'Fundo imobiliário focado em CRIs indexados ao CDI, com gestão ativa.',
        'condicoes': 'Taxa de administração: 0,70% a.a.\nPagamento: 10º dia útil do mês\nRendimento: CDI + spread',
        'venda_1min': 'Exposição ao mercado imobiliário via CRIs com rentabilidade pós-fixada e baixa volatilidade.',
        'perfil': 'Investidor conservador a moderado que busca renda imobiliária com liquidez.'
    },
    'XP Habitat Renda Imobiliária Feeder FII': {
        'resumo': 'Fundo que investe em fundos imobiliários diversificados, focado em renda.',
        'condicoes': 'Taxa de administração: 0,60% a.a.\nPagamento: 10º dia útil do mês\nRendimento: Distribuição de FIIs',
        'venda_1min': 'Diversificação automática em múltiplos fundos imobiliários, ideal para quem busca exposição ampla ao setor.',
        'perfil': 'Investidor que deseja diversificação no mercado imobiliário com gestão profissional.'
    },
    'XP Renda Imobiliária Feeder FII RL': {
        'resumo': 'Fundo de fundos imobiliários com foco em geração de renda mensal consistente.',
        'condicoes': 'Taxa de administração: 0,65% a.a.\nPagamento: 10º dia útil do mês\nRendimento: Distribuição de FIIs',
        'venda_1min': 'Acesso simplificado a um portfólio diversificado de fundos imobiliários de qualidade.',
        'perfil': 'Investidor que busca renda mensal através do mercado imobiliário com baixa complexidade.'
    },
}

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def calcular_dia_util(ano, mes, n_dia_util, feriados):
    """
    Calcula o n-ésimo dia útil de um mês
    
    Exemplo: se n_dia_util = 5, retorna o 5º dia útil do mês
    
    Parâmetros:
    - ano: ano desejado (ex: 2025)
    - mes: mês desejado (ex: 10 para outubro)
    - n_dia_util: qual dia útil queremos (ex: 5 = 5º dia útil)
    - feriados: lista com datas de feriados
    """
    try:
        # Começa no primeiro dia do mês
        dia = 1
        # Contador de dias úteis encontrados
        dias_uteis_contados = 0
        
        # Fica procurando até achar o dia útil desejado
        while dia <= 31:
            try:
                # Cria a data atual
                data_atual = date(ano, mes, dia)
                
                # Verifica se é fim de semana (sábado=5, domingo=6)
                eh_fim_semana = data_atual.weekday() >= 5
                
                # Verifica se é feriado
                eh_feriado = (mes, dia) in FERIADOS_NACIONAIS or data_atual in feriados
                
                # Se NÃO é fim de semana E NÃO é feriado, então é dia útil!
                if not eh_fim_semana and not eh_feriado:
                    dias_uteis_contados += 1
                    
                    # Se chegou no dia útil que queremos, retorna!
                    if dias_uteis_contados == n_dia_util:
                        return data_atual
                
                # Vai para o próximo dia
                dia += 1
            except ValueError:
                # Se o dia não existe neste mês, para
                break
        
        # Se não encontrou, retorna None
        return None
    except:
        return None

def buscar_info_fundo(nome_fundo, mapa_pagamentos, mapa_cores, mapa_siglas, mapa_teses):
    """
    Busca todas as informações de um fundo
    
    Retorna um dicionário com:
    - dia_util: em qual dia útil paga
    - cor: cor do fundo no calendário
    - sigla: sigla curta para o calendário
    - tese: informações detalhadas
    """
    return {
        'dia_util': mapa_pagamentos.get(nome_fundo, 0),
        'cor': mapa_cores.get(nome_fundo, '#27ae60'),
        'sigla': mapa_siglas.get(nome_fundo, nome_fundo[:10]),
        'tese': mapa_teses.get(nome_fundo, {})
    }

# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def main():
    """
    Função principal que roda o programa
    """
    
    # ============================================
    # CARREGAR DADOS DO EXCEL
    # ============================================
    try:
        # Tenta ler o arquivo Excel
        # IMPORTANTE: O arquivo deve estar na mesma pasta do programa
        df_base = pd.read_excel('calendario_Renda_mais.xlsx', sheet_name='Base')
        
        # ============================================
        # AJUSTES NOS DADOS DO EXCEL
        # ============================================
        
        # 1. Remove o "A" do código do assessor
        # No Excel: "A22359" → No código: "22359"
        df_base['Assessor'] = df_base['Código do Assessor'].astype(str).str.replace('A', '').str.strip()
        
        # 2. Renomeia as colunas para os nomes que o código espera
        df_base = df_base.rename(columns={
            'Código do Cliente': 'Cliente',  # Cliente agora tem o código
            'Fundo': 'Ativo',  # Nome do fundo
            'Valor Solicitado': 'Aplicação',  # Valor aplicado
        })
        
        # 3. Converte o rendimento de texto para número
        # No Excel: "0.0115" (string) → No código: 0.0115 (float)
        df_base['Rendimento'] = pd.to_numeric(df_base['Rendimento'], errors='coerce')
        
        # 4. Calcula o rendimento em percentual
        # 0.0115 × 100 = 1.15%
        df_base['Rendimento %'] = df_base['Rendimento'] * 100
        
        # 5. Garante que valores vazios sejam zero
        df_base['Aplicação'] = df_base['Aplicação'].fillna(0)
        df_base['Rendimento %'] = df_base['Rendimento %'].fillna(0)
        
        print("✅ Arquivo Excel carregado com sucesso!")
        print(f"Total de registros: {len(df_base)}")
        
    except FileNotFoundError:
        # Se o arquivo não for encontrado
        st.error("❌ Erro: Arquivo 'calendario_Renda_mais.xlsx' não encontrado!")
        st.info("📁 Certifique-se de que o arquivo está na mesma pasta do programa.")
        st.stop()
    except Exception as e:
        # Se houver qualquer outro erro
        st.error(f"❌ Erro ao carregar o Excel: {str(e)}")
        st.stop()
    
    # Lista de feriados do ano (vazia por enquanto, pode adicionar depois)
    feriados = []
    
    # ============================================
    # VERIFICAÇÃO DE AUTENTICAÇÃO
    # ============================================
    # Verifica se o usuário está logado
    verificar_autenticacao(df_base)
    
    # Se chegou aqui, o usuário está autenticado!
    
    # ============================================
    # CABEÇALHO DO SISTEMA
    # ============================================
    # Mostra informações do assessor logado
    st.markdown(f"""
    <div class="header-sistema">
        <h1>🌳 Calendário Renda Mais - Tauari Investimentos</h1>
        <p>Assessor: {st.session_state.nome_assessor} (Código: {st.session_state.assessor_logado})</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão de sair
    col_sair1, col_sair2, col_sair3 = st.columns([6, 1, 1])
    with col_sair3:
        if st.button("🚪 Sair", use_container_width=True):
            # Limpa todas as informações da sessão
            st.session_state.autenticado = False
            st.session_state.assessor_logado = None
            st.session_state.nome_assessor = None
            st.session_state.pagina_atual = 'login'
            st.rerun()
    
    # ============================================
    # FILTRA OS DADOS DO ASSESSOR
    # ============================================
    # Pega apenas os clientes deste assessor
    df_base_filtrado = df_base[df_base['Assessor'] == str(st.session_state.assessor_logado)].copy()
    
    if df_base_filtrado.empty:
        st.warning("⚠️ Nenhum cliente encontrado para este assessor.")
        st.stop()
    
    # Mostra quantos clientes o assessor tem
    st.markdown(f'<div class="info-cliente">📊 <strong>{len(df_base_filtrado["Cliente"].unique())}</strong> clientes encontrados | <strong>{len(df_base_filtrado)}</strong> investimentos ativos</div>', unsafe_allow_html=True)
    
    # ============================================
    # SELEÇÃO DE CLIENTE
    # ============================================
    st.markdown('<div class="selecao-cliente"><div class="titulo-selecao">👤 Selecione o Cliente</div>', unsafe_allow_html=True)
    
    # Pega lista de clientes e ordena
    clientes = sorted(df_base_filtrado['Cliente'].unique())
    
    # Cria menu dropdown para selecionar o cliente
    cliente_selecionado = st.selectbox(
        "Cliente", 
        [""] + list(clientes),  # "" = nenhum selecionado
        label_visibility="collapsed", 
        key="cliente_select"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Se nenhum cliente foi selecionado, para por aqui
    if not cliente_selecionado:
        st.stop()
    
    # ============================================
    # DADOS DO CLIENTE SELECIONADO
    # ============================================
    # Pega todos os fundos que este cliente tem
    fundos_cliente = df_base_filtrado[df_base_filtrado['Cliente'] == cliente_selecionado]

    # Define qual fundo está selecionado (padrão: primeiro da lista)
    if 'fundo_selecionado' not in st.session_state:
        st.session_state.fundo_selecionado = fundos_cliente['Ativo'].iloc[0] if not fundos_cliente.empty else None
    
    # ============================================
    # LAYOUT PRINCIPAL - 3 COLUNAS
    # ============================================
    st.markdown('<div class="container-principal">', unsafe_allow_html=True)
    
    # Cria 3 colunas com tamanhos diferentes
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    # ============================================
    # COLUNA 1: LISTA DE FUNDOS DO CLIENTE
    # ============================================
    with col1:
        st.markdown('<div class="box"><div class="box-titulo">📊 FUNDOS DO CLIENTE</div><div class="box-conteudo">', unsafe_allow_html=True)
        
        # Para cada fundo que o cliente tem
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            
            # Pega o valor aplicado (usa a coluna 'Aplicação' da base)
            try:
                valor_aplicado = float(fundo['Aplicação'])
            except:
                valor_aplicado = 0.0
            
            # Pega o percentual de rendimento
            try:
                percentual_liquido = float(fundo['Rendimento %'])
            except:
                percentual_liquido = 0.0
            
            # Calcula o valor do cupom (rendimento em reais)
            valor_liquido_cupom = valor_aplicado * (percentual_liquido / 100)
            
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
            
            # Formata a data
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
                        <div style="margin-bottom: 4px;">📈 <strong>% Líquido:</strong> <span class="valor">{percentual_liquido:.2f}%</span></div>
                        <div>💵 <strong>Valor Líquido:</strong> <span class="valor">R$ {valor_liquido_cupom:,.2f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Botão para selecionar este fundo
            if st.button("📊", key=f"sel_{ativo}", help=f"Selecionar {ativo}"):
                st.session_state.fundo_selecionado = ativo
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ============================================
    # COLUNA 2: TESE DO FUNDO SELECIONADO
    # ============================================
    with col2:
        st.markdown('<div class="box"><div class="box-titulo">📝 TESE DO FUNDO</div>', unsafe_allow_html=True)
        
        if st.session_state.fundo_selecionado:
            # Busca informações do fundo selecionado
            info = buscar_info_fundo(st.session_state.fundo_selecionado, MAPA_PAGAMENTOS, MAPA_CORES, MAPA_SIGLAS, MAPA_TESES)
            tese = info.get('tese', {})
            
            # Mostra as informações
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
    
    # ============================================
    # COLUNA 3: CALENDÁRIO
    # ============================================
    with col3:
        st.markdown('<div class="box"><div class="box-titulo">📅 CALENDÁRIO</div>', unsafe_allow_html=True)
        
        # Define mês e ano inicial (se ainda não foi definido)
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
        
        # Gera o calendário do mês
        cal = calendar.monthcalendar(st.session_state.ano_atual, st.session_state.mes_atual)
        
        # Cabeçalho do calendário (dias da semana)
        dias_semana = ['seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.', 'dom.']
        html_cal = '<div class="calendario-grid">'
        
        for dia in dias_semana:
            html_cal += f'<div class="cal-header">{dia}</div>'
        
        # Prepara os eventos (pagamentos) do mês
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
        
        # Gera os dias do calendário
        for semana in cal:
            for dia in semana:
                if dia == 0:
                    # Dia vazio (mês anterior/posterior)
                    html_cal += '<div class="cal-dia" style="background: #f8f9fa;"></div>'
                else:
                    # Dia do mês atual
                    data = date(st.session_state.ano_atual, st.session_state.mes_atual, dia)
                    classe = "cal-dia fim-semana" if data.weekday() >= 5 else "cal-dia" 
                    
                    # Adiciona eventos (pagamentos) deste dia
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
# EXECUÇÃO DO PROGRAMA
# ============================================
# Esta é a linha que roda o programa
if __name__ == "__main__":
    main()
