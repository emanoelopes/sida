<!-- 458b7da2-814b-45ad-ae30-d9404a986b68 9264002c-cf45-4fff-9818-240858d2a94e -->
# Plano de Unificação de Datasets (UCI e OULAD)

## Visão Geral

Criar um dataset unificado combinando UCI e OULAD com nomes de colunas em português, variável alvo padronizada como `resultado_final`, e dados OULAD agregados (uma linha por estudante).

## Análise das Bases Existentes

### UCI Dataset

**Localização:** `datasets/uci_data/student-mat.csv` e `student-por.csv`

**Colunas principais (33 colunas):**

- **Demográficas:** `sex`, `age`, `address`, `famsize`, `Pstatus`, `Medu`, `Fedu`, `Mjob`, `Fjob`
- **Acadêmicas:** `failures`, `absences`, `schoolsup`, `famsup`, `paid`, `G1`, `G2`, `G3`
- **Comportamentais:** `studytime`, `traveltime`, `goout`, `Dalc`, `Walc`, `freetime`, `health`
- **Sociais:** `activities`, `nursery`, `higher`, `internet`, `romantic`, `famrel`
- **Outros:** `school`, `reason`, `guardian`
- **Origem:** Campo `origem` adicionado ('mat' ou 'por')

**Target:** `G3` (nota final, escala 0-20)

### OULAD Dataset

**Localização:** `datasets/oulad_data/` (7 arquivos CSV)

**Estrutura atual:** Múltiplas tabelas relacionadas

- `studentInfo.csv`: dados demográficos e resultado final
- `studentAssessment.csv`: notas em avaliações
- `studentVle.csv`: interações com ambiente virtual (cliques)
- `assessments.csv`, `courses.csv`, `vle.csv`, `studentRegistration.csv`

**Colunas principais após processamento:**

- **Demográficas:** `gender`, `region`, `age_band`, `highest_education`, `disability`, `imd_band`
- **Acadêmicas:** `final_result`, `num_of_prev_attempts`, `studied_credits`, `score`
- **Interações:** `sum_click`, `date`, `activity_type`
- **Curso:** `code_module`, `code_presentation`, `module_presentation_length`

**Target:** `final_result` (Pass/Fail/Distinction/Withdrawn)

**Desafio:** Dataset tem múltiplas linhas por estudante devido a interações e avaliações

## Mapeamento de Colunas para Harmonização

### Colunas Comuns (conceitos similares entre UCI e OULAD)

| Conceito | UCI | OULAD | Nome Unificado |

|----------|-----|-------|----------------|

| Gênero | `sex` | `gender` | `genero` |

| Idade | `age` (numérico) | `age_band` (categórico) | `idade` |

| Região | `address` (U/R) | `region` | `regiao` |

| Faltas | `absences` | - | `faltas` |

| Resultado Final | `G3` (0-20) | `final_result` (categórico) | `resultado_final` |

| Tentativas Anteriores | `failures` | `num_of_prev_attempts` | `tentativas_anteriores` |

| Educação | `Medu`, `Fedu` | `highest_education` | `nivel_educacao` |

### Colunas Específicas UCI (preservadas com prefixo `uci_`)

- Educação dos pais: `uci_educacao_mae`, `uci_educacao_pai`
- Profissão dos pais: `uci_trabalho_mae`, `uci_trabalho_pai`
- Consumo de álcool: `uci_alcool_semana`, `uci_alcool_fds`
- Tempo de estudo: `uci_tempo_estudo`
- Notas intermediárias: `uci_nota_periodo1`, `uci_nota_periodo2`
- Suporte: `uci_suporte_escolar`, `uci_suporte_familiar`
- Outros: `uci_saude`, `uci_tempo_livre`, `uci_relacionamento`, etc.

### Colunas Específicas OULAD (preservadas com prefixo `oulad_`)

- Interações: `oulad_total_cliques`, `oulad_media_cliques_dia`
- Avaliações: `oulad_media_score`, `oulad_num_avaliacoes`
- Curso: `oulad_modulo`, `oulad_apresentacao`, `oulad_duracao_curso`
- Registro: `oulad_data_registro`, `oulad_data_cancelamento`
- Créditos: `oulad_creditos_estudados`
- Deficiência: `oulad_deficiencia`
- Banda IMD: `oulad_imd_band`

