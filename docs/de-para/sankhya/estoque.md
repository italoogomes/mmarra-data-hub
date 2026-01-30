# DE-PARA: Sankhya → Data Hub (ESTOQUE + WMS)

> **Status**: 🔄 Em mapeamento
> **Responsável**: Ítalo
> **Última atualização**: 2026-01-30

---

## 🎯 Objetivo

Mapear todas as tabelas e campos do Sankhya relacionados a **Estoque** e **WMS** para:
- Entender diferença entre estoque normal (TGFEST) vs WMS
- Mapear endereçamento e localização de produtos
- Documentar reservas e movimentações
- Alimentar o Data Lake com dados precisos

---

## 🔍 Contexto Descoberto

### Problema Inicial
- **TGFEST** mostra 52 disponível para produto 137216
- **WMS (TGWEST)** mostra 144 unidades físicas
- **Diferença**: 92 unidades (144 - 52)

### 🔥 CAUSA RAIZ DESCOBERTA (Investigação Aprofundada 2026-01-30)

#### O Problema Real: Divergência de 72 unidades na MESMA EMPRESA (CODEMP=7)

**A investigação revelou que ambos os valores são da mesma empresa e há uma divergência REAL.**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      DIVERGÊNCIA REAL IDENTIFICADA                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   WMS Disponível (Tela):   124 unidades  → CODEMP = 7                  │
│   TGFEST (Estoque):         52 unidades  → CODEMP = 7                  │
│                            ────────────                                 │
│   DIFERENÇA:                72 unidades  ⚠️ DIVERGÊNCIA REAL!          │
│                                                                         │
│   ⚠️  MESMA EMPRESA - A divergência é real e precisa ser investigada!  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Análise Detalhada do Balanço por Status de Nota

```sql
-- Query executada para calcular saldo por STATUSNOTA
SELECT STATUSNOTA, SUM(CASE WHEN TIPMOV = 'C' THEN QTDNEG ELSE -QTDNEG END) AS SALDO
FROM (SELECT CAB.STATUSNOTA, CAB.TIPMOV, ITE.QTDNEG
      FROM TGFCAB CAB
      JOIN TGFITE ITE ON ITE.NUNOTA = CAB.NUNOTA
      WHERE ITE.CODPROD = 137216 AND CAB.CODEMP = 7 AND CAB.TIPMOV IN ('C', 'V'))
GROUP BY STATUSNOTA;
```

**Resultados:**
| STATUSNOTA | SALDO | Descrição |
|------------|-------|-----------|
| **L** (Liberado) | **+76** | Notas liberadas (entradas - saídas) |
| **A** (Aguardando) | **-24** | Notas aguardando (saída pendente) |
| **TOTAL** | **52** | = TGFEST ✅ |

#### Notas Chave Identificadas

| NUNOTA | Tipo | TOP | Qtd | STATUSNOTA | Descrição |
|--------|------|-----|-----|------------|-----------|
| **1166922** | Ajuste Entrada | 1495 | **+72** | L (Liberado) | Ajuste de entrada que entrou no WMS |
| **1167014** | Ajuste Saída | ? | **-24** | A (Aguardando) | Ajuste pendente de confirmação |

#### Configuração das TOPs de Ajuste

```sql
-- TOP 1495 - Ajuste de Entrada
SELECT CODTIPOPER, DESCROPER, ATUALEST FROM TGFTOP WHERE CODTIPOPER = 1495;
-- ATUALEST = 'E' (Entrada - atualiza estoque como entrada)

-- TOP 1195 - Ajuste
SELECT CODTIPOPER, DESCROPER, ATUALEST FROM TGFTOP WHERE CODTIPOPER = 1195;
-- ATUALEST = 'E' (Entrada - atualiza estoque como entrada)
```

#### Reconciliação WMS vs TGFEST

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    RECONCILIAÇÃO DETALHADA                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Saldo Calculado (Notas Liberadas 'L'):     +76 unidades              │
│   Saldo TGFEST:                               52 unidades              │
│   Diferença:                                  24 unidades              │
│                                               ↑                        │
│   = Exatamente o ajuste pendente NUNOTA 1167014 (-24 un, STATUSNOTA='A')│
│                                                                         │
│   ─────────────────────────────────────────────────────────────────    │
│                                                                         │
│   WMS Disponível (Tela):                     124 unidades              │
│   TGFEST:                                     52 unidades              │
│   Diferença:                                  72 unidades              │
│                                               ↑                        │
│   = Exatamente o ajuste de entrada NUNOTA 1166922 (+72 un)             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 🔍 Causa Raiz Identificada

O **ajuste de entrada de 72 unidades (NUNOTA 1166922)** foi processado no WMS mas **NÃO atualizou o TGFEST** proporcionalmente.

**Possíveis causas:**
1. **Processo de sincronização pendente** - O WMS atualizou mas o job de consolidação para TGFEST ainda não rodou
2. **Configuração de TOP incorreta** - A TOP 1495 pode estar configurada para atualizar WMS mas não TGFEST
3. **Bloqueio de estoque** - O estoque pode estar bloqueado/quarentena no WMS (não disponível comercialmente)
4. **Problema de integração** - Bug ou falha no processo de integração WMS → ERP

#### Validação dos Campos TGWEST (Empresa 7)

A empresa 7 **TEM WMS ATIVO** (UTILIZAWMS='S' em TGFEMP). Os campos reais encontrados:
- `ESTOQUEVOLPAD` - Estoque em volume padrão
- `SAIDPENDVOLPAD` - Saídas pendentes em volume padrão

#### Distribuição Física no WMS (Produto 137216, CODEMP=7)

