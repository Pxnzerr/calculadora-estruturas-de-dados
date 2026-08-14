"""
Módulo de Conversão: Notação Infixa para Pós-Fixa (Shunting Yard de Dijkstra)

O Algoritmo Shunting Yard foi inventado por Edsger Dijkstra para converter expressões
matemáticas da notação infixa comum (ex: 3 + 4 * 2) para a Notação Polonesa Reversa
(RPN / Pós-Fixa, ex: 3 4 2 * +), eliminando a necessidade de parênteses e ambiguidades
de precedência.

Estruturas de Dados Utilizadas:
- Pilha (Stack): Armazena operadores temporariamente e gerencia a precedência e aninhamento de parênteses (LIFO).
- Fila (Queue): Armazena o fluxo de saída da expressão pós-fixa na ordem correta de execução (FIFO).
"""

from typing import List, Dict, NamedTuple
from .stack import Stack
from .queue_ds import Queue
from .tokenizer import Token, TokenType


class OperatorInfo(NamedTuple):
    precedence: int
    is_right_associative: bool


class ShuntingYardError(Exception):
    """Exceção levantada para erros durante a conversão infixa -> pós-fixa."""
    pass


class MismatchedParenthesesError(ShuntingYardError):
    """Exceção levantada quando parênteses não estão devidamente balanceados."""
    pass


class InfixToPostfixConverter:
    """
    Conversor de Notação Infixa para Notação Pós-Fixa utilizando o Algoritmo Shunting Yard.
    
    Complexidade:
    - Tempo: O(n), cada token é lido uma vez, empilhado no máximo uma vez e desenfileirado no máximo uma vez.
    - Espaço: O(n), para a pilha de operadores e a fila de saída.
    """

    OPERATORS_CONFIG: Dict[str, OperatorInfo] = {
        'u-': OperatorInfo(precedence=4, is_right_associative=True),
        '^': OperatorInfo(precedence=3, is_right_associative=True),
        '*': OperatorInfo(precedence=2, is_right_associative=False),
        '/': OperatorInfo(precedence=2, is_right_associative=False),
        '%': OperatorInfo(precedence=2, is_right_associative=False),
        '+': OperatorInfo(precedence=1, is_right_associative=False),
        '-': OperatorInfo(precedence=1, is_right_associative=False),
    }

    def __init__(self):
        self.operator_stack: Stack[Token] = Stack()
        self.output_queue: Queue[Token] = Queue()

    def convert(self, tokens: List[Token]) -> Queue[Token]:
        """
        Executa a conversão dos tokens infixos para uma fila de tokens pós-fixos.
        
        Args:
            tokens: Lista ordenada de Tokens infixos.
            
        Returns:
            Fila contendo os tokens em Notação Pós-Fixa (RPN).
            
        Raises:
            MismatchedParenthesesError: Se houver parênteses não correspondentes.
            ShuntingYardError: Se ocorrer erro inesperado no parsing.
        """
        self.operator_stack.clear()
        self.output_queue.clear()

        for token in tokens:
            # 1. Se o token for um número, envia diretamente para a fila de saída
            if token.type == TokenType.NUMBER:
                self.output_queue.enqueue(token)

            # 2. Se for um operador (binário ou unário)
            elif token.type in (TokenType.OPERATOR, TokenType.UNARY_MINUS):
                o1_info = self.OPERATORS_CONFIG.get(token.value)
                if not o1_info:
                    raise ShuntingYardError(f"Operador desconhecido: '{token.value}'")

                while not self.operator_stack.is_empty():
                    top_token = self.operator_stack.peek()

                    # Interrompe se o topo da pilha for '('
                    if top_token.type == TokenType.LPAREN:
                        break

                    o2_info = self.OPERATORS_CONFIG.get(top_token.value)
                    if not o2_info:
                        break

                    # Regra de Dijkstra:
                    # Desempilhar o2 se:
                    # (o2 tem maior precedência que o1) OU
                    # (o2 tem mesma precedência E o1 é associativo à esquerda)
                    has_greater_prec = o2_info.precedence > o1_info.precedence
                    has_equal_prec_left = (o2_info.precedence == o1_info.precedence and not o1_info.is_right_associative)

                    if has_greater_prec or has_equal_prec_left:
                        self.output_queue.enqueue(self.operator_stack.pop())
                    else:
                        break

                self.operator_stack.push(token)

            # 3. Se for parêntese de abertura '(', empilha
            elif token.type == TokenType.LPAREN:
                self.operator_stack.push(token)

            # 4. Se for parêntese de fechamento ')'
            elif token.type == TokenType.RPAREN:
                matched_lparen = False
                while not self.operator_stack.is_empty():
                    popped = self.operator_stack.pop()
                    if popped.type == TokenType.LPAREN:
                        matched_lparen = True
                        break
                    self.output_queue.enqueue(popped)

                if not matched_lparen:
                    raise MismatchedParenthesesError(
                        f"Parênteses desbalanceados: ')' sem correspondente na posição {token.position + 1}."
                    )

        # 5. Esvazia o restante da pilha de operadores para a fila de saída
        while not self.operator_stack.is_empty():
            remaining_token = self.operator_stack.pop()
            if remaining_token.type == TokenType.LPAREN:
                raise MismatchedParenthesesError(
                    f"Parênteses desbalanceados: '(' não foi fechado (posição {remaining_token.position + 1})."
                )
            self.output_queue.enqueue(remaining_token)

        return self.output_queue

    @property
    def max_stack_depth(self) -> int:
        """Retorna a profundidade máxima atingida pela pilha de operadores durante a conversão."""
        return self.operator_stack.max_depth
