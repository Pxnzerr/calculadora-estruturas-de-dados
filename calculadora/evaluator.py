"""
Módulo de Avaliação: Notação Pós-Fixa (Reverse Polish Notation - RPN)

A Notação Pós-Fixa (RPN) permite avaliar expressões matemáticas sem a necessidade de parênteses
ou regras complexas de precedência durante o cálculo, utilizando uma única Pilha de operandos.

Funcionamento:
1. Percorre os tokens pós-fixos da esquerda para a direita.
2. Se o token for um número, empilha na pilha de operandos.
3. Se for um operador binário, desempilha os dois últimos operandos (b e a),
   aplica a operação (a OP b) e empilha o resultado de volta.
4. Se for um operador unário de negação (u-), desempilha o último operando (a),
   inverte o sinal (-a) e empilha de volta.
5. Ao final, o topo da pilha contém o resultado final da expressão.
"""

from typing import Union
import math
from .stack import Stack
from .queue_ds import Queue
from .tokenizer import Token, TokenType


class EvaluationError(Exception):
    """Exceção base para erros durante o cálculo da expressão."""
    pass


class DivisionByZeroError(EvaluationError):
    """Exceção levantada para divisão ou módulo por zero."""
    pass


class PostfixEvaluator:
    """
    Avaliador de Notação Pós-Fixa (RPN) baseado em Pilha.
    
    Complexidade:
    - Tempo: O(n), onde n é a quantidade de tokens pós-fixos. Cada token é processado em O(1).
    - Espaço: O(n), para armazenar os operandos intermediários na pilha.
    """

    def __init__(self):
        self.operand_stack: Stack[float] = Stack()

    def evaluate(self, postfix_queue: Queue[Token]) -> Union[int, float]:
        """
        Avalia a fila de tokens em notação pós-fixa e retorna o resultado numérico.
        
        Args:
            postfix_queue: Fila contendo os tokens em RPN.
            
        Returns:
            Resultado do cálculo (int se for exato, ou float).
            
        Raises:
            DivisionByZeroError: Se houver divisão ou módulo por zero.
            EvaluationError: Se a expressão estiver matematicamente inválida ou incompleta.
        """
        self.operand_stack.clear()


        if postfix_queue.is_empty():
            raise EvaluationError("Fila de avaliação vazia.")

        for token in postfix_queue:
            if token.type == TokenType.NUMBER:
                try:
                    val = float(token.value)
                    self.operand_stack.push(val)
                except ValueError:
                    raise EvaluationError(f"Valor numérico inválido: '{token.value}'")

            elif token.type == TokenType.UNARY_MINUS or token.value == 'u-':
                if self.operand_stack.is_empty():
                    raise EvaluationError(
                        f"Sintaxe inválida: operando insuficiente para a negação unária."
                    )
                val = self.operand_stack.pop()
                self.operand_stack.push(-val)

            elif token.type == TokenType.OPERATOR:
                if self.operand_stack.size() < 2:
                    raise EvaluationError(
                        f"Sintaxe inválida: operandos insuficientes para o operador '{token.value}'."
                    )

                b = self.operand_stack.pop()
                a = self.operand_stack.pop()
                result = self._apply_operator(a, b, token.value, token.position)
                self.operand_stack.push(result)

            elif token.type == TokenType.FUNCTION:
                if self.operand_stack.is_empty():
                    raise EvaluationError(
                        f"Sintaxe inválida: operando insuficiente para a função '{token.value}'."
                    )
                val = self.operand_stack.pop()
                result = self._apply_function(token.value, val, token.position)
                self.operand_stack.push(result)

            else:
                raise EvaluationError(f"Token inesperado na avaliação pós-fixa: '{token.value}'")

        if self.operand_stack.size() != 1:
            raise EvaluationError(
                f"Expressão inválida: sobraram {self.operand_stack.size()} valores não operados na pilha."
            )

        final_val = self.operand_stack.pop()

        # Retorna int se o número for inteiro exato (ex: 5.0 -> 5)
        if final_val.is_integer():
            return int(final_val)
        return final_val

    def _apply_operator(self, a: float, b: float, op: str, position: int) -> float:
        """Executa a operação matemática correspondente entre a e b."""
        try:
            if op == '+':
                return a + b
            elif op == '-':
                return a - b
            elif op == '*':
                return a * b
            elif op == '/':
                if b == 0:
                    raise DivisionByZeroError(f"Divisão por zero na posição {position + 1}.")
                return a / b
            elif op == '%':
                if b == 0:
                    raise DivisionByZeroError(f"Operação de módulo por zero na posição {position + 1}.")
                return a % b
            elif op == '^':
                if a < 0 and not b.is_integer():
                    raise EvaluationError(
                        f"Potência com base negativa e expoente fracionário resulta em número complexo não suportado."
                    )
                return a ** b
            else:
                raise EvaluationError(f"Operador desconhecido: '{op}'")
        except OverflowError:
            raise EvaluationError(f"Estouro numérico (Overflow) na operação '{a} {op} {b}'.")

    def _apply_function(self, func_name: str, value: float, position: int) -> float:
        """
        Aplica uma função matemática ao valor fornecido.
        
        Funções suportadas: sin, cos, tan, sqrt, log (base 10), ln (natural), abs, ceil, floor.
        
        Args:
            func_name: Nome da função.
            value: Operando da função.
            position: Posição original no texto para mensagens de erro.
            
        Returns:
            Resultado da função aplicada.
            
        Raises:
            EvaluationError: Se o argumento estiver fora do domínio da função.
        """
        try:
            if func_name == 'sin':
                return math.sin(value)
            elif func_name == 'cos':
                return math.cos(value)
            elif func_name == 'tan':
                # Verifica se está próximo de π/2 + kπ (tangente indefinida)
                cos_val = math.cos(value)
                if abs(cos_val) < 1e-15:
                    raise EvaluationError(
                        f"Tangente indefinida para o argumento {value} (próximo de π/2 + kπ)."
                    )
                return math.tan(value)
            elif func_name == 'sqrt':
                if value < 0:
                    raise EvaluationError(
                        f"Raiz quadrada de número negativo não é suportada: sqrt({value})."
                    )
                return math.sqrt(value)
            elif func_name == 'log':
                if value <= 0:
                    raise EvaluationError(
                        f"Logaritmo de número não-positivo não é definido: log({value})."
                    )
                return math.log10(value)
            elif func_name == 'ln':
                if value <= 0:
                    raise EvaluationError(
                        f"Logaritmo natural de número não-positivo não é definido: ln({value})."
                    )
                return math.log(value)
            elif func_name == 'abs':
                return abs(value)
            elif func_name == 'ceil':
                return math.ceil(value)
            elif func_name == 'floor':
                return math.floor(value)
            elif func_name == 'exp':
                return math.exp(value)
            elif func_name == 'round':
                return float(round(value))
            else:
                raise EvaluationError(f"Função desconhecida: '{func_name}'")
        except OverflowError:
            raise EvaluationError(f"Estouro numérico (Overflow) ao calcular {func_name}({value}).")

    @property
    def max_stack_depth(self) -> int:
        """Retorna a profundidade máxima atingida pela pilha de operandos durante a avaliação."""
        return self.operand_stack.max_depth
