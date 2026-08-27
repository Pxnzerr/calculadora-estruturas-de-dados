"""
Módulo de Estrutura de Dados: Fila (Queue)

A Fila é uma estrutura de dados linear que segue o princípio FIFO (First-In, First-Out).
O primeiro elemento inserido é o primeiro a ser processado e removido.

Nesta calculadora, a Fila é utilizada para:
1. Armazenar o fluxo de saída de tokens gerados pelo algoritmo de Shunting Yard
   na ordem exata em que devem ser avaliados pela notação pós-fixa (RPN).
"""

from typing import TypeVar, Generic, List, Optional
from collections import deque

T = TypeVar('T')


class Queue(Generic[T]):
    """
    Implementação genérica de uma Fila (Queue) FIFO com garantia O(1) para operações básicas.
    
    Complexidade:
    - enqueue: O(1)
    - dequeue: O(1)
    - peek:    O(1)
    - is_empty: O(1)
    - size:    O(1)
    - Espaço:  O(n) onde n é o número de elementos na fila
    """

    def __init__(self) -> None:
        """Inicializa uma fila vazia."""
        self._items: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        """
        Insere um item no final da fila.
        
        Args:
            item: Elemento a ser enfileirado.
        """
        self._items.append(item)

    def dequeue(self) -> T:
        """
        Remove e retorna o item do início da fila.
        
        Returns:
            O elemento mais antigo da fila.
            
        Raises:
            IndexError: Se a fila estiver vazia.
        """
        if self.is_empty():
            raise IndexError("Erro de Fila: tentativa de desenfileirar (dequeue) de uma fila vazia.")
        return self._items.popleft()

    def peek(self) -> T:
        """
        Retorna o item no início da fila sem removê-lo.
        
        Returns:
            O elemento no início da fila.
            
        Raises:
            IndexError: Se a fila estiver vazia.
        """
        if self.is_empty():
            raise IndexError("Erro de Fila: tentativa de espiar (peek) em uma fila vazia.")
        return self._items[0]

    def is_empty(self) -> bool:
        """
        Verifica se a fila está vazia.
        
        Returns:
            True se vazia, False caso contrário.
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Retorna a quantidade atual de itens na fila.
        
        Returns:
            Tamanho atual da fila.
        """
        return len(self._items)

    def clear(self) -> None:
        """Esvazia a fila."""
        self._items.clear()

    def to_list(self) -> List[T]:
        """
        Retorna uma lista com os elementos da fila do início para o fim.
        
        Returns:
            Lista com os elementos ordenados por ordem de chegada.
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
        if not isinstance(other, Queue):
            return False
        return list(self._items) == list(other._items)

    def copy(self) -> 'Queue[T]':
        """
        Retorna uma cópia da fila com os mesmos elementos.
        
        Returns:
            Nova instância de Queue contendo os mesmos itens.
        """
        new_queue = Queue[T]()
        new_queue._items = deque(self._items)
        return new_queue

    def __repr__(self) -> str:
        return f"Queue({list(self._items)})"