## Estratégia de Transformação

### 1. Agregação OULAD (uma linha por estudante)

```python
# Por id_student, agregar:
- sum_click: SOMA → oulad_total_cliques
- score: MÉDIA → oulad_media_score
- Contar avaliações → oulad_num_avaliacoes
- Calcular média de cliques por dia
- Manter dados demográficos (primeira ocorrência)
```

### 2. Normalização da Variável Target

```python
# UCI: G3 (0-20) → resultado_final (0-10)
resultado_final = G3 / 2

# OULAD: final_result (categórico) → resultado_final (0-10)
- 'Distinction': 9.0
- 'Pass': 7.0
- 'Fail': 3.0
- 'Withdrawn': 0.0
```

### 3. Padronização de Valores Categóricos

```python
# Gênero
UCI: 'M'/'F' → 'Masculino'/'Feminino'
OULAD: 'M'/'F' → 'Masculino'/'Feminino'

# Idade
UCI: número (15-22) → manter como int
OULAD: '0-35', '35-55', '55<=' → converter para faixas numéricas
```

### 4. Estratégia de Tratamento de Dados Ausentes

#### **Categorização dos Valores Ausentes**

**Ausências Estruturais (Esperadas):**

- UCI: Colunas OULAD serão NaN (ex: `oulad_total_cliques`, `oulad_modulo`)
- OULAD: Colunas UCI serão NaN (ex: `uci_alcool_semana`, `uci_nota_periodo1`)

**Ausências Reais (Problemas):**

- Valores ausentes dentro do próprio dataset
- Campos obrigatórios vazios
- Inconsistências nos dados originais

#### **Estratégias por Tipo de Coluna**

**Colunas Numéricas:**

```python
# Prioridade de imputação:
1. Mediana por grupo (ex: mediana por região/gênero)
2. Mediana global
3. Zero (para contadores como faltas)
4. Valor mínimo/máximo (contexto específico)
```

**Colunas Categóricas:**

```python
# Prioridade de imputação:
1. Moda por grupo (ex: moda por região)
2. Moda global
3. Categoria "Desconhecido" ou "Não informado"
```

**Colunas de Target (`resultado_final`):**

```python
# CRÍTICO: Não pode ter NaN
# Estratégia:
1. Se UCI: usar G1/G2 para estimar G3 ausente
2. Se OULAD: usar média de scores para estimar resultado
3. Fallback: valor médio global (5.0)
```

#### **Casos Especiais**

**Dados Ausentes Estratégicos:**

- Manter NaN informativo para algumas colunas (ex: `uci_alcool_semana`)
- Converter NaN para "Não informado" quando apropriado (ex: `oulad_deficiencia`)

**Tratamento de Outliers:**

- `resultado_final`: clip entre 0-10
- `faltas`: clip entre 0-50
- Valores suspeitos identificados e tratados

## Implementação

### Arquivo Principal: `webapp/src/unificar_datasets.py`

**Funções de Mapeamento:**

1. `mapear_colunas_uci(df_uci)` - Renomeia e transforma colunas UCI
2. `agregar_oulad_por_estudante(dataframes_oulad)` - Agrega OULAD em uma linha por estudante
3. `mapear_colunas_oulad(df_oulad_agregado)` - Renomeia e transforma colunas OULAD
4. `normalizar_target_uci(valor_g3)` - Converte G3 (0-20) para escala 0-10
5. `normalizar_target_oulad(final_result)` - Converte resultado categórico para 0-10
6. `adicionar_coluna_origem(df, origem)` - Adiciona coluna `origem_dado`

**Funções de Tratamento de Dados Ausentes:**

1. `tratar_dados_ausentes(df_unificado)` - Função principal de imputação
2. `imputar_numerica_por_grupo(df, coluna)` - Imputa coluna numérica usando mediana por grupo
3. `imputar_categorica_por_grupo(df, coluna)` - Imputa coluna categórica usando moda por grupo
4. `imputar_numerica_uci(df, coluna)` - Imputa colunas específicas UCI
5. `imputar_numerica_oulad(df, coluna)` - Imputa colunas específicas OULAD
6. `imputar_resultado_final(row)` - Imputa target usando informações auxiliares
7. `tratar_outliers(df)` - Trata outliers após imputação
8. `validar_imputacao(df)` - Valida qualidade da imputação

