# StockFlow — Dashboard de Estoque e Faturamento

O **StockFlow** é um sistema completo e local-first desenvolvido em Python, utilizando a biblioteca Streamlit para prover uma interface visual moderna e interativa. Seu objetivo principal é fornecer uma gestão unificada de inventário e caixa para lojas de varejo e vestuário, entregando métricas em tempo real e controle detalhado de variações de produtos (como grades de cores e tamanhos).

Atualmente otimizado e configurado para uma loja com temática esportiva/fitness, ele permite o cadastro rápido de produtos, gerência inteligente de custos e monitoramento dinâmico de performance de vendas.

---

## Índice

- [Funcionalidades Principais](#funcionalidades-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Como Configurar e Rodar o Projeto](#como-configurar-e-rodar-o-projeto)
- [Regras de Negócio e Lógica Automática](#regras-de-negócio-e-lógica-automática)
- [Personalização de Cores e Estilos](#personalização-de-cores-e-estilos)

---

## Funcionalidades Principais

1. **Painel Principal (Dashboard Central)**
   - Exibição de KPIs dinâmicos: Unidades em Estoque, Receita Total, Total de Saídas e Saldo em Caixa atualizado.
   - Gráficos integrados (Plotly) traçando o faturamento dos últimos 7 dias e a evolução contínua do estoque.
   - Alertas visuais automáticos caso o caixa fique negativo ou certos produtos atinjam um limite crítico de estoque.

2. **Gestão Avançada de Produtos**
   - Criação e edição de produtos com dados cruciais: custo variável, preço de compra, preço de venda e cálculo automático de lucro.
   - **Grade de Cores e Tamanhos**: Sistema nativo onde cada produto pode ter variações de cores (com suporte a paleta HEX personalizada) e múltiplos tamanhos (P, M, G, GG, Único).
   - A quantidade macro de estoque do produto é automaticamente sincronizada com a soma total das variações cadastradas.
   - Exclusão via *Soft Delete* (apenas inativa o produto para que históricos de vendas não sejam perdidos).

3. **Movimentação de Estoque e Registro Integrado**
   - Registro de Entradas (Reposição) com lançamento automático de despesa no controle do Caixa.
   - Registro de Saídas (Vendas/Perdas/Devoluções) especificando também tamanho e variação de cor escolhidos. Caso seja uma venda, a receita é atrelada instantaneamente.
   - O Histórico de Movimentações registra quem comprou o que e quando, com fácil acesso na tabela central.

4. **Controle Financeiro (Caixa)**
   - Lançamento manual de despesas eventuais ou receitas diversas.
   - Visão de gráfico rosca/donut comparando o peso das Gastos vs Entradas.
   - Tabela de extrato financeiro filtrável, essencial para o fechamento diário/mensal de caixa.

5. **Relatórios e BI**
   - Visualização de Ranking de Produtos mais vendidos (Top 10).
   - Tabelas e gráficos ressaltando as Categorias com maior Giro de Estoque.
   - Cruzamento de dados de Faturamento vs Data, ótimo para planejamento das melhores épocas de venda no mês.

---

## Tecnologias Utilizadas

| Componente | Tecnologia |
|---|---|
| **Interface Frontend** | [Streamlit](https://streamlit.io/) + CSS customizado para aparência minimalista. |
| **Banco de Dados** | SQLite3 (Integrado perfeitamente para uso local via SQLAlchemy). |
| **Gráficos** | [Plotly Graph Objects e Express](https://plotly.com/python/). |
| **Linguagem Principal** | Python 3.10+ |

---

## Estrutura do Repositório 

```bash
Projeto_dashboard_control/
├── app.py                 # Arquivo base inicial (Roteamento e CSS Root)
├── database.py            # Definição e inicialização de conexão SQL
├── models.py              # Entidades do sistema relacional (ORM)
├── services.py            # Camada de lógica de dados e CRUD principal
├── seed.py                # Script que popula ambiente zero com dados de teste
├── requirements.txt       # Arquivo padrão com dependências
├── .streamlit/
│   └── config.toml        # Sobrescrita de configurações primárias e tipografia
└── views/
    ├── painel.py          # Dashboard Principal (Index)
    ├── produtos.py        # Lista e Cadastros (Matriz de Variações e Cores)
    ├── estoque.py         # Tela de Entradas e Saídas
    ├── caixa.py           # Gestão de Receitas e Despesas do fluxo
    └── relatorios.py      # Business Intelligence e Top Sellers
```

---

## Como Configurar e Rodar o Projeto

**1. Clonando o repositório em sua máquina:**
```bash
git clone <url-do-seu-repositorio>
cd Projeto_dashboard_control
```

**2. Criando o ambiente virtual Python:**
Este passo previne conflitos de versão na sua máquina.
```bash
python3 -m venv venv

# Ativação via Linux/Mac:
source venv/bin/activate
# Ativação via Windows CMD / PowerShell:
# venv\Scripts\activate
```

**3. Instalando as bibliotecas:**
```bash
pip install -r requirements.txt
```

**4. Iniciando a aplicação Streamlit:**
```bash
streamlit run app.py
```
O Steamlit normalmente abrirá sozinho uma aba de navegador ligando na porta configurada (geralmente localhost:8501). Na primeira vez que iniciar o programa, um banco de dados `loja.db` será criado e abastecido com um dataset inteligente de teste.

---

## Regras de Negócio e Lógica Automática

Para manter um padrão corporativo fidedigno, o sistema executa lógicas ocultas essenciais:
- Ao lançar uma Entrada em `estoque.py`, não é preciso lançar o custo do produto no Caixa manualmente. O código já reconhece se foi "Reposição" e injeta em Despesas o montante baseado no Preço de Custo salvo.
- Uma Saída sob a categoria "Venda" vai abater o físico e registrar a entrada de recursos automaticamente no controle financeiro.
- Relacionamentos (como Cor do Produto e Tamanho) são cruciais, as baixas e altas em uma variação repassam para o macro saldo do produto. Se você vendeu 1 camiseta Preta 'M', o Estoque geral do Produto cai 1.
- *Status Colorizado em Tabela:* Quantidade zero resulta no campo "ESGOTADO", permitindo priorizar recompra na visualização da lista.

---

**Licença:** MIT
Desenvolvido em Python para impulsionamento e gerencia local.
