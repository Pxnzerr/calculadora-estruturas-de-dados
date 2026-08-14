"""
Módulo de Interface de Usuário (UI): CLI Interativa e GUI Tkinter

Oferece duas experiências de uso:
1. CLI: Terminal interativo com tabelas ASCII, painel de complexidade e comandos rápidos.
2. GUI: Janela gráfica moderna em Tkinter com histórico dinâmico, painel de análise e atalhos de teclado.
"""

import sys
import os
from typing import Optional
from . import CalculatorEngine, CalculationResult


class CLIInterface:
    """Interface de Linha de Comando (CLI) interativa para a calculadora."""

    BANNER = r"""
========================================================================
   CALCULADORA DE ESTRUTURAS DE DADOS & ANÁLISE DE ALGORITMOS
   Pilha (Stack) | Fila (Queue) | Shunting Yard | Avaliação RPN | O(n)
========================================================================
 Operadores suportados: +  -  *  /  ^ (potência)  % (módulo)  ( )
 Comandos especiais:
   :h, :help      -> Exibe ajuda e exemplos
   :hist, :history-> Exibe as últimas operações
   :c, :clear     -> Limpa o histórico
   :q, :exit      -> Sair do programa
------------------------------------------------------------------------
"""

    def __init__(self, engine: Optional[CalculatorEngine] = None):
        self.engine = engine or CalculatorEngine(max_history=10)

    def run(self) -> None:
        """Inicia o loop REPL interativo no terminal."""
        print(self.BANNER)

        while True:
            try:
                user_input = input("\n[Calc] Digite a expressão (ou :help): ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nEncerrando a calculadora. Até logo!")
                break

            if not user_input:
                continue

            cmd = user_input.lower()
            if cmd in (':q', ':exit', 'exit', 'sair', 'quit'):
                print("Encerrando a calculadora. Até logo!")
                break
            elif cmd in (':h', ':help', 'help', 'ajuda'):
                self._show_help()
                continue
            elif cmd in (':hist', ':history', 'history', 'historico'):
                self._show_history()
                continue
            elif cmd in (':c', ':clear', 'clear', 'limpar'):
                self.engine.clear_history()
                print(">> Histórico limpo com sucesso!")
                continue

            # Processar cálculo
            res = self.engine.calculate(user_input)
            self._display_result(res)

    def _display_result(self, res: CalculationResult) -> None:
        """Exibe os detalhes do resultado e da complexidade."""
        if res.error:
            print(f"\n[X] {res.error}")
            return

        print(f"\n------------------------------------------------------------")
        print(f" EXPRESSÃO ORIGINAL: {res.expression}")
        print(f" NOTAÇÃO PÓS-FIXA:  {res.postfix_expression}")
        print(f" RESULTADO FINAL:   \033[1;32m{res.result}\033[0m")
        print(f"------------------------------------------------------------")
        if res.complexity:
            print(res.complexity.format_summary())

    def _show_history(self) -> None:
        """Exibe o histórico das últimas operações."""
        history = self.engine.get_history()
        if not history:
            print(">> Histórico vazio.")
            return

        print("\n=== HISTÓRICO DAS ÚLTIMAS OPERAÇÕES ===")
        for i, item in enumerate(history, 1):
            if item.error:
                status = f"[ERRO] {item.error}"
            else:
                status = f"= {item.result} (RPN: {item.postfix_expression})"
            time_str = item.timestamp.strftime("%H:%M:%S")
            print(f" {i:2d}. [{time_str}] {item.expression} {status}")
        print("=======================================")

    def _show_help(self) -> None:
        """Exibe a documentação de ajuda e exemplos práticos."""
        help_text = """
=== GUIA RÁPIDO E EXEMPLOS ===
Precedência de Operadores:
  1. Parênteses: ( ... )
  2. Potência:   ^  (Associatividade à Direita: 2 ^ 3 ^ 2 = 2 ^ 9 = 512)
  3. Mult/Div/Mod: *, /, % (Associatividade à Esquerda)
  4. Soma/Sub:   +, - (Associatividade à Esquerda)

Exemplos válidos:
  - 2 + 3 * 4              -> 14
  - (10 - 5) / 2           -> 2.5
  - 2 ^ 3 + 1              -> 9
  - 100 % 7                -> 2
  - ((2 + 3) * 4) - 1      -> 19
  - -5 + 3                 -> -2
  - 3.5 * 2 + 0.5          -> 7.5
==============================
"""
        print(help_text)