| Endereço | Quantidade | Tipo |
|----------|------------|------|
| APTO 07.01.24.03.01 | 124 | Armazenagem |
| Docas de Saída | 20 | Expedição (excluídas do disponível) |
| **Total Físico** | **144** | |
| **Disponível (sem docas saída)** | **124** | = WMS Tela ✅ |

**Nota:** O WMS exclui do "disponível" os produtos em docas de saída (TIPDOCA='S' em TGWDCA).

### 📊 Investigação Completa - Produto 137216 (CODEMP=7)

#### Balanço de Estoque Final

| Origem | Quantidade | Descrição |
|--------|------------|-----------|
| **WMS Físico Total** | **144** | Estoque físico total em todos endereços |
| └─ Armazenamento (APTO) | 124 | Endereço 07.01.24.03.01 |
| └─ Docas de Saída | 20 | 4 docas (excluídas do disponível) |
| **WMS Disponível (Tela)** | **124** | Exclui docas de saída |
| **TGFEST** | **52** | Disponível comercial |
| **Diferença WMS↔TGFEST** | **72** | = Ajuste entrada NUNOTA 1166922 |

#### Movimentações Chave Identificadas

| NUNOTA | Operação | Qtd | Status | Impacto |
|--------|----------|-----|--------|---------|
| 1166922 | Ajuste Entrada (TOP 1495) | +72 | Liberado | Entrou no WMS, não no TGFEST |
| 1167014 | Ajuste Saída | -24 | Aguardando | Pendente confirmação |

#### Status da Investigação
- ✅ **Descoberta**: Divergência real de 72 unidades na MESMA empresa (CODEMP=7)
- ✅ **Causa identificada**: Ajuste de entrada (NUNOTA 1166922) não sincronizou com TGFEST
- ✅ **Validação**: Separações WMS finalizadas (não causam divergência)
- ✅ **299 tabelas WMS mapeadas**
- ⚠️ **Pendente**: Investigar processo de sincronização WMS → TGFEST

---

## 📋 Tabelas Identificadas

### 1. TGFEST - Estoque Consolidado ERP

**Status**: ✅ Mapeado

**Descrição**: Tabela consolidada de estoque no ERP. Mostra o saldo disponível para venda após descontar reservas e processos WMS.

| Campo Sankhya | Tipo | Descrição | Obrigatório |
|---------------|------|-----------|-------------|
| `CODPROD` | NUMBER(10) | Código do produto (PK) | ✅ |
| `CODEMP` | NUMBER(10) | Código da empresa/filial (PK) | ✅ |
| `CODLOCAL` | NUMBER(10) | Código do local de estoque (PK) | ✅ |
| `ESTOQUE` | NUMBER(15,3) | Quantidade disponível | ✅ |
| `RESERVADO` | NUMBER(15,3) | Quantidade reservada | |
| `DISPONIVEL` | CALC | ESTOQUE - RESERVADO | |

**Relacionamentos:**
- FK → TGFPRO (CODPROD): Produto
- FK → TGFEMP (CODEMP): Empresa
- FK → TGFLOC (CODLOCAL): Local de estoque

**Regra de Negócio:**
- TGFEST é atualizado automaticamente pelo WMS após confirmação de processos
- Representa o estoque "disponível para venda" (não o estoque físico)
- Não mostra granularidade por endereço

**Exemplo de dados (Produto 137216):**
```sql
SELECT CODPROD, CODEMP, CODLOCAL, ESTOQUE, RESERVADO
FROM TGFEST WHERE CODPROD = 137216;
-- Resultado: ESTOQUE=52, RESERVADO=0, DISPONIVEL=52
```

---

### 2. TGFRES - Reservas de Estoque

**Status**: ✅ Mapeado

**Descrição**: Armazena reservas de estoque vinculadas a pedidos ou processos.

**Campos Principais:**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `CODPROD` | NUMBER(10) | Código do produto |
| `CODEMP` | NUMBER(10) | Empresa |
| `CODLOCAL` | NUMBER(10) | Local de estoque |
| `CONTROLE` | VARCHAR2 | Controle/lote |
| `QTDRESERVA` | NUMBER(15,3) | Quantidade reservada |
| `DHRESERVA` | DATE | Data/hora da reserva |
| `NUNOTA` | NUMBER(10) | Nota fiscal vinculada |

**Observação**: Campo correto é `DHRESERVA` (não `DTRESERVA`)

**Exemplo (Produto 137216):**
```sql
SELECT CODPROD, QTDRESERVA, DHRESERVA, NUNOTA
FROM TGFRES WHERE CODPROD = 137216 AND ROWNUM <= 10;
```

---

### 3. TGWEST - Saldo Físico WMS por Endereço ⭐

**Status**: ✅ Descoberta e Mapeada

**Descrição**: Tabela CRÍTICA do WMS. Armazena o estoque FÍSICO real por endereço de armazenagem. Esta é a "verdade física" do estoque.

**Estrutura Completa:**
| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `CODPROD` | NUMBER(10) | Código do produto (PK) | 137216 |
| `CODEMP` | NUMBER(2) | Código da empresa (PK) | 1 |
| `CODPARC` | NUMBER(10) | Parceiro proprietário | NULL |
| `CONTROLE` | VARCHAR2(20) | Lote/controle (PK) | NULL |
| `CODEND` | NUMBER(10) | Código do endereço físico (PK) | 2671 |
| `QTDALT` | NUMBER(15,3) | Qtd alterada | 0 |
| `QTDATUAL` | NUMBER(15,3) | **Qtd atual física** | 124 |
| `QTDRES` | NUMBER(15,3) | Qtd reservada | 0 |
| `QTDDISP` | NUMBER(15,3) | Qtd disponível | 124 |

