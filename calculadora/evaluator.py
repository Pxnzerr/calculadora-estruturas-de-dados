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

        # Copia os tokens para não consumir a fila original se for reutilizada
        tokens = postfix_queue.to_list()

        if not tokens:
            raise EvaluationError("Fila de avaliação vazia.")

        for token in tokens:
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

    @property
    def max_stack_depth(self) -> int:
        """Retorna a profundidade máxima atingida pela pilha de operandos durante a avaliação."""
        return self.operand_stack.max_depth
