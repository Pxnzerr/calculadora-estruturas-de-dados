"""
Suíte de Testes Unitários para a Calculadora de Estruturas de Dados e Algoritmos.
"""

import math
import os
import tempfile
import unittest
from calculadora.stack import Stack
from calculadora.queue_ds import Queue
from calculadora.tokenizer import Tokenizer, TokenType, TokenizerError
from calculadora.converter import InfixToPostfixConverter, MismatchedParenthesesError, ShuntingYardError
from calculadora.evaluator import PostfixEvaluator, DivisionByZeroError, EvaluationError
from calculadora.analyzer import ComplexityAnalyzer
from calculadora import CalculatorEngine


class TestStack(unittest.TestCase):
    """Testes para a estrutura de dados Pilha (Stack)."""

    def setUp(self):
        self.stack = Stack[int]()

    def test_push_and_pop(self):
        self.assertTrue(self.stack.is_empty())
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.size(), 2)
        self.assertEqual(self.stack.peek(), 20)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.pop(), 10)
        self.assertTrue(self.stack.is_empty())

    def test_pop_empty_raises(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek_empty_raises(self):
        with self.assertRaises(IndexError):
            self.stack.peek()

    def test_max_depth(self):
        self.assertEqual(self.stack.max_depth, 0)
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.assertEqual(self.stack.max_depth, 3)
        self.stack.pop()
        self.stack.pop()
        self.assertEqual(self.stack.max_depth, 3)
        self.stack.push(4)
        self.stack.push(5)
        self.stack.push(6)
        self.assertEqual(self.stack.max_depth, 4)


class TestQueue(unittest.TestCase):
    """Testes para a estrutura de dados Fila (Queue)."""

    def setUp(self):
        self.queue = Queue[str]()

    def test_enqueue_and_dequeue(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue("a")
        self.queue.enqueue("b")
        self.queue.enqueue("c")
        self.assertEqual(self.queue.size(), 3)
        self.assertEqual(self.queue.peek(), "a")
        self.assertEqual(self.queue.dequeue(), "a")
        self.assertEqual(self.queue.dequeue(), "b")
        self.assertEqual(self.queue.dequeue(), "c")
        self.assertTrue(self.queue.is_empty())

    def test_dequeue_empty_raises(self):
        with self.assertRaises(IndexError):
            self.queue.dequeue()

    def test_peek_empty_raises(self):
        with self.assertRaises(IndexError):
            self.queue.peek()


class TestTokenizer(unittest.TestCase):
    """Testes para o Tokenizer / Lexer."""

    def test_basic_tokens(self):
        tok = Tokenizer("2 + 3 * 4").tokenize()
        values = [t.value for t in tok]
        self.assertEqual(values, ["2", "+", "3", "*", "4"])

    def test_floats_and_decimals(self):
        tok = Tokenizer("3.14 + .5").tokenize()
        values = [t.value for t in tok]
        self.assertEqual(values, ["3.14", "+", "0.5"])

    def test_unary_minus_at_start(self):
        tok = Tokenizer("-5 + 3").tokenize()
        values = [t.value for t in tok]
        self.assertEqual(values, ["-5", "+", "3"])

    def test_unary_minus_inside_parentheses(self):
        tok = Tokenizer("2 * (-3)").tokenize()
        values = [t.value for t in tok]
        self.assertEqual(values, ["2", "*", "(", "-3", ")"])

    def test_unary_minus_before_parenthesis(self):
        tok = Tokenizer("-(3 + 4)").tokenize()
        values = [t.value for t in tok]
        self.assertEqual(values, ["u-", "(", "3", "+", "4", ")"])

    def test_unary_plus_ignored(self):
        tok = Tokenizer("+5 + (+3)").tokenize()
        values = [t.value for t in tok]
        self.assertEqual(values, ["5", "+", "(", "3", ")"])

    def test_invalid_characters(self):
        with self.assertRaises(TokenizerError):
            Tokenizer("2 + $ 3").tokenize()

    def test_consecutive_operators(self):
        with self.assertRaises(TokenizerError):
            Tokenizer("2 + * 3").tokenize()

    def test_empty_parentheses(self):
        with self.assertRaises(TokenizerError):
            Tokenizer("2 + ()").tokenize()

    def test_empty_string(self):
        with self.assertRaises(TokenizerError):
            Tokenizer("   ").tokenize()

    # ===== NOVOS TESTES: Funções Matemáticas =====

    def test_function_tokens(self):
        """Funções devem ser tokenizadas como TokenType.FUNCTION."""
        tok = Tokenizer("sin(3.14)").tokenize()
        types = [t.type for t in tok]
        self.assertIn(TokenType.FUNCTION, types)
        self.assertEqual(tok[0].value, "sin")

    def test_function_sqrt(self):
        tok = Tokenizer("sqrt(16)").tokenize()
        values = [t.value for t in tok]
        self.assertEqual(values, ["sqrt", "(", "16", ")"])

    def test_function_case_insensitive(self):
        """Funções devem ser case-insensitive."""
        tok = Tokenizer("SIN(1) + COS(2)").tokenize()
        func_values = [t.value for t in tok if t.type == TokenType.FUNCTION]
        self.assertEqual(func_values, ["sin", "cos"])

    def test_function_without_parenthesis_raises(self):
        """Função seguida de algo que não é '(' deve dar erro."""
        with self.assertRaises(TokenizerError):
            Tokenizer("sin 3").tokenize()

    def test_unknown_identifier_raises(self):
        """Identificador desconhecido deve dar erro."""
        with self.assertRaises(TokenizerError):
            Tokenizer("foo(3)").tokenize()

    # ===== NOVOS TESTES: Constantes =====

    def test_constant_pi(self):
        """'pi' deve ser tokenizado como NUMBER com o valor de math.pi."""
        tok = Tokenizer("pi + 1").tokenize()
        self.assertEqual(tok[0].type, TokenType.NUMBER)
        self.assertAlmostEqual(float(tok[0].value), math.pi)

    def test_constant_e(self):
        """'e' deve ser tokenizado como NUMBER com o valor de math.e."""
        tok = Tokenizer("e * 2").tokenize()
        self.assertEqual(tok[0].type, TokenType.NUMBER)
        self.assertAlmostEqual(float(tok[0].value), math.e)

    def test_constant_case_insensitive(self):
        """Constantes devem ser case-insensitive."""
        tok = Tokenizer("PI + E").tokenize()
        self.assertAlmostEqual(float(tok[0].value), math.pi)
        self.assertAlmostEqual(float(tok[2].value), math.e)

    # ===== NOVOS TESTES: Variável 'ans' =====

    def test_ans_with_value(self):
        """'ans' deve ser expandido para o último resultado."""
        tok = Tokenizer("ans + 1", ans_value=42.0).tokenize()
        self.assertEqual(tok[0].type, TokenType.NUMBER)
        self.assertEqual(float(tok[0].value), 42.0)

    def test_ans_without_value_raises(self):
        """'ans' sem valor anterior deve dar erro."""
        with self.assertRaises(TokenizerError):
            Tokenizer("ans + 1").tokenize()


class TestShuntingYardConverter(unittest.TestCase):
    """Testes para a conversão Infixa -> Pós-Fixa (RPN)."""

    def setUp(self):
        self.converter = InfixToPostfixConverter()

    def _convert_str(self, expr: str) -> str:
        tokens = Tokenizer(expr).tokenize()
        queue = self.converter.convert(tokens)
        return " ".join(t.value for t in queue.to_list())

    def test_operator_precedence(self):
        self.assertEqual(self._convert_str("2 + 3 * 4"), "2 3 4 * +")
        self.assertEqual(self._convert_str("10 - 5 * 2"), "10 5 2 * -")

    def test_parentheses_overrides(self):
        self.assertEqual(self._convert_str("(2 + 3) * 4"), "2 3 + 4 *")
        self.assertEqual(self._convert_str("((2 + 3) * 4) - 1"), "2 3 + 4 * 1 -")

    def test_power_right_associativity(self):
        # 2 ^ 3 ^ 2 deve ser avaliado como 2 ^ (3 ^ 2), portanto RPN: 2 3 2 ^ ^
        self.assertEqual(self._convert_str("2 ^ 3 ^ 2"), "2 3 2 ^ ^")

    def test_modulo_operator(self):
        self.assertEqual(self._convert_str("100 % 7 + 2"), "100 7 % 2 +")

    def test_unbalanced_parentheses_open(self):
        with self.assertRaises(MismatchedParenthesesError):
            self._convert_str("(2 + 3 * 4")

    def test_unbalanced_parentheses_close(self):
        with self.assertRaises(MismatchedParenthesesError):
            self._convert_str("2 + 3) * 4")

    # ===== NOVOS TESTES: Funções no Shunting Yard =====

    def test_function_in_rpn(self):
        """Função deve aparecer após seu argumento na RPN."""
        rpn = self._convert_str("sqrt(16)")
        self.assertEqual(rpn, "16 sqrt")

    def test_function_with_expression_arg(self):
        """Função com expressão complexa como argumento."""
        rpn = self._convert_str("sqrt(9 + 16)")
        self.assertEqual(rpn, "9 16 + sqrt")

    def test_function_combined_with_operators(self):
        """Função combinada com operadores."""
        rpn = self._convert_str("sin(1) + cos(2)")
        self.assertEqual(rpn, "1 sin 2 cos +")

    def test_nested_functions(self):
        """Funções aninhadas."""
        rpn = self._convert_str("sqrt(abs(-16))")
        self.assertEqual(rpn, "-16 abs sqrt")


class TestCalculatorEngine(unittest.TestCase):
    """Testes de ponta a ponta com o CalculatorEngine."""

    def setUp(self):
        self.engine = CalculatorEngine()

    def test_user_examples(self):
        cases = [
            ("2 + 3", 5),
            ("10 - 5 * 2", 0),
            ("(3 + 4) * 2", 14),
            ("16 / 4 + 2", 6),
            ("2 ^ 3 + 1", 9),
            ("(10 + 5) / 3", 5),
            ("100 % 7", 2),
            ("((2 + 3) * 4) - 1", 19),
        ]
        for expr, expected in cases:
            with self.subTest(expr=expr):
                res = self.engine.calculate(expr)
                self.assertIsNone(res.error, f"Falhou com erro inesperado em '{expr}': {res.error}")
                self.assertEqual(res.result, expected)

    def test_right_associativity_power_result(self):
        # 2 ^ 3 ^ 2 = 2 ^ 9 = 512 (e não (2^3)^2 = 64)
        res = self.engine.calculate("2 ^ 3 ^ 2")
        self.assertEqual(res.result, 512)

    def test_decimals_and_floats(self):
        res = self.engine.calculate("3.5 * 2 + 0.5")
        self.assertAlmostEqual(res.result, 7.5)

    def test_negative_numbers(self):
        self.assertEqual(self.engine.calculate("-5 + 3").result, -2)
        self.assertEqual(self.engine.calculate("2 * -3").result, -6)
        self.assertEqual(self.engine.calculate("-(3 + 4) * 2").result, -14)
        self.assertEqual(self.engine.calculate("(-2) ^ 3").result, -8)
        self.assertEqual(self.engine.calculate("(-2) ^ 2").result, 4)

    def test_division_by_zero(self):
        res = self.engine.calculate("10 / 0")
        self.assertIsNotNone(res.error)
        self.assertIn("Divisão por zero", res.error)

    def test_modulo_by_zero(self):
        res = self.engine.calculate("10 % 0")
        self.assertIsNotNone(res.error)
        self.assertIn("módulo por zero", res.error.lower())

    def test_complexity_metrics(self):
        res = self.engine.calculate("(2 + 3) * 4")
        self.assertIsNotNone(res.complexity)
        comp = res.complexity
        self.assertEqual(comp.num_operands, 3)     # 2, 3, 4
        self.assertEqual(comp.num_operators, 2)    # +, *
        self.assertEqual(comp.num_parentheses, 2)  # (, )
        self.assertGreater(comp.overall_max_stack_depth, 0)
        self.assertEqual(comp.time_complexity_theoretical, "O(n) - Linear")
        self.assertEqual(comp.space_complexity_theoretical, "O(n) - Linear")

    def test_history_limit(self):
        engine = CalculatorEngine(max_history=3)
        engine.calculate("1 + 1")
        engine.calculate("2 + 2")
        engine.calculate("3 + 3")
        engine.calculate("4 + 4")
        hist = engine.get_history()
        self.assertEqual(len(hist), 3)
        self.assertEqual(hist[-1].expression, "4 + 4")
        self.assertEqual(hist[0].expression, "2 + 2")
        engine.clear_history()
        self.assertEqual(len(engine.get_history()), 0)

    # ===== NOVOS TESTES: Funções Matemáticas (Ponta a Ponta) =====

    def test_sqrt(self):
        res = self.engine.calculate("sqrt(16)")
        self.assertIsNone(res.error)
        self.assertEqual(res.result, 4)

    def test_sqrt_with_expression(self):
        res = self.engine.calculate("sqrt(9 + 16)")
        self.assertIsNone(res.error)
        self.assertEqual(res.result, 5)

    def test_sin_zero(self):
        res = self.engine.calculate("sin(0)")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, 0.0, places=10)

    def test_sin_pi_half(self):
        res = self.engine.calculate("sin(pi / 2)")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, 1.0, places=10)

    def test_cos_zero(self):
        res = self.engine.calculate("cos(0)")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, 1.0, places=10)

    def test_cos_pi(self):
        res = self.engine.calculate("cos(pi)")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, -1.0, places=10)

    def test_tan_zero(self):
        res = self.engine.calculate("tan(0)")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, 0.0, places=10)

    def test_log_100(self):
        """log é logaritmo base 10."""
        res = self.engine.calculate("log(100)")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, 2.0, places=10)

    def test_ln_e(self):
        """ln é logaritmo natural (base e)."""
        res = self.engine.calculate("ln(e)")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, 1.0, places=10)

    def test_abs_negative(self):
        res = self.engine.calculate("abs(-42)")
        self.assertIsNone(res.error)
        self.assertEqual(res.result, 42)

    def test_ceil_decimal(self):
        res = self.engine.calculate("ceil(3.2)")
        self.assertIsNone(res.error)
        self.assertEqual(res.result, 4)

    def test_floor_decimal(self):
        res = self.engine.calculate("floor(3.9)")
        self.assertIsNone(res.error)
        self.assertEqual(res.result, 3)

    def test_nested_functions(self):
        """Funções aninhadas: sqrt(abs(-25))"""
        res = self.engine.calculate("sqrt(abs(-25))")
        self.assertIsNone(res.error)
        self.assertEqual(res.result, 5)

    def test_function_combined_with_arithmetic(self):
        """Funções combinadas com aritmética."""
        res = self.engine.calculate("sqrt(16) + sqrt(9)")
        self.assertIsNone(res.error)
        self.assertEqual(res.result, 7)

    # ===== NOVOS TESTES: Erros de Domínio =====

    def test_sqrt_negative_error(self):
        res = self.engine.calculate("sqrt(-4)")
        self.assertIsNotNone(res.error)
        self.assertIn("negativo", res.error.lower())

    def test_log_zero_error(self):
        res = self.engine.calculate("log(0)")
        self.assertIsNotNone(res.error)

    def test_log_negative_error(self):
        res = self.engine.calculate("log(-1)")
        self.assertIsNotNone(res.error)

    def test_ln_zero_error(self):
        res = self.engine.calculate("ln(0)")
        self.assertIsNotNone(res.error)

    # ===== NOVOS TESTES: Constantes =====

    def test_pi_value(self):
        res = self.engine.calculate("pi")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, math.pi)

    def test_e_value(self):
        res = self.engine.calculate("e")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, math.e)

    def test_pi_arithmetic(self):
        res = self.engine.calculate("2 * pi")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, 2 * math.pi)

    def test_trigonometric_identities(self):
        """Testa identidade sen^2(x) + cos^2(x) = 1."""
        res = self.engine.calculate("(sin(pi / 4)) ^ 2 + (cos(pi / 4)) ^ 2")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, 1.0, places=7)

    def test_exp_log_inverse(self):
        """Testa a relação inversa exponencial e logaritmo e^(ln(x)) = x."""
        res = self.engine.calculate("e ^ (ln(5))")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, 5.0, places=7)

    def test_nested_unary_and_constants(self):
        """Testa unário com constantes matemáticas."""
        res = self.engine.calculate("-1 * pi")
        self.assertIsNone(res.error)
        self.assertAlmostEqual(res.result, -math.pi)

    # ===== NOVOS TESTES: Variável 'ans' =====

    def test_ans_basic(self):
        """'ans' deve retornar o último resultado."""
        self.engine.calculate("10 + 5")  # ans = 15
        res = self.engine.calculate("ans * 2")
        self.assertIsNone(res.error)
        self.assertEqual(res.result, 30)

    def test_ans_chain(self):
        """Encadear cálculos com 'ans'."""
        self.engine.calculate("100")  # ans = 100
        self.engine.calculate("ans / 2")  # ans = 50
        res = self.engine.calculate("ans + 25")
        self.assertIsNone(res.error)
        self.assertEqual(res.result, 75)

    def test_ans_no_previous_error(self):
        """'ans' sem cálculo anterior deve dar erro."""
        engine = CalculatorEngine()
        res = engine.calculate("ans + 1")
        self.assertIsNotNone(res.error)
        self.assertIn("ans", res.error.lower())

    # ===== NOVOS TESTES: Exportação de Histórico =====

    def test_export_history(self):
        """Exportar histórico deve criar um arquivo válido."""
        self.engine.calculate("2 + 3")
        self.engine.calculate("sqrt(16)")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name

        try:
            result_path = self.engine.export_history(temp_path)
            self.assertTrue(os.path.exists(result_path))

            with open(result_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.assertIn("2 + 3", content)
            self.assertIn("sqrt(16)", content)
            self.assertIn("HISTORICO", content)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_export_empty_history(self):
        """Exportar histórico vazio deve funcionar sem erro."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name

        try:
            result_path = self.engine.export_history(temp_path)
            self.assertTrue(os.path.exists(result_path))

            with open(result_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.assertIn("vazio", content.lower())
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    # ===== NOVO TESTE: last_result property =====

    def test_last_result_property(self):
        """last_result deve rastrear o último resultado com sucesso."""
        self.assertIsNone(self.engine.last_result)
        self.engine.calculate("7 * 6")
        self.assertEqual(self.engine.last_result, 42)


if __name__ == "__main__":
    unittest.main()
