"""
Pacote Calculadora de Estruturas de Dados e Análise de Algoritmos.
"""

from typing import List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import os

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
        self._last_result: Optional[Union[int, float]] = None

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
            # 1. Tokenização / Análise Léxica e Sintática (com suporte a 'ans')
            ans_val = float(self._last_result) if self._last_result is not None else None
            tokenizer = self.tokenizer_cls(expression_str, ans_value=ans_val)
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

            self._last_result = result_val
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

    @property
    def last_result(self) -> Optional[Union[int, float]]:
        """Retorna o último resultado calculado com sucesso (para uso com 'ans')."""
        return self._last_result

    def export_history(self, filepath: str) -> str:
        """
        Exporta o histórico de operações para um arquivo de texto legível.
        
        Args:
            filepath: Caminho do arquivo de saída.
            
        Returns:
            Caminho absoluto do arquivo gerado.
        """
        lines = []
        lines.append("=" * 70)
        lines.append("  HISTORICO DE OPERACOES — Calculadora de Estruturas de Dados")
        lines.append(f"  Exportado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append("")

        if not self._history:
            lines.append("  (Historico vazio)")
        else:
            for i, item in enumerate(self._history, 1):
                time_str = item.timestamp.strftime("%H:%M:%S")
                lines.append(f"  [{i:02d}] {time_str} | {item.expression}")
                if item.error:
                    lines.append(f"       ERRO: {item.error}")
                else:
                    lines.append(f"       RPN:       {item.postfix_expression}")
                    lines.append(f"       Resultado: {item.result}")
                    if item.complexity:
                        lines.append(f"       Tokens: {item.complexity.total_tokens} | "
                                     f"Operandos: {item.complexity.num_operands} | "
                                     f"Operadores: {item.complexity.num_operators}")
                lines.append("")

        lines.append("=" * 70)

        abs_path = os.path.abspath(filepath)
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))

        return abs_path


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
