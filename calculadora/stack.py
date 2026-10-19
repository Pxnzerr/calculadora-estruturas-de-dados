"""
Módulo de Estrutura de Dados: Pilha (Stack)

A Pilha é uma estrutura de dados linear que segue o princípio LIFO (Last-In, First-Out).
O último elemento inserido é o primeiro a ser removido.

Nesta calculadora, a Pilha é utilizada para:
1. Armazenar operadores temporariamente durante o algoritmo de Shunting Yard.
2. Validar o balanceamento e aninhamento de parênteses.
3. Armazenar operandos (valores numéricos) durante a avaliação da notação pós-fixa.
"""

from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')


class Stack(Generic[T]):
    """
    Implementação genérica de uma Pilha (Stack) LIFO.
    
    Complexidade:
    - push: O(1) amortizado
    - pop:  O(1)
    - peek: O(1)
    - is_empty: O(1)
    - size: O(1)
    - Espaço: O(n) onde n é o número de elementos na pilha
    """

    def __init__(self) -> None:
        """Inicializa uma pilha vazia e zera o rastreador de profundidade máxima."""
        self._items: List[T] = []
        self._max_depth: int = 0

    def push(self, item: T) -> None:
        """
        Insere um item no topo da pilha.
        
        Args:
            item: Elemento a ser empilhado.
        """
        self._items.append(item)
        depth = len(self._items)
        if depth > self._max_depth:
            self._max_depth = depth

    def pop(self) -> T:
        """
        Remove e retorna o item do topo da pilha.
        
        Returns:
            O elemento no topo da pilha.
            
        Raises:
            IndexError: Se a pilha estiver vazia.
        """
        if self.is_empty():
            raise IndexError("Erro de Pilha: tentativa de desempilhar (pop) de uma pilha vazia.")
        return self._items.pop()

    def peek(self) -> T:
        """
        Retorna o item no topo da pilha sem removê-lo.
        
        Returns:
            O elemento no topo da pilha.
            
        Raises:
            IndexError: Se a pilha estiver vazia.
        """
        if self.is_empty():
            raise IndexError("Erro de Pilha: tentativa de espiar (peek) em uma pilha vazia.")
        return self._items[-1]

    def is_empty(self) -> bool:
        """
        Verifica se a pilha está vazia.
        
        Returns:
            True se vazia, False caso contrário.
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Retorna a quantidade atual de itens na pilha.
        
        Returns:
            Tamanho atual da pilha.
        """
        return len(self._items)

    def clear(self) -> None:
        """Esvazia a pilha e redefine a profundidade máxima."""
        self._items.clear()
        self._max_depth = 0

    @property
    def max_depth(self) -> int:
        """
        Retorna a profundidade máxima atingida pela pilha durante sua utilização.
        
        Returns:
            Pico de elementos armazenados simultaneamente.
        """
        return self._max_depth

    def to_list(self) -> List[T]:
        """
        Retorna uma cópia da lista interna de elementos (da base para o topo).
        
        Returns:
            Lista com os elementos.
        """
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def __iter__(self):
        return iter(self._items)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stack):
            return False
        return self._items == other._items

    def copy(self) -> 'Stack[T]':
        """
        Retorna uma cópia da pilha com os mesmos elementos e profundidade máxima.
        
        Returns:
            Nova instância de Stack contendo os mesmos itens.
        """
        new_stack = Stack[T]()
        new_stack._items = list(self._items)
        new_stack._max_depth = self._max_depth
        return new_stack

    def __repr__(self) -> str:
        return f"Stack({self._items})"

