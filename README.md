# StockFlow — Analytics Operacional de Estoque, Margem e Fluxo de Caixa

> *Local-first Business Intelligence & Inventory Analytics dashboard built with Python, Streamlit, Plotly, SQLAlchemy, and SQLite.*

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Analytics_App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-Relational_DB-003B57?style=flat-square&logo=sqlite&logoColor=white)

---

## Contexto de Negócio

Pequenos e médios varejistas frequentemente controlam entradas de mercadoria e fluxo financeiro em planilhas desconectadas, dificultando a leitura de **giro por categoria**, **ruptura de grade (cor/tamanho)** e **impacto imediato das reposições no caixa**.

O **StockFlow** integra um modelo relacional transacional (`SQLAlchemy + SQLite`) a painéis visuais interativos (`Streamlit + Plotly`) para transformar movimentações operacionais em indicadores de decisão comercial em tempo real.

---

## Indicadores (KPIs) e Módulos Analíticos

1. **Painel Executivo (`views/painel.py`)**
   - KPIs consolidados em tempo real: **Unidades em Estoque**, **Receita Potencial Estimada**, **Custo Imobilizado** e **Saldo de Caixa**.
   - Alertas visuais automáticos de **ruptura (`ESGOTADO`)** e estoque crítico para priorização de recompra.
2. **Business Intelligence & Curva de Vendas (`views/relatorios.py`)**
   - Ranking de *Top Sellers* e categorias com maior **Giro de Estoque**.
   - Série temporal de **Faturamento vs. Período** em gráficos interativos `Plotly` para análise de sazonalidade.
3. **Modelagem de Grade e Conciliação Automática (`services.py`, `models.py`)**
   - Controle granular por matriz de variações (ex.: cor e tamanho) sincronizado automaticamente com o saldo consolidado do produto.
   - **Regra contábil integrada:** entradas classificadas como *Reposição* lançam automaticamente a despesa correspondente pelo preço de custo no caixa; saídas por *Venda* abatem a grade física e registram a receita líquida.

---

## Estrutura do Repositório

```text
StockFLow/
├── app.py                 # Ponto de entrada, roteamento e layout Streamlit
├── database.py            # Conexão relacional SQLite via SQLAlchemy
├── models.py              # Entidades relacionais (Produtos, Variações, Movimentações, Caixa)
├── services.py            # Regras de negócio, cálculo de KPIs e conciliação estoque-caixa
├── seed.py                # Carga inicial determinística para demonstração imediata
├── requirements.txt       # Dependências do projeto
├── .streamlit/
│   └── config.toml        # Tema visual e tipografia
└── views/
    ├── painel.py          # Visão executiva de KPIs
    ├── produtos.py        # Catálogo e matriz de variações
    ├── estoque.py         # Movimentações de entrada e saída
    ├── caixa.py           # Demonstrativo de receitas e despesas
    └── relatorios.py      # Análises de giro, faturamento e Top Sellers
```

---

## Como Executar Localmente

```bash
git clone https://github.com/WnMoura/StockFLow.git
cd StockFLow

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Na primeira execução, `seed.py` inicializa automaticamente o banco `loja.db` com uma massa de dados demonstrativa para exploração imediata dos dashboards em `http://localhost:8501`.

---

## Stack Utilizada

| Componente | Tecnologia |
| :--- | :--- |
| Linguagem | `Python 3.10+` |
| Visualização & UI | `Streamlit`, `Plotly Express`, `Plotly Graph Objects` |
| Persistência & ORM | `SQLite3`, `SQLAlchemy` |

**Licença:** MIT