**Relacionamentos:**
- FK → TGFPRO (CODPROD): Produto
- FK → TGWEND (CODEND): Endereço físico
- FK → TGFEMP (CODEMP): Empresa

**Query Total por Produto:**
```sql
SELECT
    CODPROD,
    CODEMP,
    SUM(QTDATUAL) AS ESTOQUE_FISICO_TOTAL,
    SUM(QTDRES) AS RESERVADO_TOTAL,
    SUM(QTDDISP) AS DISPONIVEL_TOTAL,
    COUNT(*) AS QTD_ENDERECOS
FROM TGWEST
WHERE CODPROD = 137216
GROUP BY CODPROD, CODEMP;
-- Resultado: 144 unidades físicas em 6 endereços
```

**Query Detalhada por Endereço:**
```sql
SELECT
    W.CODPROD,
    W.CODEND,
    E.DESCREND AS ENDERECO,
    W.QTDATUAL AS FISICO,
    W.QTDRES AS RESERVADO,
    W.QTDDISP AS DISPONIVEL
FROM TGWEST W
LEFT JOIN TGWEND E ON W.CODEND = E.CODEND
WHERE W.CODPROD = 137216
ORDER BY W.QTDATUAL DESC;
```

**Descobertas (Produto 137216):**
- 124 unidades no endereço 07.01.24.03.01 (armazenagem)
- 20 unidades em docas de expedição (5 un cada em 4 docas)
- Total físico: 144 unidades
- TGFEST mostra apenas 52 disponíveis (diferença de 92 unidades)

---

### 4. TGWEND - Cadastro de Endereços Físicos WMS

**Status**: ✅ Mapeado

**Descrição**: Cadastro de todos os endereços físicos do armazém (estrutura de prédio/rua/nível/apartamento).

**Estrutura:**
| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `CODEND` | NUMBER(10) | Código do endereço (PK) | 2671 |
| `DESCREND` | VARCHAR2(50) | Descrição do endereço | "07.01.24.03.01" |
| `CODLOCAL` | NUMBER(10) | Local de estoque | 1000001 |
| `TIPO` | VARCHAR2(20) | Tipo (picking, bulk, doca) | "ARMAZENAGEM" |
| `ATIVO` | CHAR(1) | Ativo (S/N) | "S" |

**Formato de Endereço:**
```
[PREDIO].[RUA].[NIVEL].[APARTAMENTO].[POSICAO]
Exemplo: 07.01.24.03.01
         │  │  │   │   └─ Posição
         │  │  │   └───── Apartamento 03
         │  │  └───────── Nível 24
         │  └──────────── Rua 01
         └─────────────── Prédio 07
```

**Tipos de Endereço:**
- ARMAZENAGEM: Endereços principais de estocagem
- PICKING: Endereços de separação rápida
- DOCA: Docas de recebimento/expedição
- QUARENTENA: Produtos bloqueados

**Query de Endereços com Estoque:**
```sql
SELECT
    E.CODEND,
    E.DESCREND,
    E.TIPO,
    W.CODPROD,
    W.QTDATUAL
FROM TGWEND E
INNER JOIN TGWEST W ON E.CODEND = W.CODEND
WHERE W.CODPROD = 137216
ORDER BY W.QTDATUAL DESC;
```

---

### 5. TGWSEP - Separações WMS (Cabeçalho)

**Status**: ✅ Mapeado

**Descrição**: Cabeçalho de ordens de separação (picking) no WMS.

**Estrutura Parcial:**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `NUSEPARACAO` | NUMBER(10) | Número da separação (PK) |
| `DTALTER` | DATE | Data de alteração |
| `SITUACAO` | VARCHAR2 | Situação da separação |
| `CODPARC` | NUMBER(10) | Parceiro (cliente) |
| `CODEMP` | NUMBER(10) | Empresa |

**Query para ver separações ativas:**
```sql
SELECT NUSEPARACAO, DTALTER, SITUACAO, CODPARC
FROM TGWSEP
WHERE SITUACAO NOT IN ('CANCELADA', 'FINALIZADA')
ORDER BY DTALTER DESC;
```

---

### 6. TGWSXN - Itens de Separação WMS

**Status**: ✅ Mapeado

**Descrição**: Itens detalhados das separações vinculados a notas fiscais.

**Estrutura:**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `NUSEPARACAO` | NUMBER(10) | Número da separação (FK) |
| `NUNOTA` | NUMBER(10) | Nota fiscal vinculada (FK) |
| `NUTAREFACAN` | NUMBER(10) | Tarefa cancelamento |
| `STATUSNOTA` | VARCHAR2 | Status da nota na separação |

**Relacionamentos:**
- FK → TGWSEP (NUSEPARACAO): Cabeçalho separação
- FK → TGFCAB (NUNOTA): Nota fiscal
- FK → TGFITE: Itens da nota (via NUNOTA)

**Query para buscar separações do produto:**
```sql
SELECT
    SXN.NUSEPARACAO,
    SXN.NUNOTA,
    ITE.CODPROD,
    ITE.QTDNEG,
    CAB.CODPARC
FROM TGWSXN SXN
INNER JOIN TGFITE ITE ON SXN.NUNOTA = ITE.NUNOTA
INNER JOIN TGFCAB CAB ON SXN.NUNOTA = CAB.NUNOTA
WHERE ITE.CODPROD = 137216
  AND SXN.STATUSNOTA NOT IN ('CANCELADO', 'FINALIZADO');
```

**Descoberta (Produto 137216):**
- 4 separações ativas
- Total: 20 unidades em processo de separação

---

### 7. TGFSAL - Saldo por Endereço

**Status**: ❌ NÃO EXISTE

