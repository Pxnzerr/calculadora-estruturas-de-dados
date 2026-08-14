"""
Suíte de Testes Unitários para a Calculadora de Estruturas de Dados e Algoritmos.
"""

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


if __name__ == "__main__":
    unittest.main()
