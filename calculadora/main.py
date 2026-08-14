"""
Ponto de Entrada Principal da Calculadora Algorítmica.

Permite execução tanto em modo CLI (linha de comando interativa)
quanto em modo GUI (interface gráfica Tkinter).
"""

import sys
import argparse

# Configuração de codificação segura para terminal Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from .ui import CLIInterface, run_gui


def main():
    parser = argparse.ArgumentParser(
        description="Calculadora de Estruturas de Dados e Análise de Algoritmos"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Executa a calculadora no terminal em modo CLI"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Executa a calculadora com interface gráfica (Tkinter)"
    )
    parser.add_argument(
        "-e", "--eval",
        type=str,
        help="Avalia uma única expressão diretamente e sai"
    )

    args = parser.parse_args()

    if args.eval:
        from . import CalculatorEngine
        engine = CalculatorEngine()
        res = engine.calculate(args.eval)
        if res.error:
            print(f"Erro: {res.error}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Expressão: {res.expression}")
            print(f"RPN:       {res.postfix_expression}")
            print(f"Resultado: {res.result}")
            if res.complexity:
                print(res.complexity.format_summary())
        return

    if args.gui:
        run_gui()
    else:
        # Padrão é CLI (ou se passar --cli)
        cli = CLIInterface()
        cli.run()


if __name__ == "__main__":
    main()