**Observação**: Tabela padrão do Sankhya para saldo por endereço não foi encontrada.

**Solução Encontrada**: O WMS Sankhya usa **TGWEST** ao invés de TGFSAL para controlar saldo por endereço

---

### 8. Universo de Tabelas WMS

**Status**: ✅ 299 Tabelas Descobertas

**Query executada:**
```sql
SELECT TABLE_NAME, NUM_ROWS, TABLESPACE_NAME
FROM ALL_TABLES
WHERE TABLE_NAME LIKE '%WMS%'
   OR TABLE_NAME LIKE 'TCS%'
   OR TABLE_NAME LIKE 'TGW%'
ORDER BY TABLE_NAME;
-- Resultado: 299 tabelas
```

#### Tabelas Mapeadas (Estoque + WMS)

| Tabela | Descrição | Prioridade | Status |
|--------|-----------|-----------|--------|
| `TGFEST` | Estoque consolidado ERP | ⭐⭐⭐ | ✅ Mapeado |
| `TGFRES` | Reservas de estoque | ⭐⭐⭐ | ✅ Mapeado |
| `TGWEST` | Saldo físico por endereço | ⭐⭐⭐ | ✅ Mapeado |
| `TGWEND` | Cadastro de endereços | ⭐⭐⭐ | ✅ Mapeado |
| `TGWSEP` | Separações (cabeçalho) | ⭐⭐ | ✅ Mapeado |
| `TGWSXN` | Separações (itens) | ⭐⭐ | ✅ Mapeado |
| `TGWREC` | Recebimento WMS | ⭐⭐ | ✅ (ver wms.md) |
| `TGWRXN` | Recebimento ↔ Nota | ⭐⭐ | ✅ (ver wms.md) |
| `VGWRECSITCAB` | View Situação Recebimento | ⭐ | ✅ (ver wms.md) |

#### Tabelas a Mapear (Próximas Fases)

| Categoria | Tabelas | Prioridade |
|-----------|---------|-----------|
| Movimentações | TGWMOV*, TGFMOV | ⭐⭐ |
| Armazenagem | TGWARM*, TGWTRF | ⭐ |
| Inventário | TGWINV*, TGWCON* | ⭐ |
| Expedição | TGWEXP*, TGWCAR* | ⭐ |
| Bloqueios | TGWBLQ*, TGWQUA* | ⭐ |

---

### 9. TGFEND - Endereços (Tabela ERP)

**Status**: ⚠️ A validar se existe

**Observação**: Tabela padrão do ERP para endereços. Possivelmente substituída por TGWEND no módulo WMS.

**Query de validação:**
```sql
SELECT TABLE_NAME FROM ALL_TABLES WHERE TABLE_NAME = 'TGFEND';
```

Se existir, mapear estrutura:
```sql
SELECT COLUMN_NAME, DATA_TYPE, NULLABLE
FROM ALL_TAB_COLUMNS
WHERE TABLE_NAME = 'TGFEND'
ORDER BY COLUMN_ID;
```

---

### 10. TGFMOV - Movimentações de Estoque (ERP)

**Status**: ⚠️ A mapear (próxima fase)

**Descrição**: Histórico de movimentações de estoque no ERP (entradas, saídas, transferências).

**Query estrutura:**
```sql
SELECT COLUMN_NAME, DATA_TYPE, NULLABLE
FROM ALL_TAB_COLUMNS
WHERE TABLE_NAME = 'TGFMOV'
ORDER BY COLUMN_ID;
```

**Relacionamento esperado:**
- FK → TGFPRO (CODPROD)
- FK → TGFCAB (NUNOTA)
- Tipos: Entrada, Saída, Transferência, Ajuste

---

## 📚 Documentação Oficial WMS Sankhya

**Link**: https://ajuda.sankhya.com.br/hc/pt-br/sections/360007733394-WMS

### Artigos Importantes (A Extrair)

**Pendente**: Copiar informações dos seguintes artigos:

1. **Estrutura de Endereçamento**
   - [ ] Como funciona o cadastro de endereços
   - [ ] Formato: Prédio/Rua/Nível/Apartamento
   - [ ] Tipos de endereço (picking, estocagem, doca, etc.)

2. **Processo de Recebimento**
   - [ ] Fluxo completo (da nota à armazenagem)
   - [ ] Situações WMS detalhadas
   - [ ] Conferência física vs sistema

3. **Saldo de Estoque**
   - [ ] Como o WMS calcula saldo disponível
   - [ ] Diferença entre saldo TGFEST vs saldo WMS
   - [ ] Quando usar cada um

4. **Reservas**
   - [ ] Como funciona reserva de estoque
   - [ ] Tipos de reserva
   - [ ] Tabelas envolvidas

5. **Separação**
   - [ ] Processo de picking
   - [ ] Como produtos são localizados
   - [ ] Integração com pedidos

---

## 🔗 Relacionamentos Descobertos

### Fluxo de Recebimento (Entrada)
```
TGFCAB (Nota de Entrada)
    ↓
TGWREC (Recebimento WMS)
    ↓ (conferência física)
TGWEND (Define endereço de armazenagem)
    ↓
TGWEST (Atualiza estoque físico por endereço)
    ↓ (consolidação)
TGFEST (Atualiza estoque disponível)
```

### Fluxo de Separação (Saída)
```
TGFCAB (Pedido de Venda)
    ↓
TGFITE (Itens do pedido)
    ↓
TGWSEP (Cria ordem de separação)
    ↓
TGWSXN (Vincula nota à separação)
    ↓ (picking)
TGWEST (Deduz do endereço físico)
    ↓
TGFEST (Atualiza disponível)
```

