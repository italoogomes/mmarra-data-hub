# 📊 Mapeamento: Empenho e Cotação - Sankhya

**Versão:** 1.0.0
**Data:** 2026-02-02
**Status:** ✅ Mapeado e Testado
**Autor:** Claude + Ítalo Gomes

---

## 🎯 Objetivo

Este documento mapeia as tabelas do Sankhya relacionadas ao **Sistema de Empenho** e **Processo de Cotação**, descobertas durante a criação da query "Gestão de Empenho por Fornecedor + Cotação".

---

## 📋 Índice

1. [Workflow do Sistema](#workflow-do-sistema)
2. [Tabelas Mapeadas](#tabelas-mapeadas)
3. [Relacionamentos](#relacionamentos)
4. [Campos Customizados](#campos-customizados)
5. [Queries de Exemplo](#queries-de-exemplo)
6. [Problemas e Soluções](#problemas-e-soluções)

---

## 🔄 Workflow do Sistema

### Fluxo Completo: Venda → Empenho → Cotação → Compra → WMS

```
1. VENDA CRIADA
   ↓ (TGFCAB com TIPMOV='V')
   │
2. EMPENHO GERADO
   ↓ (TGWEMPE vincula venda → compra)
   │
3. COMPRADOR CRIA COTAÇÃO
   ↓ (TGFCOT + TGFITC)
   │ - Envia para N fornecedores
   │ - Fornecedores respondem com preços
   │
4. COMPRADOR SELECIONA MELHOR COTAÇÃO
   ↓ (Analisa peso, custo, prazo)
   │
5. ORDEM DE COMPRA CRIADA
   ↓ (TGFCAB com TIPMOV='C')
   │
6. MERCADORIA CHEGA
   ↓ (TGWREC - Recebimento WMS)
   │
7. WMS SEPARA PARA VENDA
   ↓ (VGWSEPSITCAB)
   │
8. PRODUTO SAI DO ESTOQUE
   ✅ (Ciclo completo)
```

---

## 📊 Tabelas Mapeadas

### 1. TGWEMPE - Empenho (Tabela Bridge)

**Propósito:** Vincula pedidos de VENDA aos pedidos de COMPRA através do sistema de empenho/reserva.

#### Estrutura Principal

| Campo | Tipo | Descrição | Observação |
|-------|------|-----------|------------|
| `NUNOTAPEDVEN` | NUMBER | Número único do pedido de **VENDA** | FK → TGFCAB.NUNOTA |
| `NUNOTA` | NUMBER | Número único do pedido de **COMPRA** | FK → TGFCAB.NUNOTA |
| `CODPROD` | NUMBER | Código do produto | FK → TGFPRO.CODPROD |
| `QTDEMPENHO` | NUMBER | Quantidade empenhada | Pode ser parcial |

#### Características
- **Tabela intermediária** que conecta vendas a compras
- Permite rastrear qual compra atende qual venda
- Um pedido de venda pode ter múltiplos empenhos (compras diferentes)
- Um pedido de compra pode atender múltiplas vendas

#### Exemplo de Registro
```sql
NUNOTAPEDVEN = 1192580  -- Pedido de venda
NUNOTA       = 1195234  -- Pedido de compra
CODPROD      = 45678
QTDEMPENHO   = 10       -- 10 unidades empenhadas
```

---

### 2. TGFCOT - Cabeçalho da Cotação

**Propósito:** Armazena informações gerais da cotação criada pelo comprador.

#### Estrutura Principal

| Campo | Tipo | Descrição | Observação |
|-------|------|-----------|------------|
| `NUMCOTACAO` | NUMBER | Número único da cotação | PK |
| `CODUSURESP` | NUMBER | Código do usuário responsável | FK → TSIUSU.CODUSU |
| `SITUACAO` | VARCHAR2(1) | Situação da cotação | 'O' = Aberta, 'P' = Pendente, etc |
| `DTCOTACAO` | DATE | Data da cotação | |
| `OBSERVACAO` | VARCHAR2(4000) | Observações gerais | |

#### Características
- Uma cotação pode ter múltiplos itens (TGFITC)
- Pode envolver múltiplos fornecedores
- Responsável é o comprador que criou a cotação
- Situação controla o fluxo de aprovação

#### Campos Relacionados ao Processo
- Peso dos critérios (custo, prazo, qualidade)
- Data de abertura e fechamento
- Vencedor da cotação

---

### 3. TGFITC - Itens da Cotação (por Fornecedor)

**Propósito:** Armazena as respostas de cada fornecedor para cada produto cotado.

#### Estrutura Principal

| Campo | Tipo | Descrição | Observação |
|-------|------|-----------|------------|
| `NUMCOTACAO` | NUMBER | Número da cotação | FK → TGFCOT.NUMCOTACAO |
| `CODPARC` | NUMBER | Código do parceiro (fornecedor) | FK → TGFPAR.CODPARC |
| `CODPROD` | NUMBER | Código do produto | FK → TGFPRO.CODPROD |
| `STATUSPRODCOT` | VARCHAR2(1) | Status da cotação do produto | 'A' = Aguardando, 'C' = Cotado |
| `VLRUNIT` | NUMBER | Valor unitário cotado | Preço oferecido |
| `QTDCOT` | NUMBER | Quantidade cotada | |
| `PRAZOENTR` | NUMBER | Prazo de entrega (dias) | |

#### Características
- **Nível de granularidade:** Cotação × Fornecedor × Produto
- Múltiplos fornecedores podem cotar o mesmo produto
- Comprador analisa e escolhe a melhor oferta
- Status indica se o fornecedor já respondeu

#### Exemplo de Registro
```sql
NUMCOTACAO     = 5234
CODPARC        = 1500     -- Fornecedor A
CODPROD        = 45678
STATUSPRODCOT  = 'C'      -- Cotado
VLRUNIT        = 150.00
PRAZOENTR      = 15       -- 15 dias
```

---

### 4. TSIUSU - Usuários do Sistema

**Propósito:** Cadastro de usuários do Sankhya (compradores, vendedores, etc).

#### Estrutura Principal

| Campo | Tipo | Descrição | Observação |
|-------|------|-----------|------------|
| `CODUSU` | NUMBER | Código do usuário | PK |
| `NOMEUSU` | VARCHAR2(60) | Nome do usuário | Ex: "João Silva" |
| `AD_USUARIO` | VARCHAR2(30) | Login do usuário | Campo customizado |

#### Características
- Usado para identificar responsável pela cotação
- Vínculo: TGFCOT.CODUSURESP → TSIUSU.CODUSU
- Pode ter campos customizados (AD_*)

---

### 5. TGFCAB - Cabeçalho Unificado (Vendas e Compras)

**Propósito:** Tabela unificada para pedidos de venda E compra.

#### Campos Relevantes para Empenho

| Campo | Tipo | Descrição | Observação |
|-------|------|-----------|------------|
| `NUNOTA` | NUMBER | Número único da nota | PK |
| `CODTIPOPER` | NUMBER | Código tipo de operação | Define se é venda/compra |
| `TIPMOV` | VARCHAR2(1) | Tipo movimento | 'V' = Venda, 'C' = Compra |
| `CODPARC` | NUMBER | Código do parceiro | Cliente (venda) ou Fornecedor (compra) |
| `PENDENTE` | VARCHAR2(1) | Pedido pendente? | 'S' = Sim, 'N' = Não |
| `STATUSNOTA` | VARCHAR2(1) | Status da nota | 'L' = Liberado, 'P' = Pendente |
| `NUMNOTA` | NUMBER | Número da nota fiscal | Número formatado da NF |
| `AD_RESERVAEMPENHO` | VARCHAR2(1) | Usa empenho? | Campo customizado |

#### Filtros Importantes
```sql
-- Para pegar apenas pedidos COM empenho ativo:
WHERE PENDENTE = 'S'
  AND STATUSNOTA = 'L'
  AND AD_RESERVAEMPENHO = 'S'  -- Tipo operação configurado para empenho
```

---

## 🔗 Relacionamentos

### Diagrama de Relacionamentos

```
TGFCAB (Venda)
    ↓ NUNOTA
    ↓
TGWEMPE ────────────→ TGFCAB (Compra)
    │                      ↓ CODPARC
    │ CODPROD             ↓
    ↓                     ↓
TGFPRO              TGFPAR (Fornecedor)
                          ↓ CODPARC
                          ↓
                    TGFITC ←──── TGFCOT
                      ↑              ↓ CODUSURESP
                      │ NUMCOTACAO  ↓
                      │           TSIUSU
                      │
                    CODPROD
```

### Query de Exemplo: Junção Completa

```sql
-- Obter dados de venda + empenho + compra + cotação
SELECT
    -- Venda
    cv.NUNOTA AS nunota_venda,
    cv.CODPARC AS cliente,

    -- Empenho
    e.QTDEMPENHO,

    -- Compra
    cc.NUNOTA AS nunota_compra,
    cc.CODPARC AS fornecedor,
    cc.NUMNOTA AS nf_compra,

    -- Cotação
    itc.NUMCOTACAO,
    itc.STATUSPRODCOT,
    cot.CODUSURESP,
    usu.NOMEUSU AS responsavel_cotacao

FROM TGFCAB cv
JOIN TGWEMPE e ON e.NUNOTAPEDVEN = cv.NUNOTA
JOIN TGFCAB cc ON cc.NUNOTA = e.NUNOTA
LEFT JOIN TGFITC itc ON itc.CODPARC = cc.CODPARC AND itc.CODPROD = e.CODPROD
LEFT JOIN TGFCOT cot ON cot.NUMCOTACAO = itc.NUMCOTACAO
LEFT JOIN TSIUSU usu ON usu.CODUSU = cot.CODUSURESP
WHERE cv.TIPMOV = 'V'
  AND cc.TIPMOV = 'C'
```

---

## 🔧 Campos Customizados

### AD_RESERVAEMPENHO (TGFTOP)

**Localização:** TGFTOP.AD_RESERVAEMPENHO
**Tipo:** VARCHAR2(1)
**Valores:** 'S' = Sim, 'N' = Não

**Propósito:** Define se o tipo de operação utiliza o sistema de empenho/reserva.

**Como usar:**
```sql
-- Verificar se CODTIPOPER usa empenho
SELECT TOP.CODTIPOPER, TOP.AD_RESERVAEMPENHO
FROM TGFTOP TOP
WHERE TOP.CODTIPOPER = 3001
```

**Importante:**
- Sempre usar ROW_NUMBER() para pegar versão mais recente:
```sql
SELECT CODTIPOPER, AD_RESERVAEMPENHO
FROM (
    SELECT CODTIPOPER, AD_RESERVAEMPENHO,
           ROW_NUMBER() OVER (PARTITION BY CODTIPOPER ORDER BY DHALTER DESC) AS RN
    FROM TGFTOP
) WHERE RN = 1
```

---

## 📝 Queries de Exemplo

### 1. Listar Empenhos de um Pedido

```sql
SELECT
    e.NUNOTAPEDVEN AS pedido_venda,
    e.NUNOTA AS pedido_compra,
    e.CODPROD,
    p.DESCRPROD,
    e.QTDEMPENHO,
    cc.CODPARC AS fornecedor,
    par.NOMEPARC AS nome_fornecedor
FROM TGWEMPE e
JOIN TGFPRO p ON p.CODPROD = e.CODPROD
JOIN TGFCAB cc ON cc.NUNOTA = e.NUNOTA
JOIN TGFPAR par ON par.CODPARC = cc.CODPARC
WHERE e.NUNOTAPEDVEN = 1192580
```

### 2. Verificar Cotações de um Produto

```sql
SELECT
    cot.NUMCOTACAO,
    cot.DTCOTACAO,
    usu.NOMEUSU AS responsavel,
    itc.CODPARC AS fornecedor,
    par.NOMEPARC AS nome_fornecedor,
    itc.VLRUNIT,
    itc.PRAZOENTR,
    itc.STATUSPRODCOT
FROM TGFCOT cot
JOIN TSIUSU usu ON usu.CODUSU = cot.CODUSURESP
JOIN TGFITC itc ON itc.NUMCOTACAO = cot.NUMCOTACAO
JOIN TGFPAR par ON par.CODPARC = itc.CODPARC
WHERE itc.CODPROD = 45678
ORDER BY itc.VLRUNIT ASC
```

### 3. Consolidar Fornecedores por Venda + Produto

```sql
SELECT
    e.NUNOTAPEDVEN,
    e.CODPROD,
    LISTAGG(TO_CHAR(cc.CODPARC), ', ') WITHIN GROUP (ORDER BY cc.CODPARC) AS fornecedores
FROM TGWEMPE e
JOIN TGFCAB cc ON cc.NUNOTA = e.NUNOTA
GROUP BY e.NUNOTAPEDVEN, e.CODPROD
```

---

## ⚠️ Problemas e Soluções

### Problema 1: ORA-00904 - "ITC"."EMPRESA": identificador inválido

**Contexto:** Tentativa de filtrar TGFITC por empresa.

**Erro:**
```sql
LEFT JOIN TGFITC ITC
  ON ITC.CODPARC = b.codparc_fornecedor
 AND ITC.CODPROD = b.codprod
 AND ITC.EMPRESA = C.CODEMP  -- ❌ Campo não existe!
```

**Solução:** Campo EMPRESA não existe em TGFITC. Filtrar apenas por CODPARC + CODPROD é suficiente, pois CODPARC já identifica o fornecedor unicamente.

```sql
LEFT JOIN TGFITC ITC
  ON ITC.CODPARC = b.codparc_fornecedor
 AND ITC.CODPROD = b.codprod  -- ✅ Suficiente!
```

**Aprendizado:** TGFITC não tem conceito de empresa (CODEMP), apenas fornecedor (CODPARC) e produto (CODPROD).

---

### Problema 2: ORA-00904 - "ITC"."USURESP": identificador inválido

**Contexto:** Tentativa de obter usuário responsável direto de TGFITC.

**Erro:**
```sql
LEFT JOIN TGFITC ITC ON ...
LEFT JOIN TSIUSU U ON U.CODUSU = ITC.USURESP  -- ❌ Campo não existe!
```

**Solução:** O responsável pela cotação está no **cabeçalho** (TGFCOT), não nos itens (TGFITC).

Caminho correto:
```
TGFITC.NUMCOTACAO → TGFCOT.NUMCOTACAO → TGFCOT.CODUSURESP → TSIUSU.CODUSU
```

```sql
LEFT JOIN TGFITC ITC ON ITC.CODPARC = ... AND ITC.CODPROD = ...
LEFT JOIN TGFCOT COT ON COT.NUMCOTACAO = ITC.NUMCOTACAO  -- ✅ Via NUMCOTACAO
LEFT JOIN TSIUSU U ON U.CODUSU = COT.CODUSURESP           -- ✅ Via cabeçalho
```

**Aprendizado:**
- Cotação tem estrutura **cabeçalho (TGFCOT) + itens (TGFITC)**
- Dados gerais (responsável, data) ficam no cabeçalho
- Dados específicos (preço, prazo) ficam nos itens

---

### Problema 3: Pedido sem Cotação

**Contexto:** Pedido 1192177 aparecia no relatório mas sem dados de cotação.

**Investigação:**
```sql
-- Verificar se tem empenho
SELECT COUNT(*) FROM TGWEMPE WHERE NUNOTAPEDVEN = 1192177;
-- Resultado: 0 registros
```

**Diagnóstico:** Pedido ainda não foi empenhado (status "Item não empenhado").

**Conclusão:**
- Comportamento **correto**!
- Sem empenho → sem compra criada → sem cotação possível
- Workflow: Venda → **Empenho** → Cotação → Compra

**Aprendizado:** Sempre verificar se pedido tem empenho antes de esperar dados de cotação.

---

## 📊 Estatísticas da Query Atual

### Resultado da Execução (2026-02-02)

```
Total de registros: 2.103
Registros COM cotação: 309 (14.7%)
Registros SEM cotação: 1.794 (85.3%)
```

### Campos Retornados (29 campos)

| # | Campo | Origem | Tipo |
|---|-------|--------|------|
| 1 | Data | TGFCAB.DTNEG + HRMOV | TIMESTAMP |
| 2 | Num_Unico | TGFCAB.NUNOTA | NUMBER |
| 3 | Cod_Cliente | TGFCAB.CODPARC | NUMBER |
| 4 | Cliente | TGFPAR.NOMEPARC | VARCHAR2 |
| 5 | Emp | TGFCAB.CODEMP | NUMBER |
| 6 | Previsao_Entrega | TGFCAB.DTPREVENT | DATE |
| 7 | Cod_Vend | TGFCAB.CODVEND | NUMBER |
| 8 | Vendedor | TGFVEN.APELIDO | VARCHAR2 |
| 9 | Cod_Prod | TGFITE.CODPROD | NUMBER |
| 10 | Produto | TGFPRO.DESCRPROD | VARCHAR2 |
| 11 | Qtd_SKUs | SUM(TGFITE.QTDNEG) | NUMBER |
| 12 | Qtd_Com_Empenho | SUM(TGWEMPE.QTDEMPENHO) | NUMBER |
| 13 | Qtd_Sem_Empenho | Calculado | NUMBER |
| 14 | Valor | SUM(TGFITE.VLRTOT) | NUMBER |
| 15 | Custo | SUM(compra VLRTOT) | NUMBER |
| 16 | Custo_Medio | Calculado | NUMBER |
| 17 | Cod_Forn | LISTAGG(CODPARC) | VARCHAR2 |
| 18 | Fornecedor | LISTAGG(NOMEPARC) | VARCHAR2 |
| 19 | Num_Unico_NF_Empenho | LISTAGG(NUNOTA compra) | VARCHAR2 |
| 20 | Num_NF_Empenho | LISTAGG(NUMNOTA compra) | VARCHAR2 |
| 21 | **Cod_Cotacao** | TGFITC.NUMCOTACAO | NUMBER |
| 22 | **Nome_Resp_Cotacao** | TSIUSU.NOMEUSU | VARCHAR2 |
| 23 | **Status_Cotacao** | TGFITC.STATUSPRODCOT | VARCHAR2 |
| 24 | status_empenho_item | Calculado | VARCHAR2 |
| 25 | status_wms | Calculado | VARCHAR2 |
| 26 | status_logistico_item | Calculado | VARCHAR2 |
| 27 | status_geral_item | Calculado | VARCHAR2 |
| 28 | bkcolor | Calculado (cor fundo) | VARCHAR2 |
| 29 | fgcolor | Calculado (cor texto) | VARCHAR2 |

**Campos adicionados nesta sessão:** 21, 22, 23, 19, 20 ⭐

---

## 🎯 Próximos Passos

### Melhorias Futuras

1. **Mapear Status de Cotação**
   - Documentar valores possíveis de STATUSPRODCOT
   - Criar DE-PARA: 'A' = "Aguardando", 'C' = "Cotado", etc

2. **Critérios de Seleção**
   - Investigar campos de peso (custo vs prazo vs qualidade)
   - Entender como sistema escolhe vencedor

3. **Histórico de Cotações**
   - Verificar se há tabela de log/histórico
   - Mapear alterações de cotação

4. **Performance**
   - Avaliar índices nas tabelas
   - Otimizar LISTAGG com grandes volumes

---

## 📚 Referências

- **Arquivo SQL:** `query_empenho_com_cotacao.sql`
- **Arquivo SQL (sem parâmetros):** `query_empenho_com_cotacao_sem_parametros.sql`
- **Script Execução:** `executar_empenho_com_cotacao.py`
- **Script HTML:** `gerar_html_empenho.py`
- **Diagnóstico:** `investigar_pedido_1192177.py`, `investigar_pedido_simples.py`
- **Resultado:** `resultado_empenho_com_cotacao.json`
- **Relatório:** `relatorio_empenho_cotacao.html`

---

**Última atualização:** 2026-02-02
**Próxima revisão:** Ao mapear novos campos ou descobrir novos relacionamentos

---

✅ **Documento completo e validado com dados reais**
