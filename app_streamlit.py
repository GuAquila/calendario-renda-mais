# ==============================================================
# CÓDIGO COMPLETO CORRIGIDO - Para Iniciantes
# ==============================================================
# Este arquivo mostra ONDE e COMO usar o código corretamente
# ==============================================================

import streamlit as st
import pandas as pd

# ==============================================================
# PASSO 1: CARREGAR OS DADOS
# ==============================================================
# Primeiro, você precisa TER os dados antes de usá-los!
# Exemplo: carregar de um arquivo CSV ou Excel

# Substitua "seu_arquivo.csv" pelo nome do seu arquivo real
# df = pd.read_csv("seu_arquivo.csv")
# OU
# df = pd.read_excel("seu_arquivo.xlsx")

# Para este exemplo, vamos criar dados fictícios:
df = pd.DataFrame({
    'Fundo': ['Fundo A', 'Fundo B', 'Fundo C'],
    'Ativo': ['Sim', 'Não', 'Sim'],
    'Aplicação': ['R$ 1.500,00', 'R$ 2.300,50', 'R$ 890,00']
})

print("Dados carregados:")
print(df)
print("\n" + "="*60 + "\n")

# ==============================================================
# PASSO 2: SELECIONAR UM FUNDO ESPECÍFICO
# ==============================================================
# No Streamlit, você provavelmente tem algo como:
# fundo_selecionado = st.selectbox("Escolha um fundo", df['Fundo'])

# Para este exemplo, vamos selecionar manualmente:
fundo_selecionado = 'Fundo A'

print(f"Fundo selecionado: {fundo_selecionado}")
print("\n" + "="*60 + "\n")

# ==============================================================
# PASSO 3: BUSCAR AS INFORMAÇÕES DO FUNDO
# ==============================================================
# AGORA SIM podemos criar a variável 'fundo'!
# Pegamos a linha do DataFrame que corresponde ao fundo selecionado

fundo = df[df['Fundo'] == fundo_selecionado].iloc[0]

# Explicação para iniciantes:
# - df[df['Fundo'] == fundo_selecionado] --> Filtra as linhas onde o nome do fundo é igual
# - .iloc[0] --> Pega a primeira linha do resultado

print("Informações do fundo encontrado:")
print(fundo)
print("\n" + "="*60 + "\n")

# ==============================================================
# PASSO 4: AGORA SIM USAR O CÓDIGO CORRIGIDO!
# ==============================================================
# ✅ AGORA 'fundo' existe! Podemos usar!

# Buscar se o fundo está ativo
ativo = fundo["Ativo"]
print(f"Fundo está ativo? {ativo}")

# CORRIGIDO: Buscar o valor da aplicação
try:
    # Verificar se a coluna "Aplicação" existe
    if "Aplicação" in fundo.index:
        # USAR ASPAS DUPLAS para evitar erro de sintaxe!
        valor_str = str(fundo["Aplicação"]).replace("R$", "").replace(" ", "").strip()
        
        print(f"Valor como texto (após remover R$): '{valor_str}'")
        
        # Remover pontos de milhar e substituir vírgula por ponto
        valor_str = valor_str.replace(".", "").replace(",", ".")
        
        print(f"Valor formatado para Python: '{valor_str}'")
        
        # Converter para número decimal
        valor_aplicado = float(valor_str)
        
        print(f"Valor como número: {valor_aplicado}")
        
except Exception as e:
    # Se der qualquer erro, usar 0
    print(f"Erro ao processar valor: {e}")
    valor_aplicado = 0.0

print("\n" + "="*60 + "\n")
print(f"✅ RESULTADO FINAL:")
print(f"   Fundo: {fundo_selecionado}")
print(f"   Ativo: {ativo}")
print(f"   Valor Aplicado: R$ {valor_aplicado:,.2f}")

# ==============================================================
# RESUMO PARA INICIANTES:
# ==============================================================
# A ORDEM CORRETA É:
# 1. Carregar os dados (DataFrame)
# 2. Selecionar qual fundo você quer
# 3. CRIAR a variável 'fundo' pegando a linha do DataFrame
# 4. DEPOIS usar fundo["Ativo"], fundo["Aplicação"], etc.
#
# ❌ ERRADO: Usar 'fundo' do nada
# ✅ CERTO: Criar 'fundo' primeiro, DEPOIS usar
# ==============================================================
