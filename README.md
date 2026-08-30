# Calculadora Algorítmica em Python (Pilha, Fila & Shunting Yard)

Uma calculadora didática e de alto desempenho desenvolvida em Python, demonstrando conceitos fundamentais de **Estruturas de Dados** (Pilha e Fila), **Análise de Algoritmos**, **Parsing Léxico/Sintático**, conversão de expressões via algoritmo **Shunting Yard de Dijkstra**, avaliação de **Notação Pós-Fixa (RPN)** e **Métricas de Complexidade Assintótica e Empírica**.

---

## 🎯 Conceitos Fundamentais Demonstrados

### 1. Pilha (Stack) — LIFO (Last-In, First-Out)
- **Onde é usada**:
  1. **Shunting Yard**: Armazenamento temporário de operadores (`+`, `-`, `*`, `/`, `^`, `%`) e controle de precedência e aninhamento de parênteses.
  2. **Avaliação Pós-Fixa (RPN)**: Pilha de operandos para armazenar valores numéricos imediatos e resultados de sub-expressões.
  3. **Validação de Parênteses**: Detecção de desbalanceamento e aninhamentos inválidos.
- **Complexidade**:
  - `push`, `pop`, `peek`, `is_empty`, `size`: $O(1)$ constante amortizado.
  - Espaço: $O(n)$.

### 2. Fila (Queue) — FIFO (First-In, First-Out)
- **Onde é usada**:
  - Armazenamento do fluxo de saída de tokens gerados pelo algoritmo Shunting Yard na ordem linear exata em que devem ser consumidos pelo avaliador RPN.
- **Complexidade**:
  - `enqueue`, `dequeue`, `peek`, `is_empty`, `size`: $O(1)$ garantido (usando `collections.deque`).
  - Espaço: $O(n)$.

### 3. Algoritmo Shunting Yard de Dijkstra
- Converte a notação **Infixa** (ex: `2 + 3 * 4` ou `((2 + 3) * 4) - 1`) para a **Notação Polonesa Reversa (RPN / Pós-Fixa)** (ex: `2 3 4 * +` ou `2 3 + 4 * 1 -`).
- **Suporte a Funções**: Funções matemáticas (`sin`, `cos`, `sqrt`, etc.) são empilhadas e desempilhadas corretamente seguindo as regras do Shunting Yard.
- **Tabela de Precedência e Associatividade**:
  | Operador | Operação | Precedência | Associatividade |
  | :--- | :--- | :---: | :---: |
  | `^` | Potenciação | 3 | À Direita |
  | `*`, `/`, `%` | Mult / Div / Módulo | 2 | À Esquerda |
  | `+`, `-` | Soma / Subtração | 1 | À Esquerda |

### 4. Análise de Complexidade
- **Complexidade de Tempo**: $O(n)$ linear, onde $n$ é a quantidade total de tokens.
  - Cada token é lido uma vez pelo lexer, empilhado no máximo uma vez no Shunting Yard e processado no avaliador RPN em $O(1)$.
- **Complexidade de Espaço**: $O(n)$ linear, proporcional ao número de tokens mantidos nas estruturas lineares.
- **Métricas Empíricas**:
  - Contagem de operandos, operadores e parênteses.
  - Rastreamento da **profundidade máxima da pilha** (pico de memória atingido) nas fases de conversão e avaliação.

---

## 📁 Estrutura do Projeto

```
Calc/
├── calculadora/
│   ├── __init__.py          # Facade central e CalculatorEngine
│   ├── stack.py             # Classe Stack genérica com métricas
│   ├── queue_ds.py          # Classe Queue genérica com O(1)
│   ├── tokenizer.py         # Lexer, normalizador de unários, funções, constantes e validador
│   ├── converter.py         # Algoritmo Shunting Yard de Dijkstra (Infixa -> Pós-Fixa)
│   ├── evaluator.py         # Avaliador de Notação Pós-Fixa (RPN) com funções matemáticas
│   ├── analyzer.py          # Analisador de métricas e complexidade
│   ├── ui.py                # Interfaces: CLI interativa e GUI Tkinter
│   └── main.py              # Ponto de entrada com seleção CLI/GUI/eval
├── tests/
│   ├── __init__.py
│   └── test_calculator.py   # Suíte de testes unitários abrangente (81 testes)
├── main.py                  # Executável raiz
└── README.md                # Documentação técnica e guia de uso
```

---

## 🚀 Como Executar

### 1. Interface de Linha de Comando (CLI Interativa)
Execute o terminal interativo:
```bash
python main.py
# ou
python -m calculadora.main --cli
```

Comandos especiais disponíveis na CLI:
- `:help` ou `:h` — Exibe o guia de operadores, funções e exemplos.
- `:history` ou `:hist` — Exibe as últimas 10 operações realizadas.
- `:clear` ou `:c` — Limpa o histórico da sessão.
- `:export [caminho]` — Exporta o histórico para um arquivo de texto (padrão: `historico_calculadora.txt`).
- `:exit` ou `:q` — Encerra a aplicação.

### 2. Interface Gráfica (GUI Tkinter)
Para iniciar a interface visual moderna:
```bash
python main.py --gui
```
Recursos da GUI:
- Campo de expressão com suporte à tecla `<Enter>`.
- Painel de resultado instantâneo e notação RPN.
- Painel de análise de complexidade em tempo real.
- Histórico com as últimas 10 operações e atalho `Ctrl+L` para limpar.
- **Botão "Exportar"** para salvar o histórico em arquivo `.txt`.

