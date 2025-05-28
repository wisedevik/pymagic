from typing import TypeVar, Generic, Iterator, Optional

T = TypeVar('T')

class LogicArrayList(Generic[T]):
    def __init__(self, initial_capacity: int = 0):
        self._items: list[Optional[T]] = [None] * initial_capacity
        self._count: int = 0
        self._item_type: Optional[type] = None


    def __getitem__(self, index: int) -> T:
        item = self._items[index]
        assert item is not None, "Accessing uninitialized item"
        return item

    def __setitem__(self, index: int, value: T) -> None:
        self._items[index] = value

    @property
    def count(self) -> int:
        return self._count

    def clear(self) -> None:
        for i in range(self._count):
            self._items[i] = None
        self._count = 0

    def add(self, item: T) -> None:
        if self._count == len(self._items):
            self.ensure_capacity(len(self._items) * 2 if len(self._items) != 0 else 5)

        if self._item_type is None and item is not None:
            self._item_type = type(item)

        self._items[self._count] = item
        self._count += 1

    def add_at(self, index: int, item: T) -> None:
        if self._count == len(self._items):
            self.ensure_capacity(len(self._items) * 2 if len(self._items) != 0 else 5)
        if self._count > index:
            self._items[index+1:self._count+1] = self._items[index:self._count]
        self._items[index] = item
        self._count += 1

    def index_of(self, item: T) -> int:
        for i in range(self._count):
            if self._items[i] == item:
                return i
        return -1

    def remove(self, index: int) -> None:
        if index < self._count:
            self._count -= 1
            if index != self._count:
                self._items[index:self._count] = self._items[index+1:self._count+1]
            self._items[self._count] = None

    def ensure_capacity(self, count: int) -> None:
        if len(self._items) < count:
            self._items += [None] * (count - len(self._items))

    def __iter__(self) -> Iterator[T]:
        for i in range(self._count):
            yield self._items[i]  # type: ignore

    def __repr__(self) -> str:
        return repr(self._items[:self._count])
