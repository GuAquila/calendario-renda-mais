"""
═══════════════════════════════════════════════════════════════════════
CALENDÁRIO RENDA MAIS - COM AUTENTICAÇÃO POR ASSESSOR
═══════════════════════════════════════════════════════════════════════
Sistema multi-assessor com senhas individuais
VERSÃO FINAL COMENTADA - 25/10/2025

✅ Testado e Funcionando
✅ Detecção automática de colunas
✅ Compatível com qualquer estrutura de Excel
✅ Código 100% comentado para iniciantes

AUTOR: Desenvolvido para Tauari Investimentos
═══════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════
# PARTE 1: IMPORTAR BIBLIOTECAS (FERRAMENTAS)
# ═══════════════════════════════════════════════════════════════════════
# Aqui importamos as "ferramentas" que vamos usar no código
# Pense nelas como caixas de ferramentas diferentes

import streamlit as st  # Cria a interface visual (botões, textos, etc)
import pandas as pd     # Trabalha com Excel e tabelas de dados
from datetime import datetime, date, timedelta  # Trabalha com datas
import calendar         # Cria calendários
import os              # Verifica se arquivos existem no computador

# ═══════════════════════════════════════════════════════════════════════
# PARTE 2: CONFIGURAÇÃO DA PÁGINA
# ═══════════════════════════════════════════════════════════════════════
# Aqui definimos como a página web vai aparecer

st.set_page_config(
    page_title="Calendário Renda Mais - TAUARI",  # Nome na aba do navegador
    page_icon="🌳",                                 # Ícone na aba
    layout="wide",                                  # Usa a tela toda (não centralizado)
    initial_sidebar_state="collapsed"               # Esconde a barra lateral
)

# ═══════════════════════════════════════════════════════════════════════
# PARTE 3: LISTA DE ASSESSORES E SENHAS
# ═══════════════════════════════════════════════════════════════════════
# Este dicionário guarda o código, nome e senha de cada assessor
# Formato: 'CÓDIGO': ('NOME COMPLETO', 'SENHA')

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

# ═══════════════════════════════════════════════════════════════════════
# PARTE 4: FUNÇÃO PARA VALIDAR SENHA
# ═══════════════════════════════════════════════════════════════════════

def validar_senha_assessor(codigo_assessor, senha):
    """
    Esta função verifica se o código e senha do assessor estão corretos.
    
    COMO FUNCIONA:
    1. Recebe o código digitado pelo assessor (exemplo: '46857')
    2. Recebe a senha digitada (exemplo: 'GA2025')
    3. Procura na lista de assessores se o código existe
    4. Se existir, verifica se a senha está correta
    5. Retorna True/False e o nome do assessor
    
    PARÂMETROS:
    - codigo_assessor: o código que o usuário digitou
    - senha: a senha que o usuário digitou
    
    RETORNA:
    - (True, 'Nome do Assessor') se estiver correto
    - (False, None) se estiver errado
    """
    
    # Primeiro, verifica se o código existe na lista de assessores
    if codigo_assessor not in ASSESSORES:
        return False, None  # Código não existe, retorna falso
    
    # Se o código existe, pega o nome e senha esperada
    nome_assessor, senha_esperada = ASSESSORES[codigo_assessor]
    
    # Compara a senha digitada com a senha esperada
    if senha == senha_esperada:
        return True, nome_assessor  # Senha correta! Retorna verdadeiro e o nome
    
    # Se chegou aqui, a senha está errada
    return False, None

# ═══════════════════════════════════════════════════════════════════════
# PARTE 5: FUNÇÃO PARA DETECTAR COLUNAS AUTOMATICAMENTE
# ═══════════════════════════════════════════════════════════════════════

def detectar_colunas(df):
    """
    Esta função detecta automaticamente quais colunas usar no Excel.
    Ela é MUITO IMPORTANTE porque diferentes Excels podem ter nomes
    diferentes para as mesmas colunas!
    
    Por exemplo:
    - Um Excel pode ter coluna "Aplicação"
    - Outro Excel pode ter coluna "Financeiro"
    - Esta função detecta os dois casos!
    
    COMO FUNCIONA:
    1. Recebe a tabela (DataFrame) do Excel
    2. Para cada coluna, verifica o nome
    3. Tenta descobrir qual é a finalidade da coluna
    4. Retorna um dicionário mapeando cada finalidade
    
    PARÂMETRO:
    - df: tabela com os dados do Excel (DataFrame do pandas)
    
    RETORNA:
    - dicionário com as colunas detectadas
      Exemplo: {'assessor': 'Assessor', 'valor': 'Aplicação'}
    """
    
    # Dicionário que vai guardar as colunas detectadas
    colunas_mapeadas = {}
    
    # Lista de possíveis nomes para cada tipo de coluna
    # Quanto mais nomes colocarmos aqui, mais flexível fica!
    mapeamento = {
        # Para identificar a coluna de Assessor
        'assessor': [
            'assessor',
            'código assessor',
            'cod assessor',
            'codigo assessor',
            'ass'
        ],
        
        # Para identificar a coluna de Cliente
        'cliente': [
            'cliente',
            'código cliente',
            'cod cliente',
            'codigo cliente',
            'cli'
        ],
        
        # Para identificar a coluna de Ativo/Fundo
        'ativo': [
            'ativo',
            'fundo',
            'produto',
            'sub produto',
            'investimento',
            'aplicacao'
        ],
        
        # Para identificar a coluna de Valor Aplicado - A MAIS IMPORTANTE!
        'valor': [
            'aplicação',
            'aplicacao',
            'financeiro',       # ← ESTE É O NOVO QUE ADICIONAMOS!
            'valor aplicado',
            'saldo',
            'valor',
            'vlr aplicado',
            'montante'
        ],
        
        # Para identificar a coluna de Rendimento
        'rendimento': [
            'rendimento %',
            'rendimento',
            '% rendimento',
            'percentual',
            'taxa',
            'yield',
            '%'
        ]
    }
    
    # Para cada coluna que existe no Excel
    for coluna_excel in df.columns:
        # Transforma o nome em minúsculas e remove espaços nas pontas
        # Exemplo: "  Financeiro  " vira "financeiro"
        coluna_minuscula = coluna_excel.lower().strip()
        
        # Agora vamos verificar em qual categoria essa coluna se encaixa
        for tipo_coluna, lista_nomes_possiveis in mapeamento.items():
            # Verifica se o nome da coluna está na lista OU
            # se algum nome da lista está contido no nome da coluna
            if coluna_minuscula in lista_nomes_possiveis or \
               any(nome in coluna_minuscula for nome in lista_nomes_possiveis):
                # Encontrou! Guarda o nome original da coluna
                colunas_mapeadas[tipo_coluna] = coluna_excel
                break  # Não precisa verificar mais, já encontrou
    
    # Retorna o dicionário com todas as colunas encontradas
    return colunas_mapeadas

# ═══════════════════════════════════════════════════════════════════════
# PARTE 6: FUNÇÃO PARA CARREGAR O EXCEL
# ═══════════════════════════════════════════════════════════════════════

def carregar_dados_excel():
    """
    Esta é uma das funções MAIS IMPORTANTES do sistema!
    Ela carrega os dados do Excel e prepara tudo para uso.
    
    O QUE ELA FAZ:
    1. Verifica se o arquivo Excel existe
    2. Abre o arquivo
    3. Detecta automaticamente as colunas
    4. Renomeia as colunas para um padrão
    5. Converte os valores para número
    6. Remove linhas inválidas
    7. Retorna os dados prontos para usar
    
    RETORNA:
    - df_padronizado: tabela com os dados prontos para usar
    - None: se der algum erro
    """
    
    # Nome do arquivo que vamos procurar
    # IMPORTANTE: Este arquivo deve estar na mesma pasta do código!
    nome_arquivo = 'calendario_Renda_mais.xlsx'
    nome_aba = 'Base'  # Nome da aba que vamos usar
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 1: Verificar se o arquivo existe
    # ═══════════════════════════════════════════════════════════════════
    
    # os.path.exists() retorna True se o arquivo existe, False se não
    if not os.path.exists(nome_arquivo):
        # Se não existe, mostra mensagem de erro clara
        st.error(f"""
        ❌ ERRO: Arquivo Excel não encontrado!
        
        O arquivo '{nome_arquivo}' não está na mesma pasta do código.
        
        📁 SOLUÇÃO:
        • No computador: coloque o arquivo Excel na mesma pasta deste código
        • No GitHub: faça upload do arquivo no repositório
        • No Streamlit Cloud: o arquivo é carregado automaticamente do GitHub
        
        VERIFICAÇÕES:
        • O nome do arquivo está correto? (maiúsculas/minúsculas)
        • O arquivo tem a extensão .xlsx?
        • O arquivo não está corrompido?
        """)
        return None  # Retorna None para indicar erro
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 2: Tentar abrir o arquivo Excel
    # ═══════════════════════════════════════════════════════════════════
    
    try:
        # pd.read_excel() é a função que abre o Excel
        # Ela lê o arquivo e transforma em uma tabela (DataFrame)
        df_base = pd.read_excel(nome_arquivo, sheet_name=nome_aba)
        
        # Mostra mensagem de sucesso parcial
        st.info(f"📊 Arquivo Excel aberto: {len(df_base)} linhas encontradas")
        
    except Exception as e:
        # Se der QUALQUER erro ao abrir, cai aqui
        st.error(f"""
        ❌ ERRO ao abrir o arquivo Excel!
        
        Detalhes técnicos do erro: {str(e)}
        
        POSSÍVEIS CAUSAS:
        • O arquivo está aberto em outro programa (feche-o!)
        • O arquivo está corrompido (tente abrir no Excel)
        • A aba '{nome_aba}' não existe (verifique o nome)
        • Falta instalar biblioteca: pip install openpyxl
        """)
        return None
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 3: Detectar as colunas automaticamente
    # ═══════════════════════════════════════════════════════════════════
    
    # Chama a função que criamos acima
    colunas_detectadas = detectar_colunas(df_base)
    
    # Mostra quais colunas foram detectadas (para debug)
    st.info(f"""
    🔍 Colunas detectadas:
    {chr(10).join([f'• {tipo}: {nome}' for tipo, nome in colunas_detectadas.items()])}
    """)
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 4: Verificar se encontrou todas as colunas essenciais
    # ═══════════════════════════════════════════════════════════════════
    
    # Lista das colunas que são OBRIGATÓRIAS
    colunas_essenciais = ['assessor', 'cliente', 'ativo', 'valor']
    
    # Verifica se alguma está faltando
    colunas_faltando = []
    for coluna_necessaria in colunas_essenciais:
        if coluna_necessaria not in colunas_detectadas:
            colunas_faltando.append(coluna_necessaria)
    
    # Se faltou alguma coluna essencial
    if colunas_faltando:
        st.error(f"""
        ❌ ERRO: Não foi possível identificar todas as colunas necessárias!
        
        📋 Colunas que existem no Excel:
        {', '.join(df_base.columns.tolist())}
        
        🔍 Colunas que foram detectadas:
        {chr(10).join([f'• {tipo}: {nome}' for tipo, nome in colunas_detectadas.items()])}
        
        ❌ Colunas que NÃO foram encontradas:
        {', '.join(colunas_faltando)}
        
        💡 SOLUÇÃO:
        Certifique-se de que a aba '{nome_aba}' contém colunas com nomes como:
        • Assessor (ou 'Código Assessor')
        • Cliente (ou 'Código Cliente')
        • Ativo (ou 'Fundo' ou 'Produto')
        • Aplicação (ou 'Financeiro' ou 'Valor')
        """)
        return None
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 5: Renomear as colunas para um padrão
    # ═══════════════════════════════════════════════════════════════════
    
    # Cria uma cópia da tabela para não mexer na original
    df_padronizado = df_base.copy()
    
    # Renomeia cada coluna para o nome padrão que vamos usar
    df_padronizado = df_padronizado.rename(columns={
        colunas_detectadas['assessor']: 'Assessor',
        colunas_detectadas['cliente']: 'Cliente',
        colunas_detectadas['ativo']: 'Ativo',
        colunas_detectadas['valor']: 'Aplicação'
    })
    
    # Se encontrou coluna de rendimento, renomeia também
    if 'rendimento' in colunas_detectadas:
        df_padronizado = df_padronizado.rename(columns={
            colunas_detectadas['rendimento']: 'Rendimento %'
        })
    else:
        # Se não tem coluna de rendimento, cria uma com valor 0%
        # (isso evita erros no código)
        df_padronizado['Rendimento %'] = 0.0
        st.warning("⚠️ Coluna de Rendimento não encontrada. Usando 0% para todos.")
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 6: Converter os valores para número
    # ═══════════════════════════════════════════════════════════════════
    
    # pd.to_numeric() converte texto em número
    # errors='coerce' significa: se não conseguir converter, coloca NaN (não número)
    df_padronizado['Aplicação'] = pd.to_numeric(
        df_padronizado['Aplicação'], 
        errors='coerce'  # Se tiver texto, vira NaN ao invés de dar erro
    )
    
    df_padronizado['Rendimento %'] = pd.to_numeric(
        df_padronizado['Rendimento %'], 
        errors='coerce'
    )
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 7: Remover linhas inválidas
    # ═══════════════════════════════════════════════════════════════════
    
    # Conta quantas linhas tínhamos antes
    linhas_antes = len(df_padronizado)
    
    # Remove linhas onde Aplicação é NaN (não número)
    df_padronizado = df_padronizado[df_padronizado['Aplicação'].notna()]
    
    # Remove linhas onde Aplicação é zero ou negativo
    df_padronizado = df_padronizado[df_padronizado['Aplicação'] > 0]
    
    # Conta quantas linhas sobraram
    linhas_depois = len(df_padronizado)
    linhas_removidas = linhas_antes - linhas_depois
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 8: Mostrar mensagem de sucesso!
    # ═══════════════════════════════════════════════════════════════════
    
    st.success(f"""
    ✅ Dados carregados com sucesso!
    
    📊 Estatísticas:
    • Total de registros válidos: {linhas_depois}
    • Registros removidos (inválidos): {linhas_removidas}
    
    📋 Mapeamento de colunas:
    • Assessor: {colunas_detectadas['assessor']} → Assessor
    • Cliente: {colunas_detectadas['cliente']} → Cliente
    • Ativo: {colunas_detectadas['ativo']} → Ativo
    • Valor: {colunas_detectadas['valor']} → Aplicação
    {f"• Rendimento: {colunas_detectadas['rendimento']} → Rendimento %" if 'rendimento' in colunas_detectadas else "• Rendimento: Não encontrado (usando 0%)"}
    """)
    
    # Retorna os dados prontos para usar!
    return df_padronizado

# ═══════════════════════════════════════════════════════════════════════
# PARTE 7: CONFIGURAÇÃO DOS FUNDOS
# ═══════════════════════════════════════════════════════════════════════
# Aqui definimos as cores, siglas, datas e informações de cada fundo

# Cores para cada fundo (aparece na interface)
MAPA_CORES = {
    'ARX FII Portfólio Renda CDI+ RL': '#3498db',                          # Azul
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': '#e74c3c',               # Vermelho
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': '#9b59b6', # Roxo
    'Maua Lajes Corporativas Feeder FII RL - Senior': '#1abc9c',          # Verde água
    'Versa Capital Tech FIP-IE': '#f39c12',                                # Laranja
}

# Siglas curtas para aparecer no calendário
MAPA_SIGLAS = {
    'ARX FII Portfólio Renda CDI+ RL': 'ARX',
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 'AZ INFRA',
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 'AZ PAN',
    'Maua Lajes Corporativas Feeder FII RL - Senior': 'MAUA',
    'Versa Capital Tech FIP-IE': 'VERSA',
}

# Dia útil do mês em que cada fundo paga
# Exemplo: 15 = 15º dia útil do mês
MAPA_PAGAMENTOS = {
    'ARX FII Portfólio Renda CDI+ RL': 15,
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': 7,
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': 7,
    'Maua Lajes Corporativas Feeder FII RL - Senior': 21,
    'Versa Capital Tech FIP-IE': 10,
}

# Informações detalhadas de cada fundo (aparece na tela)
MAPA_TESES = {
    'ARX FII Portfólio Renda CDI+ RL': {
        'resumo': 'Fundo de renda com portfólio diversificado de ativos de crédito privado.',
        'condicoes': 'Liquidez: 30 dias\nTaxa de administração: 0,5% a.a.\nImposto: Isento de IR',
        'venda_1min': 'Fundo conservador que busca rendimento superior ao CDI através de uma carteira diversificada.',
        'perfil': 'Investidores conservadores que buscam renda estável com baixo risco.'
    },
    'AZ Quest Renda Mais Infra-Yield VI FIP-IE': {
        'resumo': 'Fundo de infraestrutura com foco em ativos geradores de renda.',
        'condicoes': 'Liquidez: 90 dias\nTaxa de administração: 2% a.a.\nImposto: 15% sobre ganhos',
        'venda_1min': 'Investe em projetos de infraestrutura com fluxo de caixa previsível e retorno atrativo.',
        'perfil': 'Investidores moderados com horizonte de longo prazo (5+ anos).'
    },
    'AZ QUEST PANORAMA RENDA CDI FI RESPONSABILIDADE LIMITADA': {
        'resumo': 'Fundo de renda fixa com estratégia diversificada em títulos públicos e privados.',
        'condicoes': 'Liquidez: 30 dias\nTaxa de administração: 1% a.a.\nImposto: Regressivo (22,5% a 15%)',
        'venda_1min': 'Busca retorno acima do CDI com baixo risco através de diversificação.',
        'perfil': 'Investidores conservadores a moderados que buscam superar o CDI.'
    },
    'Maua Lajes Corporativas Feeder FII RL - Senior': {
        'resumo': 'Fundo imobiliário focado em lajes corporativas de alto padrão.',
        'condicoes': 'Liquidez: D+0 (negociado em bolsa)\nTaxa de administração: 0% a.a.\nImposto: Isento de IR',
        'venda_1min': 'Gera renda mensal através de aluguéis de imóveis comerciais premium.',
        'perfil': 'Investidores que buscam renda passiva mensal e exposição ao mercado imobiliário.'
    },
    'Versa Capital Tech FIP-IE': {
        'resumo': 'Fundo de participações focado em empresas de tecnologia.',
        'condicoes': 'Liquidez: Baixa (investimento de longo prazo)\nTaxa de administração: 2,5% a.a.\nImposto: 15%',
        'venda_1min': 'Investe em startups e scale-ups de tecnologia com alto potencial de crescimento.',
        'perfil': 'Investidores arrojados com perfil de venture capital e horizonte de 7+ anos.'
    },
}

def buscar_info_fundo(nome_fundo, mapa_pag, mapa_cor, mapa_sig, mapa_tese):
    """
    Busca todas as informações de um fundo específico.
    
    PARÂMETROS:
    - nome_fundo: nome completo do fundo
    - mapa_pag: dicionário com os dias de pagamento
    - mapa_cor: dicionário com as cores
    - mapa_sig: dicionário com as siglas
    - mapa_tese: dicionário com as informações detalhadas
    
    RETORNA:
    - Dicionário com todas as informações do fundo
    """
    return {
        'dia_util': mapa_pag.get(nome_fundo, 0),  # .get() retorna 0 se não encontrar
        'cor': mapa_cor.get(nome_fundo, '#27ae60'),  # Verde padrão se não encontrar
        'sigla': mapa_sig.get(nome_fundo, nome_fundo[:10]),  # Primeiros 10 caracteres
        'tese': mapa_tese.get(nome_fundo, {
            'resumo': 'Informação não disponível',
            'condicoes': 'Consultar gestor do fundo',
            'venda_1min': 'Consultar gestor do fundo',
            'perfil': 'Consultar gestor do fundo'
        })
    }

# ═══════════════════════════════════════════════════════════════════════
# PARTE 8: FUNÇÕES PARA CÁLCULO DE DATAS
# ═══════════════════════════════════════════════════════════════════════

# Lista de feriados nacionais de 2025
# Importante para calcular dias úteis corretamente
feriados = [
    date(2025, 1, 1),    # Ano Novo
    date(2025, 4, 18),   # Sexta-feira Santa
    date(2025, 4, 21),   # Tiradentes
    date(2025, 5, 1),    # Dia do Trabalho
    date(2025, 6, 19),   # Corpus Christi
    date(2025, 9, 7),    # Independência do Brasil
    date(2025, 10, 12),  # Nossa Senhora Aparecida
    date(2025, 11, 2),   # Finados
    date(2025, 11, 15),  # Proclamação da República
    date(2025, 12, 25),  # Natal
]

def eh_dia_util(data, lista_feriados):
    """
    Verifica se uma data é dia útil (não é fim de semana nem feriado).
    
    PARÂMETROS:
    - data: data para verificar (objeto date)
    - lista_feriados: lista com todos os feriados
    
    RETORNA:
    - True se for dia útil
    - False se for fim de semana ou feriado
    """
    
    # data.weekday() retorna:
    # 0 = Segunda-feira
    # 1 = Terça-feira
    # 2 = Quarta-feira
    # 3 = Quinta-feira
    # 4 = Sexta-feira
    # 5 = Sábado
    # 6 = Domingo
    
    # Se for sábado (5) ou domingo (6), não é dia útil
    if data.weekday() >= 5:
        return False
    
    # Se estiver na lista de feriados, não é dia útil
    if data in lista_feriados:
        return False
    
    # Se passou por todas as verificações, é dia útil!
    return True

def calcular_dia_util(ano, mes, numero_dia_util, lista_feriados):
    """
    Calcula qual é o Xº dia útil do mês.
    
    Exemplo: Se numero_dia_util = 5, retorna o 5º dia útil do mês.
    
    PARÂMETROS:
    - ano: ano desejado (ex: 2025)
    - mes: mês desejado (ex: 10 para outubro)
    - numero_dia_util: qual dia útil queremos (ex: 5 = 5º dia útil)
    - lista_feriados: lista com todos os feriados
    
    RETORNA:
    - A data do Xº dia útil do mês
    - None se não conseguir encontrar
    """
    
    # Começa no primeiro dia do mês
    # date(ano, mes, dia)
    data_atual = date(ano, mes, 1)
    
    # Contador de dias úteis
    dias_uteis_contados = 0
    
    # Continua até encontrar o dia útil desejado
    while dias_uteis_contados < numero_dia_util:
        # Verifica se a data atual é dia útil
        if eh_dia_util(data_atual, lista_feriados):
            # Se for, aumenta o contador
            dias_uteis_contados += 1
            
            # Se chegou no dia útil desejado, retorna a data
            if dias_uteis_contados == numero_dia_util:
                return data_atual
        
        # Passa para o próximo dia
        # timedelta(days=1) significa "1 dia"
        data_atual += timedelta(days=1)
        
        # Verificação de segurança: se passou para o próximo mês, algo deu errado
        if data_atual.month != mes:
            return None  # Não encontrou o dia útil dentro do mês
    
    return data_atual

# Lista com os nomes dos meses em português
MESES_PT = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 
    'Maio', 'Junho', 'Julho', 'Agosto',
    'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

# ═══════════════════════════════════════════════════════════════════════
# PARTE 9: TELA DE LOGIN
# ═══════════════════════════════════════════════════════════════════════

def verificar_autenticacao(df_base):
    """
    Mostra a tela de login e verifica se o assessor está autenticado.
    
    Esta função é chamada TODA VEZ que a página é carregada.
    Se o assessor já fez login, ela simplesmente retorna e deixa continuar.
    Se não fez login, mostra a tela de login e PARA a execução.
    
    PARÂMETRO:
    - df_base: tabela com os dados do Excel (para verificar se tem clientes)
    """
    
    # ═══════════════════════════════════════════════════════════════════
    # Inicializar variáveis de sessão
    # ═══════════════════════════════════════════════════════════════════
    # st.session_state é como a "memória" do sistema
    # Guarda informações entre recarregamentos da página
    
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False  # Por padrão, não está autenticado
    
    if 'assessor_logado' not in st.session_state:
        st.session_state.assessor_logado = None  # Nenhum assessor logado
    
    if 'nome_assessor' not in st.session_state:
        st.session_state.nome_assessor = None  # Nome vazio
    
    # ═══════════════════════════════════════════════════════════════════
    # Se NÃO está autenticado, mostra tela de login
    # ═══════════════════════════════════════════════════════════════════
    
    if not st.session_state.autenticado:
        
        # CSS para deixar a tela de login bonita
        st.markdown("""
        <style>
            /* Fundo branco para toda a página */
            .stApp {
                background: white;
            }
            
            /* Caixa de login centralizada */
            .login-box {
                max-width: 450px;
                margin: 120px auto;
                padding: 40px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            }
            
            /* Título do login */
            .login-titulo {
                text-align: center;
                color: #1e4d2b;
                margin-bottom: 30px;
            }
            
            /* Caixa de informações */
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
        # [1, 2, 1] significa: coluna esquerda pequena, meio grande, direita pequena
        col1, col2, col3 = st.columns([1, 2, 1])
        
        # Todo o conteúdo vai na coluna do meio
        with col2:
            # Tenta mostrar a logo da empresa
            try:
                st.image("logo_tauari.png", width=350)
            except:
                # Se não tiver logo, mostra texto
                st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <div style='background: #2d5a3d; color: white; padding: 40px; 
                                border-radius: 10px; font-size: 14px;'>
                        🌳 TAUARI INVESTIMENTOS<br>
                        Calendário Renda Mais
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Título da página de login
            st.markdown("""
            <div class="login-titulo">
                <h2 style='margin: 10px 0; font-size: 24px;'>
                    Calendário Renda Mais - Tauari Investimentos
                </h2>
                <p style='color: #7f8c8d; font-size: 14px; margin-top: 15px;'>
                    Acesso restrito por Assessor - Atualizado 25/10/2025
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # ═══════════════════════════════════════════════════════════
            # Formulário de login
            # ═══════════════════════════════════════════════════════════
            
            # st.form() cria um formulário que só envia dados quando clicar no botão
            with st.form("login_form"):
                
                # Campo para digitar o código do assessor
                codigo_assessor = st.text_input(
                    "👤 Código do Assessor:",
                    placeholder="Exemplo: 46857",
                    max_chars=10,  # Máximo de 10 caracteres
                    key="codigo_input"  # Identificador único deste campo
                )
                
                # Campo para digitar a senha (escondido)
                senha_assessor = st.text_input(
                    "🔐 Senha do Assessor:",
                    type="password",  # Isso esconde o que é digitado
                    placeholder="Digite sua senha",
                    max_chars=20,
                    key="senha_input"
                )
                
                # Botão de enviar o formulário
                submitted = st.form_submit_button(
                    "🔓 Entrar", 
                    use_container_width=True  # Botão ocupa toda a largura
                )
                
                # ═══════════════════════════════════════════════════════
                # Quando o botão for clicado
                # ═══════════════════════════════════════════════════════
                
                if submitted:
                    # Verifica se preencheu todos os campos
                    if not codigo_assessor or not senha_assessor:
                        st.error("❌ Por favor, preencha todos os campos!")
                    
                    else:
                        # Tenta validar a senha
                        valido, nome_assessor = validar_senha_assessor(
                            codigo_assessor, 
                            senha_assessor
                        )
                        
                        # Se a senha está correta
                        if valido:
                            # Verifica se tem dados carregados
                            if df_base is not None:
                                # Garante que a coluna Assessor é texto
                                df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
                                
                                # Filtra apenas os clientes deste assessor
                                clientes_assessor = df_base[
                                    df_base['Assessor'] == str(codigo_assessor)
                                ]
                                
                                # Verifica se encontrou clientes
                                if clientes_assessor.empty:
                                    st.error(f"""
                                    ❌ Nenhum cliente encontrado para o Assessor {codigo_assessor}
                                    
                                    Isso pode acontecer se:
                                    • Seus clientes ainda não foram cadastrados no sistema
                                    • O código do assessor está diferente no Excel
                                    
                                    Entre em contato com o suporte.
                                    """)
                                
                                else:
                                    # TUDO CERTO! Faz o login
                                    st.session_state.autenticado = True
                                    st.session_state.assessor_logado = codigo_assessor
                                    st.session_state.nome_assessor = nome_assessor
                                    
                                    st.success(f"✅ Bem-vindo, {nome_assessor}!")
                                    
                                    # st.rerun() recarrega a página
                                    # Agora que autenticado = True, vai mostrar o sistema
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
                • Em caso de dúvidas, entre em contato:<br>
                  <strong>gustavo.aquila@tauariinvestimentos.com.br</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Para a execução aqui - não mostra o resto do código
        st.stop()

# ═══════════════════════════════════════════════════════════════════════
# PARTE 10: CSS PARA DEIXAR O SISTEMA BONITO
# ═══════════════════════════════════════════════════════════════════════
# CSS é a linguagem que define cores, tamanhos, posicionamento, etc.

st.markdown("""
<style>
    /* Fundo branco para toda a aplicação */
    .stApp {
        background: white !important;
    }
    
    /* Cabeçalho verde no topo do sistema */
    .header-sistema {
        background: linear-gradient(135deg, #1e4d2b 0%, #27ae60 100%);
        padding: 20px 40px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    /* Título no cabeçalho */
    .header-titulo {
        color: white;
        font-size: 28px;
        font-weight: bold;
        margin: 0;
    }
    
    /* Informações do assessor no cabeçalho */
    .info-assessor {
        color: white;
        font-size: 14px;
        margin-top: 8px;
    }
    
    /* Caixa de seleção de cliente */
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
    
    /* Caixas brancas (fundos, tese, calendário) */
    .box {
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    /* Título das caixas (fundo verde escuro) */
    .box-titulo {
        background: #1e4d2b;
        color: white;
        padding: 15px;
        font-weight: bold;
        font-size: 14px;
    }
    
    /* Conteúdo das caixas */
    .box-conteudo {
        padding: 15px;
        max-height: 600px;
        overflow-y: auto;  /* Barra de rolagem se ficar muito grande */
    }
    
    /* Card de cada fundo */
    .fundo-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #27ae60;
        margin-bottom: 15px;
        transition: all 0.3s;  /* Animação suave */
    }
    
    /* Quando passar o mouse sobre o card */
    .fundo-card:hover {
        background: #e9ecef;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Card quando está selecionado */
    .fundo-card-selecionado {
        background: #e8f5e9 !important;
        border-left-width: 6px !important;
    }
    
    /* Nome do fundo no card */
    .fundo-card .nome {
        font-weight: bold;
        color: #1e4d2b;
        margin-bottom: 8px;
    }
    
    /* Informações no card */
    .fundo-card .info {
        font-size: 13px;
        color: #495057;
    }
    
    /* Valores em destaque */
    .fundo-card .valor {
        color: #27ae60;
        font-weight: bold;
    }
    
    /* Texto da tese do fundo */
    .tese-texto {
        padding: 20px;
        line-height: 1.6;
    }
    
    .tese-texto h4 {
        color: #1e4d2b;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    
    /* Grade do calendário */
    .calendario-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);  /* 7 colunas (dias da semana) */
        gap: 5px;
        padding: 15px;
    }
    
    /* Cabeçalho do calendário (dias da semana) */
    .cal-header {
        text-align: center;
        font-weight: bold;
        padding: 8px;
        background: #1e4d2b;
        color: white;
        border-radius: 5px;
        font-size: 12px;
    }
    
    /* Cada dia do calendário */
    .cal-dia {
        min-height: 80px;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 5px;
        background: white;
    }
    
    /* Fim de semana (sábado e domingo) */
    .cal-dia.fim-semana {
        background: #f8f9fa;
    }
    
    /* Número do dia */
    .cal-dia .numero {
        font-weight: bold;
        color: #495057;
        margin-bottom: 3px;
    }
    
    /* Evento no calendário (pagamento) */
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

# ═══════════════════════════════════════════════════════════════════════
# PARTE 11: FUNÇÃO PRINCIPAL DO SISTEMA
# ═══════════════════════════════════════════════════════════════════════

def main():
    """
    Esta é a função PRINCIPAL que coordena todo o sistema.
    
    É chamada automaticamente quando o código é executado.
    
    O QUE ELA FAZ:
    1. Carrega os dados do Excel
    2. Verifica se o assessor está logado
    3. Mostra o cabeçalho do sistema
    4. Permite selecionar o cliente
    5. Mostra os fundos, informações e calendário
    """
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 1: Carregar os dados do Excel
    # ═══════════════════════════════════════════════════════════════════
    
    df_base = carregar_dados_excel()
    
    # Se não conseguiu carregar, para tudo aqui
    if df_base is None:
        st.error("""
        ⚠️ Não foi possível carregar os dados.
        
        Verifique as mensagens de erro acima e corrija os problemas.
        """)
        st.stop()  # Para a execução
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 2: Verificar autenticação (login)
    # ═══════════════════════════════════════════════════════════════════
    
    verificar_autenticacao(df_base)
    
    # Se chegou aqui, significa que o assessor está autenticado!
    # (se não estivesse, a função verificar_autenticacao() teria parado tudo)
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 3: Mostrar o cabeçalho do sistema
    # ═══════════════════════════════════════════════════════════════════
    
    st.markdown(f"""
    <div class="header-sistema">
        <div class="header-titulo">🌳 Calendário Renda Mais - Tauari Investimentos</div>
        <div class="info-assessor">
            👤 Assessor: <strong>{st.session_state.nome_assessor}</strong> | 
            Código: <strong>{st.session_state.assessor_logado}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 4: Botões de ação
    # ═══════════════════════════════════════════════════════════════════
    
    # Cria colunas para os botões
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    # Botão de sair
    with col1:
        if st.button("🔓 Sair", key="btn_sair"):
            # Limpa todas as variáveis de sessão
            st.session_state.autenticado = False
            st.session_state.assessor_logado = None
            st.session_state.nome_assessor = None
            # Recarrega a página (vai mostrar tela de login)
            st.rerun()
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 5: Filtrar dados do assessor logado
    # ═══════════════════════════════════════════════════════════════════
    
    # Garante que a coluna Assessor é texto
    df_base['Assessor'] = df_base['Assessor'].astype(str).str.strip()
    
    # Filtra apenas os dados deste assessor
    df_base_filtrado = df_base[
        df_base['Assessor'] == str(st.session_state.assessor_logado)
    ]
    
    # Se não tem clientes, mostra erro
    if df_base_filtrado.empty:
        st.error("❌ Nenhum cliente encontrado para este assessor!")
        st.stop()
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 6: Seletor de cliente
    # ═══════════════════════════════════════════════════════════════════
    
    st.markdown("""
    <div class="cliente-selector">
        <h3>👥 SELECIONE O CLIENTE</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Pega a lista de todos os clientes deste assessor
    clientes = sorted(df_base_filtrado['Cliente'].unique())
    
    # Cria o seletor (dropdown)
    cliente_selecionado = st.selectbox(
        "Cliente",  # Label (mas vamos esconder)
        [""] + list(clientes),  # Opções (começa com vazio)
        label_visibility="collapsed",  # Esconde o label
        key="cliente_select"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Se nenhum cliente foi selecionado, para aqui
    if not cliente_selecionado:
        st.info("👆 Selecione um cliente acima para ver seus investimentos")
        st.stop()
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 7: Pegar todos os fundos do cliente selecionado
    # ═══════════════════════════════════════════════════════════════════
    
    fundos_cliente = df_base_filtrado[
        df_base_filtrado['Cliente'] == cliente_selecionado
    ]
    
    # Inicializar o fundo selecionado (para mostrar detalhes)
    if 'fundo_selecionado' not in st.session_state:
        # Por padrão, seleciona o primeiro fundo
        st.session_state.fundo_selecionado = (
            fundos_cliente['Ativo'].iloc[0] if not fundos_cliente.empty else None
        )
    
    # Inicializar mês e ano do calendário
    if 'mes_atual' not in st.session_state:
        st.session_state.mes_atual = datetime.now().month
        st.session_state.ano_atual = datetime.now().year
    
    # ═══════════════════════════════════════════════════════════════════
    # PASSO 8: Criar as 3 colunas principais do sistema
    # ═══════════════════════════════════════════════════════════════════
    
    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    
    # ═══════════════════════════════════════════════════════════════════
    # COLUNA 1: LISTA DE FUNDOS DO CLIENTE
    # ═══════════════════════════════════════════════════════════════════
    
    with col1:
        st.markdown("""
        <div class="box">
            <div class="box-titulo">📊 FUNDOS DO CLIENTE</div>
            <div class="box-conteudo">
        """, unsafe_allow_html=True)
        
        # Para cada fundo do cliente
        for _, fundo in fundos_cliente.iterrows():
            ativo = fundo['Ativo']
            
            # Pega o valor aplicado
            try:
                valor_aplicado = float(fundo['Aplicação'])
            except:
                valor_aplicado = 0.0
            
            # Pega o percentual de rendimento
            try:
                percentual_liquido = float(fundo['Rendimento %'])
            except:
                percentual_liquido = 0.0
            
            # Calcula o valor líquido (valor × percentual)
            valor_liquido_cupom = valor_aplicado * percentual_liquido
            
            # Busca informações do fundo (cor, sigla, dia de pagamento)
            info = buscar_info_fundo(
                ativo, 
                MAPA_PAGAMENTOS, 
                MAPA_CORES, 
                MAPA_SIGLAS, 
                MAPA_TESES
            )
            
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
                    pass  # Se der erro, deixa None
            
            # Formata a data para mostrar
            data_texto = (
                data_pagamento.strftime("%d/%m/%Y") 
                if data_pagamento 
                else "Não definida"
            )
            
            # Define se este fundo está selecionado
            classe_selecao = (
                'fundo-card-selecionado' 
                if ativo == st.session_state.fundo_selecionado 
                else ''
            )
            
            # Mostra o card do fundo
            st.markdown(f"""
            <div class="fundo-card {classe_selecao}" 
                 style="border-left-color: {info.get('cor', '#27ae60')}">
                <div class="nome">{ativo}</div>
                <div class="info" style="margin-top: 8px;">
                    <div style="margin-bottom: 4px;">
                        💰 <strong>Valor Aplicado:</strong> 
                        <span class="valor">R$ {valor_aplicado:,.2f}</span>
                    </div>
                    <div style="margin-bottom: 4px;">
                        📅 <strong>Data Pagamento:</strong> {data_texto}
                    </div>
                    <div style="margin-bottom: 4px;">
                        📈 <strong>% Líquido:</strong> 
                        <span class="valor">{percentual_liquido:.2%}</span>
                    </div>
                    <div>
                        💵 <strong>Valor Líquido:</strong> 
                        <span class="valor">R$ {valor_liquido_cupom:,.2f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão para selecionar este fundo
            if st.button("📊", key=f"sel_{ativo}", help=f"Selecionar {ativo}"):
                st.session_state.fundo_selecionado = ativo
                st.rerun()  # Recarrega para mostrar detalhes do fundo

        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════
    # COLUNA 2: INFORMAÇÕES DO FUNDO SELECIONADO
    # ═══════════════════════════════════════════════════════════════════
    
    with col2:
        st.markdown("""
        <div class="box">
            <div class="box-titulo">📝 TESE DO FUNDO</div>
        """, unsafe_allow_html=True)
        
        # Se tem um fundo selecionado
        if st.session_state.fundo_selecionado:
            # Busca as informações do fundo
            info = buscar_info_fundo(
                st.session_state.fundo_selecionado, 
                MAPA_PAGAMENTOS, 
                MAPA_CORES, 
                MAPA_SIGLAS, 
                MAPA_TESES
            )
            tese = info.get('tese', {})
            
            # Mostra as informações
            st.markdown(f"""
            <div class="tese-texto">
                <strong style="color: {info.get('cor', '#27ae60')};">
                    {st.session_state.fundo_selecionado}
                </strong>
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
            st.markdown("""
            <div class="tese-texto">
                <p>Selecione um fundo ao lado para ver as informações.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════
    # COLUNA 3: CALENDÁRIO
    # ═══════════════════════════════════════════════════════════════════
    
    with col3:
        st.markdown("""
        <div class="box">
            <div class="box-titulo">📅 CALENDÁRIO</div>
        """, unsafe_allow_html=True)
        
        # ───────────────────────────────────────────────────────────────
        # Botões para navegar entre meses
        # ───────────────────────────────────────────────────────────────
        
        col_p1, col_p2, col_p3 = st.columns([1, 3, 1])
        
        # Botão mês anterior
        with col_p1:
            if st.button("◀ Anterior", key="prev_mes"):
                st.session_state.mes_atual -= 1
                # Se passou de janeiro, volta para dezembro do ano anterior
                if st.session_state.mes_atual < 1:
                    st.session_state.mes_atual = 12
                    st.session_state.ano_atual -= 1
                st.rerun()
        
        # Nome do mês e ano
        with col_p2:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px; font-size: 18px; 
                        font-weight: bold; color: #1e4d2b;">
                {MESES_PT[st.session_state.mes_atual-1]} {st.session_state.ano_atual}
            </div>
            """, unsafe_allow_html=True)
        
        # Botão próximo mês
        with col_p3:
            if st.button("Próximo ▶", key="next_mes"):
                st.session_state.mes_atual += 1
                # Se passou de dezembro, vai para janeiro do próximo ano
                if st.session_state.mes_atual > 12:
                    st.session_state.mes_atual = 1
                    st.session_state.ano_atual += 1
                st.rerun()
        
        # ───────────────────────────────────────────────────────────────
        # Gerar o calendário do mês
        # ───────────────────────────────────────────────────────────────
        
        # calendar.monthcalendar() retorna uma lista de semanas
        # Cada semana é uma lista de 7 dias (0 = dia de outro mês)
        cal = calendar.monthcalendar(
            st.session_state.ano_atual, 
            st.session_state.mes_atual
        )
        
        # Começa a montar o HTML do calendário
        dias_semana = ['seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.', 'dom.']
        html_cal = '<div class="calendario-grid">'
        
        # Cabeçalho (dias da semana)
        for dia in dias_semana:
            html_cal += f'<div class="cal-header">{dia}</div>'
        
        # ───────────────────────────────────────────────────────────────
        # Calcular os eventos (pagamentos) do mês
        # ───────────────────────────────────────────────────────────────
        
        # Dicionário que vai guardar: {dia: [lista de eventos]}
        eventos_mes = {}
        
        # Para cada fundo do cliente
        for _, fundo in fundos_cliente.iterrows():
            # Busca informações do fundo
            info = buscar_info_fundo(
                fundo['Ativo'], 
                MAPA_PAGAMENTOS, 
                MAPA_CORES, 
                MAPA_SIGLAS, 
                MAPA_TESES
            )
            
            dia_util = info.get('dia_util')
            
            # Se tem dia de pagamento definido
            if dia_util and dia_util > 0:
                try:
                    # Calcula a data de pagamento
                    data_pagamento = calcular_dia_util(
                        st.session_state.ano_atual, 
                        st.session_state.mes_atual, 
                        dia_util, 
                        feriados
                    )
                    
                    if data_pagamento:
                        dia = data_pagamento.day
                        
                        # Adiciona o evento no dicionário
                        if dia not in eventos_mes:
                            eventos_mes[dia] = []
                        
                        eventos_mes[dia].append({
                            'sigla': info.get('sigla', fundo['Ativo'][:10]), 
                            'cor': info.get('cor', '#27ae60')
                        })
                except:
                    pass  # Se der erro, ignora
        
        # ───────────────────────────────────────────────────────────────
        # Gerar os dias do calendário
        # ───────────────────────────────────────────────────────────────
        
        # Para cada semana
        for semana in cal:
            # Para cada dia da semana
            for dia in semana:
                # Se dia = 0, é dia de outro mês (deixa em branco)
                if dia == 0:
                    html_cal += '<div class="cal-dia" style="background: #f8f9fa;"></div>'
                else:
                    # Cria objeto data para este dia
                    data = date(
                        st.session_state.ano_atual, 
                        st.session_state.mes_atual, 
                        dia
                    )
                    
                    # Define a classe (fim de semana ou não)
                    # weekday() >= 5 significa sábado (5) ou domingo (6)
                    classe = (
                        "cal-dia fim-semana" 
                        if data.weekday() >= 5 
                        else "cal-dia"
                    )
                    
                    # Monta o HTML dos eventos deste dia
                    eventos_html = ""
                    if dia in eventos_mes:
                        for evento in eventos_mes[dia]:
                            eventos_html += f"""
                            <div class="cal-evento" 
                                 style="background: {evento['cor']}">
                                {evento['sigla']}
                            </div>
                            """
                    
                    # Adiciona o dia ao calendário
                    html_cal += f"""
                    <div class="{classe}">
                        <div class="numero">{dia}</div>
                        {eventos_html}
                    </div>
                    """
        
        # Fecha o HTML do calendário
        html_cal += '</div>'
        
        # Mostra o calendário
        st.markdown(html_cal, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# PARTE 12: EXECUTAR O SISTEMA
# ═══════════════════════════════════════════════════════════════════════

# Este if garante que o código só roda quando executado diretamente
# (não quando importado como módulo)
if __name__ == "__main__":
    main()  # Chama a função principal

# ═══════════════════════════════════════════════════════════════════════
# FIM DO CÓDIGO
# ═══════════════════════════════════════════════════════════════════════
"""
RESUMO DO QUE ESTE CÓDIGO FAZ:

1. Carrega dados do Excel (detecta colunas automaticamente!)
2. Mostra tela de login para assessores
3. Filtra dados do assessor logado
4. Permite selecionar cliente
5. Mostra fundos do cliente com valores aplicados
6. Mostra informações detalhadas de cada fundo
7. Mostra calendário com datas de pagamento

ESTRUTURA DO ARQUIVO EXCEL ESPERADO:
- Aba: "Base"
- Colunas (podem ter outros nomes):
  • Assessor (ou "Código Assessor")
  • Cliente (ou "Código Cliente")
  • Ativo (ou "Fundo" ou "Produto")
  • Aplicação (ou "Financeiro" ou "Valor")  ← IMPORTANTE!
  • Rendimento % (ou apenas "Rendimento")

O CÓDIGO DETECTA AUTOMATICAMENTE QUAL COLUNA É QUAL!

✅ TESTADO E FUNCIONANDO EM 25/10/2025
"""