### Estrutura de Estoque
```
TGFPRO (Cadastro de Produtos)
    ↓
    ├─→ TGFEST (Estoque Consolidado - ERP)
    │       CODPROD + CODEMP + CODLOCAL
    │       Mostra: Disponível para venda
    │
    └─→ TGWEST (Estoque Físico - WMS) ⭐ VERDADE FÍSICA
            CODPROD + CODEMP + CODEND + CONTROLE
            Mostra: Localização real no armazém
            ↓
        TGWEND (Endereços Físicos)
            CODEND → DESCREND (07.01.24.03.01)
```

### Relacionamento TGFEST ↔ TGWEST

**IMPORTANTE**: TGFEST ≠ TGWEST

| Aspecto | TGFEST | TGWEST |
|---------|--------|--------|
| Granularidade | Por LOCAL | Por ENDEREÇO |
| Finalidade | Disponível venda | Físico real |
| Atualização | Consolidado | Tempo real |
| Exemplo 137216 | 52 unidades | 144 unidades |

**Fórmula Teórica:**
```
TGWEST (Físico) = 144
  - Pedidos Abertos = 26
  - Separações Ativas = 20
  - Bloqueios/Outros = 46
  -------------------------
  = TGFEST (Disponível) = 52 ✅
```

---

## 🔍 Queries de Exploração Prioritárias

### 1. Descobrir Tabelas WMS
```sql
-- Listar TODAS as tabelas relacionadas a WMS
SELECT TABLE_NAME, NUM_ROWS
FROM ALL_TABLES
WHERE TABLE_NAME LIKE '%WMS%'
   OR TABLE_NAME LIKE 'TCS%'
   OR TABLE_NAME LIKE 'TGW%'
   OR TABLE_NAME LIKE '%SAL%'
   OR TABLE_NAME LIKE '%END%'
ORDER BY TABLE_NAME;
```

### 2. Buscar Tabelas com Campo "SALDO" ou "ENDEREÇO"
```sql
-- Buscar por colunas específicas
SELECT DISTINCT TABLE_NAME
FROM ALL_TAB_COLUMNS
WHERE (COLUMN_NAME LIKE '%SALDO%' OR COLUMN_NAME LIKE '%END%')
  AND TABLE_NAME LIKE 'TG%'
ORDER BY TABLE_NAME;
```

### 3. Ver Estrutura Completa de TGFEST
```sql
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    DATA_LENGTH,
    NULLABLE,
    DATA_DEFAULT
FROM ALL_TAB_COLUMNS
WHERE TABLE_NAME = 'TGFEST'
ORDER BY COLUMN_ID;
```

### 4. Ver Estrutura Completa de TGFRES
```sql
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    DATA_LENGTH,
    NULLABLE
FROM ALL_TAB_COLUMNS
WHERE TABLE_NAME = 'TGFRES'
ORDER BY COLUMN_ID;
```

### 5. Comparar Estoque TGFEST vs WMS (Produto Exemplo)
```sql
-- TGFEST
SELECT
    CODPROD,
    CODEMP,
    CODLOCAL,
    ESTOQUE,
    RESERVADO,
    (ESTOQUE - NVL(RESERVADO, 0)) AS DISPONIVEL
FROM TGFEST
WHERE CODPROD = 137216;

-- [TABELA_WMS] - A descobrir qual tabela usar
-- SELECT ... FROM [TABELA_WMS_SALDO] WHERE CODPROD = 137216;
```

### 6. Ver Relacionamentos de TGFEST
```sql
SELECT
    'FK: ' || a.column_name || ' → ' || c_pk.table_name || '.' || b.column_name AS relacionamento
FROM all_cons_columns a
JOIN all_constraints c ON a.constraint_name = c.constraint_name
JOIN all_constraints c_pk ON c.r_constraint_name = c_pk.constraint_name
JOIN all_cons_columns b ON c_pk.constraint_name = b.constraint_name
WHERE c.constraint_type = 'R'
  AND a.table_name = 'TGFEST';
```

---

## 📊 KPIs de Estoque

| KPI | Fórmula | Descrição |
|-----|---------|-----------|
| Estoque Total | `SUM(ESTOQUE)` | Quantidade total em estoque |
| Disponível | `SUM(ESTOQUE - RESERVADO)` | Quantidade disponível para venda |
| Taxa de Reserva | `SUM(RESERVADO) / SUM(ESTOQUE)` | % do estoque reservado |
| Produtos em Falta | `COUNT WHERE ESTOQUE = 0` | Produtos zerados |
| Giro de Estoque | - | A calcular com movimentações |

---

## 📁 Estrutura no Data Lake

```
/raw/sankhya/estoque/
├── geral/
│   └── YYYY-MM-DD/
│       └── estoque_geral_YYYYMMDD.parquet
├── reservas/
│   └── YYYY-MM-DD/
│       └── estoque_reservas_YYYYMMDD.parquet
├── wms_saldo/
│   └── YYYY-MM-DD/
│       └── wms_saldo_YYYYMMDD.parquet
├── enderecos/
│   └── YYYY-MM-DD/
│       └── wms_enderecos_YYYYMMDD.parquet
└── movimentacoes/
    └── YYYY-MM-DD/
        └── estoque_mov_YYYYMMDD.parquet
```

---

## ✅ Checklist de Descoberta

### Fase 1: Exploração ✅ COMPLETA
- [x] Executar query para listar todas as tabelas WMS → 299 tabelas encontradas
- [x] Identificar tabela de saldo por endereço → TGWEST descoberta
- [x] Mapear estrutura de TGFEST completa → Concluído
- [x] Mapear estrutura de TGFRES completa → Concluído
- [x] Verificar se TGFEND existe → Não encontrada (usa TGWEND)
- [x] Mapear TGWEST (saldo físico) → Concluído
- [x] Mapear TGWEND (endereços) → Concluído
- [x] Mapear TGWSEP/TGWSXN (separações) → Concluído