**Função Principal:**

1. `unificar_datasets()` - Orquestra todo o processo:

   - Carrega dados brutos UCI e OULAD
   - Aplica mapeamentos e transformações
   - Adiciona coluna de origem
   - Concatena DataFrames (pd.concat)
   - **Trata dados ausentes**
   - **Trata outliers**
   - **Valida imputação**
   - Retorna DataFrame unificado

**Função de Salvamento:**

1. `salvar_dataset_unificado(df_unificado, base_path)` - Salva em pickle e CSV

### Script Executável: `gerar_dataset_unificado.py`

Script na raiz do projeto que:

- Importa funções de `webapp/src/unificar_datasets.py`
- Executa unificação
- Salva arquivos
- Exibe estatísticas e validações

## Estrutura do Dataset Unificado

**Colunas Comuns (harmonizadas):**

- `origem_dado`: 'UCI' ou 'OULAD'
- `genero`: Masculino/Feminino
- `idade`: numérico ou faixa
- `regiao`: região geográfica
- `tentativas_anteriores`: número de reprovações/tentativas
- `resultado_final`: 0-10 (normalizado)

**Colunas UCI (com prefixo `uci_`):**

- Total: ~30 colunas específicas
- Todas preenchidas para registros UCI, NaN para OULAD

**Colunas OULAD (com prefixo `oulad_`):**

- Total: ~15 colunas específicas
- Todas preenchidas para registros OULAD, NaN para UCI

**Total estimado:** ~50 colunas

## Saída

**Arquivos gerados:**

- `unified_dataset.pkl` - Dataset unificado em formato pickle (otimizado)
- `unified_dataset.csv` - Dataset unificado em formato CSV (para inspeção)
- Localização: `/home/emanoel/sida/`

**Registros esperados:**

- UCI: ~1000 registros (649 mat + 649 por, alguns duplicados)
- OULAD: ~32,000 estudantes únicos (após agregação)
- Total: ~33,000 registros

## Validação

Script deve exibir:

- ✅ Número de registros por origem
- ✅ Distribuição da coluna `origem_dado`
- ✅ Estatísticas de `resultado_final` (min, max, média, NaN)
- ✅ **Nenhum NaN em `resultado_final`** (crítico para ML)
- ✅ **Distribuição de valores imputados** por origem
- ✅ **Qualidade da imputação** (comparação antes/depois)
- ✅ **Outliers tratados** (valores dentro de faixas esperadas)
- ✅ **Consistência dos dados** após imputação
- ✅ Percentual de valores ausentes por coluna
- ✅ Tipos de dados de cada coluna
- ✅ Tamanho dos arquivos gerados
- ✅ Uso de memória do DataFrame

### To-dos

- [ ] Criar arquivo webapp/src/unificar_datasets.py com estrutura básica e imports
- [ ] Implementar função mapear_colunas_uci() para renomear colunas UCI para português
- [ ] Implementar função agregar_oulad_por_estudante() para agregar múltiplas linhas por estudante
- [ ] Implementar função mapear_colunas_oulad() para renomear colunas OULAD agregadas para português
- [ ] Implementar função adicionar_coluna_origem() para marcar fonte de dados
- [ ] **Implementar função tratar_dados_ausentes() com estratégias por tipo de coluna**
- [ ] **Implementar função imputar_resultado_final() para garantir target sempre preenchido**
- [ ] **Implementar funções imputar_numerica_por_grupo() e imputar_categorica_por_grupo()**
- [ ] **Implementar funções imputar_numerica_uci() e imputar_numerica_oulad() para colunas específicas**
- [ ] **Implementar função tratar_outliers() para valores suspeitos**
- [ ] **Implementar função validar_imputacao() com relatório detalhado**
- [ ] Implementar função unificar_datasets() que orquestra todo o processo de unificação
- [ ] Implementar função salvar_dataset_unificado() para salvar em pickle e CSV
- [ ] Criar script executável gerar_dataset_unificado.py na raiz do projeto
- [ ] **Expandir validações no script executável para incluir métricas de imputação**
- [ ] Executar script e validar dataset unificado (contagem de registros, colunas, tipos)