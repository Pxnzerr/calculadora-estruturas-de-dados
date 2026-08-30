"""
Módulo de Tokenização (Lexer / Analisador Léxico e Sintático)

Responsável por:
1. Decompor a string de entrada em tokens atômicos (números, operadores, parênteses, funções).
2. Tratar números inteiros e decimais (ponto flutuante, incluindo notação '.5' -> '0.5').
3. Tratar operadores unários de sinal (+ e -) e números negativos.
4. Reconhecer funções matemáticas (sin, cos, sqrt, log, etc.) e constantes (pi, e).
5. Suportar a variável especial 'ans' (último resultado calculado).
6. Validar sintaxe básica (caracteres inválidos, operadores consecutivos inválidos, etc.).
"""

import math
from enum import Enum, auto
from typing import List, Optional
from dataclasses import dataclass


class TokenType(Enum):
    NUMBER = auto()       # 42, 3.14, -5
    OPERATOR = auto()     # +, -, *, /, ^, %
    UNARY_MINUS = auto()  # Unário de negação: u-
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    FUNCTION = auto()     # sin, cos, sqrt, log, ln, tan, abs, ceil, floor


@dataclass
class Token:
    type: TokenType
    value: str
    position: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', pos={self.position})"


class TokenizerError(Exception):
    """Exceção levantada para erros léxicos ou de sintaxe na tokenização."""
    def __init__(self, message: str, position: Optional[int] = None):
        self.position = position
        if position is not None:
            super().__init__(f"Erro de Sintaxe na posição {position + 1}: {message}")
        else:
            super().__init__(f"Erro de Sintaxe: {message}")


