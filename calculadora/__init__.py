"""
Pacote Calculadora de Estruturas de Dados e Análise de Algoritmos.
"""

from typing import List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

from .stack import Stack
from .queue_ds import Queue
from .tokenizer import Tokenizer, Token, TokenType, TokenizerError
from .converter import InfixToPostfixConverter, ShuntingYardError, MismatchedParenthesesError
from .evaluator import PostfixEvaluator, EvaluationError, DivisionByZeroError
from .analyzer import ComplexityAnalyzer, ComplexityReport


@dataclass
class CalculationResult:
    """Resultado completo de uma operação de cálculo."""
    expression: str
    postfix_expression: str
    result: Optional[Union[int, float]]
    complexity: Optional[ComplexityReport]
    timestamp: datetime
    error: Optional[str] = None


class CalculatorEngine:
    """
    Motor central que orquestra a análise léxica, conversão Shunting Yard,
    avaliação pós-fixa e métricas de complexidade, mantendo o histórico de operações.
    """

    def __init__(self, max_history: int = 10):
        self.tokenizer_cls = Tokenizer
        self.converter = InfixToPostfixConverter()
        self.evaluator = PostfixEvaluator()
        self.max_history = max_history
        self._history: List[CalculationResult] = []

    def calculate(self, expression_str: str) -> CalculationResult:
        """
        Processa uma expressão matemática completa de ponta a ponta.
        
        Args:
            expression_str: String contendo a expressão infixa.
            
        Returns:
            CalculationResult com o resultado numérico, RPN, relatório de complexidade ou erro.
        """
        now = datetime.now()
        try:
            # 1. Tokenização / Análise Léxica e Sintática
            tokenizer = self.tokenizer_cls(expression_str)
            tokens = tokenizer.tokenize()

            # 2. Conversão Infixa -> Pós-Fixa (Shunting Yard)
            postfix_queue = self.converter.convert(tokens)
            postfix_str = " ".join(t.value for t in postfix_queue.to_list())

            # 3. Avaliação da Notação Pós-Fixa (RPN)
            result_val = self.evaluator.evaluate(postfix_queue)

            # 4. Análise de Complexidade e Métricas
            complexity = ComplexityAnalyzer.analyze(
                expression_raw=expression_str,
                tokens=tokens,
                shunting_max_depth=self.converter.max_stack_depth,
                eval_max_depth=self.evaluator.max_stack_depth
            )

            calc_result = CalculationResult(
                expression=expression_str,
                postfix_expression=postfix_str,
                result=result_val,
                complexity=complexity,
                timestamp=now,
                error=None
            )

            self._add_to_history(calc_result)
            return calc_result

        except (TokenizerError, ShuntingYardError, EvaluationError) as err:
            err_result = CalculationResult(
                expression=expression_str,
                postfix_expression="",
                result=None,
                complexity=None,
                timestamp=now,
                error=str(err)
            )
            self._add_to_history(err_result)
            return err_result
        except Exception as ex:
            err_result = CalculationResult(
                expression=expression_str,
                postfix_expression="",
                result=None,
                complexity=None,
                timestamp=now,
                error=f"Erro inesperado: {type(ex).__name__} - {str(ex)}"
            )
            self._add_to_history(err_result)
            return err_result

    def _add_to_history(self, item: CalculationResult) -> None:
        """Adiciona o resultado ao histórico mantendo o limite configurado."""
        self._history.append(item)
        if len(self._history) > self.max_history:
            self._history.pop(0)

    def get_history(self) -> List[CalculationResult]:
        """Retorna cópia do histórico recente de operações."""
        return list(self._history)

    def clear_history(self) -> None:
        """Limpa o histórico de operações."""
        self._history.clear()


__all__ = [
    "Stack",
    "Queue",
    "Tokenizer",
    "Token",
    "TokenType",
    "InfixToPostfixConverter",
    "PostfixEvaluator",
    "ComplexityAnalyzer",
    "ComplexityReport",
    "CalculatorEngine",
    "CalculationResult",
    "TokenizerError",
    "ShuntingYardError",
    "MismatchedParenthesesError",
    "EvaluationError",
    "DivisionByZeroError",
]