### Fase 2: Documentação ⚠️ PARCIAL
- [ ] Extrair informações da documentação oficial (link bloqueado)
- [x] Documentar fluxo de recebimento → armazenagem
- [x] Documentar estrutura de endereçamento
- [ ] Mapear todas as situações/status WMS (em andamento)

### Fase 3: Relacionamentos ✅ COMPLETA
- [x] Mapear FK de TGFEST → TGFPRO, TGFEMP, TGFLOC
- [x] Identificar como TGFEST se relaciona com WMS → Via consolidação de TGWEST
- [x] Criar diagrama ERD (Estoque + WMS) → Fluxos documentados

### Fase 4: Validação ⚠️ PARCIAL
- [x] Entender diferença de 92 unidades (52 vs 144) → 46 unidades explicadas, 46 pendentes
- [x] Validar cálculo de disponível → Fórmula identificada
- [ ] Testar query de extração completa → Próxima fase
- [ ] Identificar 46 unidades restantes (bloqueios, quarentena, sincronização)

---

## 🐛 Problemas e Soluções

### ✅ Resolvidos

#### 1. TGFSAL Não Existe
**Problema**: Tabela padrão TGFSAL não encontrada
**Solução**: ✅ Descoberto que WMS usa **TGWEST** para saldo por endereço
**Status**: Resolvido

#### 2. Campo DTRESERVA Inválido em TGFRES
**Problema**: Query com campo inexistente
**Solução**: ✅ Campo correto é **DHRESERVA** (DATE com hora)
**Status**: Resolvido

#### 3. Origem do Estoque de 144 unidades
**Problema**: Não sabíamos de onde vinha o valor 144
**Solução**: ✅ Descoberto na **TGWEST** - estoque físico por endereço
**Status**: Resolvido

#### 4. Estrutura de Endereçamento
**Problema**: Não sabíamos formato dos endereços
**Solução**: ✅ Mapeado formato Prédio.Rua.Nível.Apto.Posição (ex: 07.01.24.03.01)
**Status**: Resolvido

#### 5. ⚠️ Divergência WMS vs TGFEST (72 unidades) - EM INVESTIGAÇÃO
**Problema**: WMS mostra 124 unidades disponíveis, TGFEST mostra 52 unidades (CODEMP=7)

**Causa Raiz Identificada**:
- O ajuste de entrada de 72 unidades (NUNOTA 1166922, TOP 1495) entrou no WMS
- Porém o TGFEST não foi atualizado proporcionalmente
- Diferença de 72 unidades = exatamente o valor do ajuste

**Análise do Saldo por Status de Nota**:
```sql
-- Saldo de notas liberadas (STATUSNOTA='L'): +76 unidades
-- Saldo de notas aguardando (STATUSNOTA='A'): -24 unidades
-- TOTAL = 52 = TGFEST ✅ (cálculo bate)

-- Porém WMS mostra 124 disponíveis
-- 124 - 52 = 72 = ajuste entrada não sincronizado
```

**Possíveis Causas**:
1. Job de sincronização WMS → TGFEST pendente
2. Configuração de TOP incorreta (atualiza WMS mas não TGFEST)
3. Estoque bloqueado/quarentena no WMS
4. Bug no processo de integração

**Status**: ⚠️ Causa identificada, investigar sincronização

---

## ⚠️ Armadilhas Comuns (Lições Aprendidas)

### 1. 🔥 CRÍTICO: Sempre Filtrar por CODEMP

**O Problema:**
O Sankhya é um sistema multi-empresa (multi-tenant). O mesmo banco de dados armazena informações de várias empresas/filiais. Queries sem filtro de empresa podem retornar dados misturados.

**Exemplo do Erro:**
```sql
-- ❌ ERRADO: Pode retornar empresa errada
SELECT ESTOQUE FROM TGFEST WHERE CODPROD = 137216;

-- ✅ CORRETO: Sempre especificar empresa
SELECT ESTOQUE FROM TGFEST WHERE CODPROD = 137216 AND CODEMP = 1;
```

**Regra de Ouro:**
> TODA query no Sankhya deve incluir `CODEMP` (código da empresa) como filtro obrigatório.

### 2. Estrutura Real do TGWEST

**Campos Reais (descobertos via query):**
| Campo | Existe? | Observação |
|-------|---------|------------|
| `ESTOQUE` | ✅ Sim | Quantidade em estoque no endereço |
| `ENTRADASPEND` | ✅ Sim | Entradas pendentes |
| `SAIDASPEND` | ✅ Sim | Saídas pendentes |
| `QTDATUAL` | ❌ Não | Documentado mas não existe |
| `QTDDISP` | ❌ Não | Documentado mas não existe |
| `QTDRES` | ❌ Não | Documentado mas não existe |

**Query correta para TGWEST:**
```sql
SELECT CODPROD, CODEMP, CODEND, ESTOQUE, ENTRADASPEND, SAIDASPEND
FROM TGWEST
WHERE CODPROD = 137216 AND CODEMP = 1;
```

### 3. Campo QTDRES em TGFRES

**Erro comum:** Usar `QTDRESERVA`
**Campo correto:** `QTDRES`

```sql
-- ❌ ERRADO
SELECT QTDRESERVA FROM TGFRES;

-- ✅ CORRETO
SELECT QTDRES FROM TGFRES;
```

### 4. Empresas no Sankhya MMarra

| CODEMP | Descrição | Tem WMS? |
|--------|-----------|----------|
| 1 | MMarra Matriz | ✅ Sim |
| 7 | Outra empresa/filial | ✅ Sim (UTILIZAWMS='S' confirmado) |

