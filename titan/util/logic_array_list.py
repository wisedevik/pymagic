from typing import TypeVar, Generic, Iterator, Optional

T = TypeVar("T")


class LogicArrayList(Generic[T]):
    def __init__(self, initial_capacity: int = 0):
        self.items: list[Optional[T]] = [None] * initial_capacity
        self.count: int = 0
        self.item_type: Optional[type] = None

    def __getitem__(self, index: int) -> T:
        item = self.items[index]
        assert item is not None, "Accessing uninitialized item"
        return item

    def __setitem__(self, index: int, value: T) -> None:
        self.items[index] = value

    def clear(self) -> None:
        for i in range(self.count):
            self.items[i] = None
        self.count = 0

    def add(self, item: T) -> None:
        if self.count == len(self.items):
            self.ensure_capacity(len(self.items) * 2 if len(self.items) != 0 else 5)

        if self.item_type is None and item is not None:
            self.item_type = type(item)

        self.items[self.count] = item
        self.count += 1

    def add_at(self, index: int, item: T) -> None:
        if self.count == len(self.items):
            self.ensure_capacity(len(self.items) * 2 if len(self.items) != 0 else 5)
        if self.count > index:
            self.items[index + 1 : self.count + 1] = self.items[index : self.count]
        self.items[index] = item
        self.count += 1

    def index_of(self, item: T) -> int:
        for i in range(self.count):
            if self.items[i] == item:
                return i
        return -1

    def remove(self, index: int) -> None:
        if index < self.count:
            self.count -= 1
            if index != self.count:
                self.items[index : self.count] = self.items[index + 1 : self.count + 1]
            self.items[self.count] = None

    def ensure_capacity(self, count: int) -> None:
        if len(self.items) < count:
            self.items += [None] * (count - len(self.items))

    def __iter__(self) -> Iterator[T]:
        for i in range(self.count):
            yield self.items[i]  # type: ignore

    def __repr__(self) -> str:
        return repr(self.items[: self.count])
