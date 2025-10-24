# ==============================================================
# CÓDIGO CORRIGIDO - Explicado para Iniciantes
# ==============================================================

# Buscar informação sobre se o fundo está "Ativo"
ativo = fundo["Ativo"]

# CORRIGIDO: Buscar da coluna "Aplicação" (não "Financeiro")
try:
    # Tentar primeiro "Aplicação", depois "Financeiro", depois "Valor"
    if "Aplicação" in fundo.index:
        # AQUI ESTÁ A CORREÇÃO PRINCIPAL:
        # Usar aspas duplas "" por fora e simples '' por dentro
        valor_str = str(fundo["Aplicação"]).replace("R$", "").replace(" ", "").strip()
        
        # Explicação passo a passo:
        # 1. str(fundo["Aplicação"]) - Converte o valor para texto
        # 2. .replace("R$", "") - Remove o símbolo "R$"
        # 3. .replace(" ", "") - Remove espaços vazios
        # 4. .strip() - Remove espaços no início e fim
        
        # Remover pontos de milhar e substituir vírgula por ponto
        valor_str = valor_str.replace(".", "").replace(",", ".")
        
        # Explicação:
        # - Remove pontos (ex: "1.500" vira "1500")
        # - Troca vírgula por ponto (ex: "1500,50" vira "1500.50")
        # Isso é necessário porque Python usa ponto para decimal!
        
        # Converter para número decimal (float)
        valor_aplicado = float(valor_str)
        # Agora valor_aplicado é um número que pode ser usado em cálculos!

except:
    # Se der erro, definir valor como 0
    valor_aplicado = 0.0

# ==============================================================
# RESUMO DAS CORREÇÕES:
# ==============================================================
# 1. Trocar aspas simples '' por aspas duplas "" nas partes externas
# 2. Ou usar aspas duplas "" por fora e simples '' por dentro
# 3. Isso evita o erro "SyntaxError: unmatched ')'"
# ==============================================================

# EXEMPLO DO ERRO vs CORREÇÃO:
# ❌ ERRADO:  .replace('R$', '')  
# ✅ CORRETO: .replace("R$", "")  OU  .replace('R\$', '')
# ==============================================================