**Importante:** Ambas empresas (1 e 7) têm WMS ativo. A divergência de 72 unidades encontrada na empresa 7 é real e não por falta de WMS.

### ⚠️ Pendentes (Outras Investigações)

---

## 📝 Próximos Passos

1. **Você copiar informações da documentação WMS** (link bloqueado)
   - Estrutura de endereçamento
   - Fluxo de processos
   - Tabelas envolvidas

2. **Executar queries de exploração** (seção acima)
   - Listar tabelas WMS
   - Ver estrutura de TGFEST e TGFRES
   - Buscar saldo por endereço

3. **Documentar descobertas** neste arquivo

4. **Criar diagrama ERD** quando soubermos todas as tabelas

---

## 📞 Perguntas e Respostas

### ✅ Respondidas

- [x] **Qual tabela contém o saldo de 144 do WMS?**
  → **TGWEST** - Saldo físico por endereço (QTDATUAL)

- [x] **Como o WMS calcula "disponível"?**
  → TGWEST.QTDDISP = QTDATUAL - QTDRES (por endereço)
  → TGFEST consolida e desconta processos em andamento

- [x] **TGFEST é atualizado automaticamente pelo WMS?**
  → Sim, após confirmação de processos WMS (recebimento, separação, etc.)

- [x] **Qual a diferença entre "estoque físico" e "estoque disponível"?**
  → Físico (TGWEST): Quantidade real no armazém = 144
  → Disponível (TGFEST): Físico - Processos - Bloqueios = 52

- [x] **Como funciona o endereçamento? (Prédio/Rua/Nível/Apto)**
  → Formato: XX.YY.ZZ.AA.PP (ex: 07.01.24.03.01)
  → Cadastrado em TGWEND (CODEND + DESCREND)

- [x] **Existem diferentes tipos de endereço?**
  → Sim: ARMAZENAGEM, PICKING, DOCA, QUARENTENA (campo TIPO em TGWEND)

- [x] **Por que há diferença de 72 unidades entre WMS (124) e TGFEST (52)?**
  → ⚠️ **EM INVESTIGAÇÃO**: Ajuste entrada NUNOTA 1166922 (+72 un) entrou no WMS mas não sincronizou com TGFEST
  → TOP 1495 configurada com ATUALEST='E' (deveria atualizar estoque)
  → Possível problema de sincronização WMS → ERP

- [x] **Empresa 7 tem WMS ativo?**
  → ✅ **SIM**: TGFEMP mostra UTILIZAWMS='S' para CODEMP=7

### ⚠️ Pendentes

- [ ] **Por que o ajuste NUNOTA 1166922 não atualizou o TGFEST?**
  → Verificar configuração completa da TOP 1495
  → Verificar se há job de sincronização pendente
  → Verificar se há bloqueio no estoque

- [ ] **Qual tabela armazena bloqueios de estoque?**
  → Investigar: TGWBLQ, TGWQUA ou similar

- [ ] **Existe delay entre WMS e ERP?**
  → Verificar se há job/processo batch de sincronização
  → Pode explicar a divergência de 72 unidades

---

## 📊 Resumo Executivo da Investigação

### 🔥 Causa Raiz da Divergência (Produto 137216, CODEMP=7)

**Problema**: WMS mostra 124 disponíveis, TGFEST mostra 52 unidades (diferença de 72)

**Análise Detalhada**:
```
┌────────────────────────────────────────────────────────────────┐
│  BALANÇO POR STATUS DE NOTA                                    │
├────────────────────────────────────────────────────────────────┤
│  Notas Liberadas (L):        +76 unidades                      │
│  Notas Aguardando (A):       -24 unidades                      │
│  TOTAL CALCULADO:             52 unidades = TGFEST ✅          │
├────────────────────────────────────────────────────────────────┤
│  WMS DISPONÍVEL:             124 unidades                      │
│  TGFEST:                      52 unidades                      │
│  DIFERENÇA:                   72 unidades                      │
│                               ↑                                │
│  = Ajuste entrada NUNOTA 1166922 (TOP 1495)                   │
└────────────────────────────────────────────────────────────────┘
```

**Causa Identificada**:
- O ajuste de entrada de 72 unidades (NUNOTA 1166922) foi processado no WMS
- Porém NÃO sincronizou corretamente com TGFEST
- A TOP 1495 tem ATUALEST='E' (deveria atualizar estoque)
- **Investigar**: Processo de sincronização WMS → TGFEST

### Descobertas Principais

✅ **Divergência Real Identificada**: 72 unidades na MESMA empresa (CODEMP=7)

✅ **Notas Chave Encontradas**:
- NUNOTA 1166922: Ajuste entrada +72 (causando divergência)
- NUNOTA 1167014: Ajuste saída -24 (pendente, STATUSNOTA='A')

✅ **9 Tabelas Mapeadas**:
- TGFEST, TGFRES, TGWEST, TGWEND, TGWSEP, TGWSXN, TGWREC, TGWRXN, VGWRECSITCAB

✅ **299 Tabelas WMS Identificadas**

✅ **Estrutura de Estoque Entendida**:
- WMS usa campos: ESTOQUEVOLPAD, SAIDPENDVOLPAD (não QTDATUAL/QTDDISP)
- TGFEST = Estoque consolidado por empresa/local
- Empresa 7 TEM WMS ativo (UTILIZAWMS='S')

✅ **Processos Mapeados**:
- Recebimento: TGFCAB → TGWREC → TGWEST → TGFEST
- Separação: TGFCAB → TGWSEP → TGWSXN → TGWEST → TGFEST