class Tokenizer:
    """
    Analisador léxico que converte uma expressão matemática em uma lista de Tokens.
    
    Complexidade:
    - Tempo: O(n), onde n é o comprimento da string de entrada.
    - Espaço: O(n), para armazenar os tokens gerados.
    """

    OPERATORS = {'+', '-', '*', '/', '^', '%'}

    FUNCTIONS = {'sin', 'cos', 'tan', 'sqrt', 'log', 'ln', 'abs', 'ceil', 'floor', 'exp', 'round'}

    CONSTANTS = {
        'pi': str(math.pi),
        'e': str(math.e),
        'tau': str(getattr(math, 'tau', 2 * math.pi)),
        'phi': '1.618033988749895',
    }

    def __init__(self, expression: str, ans_value: Optional[float] = None):
        self.expression: str = expression
        self.cursor: int = 0
        self.length: int = len(expression)
        self.ans_value: Optional[float] = ans_value

    def tokenize(self) -> List[Token]:
        """
        Executa a análise léxica completa e validações sintáticas estruturais.
        
        Returns:
            Lista de objetos Token.
            
        Raises:
            TokenizerError: Se encontrar caracteres ilegais ou formato inválido.
        """
        if not self.expression or self.expression.strip() == "":
            raise TokenizerError("A expressão fornecida está vazia.")

        raw_tokens: List[Token] = []

        while self.cursor < self.length:
            char = self.expression[self.cursor]

            # 1. Ignorar espaços em branco
            if char.isspace():
                self.cursor += 1
                continue

            # 2. Números (inteiros e decimais)
            if char.isdigit() or (char == '.' and self._is_decimal_start()):
                token = self._read_number()
                raw_tokens.append(token)
                continue

            # 3. Identificadores: funções (sin, cos...), constantes (pi, e) e ans
            if char.isalpha() or char == '_':
                token = self._read_identifier()
                raw_tokens.append(token)
                continue

            # 4. Parênteses
            if char == '(':
                raw_tokens.append(Token(TokenType.LPAREN, '(', self.cursor))
                self.cursor += 1
                continue
            elif char == ')':
                raw_tokens.append(Token(TokenType.RPAREN, ')', self.cursor))
                self.cursor += 1
                continue

            # 5. Operadores
            if char in self.OPERATORS:
                raw_tokens.append(Token(TokenType.OPERATOR, char, self.cursor))
                self.cursor += 1
                continue

            # 6. Caractere desconhecido
            raise TokenizerError(f"Caractere inválido '{char}'", self.cursor)

        # Trata unários e valida a sequência
        normalized_tokens = self._handle_unary_operators(raw_tokens)
        self._validate_syntax(normalized_tokens)
        return normalized_tokens

    def _is_decimal_start(self) -> bool:
        """Verifica se um ponto '.' é o início de um número decimal válido (ex: '.5')."""
        if self.cursor + 1 < self.length and self.expression[self.cursor + 1].isdigit():
            return True
        return False

    def _read_number(self) -> Token:
        """Lê um número inteiro ou decimal completo a partir do cursor atual."""
        start_pos = self.cursor
        has_dot = False
        num_str = ""

        while self.cursor < self.length:
            char = self.expression[self.cursor]
            if char.isdigit():
                num_str += char
                self.cursor += 1
            elif char == '.':
                if has_dot:
                    raise TokenizerError("Número decimal com múltiplos pontos flutuantes.", self.cursor)
                has_dot = True
                num_str += char
                self.cursor += 1
            else:
                break

        if num_str == ".":
            raise TokenizerError("Ponto decimal isolado sem dígitos.", start_pos)

        # Normaliza decimais sem zero à esquerda (ex: '.5' -> '0.5')
        if num_str.startswith('.'):
            num_str = '0' + num_str

        return Token(TokenType.NUMBER, num_str, start_pos)

    def _read_identifier(self) -> Token:
        """
        Lê um identificador alfabético (função, constante ou 'ans') a partir do cursor.
        
        Funções suportadas: sin, cos, tan, sqrt, log, ln, abs, ceil, floor
        Constantes suportadas: pi, e
        Variável especial: ans (último resultado)
        """
        start_pos = self.cursor
        ident = ""
        while self.cursor < self.length and (self.expression[self.cursor].isalnum() or self.expression[self.cursor] == '_'):
            ident += self.expression[self.cursor]
            self.cursor += 1

        ident_lower = ident.lower()

        # Funções matemáticas
        if ident_lower in self.FUNCTIONS:
            return Token(TokenType.FUNCTION, ident_lower, start_pos)

        # Constantes matemáticas
        if ident_lower in self.CONSTANTS:
            return Token(TokenType.NUMBER, self.CONSTANTS[ident_lower], start_pos)

        # Variável especial 'ans'
        if ident_lower == 'ans':
            if self.ans_value is not None:
                return Token(TokenType.NUMBER, str(self.ans_value), start_pos)
            else:
                raise TokenizerError(
                    "Variável 'ans' utilizada, mas nenhum resultado anterior disponível.",
                    start_pos
                )

        raise TokenizerError(f"Identificador desconhecido '{ident}'", start_pos)

    def _handle_unary_operators(self, tokens: List[Token]) -> List[Token]:
        """
        Normaliza operadores unários de sinal (+ e -).
        
        Um operador '+' ou '-' é considerado unário se:
        - Estiver no início da expressão (ex: -5 + 2)
        - Estiver logo após um '(' (ex: (-5) * 2)
        - Estiver logo após outro operador (ex: 3 * -2)
        
        Estratégia algorítmica:
        - Se for unário '-', converte para '0' e '-' ou Token de negação unária / número negativo.
        - Se for unário '+', ignora.
        """
        result: List[Token] = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            is_unary = False
            if token.type == TokenType.OPERATOR and token.value in ('+', '-'):
                if i == 0:
                    is_unary = True
                elif tokens[i - 1].type in (TokenType.OPERATOR, TokenType.LPAREN, TokenType.UNARY_MINUS):
                    is_unary = True

            if is_unary:
                if token.value == '-':
                    # Se o próximo token for um número simples, anexa o sinal diretamente ao número
                    if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.NUMBER:
                        next_tok = tokens[i + 1]
                        result.append(Token(TokenType.NUMBER, f"-{next_tok.value}", token.position))
                        i += 2
                        continue
                    else:
                        # Se for unário '-' antes de parêntese (ex: -(3 + 4)), usa UNARY_MINUS 'u-'
                        result.append(Token(TokenType.UNARY_MINUS, 'u-', token.position))
                        i += 1
                        continue
                elif token.value == '+':
                    # Unário positivo não altera valor, podemos ignorar
                    i += 1
                    continue
            else:
                result.append(token)
                i += 1

        return result

    def _validate_syntax(self, tokens: List[Token]) -> None:
        """
        Valida a coerência da sequência de tokens gerada.
        """
        if not tokens:
            raise TokenizerError("Nenhum token válido encontrado na expressão.")

        # 1. Checagem inicial
        if tokens[0].type == TokenType.OPERATOR:
            raise TokenizerError(f"A expressão não pode iniciar com o operador '{tokens[0].value}'.", tokens[0].position)

        # 2. Checagem final
        if tokens[-1].type in (TokenType.OPERATOR, TokenType.UNARY_MINUS):
            raise TokenizerError(f"A expressão não pode terminar com operador.", tokens[-1].position)

        for i in range(len(tokens) - 1):
            curr_tok = tokens[i]
            next_tok = tokens[i + 1]

            # Dois operadores binários seguidos
            if curr_tok.type == TokenType.OPERATOR and next_tok.type == TokenType.OPERATOR:
                raise TokenizerError(
                    f"Operadores consecutivos inválidos '{curr_tok.value}' e '{next_tok.value}'.",
                    next_tok.position
                )

            # Parêntese vazio '()'
            if curr_tok.type == TokenType.LPAREN and next_tok.type == TokenType.RPAREN:
                raise TokenizerError("Parênteses vazios '()' não são permitidos.", curr_tok.position)

            # Operador binário logo após '(' (ex: '(* 2)')
            if curr_tok.type == TokenType.LPAREN and next_tok.type == TokenType.OPERATOR:
                raise TokenizerError(
                    f"Operador '{next_tok.value}' inválido imediatamente após '('.",
                    next_tok.position
                )

            # Operador antes de ')' (ex: '(2 *)')
            if curr_tok.type in (TokenType.OPERATOR, TokenType.UNARY_MINUS) and next_tok.type == TokenType.RPAREN:
                raise TokenizerError(
                    f"Operador '{curr_tok.value}' inválido imediatamente antes de ')'.",
                    curr_tok.position
                )

            # Número seguido diretamente de '(' sem operador (ex: '5(2)') — mas permitir FUNCTION seguido de '('
            if curr_tok.type == TokenType.NUMBER and next_tok.type == TokenType.LPAREN:
                raise TokenizerError(
                    "Falta de operador explícito entre número e parêntese.",
                    next_tok.position
                )

            # Função DEVE ser seguida de '('
            if curr_tok.type == TokenType.FUNCTION and next_tok.type != TokenType.LPAREN:
                raise TokenizerError(
                    f"Função '{curr_tok.value}' deve ser seguida de '('.",
                    curr_tok.position
                )

            # ')' seguido diretamente de número, '(' ou função (ex: '(2)3' ou '(2)(3)')
            if curr_tok.type == TokenType.RPAREN and next_tok.type in (TokenType.NUMBER, TokenType.LPAREN, TokenType.FUNCTION):
                raise TokenizerError(
                    "Falta de operador explícito após fechamento de parêntese.",
                    next_tok.position
                )