def run_gui():
    """Inicializa a interface gráfica moderna em Tkinter."""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except ImportError:
        print("Erro: Tkinter não está disponível neste ambiente. Use a CLI com --cli.")
        return

    class CalculatorGUI:
        def __init__(self, root: tk.Tk):
            self.root = root
            self.root.title("Calculadora Algorítmica — Pilha, Fila & Shunting Yard")
            self.root.geometry("820x680")
            self.root.minsize(760, 600)
            self.engine = CalculatorEngine(max_history=10)

            # Estilo escuro / moderno
            self.bg_color = "#1e1e2e"
            self.card_color = "#252538"
            self.accent_color = "#89b4fa"
            self.accent_hover = "#b4befe"
            self.text_color = "#cdd6f4"
            self.success_color = "#a6e3a1"
            self.error_color = "#f38ba8"

            self.root.configure(bg=self.bg_color)
            self._setup_ui()

        def _setup_ui(self):
            style = ttk.Style()
            style.theme_use("clam")
            style.configure(".", background=self.bg_color, foreground=self.text_color)
            style.configure("Card.TFrame", background=self.card_color)

            # Cabeçalho
            header_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
            header_frame.pack(fill="x", padx=20)

            title_lbl = tk.Label(
                header_frame,
                text="Calculadora de Algoritmos e Estruturas de Dados",
                font=("Helvetica", 16, "bold"),
                bg=self.bg_color,
                fg=self.accent_color
            )
            title_lbl.pack(anchor="w")

            sub_lbl = tk.Label(
                header_frame,
                text="Pilha (LIFO) • Fila (FIFO) • Shunting Yard de Dijkstra • Complexidade O(n)",
                font=("Helvetica", 10),
                bg=self.bg_color,
                fg="#a6adc8"
            )
            sub_lbl.pack(anchor="w")

            # Área de Entrada
            input_frame = tk.Frame(self.root, bg=self.card_color, padx=15, pady=15, relief="flat")
            input_frame.pack(fill="x", padx=20, pady=5)

            tk.Label(
                input_frame,
                text="Expressão Matemática (Infixa):",
                font=("Helvetica", 11, "bold"),
                bg=self.card_color,
                fg=self.text_color
            ).pack(anchor="w", pady=(0, 5))

            entry_box = tk.Frame(input_frame, bg=self.card_color)
            entry_box.pack(fill="x")

            self.entry_expr = tk.Entry(
                entry_box,
                font=("Consolas", 14),
                bg="#313244",
                fg="#ffffff",
                insertbackground="#ffffff",
                relief="flat",
                highlightthickness=1,
                highlightcolor=self.accent_color,
                highlightbackground="#45475a"
            )
            self.entry_expr.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))
            self.entry_expr.focus_set()
            self.entry_expr.bind("<Return>", lambda e: self._on_calculate())

            btn_calc = tk.Button(
                entry_box,
                text="Calcular (Enter)",
                font=("Helvetica", 11, "bold"),
                bg=self.accent_color,
                fg="#11111b",
                activebackground=self.accent_hover,
                relief="flat",
                padx=15,
                pady=6,
                cursor="hand2",
                command=self._on_calculate
            )
            btn_calc.pack(side="right")

            # Área de Resultado
            result_card = tk.Frame(self.root, bg=self.card_color, padx=15, pady=12)
            result_card.pack(fill="x", padx=20, pady=10)

            res_header = tk.Frame(result_card, bg=self.card_color)
            res_header.pack(fill="x")

            tk.Label(
                res_header,
                text="Resultado:",
                font=("Helvetica", 11, "bold"),
                bg=self.card_color,
                fg=self.text_color
            ).pack(side="left")

            self.lbl_rpn = tk.Label(
                res_header,
                text="RPN: -",
                font=("Consolas", 10),
                bg=self.card_color,
                fg="#a6adc8"
            )
            self.lbl_rpn.pack(side="right")

            self.lbl_result = tk.Label(
                result_card,
                text="0",
                font=("Consolas", 22, "bold"),
                bg=self.card_color,
                fg=self.success_color,
                anchor="w"
            )
            self.lbl_result.pack(fill="x", pady=(5, 0))

            # Split: Análise de Complexidade (Esquerda) e Histórico (Direita)
            bottom_panes = tk.Frame(self.root, bg=self.bg_color)
            bottom_panes.pack(fill="both", expand=True, padx=20, pady=5)

            # Painel de Análise
            analysis_card = tk.Frame(bottom_panes, bg=self.card_color, padx=15, pady=12)
            analysis_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

            tk.Label(
                analysis_card,
                text="Painel de Análise de Complexidade",
                font=("Helvetica", 11, "bold"),
                bg=self.card_color,
                fg=self.accent_color
            ).pack(anchor="w", pady=(0, 8))

            self.analysis_text = tk.Text(
                analysis_card,
                font=("Consolas", 10),
                bg="#181825",
                fg=self.text_color,
                relief="flat",
                height=10,
                padx=8,
                pady=8
            )
            self.analysis_text.pack(fill="both", expand=True)
            self.analysis_text.insert("1.0", "Insira uma expressão para visualizar a análise de algoritmos...")
            self.analysis_text.config(state="disabled")

            # Painel de Histórico
            history_card = tk.Frame(bottom_panes, bg=self.card_color, padx=15, pady=12)
            history_card.pack(side="right", fill="both", expand=True, padx=(10, 0))

            hist_header = tk.Frame(history_card, bg=self.card_color)
            hist_header.pack(fill="x", pady=(0, 8))

            tk.Label(
                hist_header,
                text="Histórico (Últimas 10)",
                font=("Helvetica", 11, "bold"),
                bg=self.card_color,
                fg=self.accent_color
            ).pack(side="left")

            btn_clear_hist = tk.Button(
                hist_header,
                text="Limpar",
                font=("Helvetica", 9),
                bg="#45475a",
                fg=self.text_color,
                relief="flat",
                padx=8,
                cursor="hand2",
                command=self._on_clear_history
            )
            btn_clear_hist.pack(side="right")

            self.history_listbox = tk.Listbox(
                history_card,
                font=("Consolas", 10),
                bg="#181825",
                fg=self.text_color,
                selectbackground="#45475a",
                relief="flat",
                height=10
            )
            self.history_listbox.pack(fill="both", expand=True)
            self.history_listbox.bind("<Double-Button-1>", self._on_history_select)

            # Atalho Ctrl+L para limpar histórico
            self.root.bind("<Control-l>", lambda e: self._on_clear_history())

        def _on_calculate(self):
            expr = self.entry_expr.get().strip()
            if not expr:
                return

            res = self.engine.calculate(expr)

            if res.error:
                self.lbl_result.config(text="ERRO", fg=self.error_color)
                self.lbl_rpn.config(text=f"Erro: {res.error}")
                self._update_analysis(f"Ocorreu um erro no processamento:\n\n{res.error}")
            else:
                self.lbl_result.config(text=str(res.result), fg=self.success_color)
                self.lbl_rpn.config(text=f"RPN: {res.postfix_expression}")
                if res.complexity:
                    self._update_analysis(res.complexity.format_summary())

            self._update_history_list()

        def _update_analysis(self, content: str):
            self.analysis_text.config(state="normal")
            self.analysis_text.delete("1.0", "end")
            self.analysis_text.insert("1.0", content)
            self.analysis_text.config(state="disabled")

        def _update_history_list(self):
            self.history_listbox.delete(0, "end")
            for item in reversed(self.engine.get_history()):
                if item.error:
                    self.history_listbox.insert("end", f"✗ {item.expression} -> ERRO")
                else:
                    self.history_listbox.insert("end", f"✓ {item.expression} = {item.result}")

        def _on_history_select(self, event):
            selection = self.history_listbox.curselection()
            if selection:
                idx = selection[0]
                history = list(reversed(self.engine.get_history()))
                if 0 <= idx < len(history):
                    selected_item = history[idx]
                    self.entry_expr.delete(0, "end")
                    self.entry_expr.insert(0, selected_item.expression)

        def _on_clear_history(self):
            self.engine.clear_history()
            self._update_history_list()

    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