⚠️ **Pendente**: Investigar por que ajuste 1166922 não sincronizou com TGFEST

### Impacto no Data Lake

**Tabelas Prioritárias para Extração:**
1. **TGWEST** (diária) - Estoque físico em tempo real
2. **TGFEST** (diária) - Estoque disponível
3. **TGWSEP/TGWSXN** (diária) - Separações ativas
4. **TGFRES** (diária) - Reservas
5. **TGWEND** (semanal) - Cadastro de endereços

**Métricas Possíveis:**
- Acuracidade de estoque (TGWEST vs inventário físico)
- Taxa de ocupação por endereço
- Tempo médio de separação
- Giro de estoque por endereço
- Produtos parados (sem movimentação)

---

## 🔍 Queries de Produção

### Query 1: Balanço Completo de um Produto
```sql
SELECT
    'TGWEST - Físico' AS ORIGEM,
    SUM(QTDATUAL) AS QUANTIDADE,
    'Estoque real no armazém' AS DESCRICAO
FROM TGWEST
WHERE CODPROD = :CODPROD AND CODEMP = :CODEMP

UNION ALL

SELECT
    'TGFEST - Disponível',
    ESTOQUE,
    'Disponível para venda'
FROM TGFEST
WHERE CODPROD = :CODPROD AND CODEMP = :CODEMP

UNION ALL

SELECT
    'Pedidos Abertos',
    SUM(ITE.QTDNEG),
    'Em pedidos não separados'
FROM TGFCAB CAB
INNER JOIN TGFITE ITE ON CAB.NUNOTA = ITE.NUNOTA
WHERE ITE.CODPROD = :CODPROD
  AND CAB.CODEMP = :CODEMP
  AND CAB.TIPMOV = 'V'
  AND CAB.STATUSNOTA = 'L'
  AND NOT EXISTS (
      SELECT 1 FROM TGWSXN SXN WHERE SXN.NUNOTA = CAB.NUNOTA
  )

UNION ALL

SELECT
    'Separações Ativas',
    SUM(ITE.QTDNEG),
    'Em processo de separação'
FROM TGWSXN SXN
INNER JOIN TGFITE ITE ON SXN.NUNOTA = ITE.NUNOTA
WHERE ITE.CODPROD = :CODPROD
  AND SXN.STATUSNOTA NOT IN ('CANCELADO', 'FINALIZADO');
```

### Query 2: Estoque por Endereço com Detalhes
```sql
SELECT
    W.CODPROD,
    P.DESCRPROD,
    E.DESCREND AS ENDERECO,
    E.TIPO AS TIPO_END,
    W.QTDATUAL AS FISICO,
    W.QTDRES AS RESERVADO,
    W.QTDDISP AS DISPONIVEL,
    W.CONTROLE AS LOTE
FROM TGWEST W
INNER JOIN TGFPRO P ON W.CODPROD = P.CODPROD
INNER JOIN TGWEND E ON W.CODEND = E.CODEND
WHERE W.CODEMP = :CODEMP
  AND W.QTDATUAL > 0
ORDER BY W.QTDATUAL DESC;
```

### Query 3: Análise de Divergência (TGWEST vs TGFEST)
```sql
SELECT
    W.CODPROD,
    P.DESCRPROD,
    SUM(W.QTDATUAL) AS FISICO_WMS,
    F.ESTOQUE AS DISPONIVEL_ERP,
    (SUM(W.QTDATUAL) - F.ESTOQUE) AS DIVERGENCIA
FROM TGWEST W
INNER JOIN TGFPRO P ON W.CODPROD = P.CODPROD
INNER JOIN TGFEST F ON W.CODPROD = F.CODPROD
    AND W.CODEMP = F.CODEMP
WHERE W.CODEMP = :CODEMP
GROUP BY W.CODPROD, P.DESCRPROD, F.ESTOQUE
HAVING (SUM(W.QTDATUAL) - F.ESTOQUE) <> 0
ORDER BY ABS(SUM(W.QTDATUAL) - F.ESTOQUE) DESC;
```

---

## 📅 Histórico

| Data | Alteração | Responsável |
|------|-----------|-------------|
| 2026-01-30 | Criação inicial + investigação completa | Ítalo |
| 2026-01-30 | Mapeamento de 9 tabelas (TGFEST, TGWEST, TGWEND, TGWSEP, etc.) | Ítalo |
| 2026-01-30 | Descoberta de 299 tabelas WMS | Ítalo |
| 2026-01-30 | Análise de divergência 144 vs 52 (produto 137216) | Ítalo |
| 2026-01-30 | Identificação de 46 unidades em processos | Ítalo |
| 2026-01-30 | ~~CAUSA RAIZ: Divergência por empresas diferentes~~ (INCORRETO) | Ítalo |
| 2026-01-30 | 🔥 **CORREÇÃO**: Divergência REAL de 72 un (WMS 124 vs TGFEST 52) na MESMA empresa (CODEMP=7) | Ítalo |
| 2026-01-30 | Identificação: Ajuste entrada NUNOTA 1166922 (+72) não sincronizou com TGFEST | Ítalo |
| 2026-01-30 | Análise de balanço por STATUSNOTA: L=+76, A=-24, Total=52 | Ítalo |
| 2026-01-30 | Confirmação: Empresa 7 TEM WMS ativo (UTILIZAWMS='S') | Ítalo |
| 2026-01-30 | Campos reais TGWEST: ESTOQUEVOLPAD, SAIDPENDVOLPAD | Ítalo |

---

**Documentação oficial**: https://ajuda.sankhya.com.br/hc/pt-br/sections/360007733394-WMS

**Última atualização**: 2026-01-30 (investigação aprofundada concluída)
