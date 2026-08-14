"""
Módulo de Análise de Complexidade de Algoritmos e Estruturas de Dados

Responsável por:
1. Extrair métricas estruturais da expressão (tokens, operandos, operadores, parênteses).
2. Monitorar a profundidade máxima de pilha atingida nas fases de conversão e avaliação.
3. Explicar e documentar a complexidade assintótica de Tempo O(n) e Espaço O(n).
4. Gerar relatórios de complexidade formatados para o usuário (CLI e GUI).
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from .tokenizer import Token, TokenType
from .queue_ds import Queue


@dataclass
class ComplexityReport:
    """Relatório estruturado com as métricas de análise de complexidade da expressão."""
    expression_raw: str
    total_tokens: int
    num_operands: int
    num_operators: int
    num_parentheses: int
    shunting_yard_max_depth: int
    evaluation_max_depth: int
    overall_max_stack_depth: int
    time_complexity_theoretical: str = "O(n) - Linear"
    space_complexity_theoretical: str = "O(n) - Linear"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "expressao": self.expression_raw,
            "total_tokens": self.total_tokens,
            "operandos": self.num_operands,
            "operadores": self.num_operators,
            "parenteses": self.num_parentheses,
            "profundidade_max_shunting_yard": self.shunting_yard_max_depth,
            "profundidade_max_avaliacao": self.evaluation_max_depth,
            "profundidade_max_geral": self.overall_max_stack_depth,
            "complexidade_tempo": self.time_complexity_theoretical,
            "complexidade_espaco": self.space_complexity_theoretical,
        }

    def format_summary(self) -> str:
        """Gera uma visualização tabular amigável e segura para todos os terminais (UTF-8 e Windows CP1252)."""
        sep = "+" + "-" * 60 + "+"
        lines = [
            sep,
            "|                 ANALISE DE COMPLEXIDADE                    |",
            sep,
            f"|  * Expressao Original:        {self.expression_raw:<28} |",
            f"|  * Total de Tokens (n):       {self.total_tokens:<28} |",
            f"|  * Operandos (Numeros):       {self.num_operands:<28} |",
            f"|  * Operadores:                {self.num_operators:<28} |",
            f"|  * Parenteses:                {self.num_parentheses:<28} |",
            sep,
            f"|  * Profundidade Pilha (Conv): {self.shunting_yard_max_depth:<28} |",
            f"|  * Profundidade Pilha (Eval): {self.evaluation_max_depth:<28} |",
            f"|  * Pico Maximo da Pilha:      {self.overall_max_stack_depth:<28} |",
            sep,
            f"|  * Complexidade de Tempo:     {self.time_complexity_theoretical:<28} |",
            f"|  * Complexidade de Espaco:    {self.space_complexity_theoretical:<28} |",
            sep,
        ]
        return "\n".join(lines)


class ComplexityAnalyzer:
    """
    Analisador de métricas e complexidade para expressões matemáticas.
    """

    @staticmethod
    def analyze(
        expression_raw: str,
        tokens: List[Token],
        shunting_max_depth: int,
        eval_max_depth: int
    ) -> ComplexityReport:
        """
        Analisa os tokens e gera o relatório completo de complexidade.
        
        Args:
            expression_raw: A string original digitada pelo usuário.
            tokens: Lista de tokens resultantes da tokenização.
            shunting_max_depth: Profundidade máxima de pilha durante o Shunting Yard.
            eval_max_depth: Profundidade máxima de pilha durante a avaliação RPN.
            
        Returns:
            Instância de ComplexityReport.
        """
        num_operands = 0
        num_operators = 0
        num_parentheses = 0

        for token in tokens:
            if token.type == TokenType.NUMBER:
                num_operands += 1
            elif token.type in (TokenType.OPERATOR, TokenType.UNARY_MINUS):
                num_operators += 1
            elif token.type in (TokenType.LPAREN, TokenType.RPAREN):
                num_parentheses += 1

        overall_max_depth = max(shunting_max_depth, eval_max_depth)

        return ComplexityReport(
            expression_raw=expression_raw,
            total_tokens=len(tokens),
            num_operands=num_operands,
            num_operators=num_operators,
            num_parentheses=num_parentheses,
            shunting_yard_max_depth=shunting_max_depth,
            evaluation_max_depth=eval_max_depth,
            overall_max_stack_depth=overall_max_depth,
            time_complexity_theoretical="O(n) - Linear",
            space_complexity_theoretical="O(n) - Linear"
        )