### 3. Modo de Avaliação Direta (One-Shot CLI)
```bash
python main.py -e "(3 + 4) * 2 ^ 3"
```

---

## 🧮 Funções Matemáticas Suportadas

A calculadora suporta funções matemáticas de uso comum. Todas recebem um argumento entre parênteses:

| Função | Descrição | Exemplo | Resultado |
| :--- | :--- | :--- | :---: |
| `sin(x)` | Seno (x em radianos) | `sin(pi / 2)` | `1.0` |
| `cos(x)` | Cosseno (x em radianos) | `cos(0)` | `1.0` |
| `tan(x)` | Tangente (x em radianos) | `tan(0)` | `0.0` |
| `sqrt(x)` | Raiz quadrada | `sqrt(16)` | `4` |
| `exp(x)` | Exponencial ($e^x$) | `exp(0)` | `1.0` |
| `log(x)` | Logaritmo base 10 | `log(100)` | `2.0` |
| `ln(x)` | Logaritmo natural (base *e*) | `ln(e)` | `1.0` |
| `abs(x)` | Valor absoluto | `abs(-42)` | `42` |
| `round(x)` | Arredondamento ao inteiro mais próximo | `round(3.7)` | `4` |
| `ceil(x)` | Arredondamento para cima | `ceil(3.2)` | `4` |
| `floor(x)` | Arredondamento para baixo | `floor(3.9)` | `3` |

Funções podem ser **aninhadas**: `sqrt(abs(-25))` → `5`

---

## 🔢 Constantes e Variável Especial

| Nome | Valor | Descrição |
| :--- | :--- | :--- |
| `pi` | `3.141592653589793` | Constante π (pi) |
| `e` | `2.718281828459045` | Constante de Euler |
| `tau` | `6.283185307179586` | Constante τ ($2\pi$) |
| `phi` | `1.618033988749895` | Proporção Áurea ($\phi$) |
| `ans` | *(último resultado)* | Retorna o resultado do cálculo anterior |

**Exemplos com constantes e `ans`:**
```
> 2 * pi
→ 6.283185307179586

> sin(pi / 2)
→ 1.0

> ans * 10
→ 10.0
```

---

## 🧪 Executando os Testes Unitários

Para rodar a suíte completa de **81 testes** automatizados com `unittest`:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 💡 Exemplos de Expressões Suportadas

| Expressão Infixa | Notação Pós-Fixa (RPN) | Resultado | Observação |
| :--- | :--- | :---: | :--- |
| `2 + 3` | `2 3 +` | `5` | Adição básica |
| `10 - 5 * 2` | `10 5 2 * -` | `0` | Precedência da multiplicação |
| `(3 + 4) * 2` | `3 4 + 2 *` | `14` | Parênteses alterando precedência |
| `16 / 4 + 2` | `16 4 / 2 +` | `6` | Divisão e soma |
| `2 ^ 3 + 1` | `2 3 ^ 1 +` | `9` | Potenciação com maior precedência |
| `2 ^ 3 ^ 2` | `2 3 2 ^ ^` | `512` | Associatividade à direita da potência ($2^{3^2} = 2^9$) |
| `(10 + 5) / 3` | `10 5 + 3 /` | `5` | Divisão inteira exata |
| `100 % 7` | `100 7 %` | `2` | Operador de módulo |
| `((2 + 3) * 4) - 1` | `2 3 + 4 * 1 -` | `19` | Parênteses aninhados |
| `-5 + 3` | `0 5 - 3 +` | `-2` | Operador unário de sinal negativo |
| `3.5 * 2 + 0.5` | `3.5 2 * 0.5 +` | `7.5` | Números de ponto flutuante (decimais) |
| `sqrt(16)` | `16 sqrt` | `4` | Função raiz quadrada |
| `sin(pi / 2)` | `pi 2 / sin` | `1.0` | Seno com constante π |
| `ln(e)` | `e ln` | `1.0` | Logaritmo natural da constante *e* |
| `log(100)` | `100 log` | `2.0` | Logaritmo base 10 |
| `sqrt(abs(-25))` | `-25 abs sqrt` | `5` | Funções aninhadas |
| `ceil(3.2) + floor(3.9)` | `3.2 ceil 3.9 floor +` | `7` | Arredondamento |

---

## 🛡️ Tratamento de Erros e Casos Extremos

A calculadora possui validação em múltiplas camadas:
1. **Erros Léxicos**: Caracteres ilegais, múltiplos pontos decimais em um número (`3.14.15`), identificadores desconhecidos.
2. **Erros de Sintaxe**: Operadores consecutivos inválidos (`2 ++ 3`), parênteses vazios `()`, operador no início ou fim inválido, função sem parênteses (`sin 3`).
3. **Parênteses Desbalanceados**: `(` sem fechamento ou `)` órfão com indicação da posição exata.
4. **Erros Aritméticos**: Divisão por zero (`x / 0`), módulo por zero (`x % 0`), base negativa com expoente fracionário e overflow numérico.
5. **Erros de Domínio**: Raiz quadrada de negativo (`sqrt(-4)`), logaritmo de zero ou negativo (`log(0)`, `ln(-1)`), tangente indefinida.
6. **Variável `ans` indisponível**: Uso de `ans` sem cálculo anterior.

---

## 👤 Autor

Arthur Clark Francisco
