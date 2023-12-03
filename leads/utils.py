from copy import copy as _copy
from typing import TextIO as _TextIO, TypeVar as _TypeVar, Generic as _Generic, Sequence as _Sequence, \
    Callable as _Callable

from numpy import mean as _mean

T = _TypeVar("T")

Compressor = _Callable[[list[T], int], list[T]]
Stringifier = _Callable[[T], str]


def mean_compressor(sequence: list[T], target_size: int) -> list[T]:
    chunk_size = int(len(sequence) / target_size)
    if chunk_size < 2:
        return sequence
    r = []
    for i in range(target_size - 1):
        r.append(_mean(sequence[i * chunk_size: (i + 1) * chunk_size]))
    r.append(_mean(sequence[(target_size - 1) * chunk_size:]))
    return r


def csv_stringifier(element: T) -> str:
    return str(element) + ","


class DataPersistence(_Sequence, _Generic[T]):
    def __init__(self,
                 file: str | _TextIO,
                 max_size: int = -1,
                 chunk_scale: int = 1,
                 compressor: Compressor = mean_compressor,
                 stringifier: Stringifier = csv_stringifier):
        self._file: _TextIO = open(file, "a") if isinstance(file, str) else file
        self._max_size: int = max_size
        self._chunk_scale: int = chunk_scale
        self._compressor: Compressor = compressor
        self._stringifier: Stringifier = stringifier
        self._data: list[T] = []
        self._chunk: list[T] = []
        self._chunk_size: int = chunk_scale

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, item: slice) -> T | list[T]:
        return self._data[item]

    def __str__(self) -> str:
        return str(self._data)

    def close(self):
        self._file.close()

    def get_chunk_size(self) -> int:
        return self._chunk_size

    def to_list(self) -> list[T]:
        return _copy(self._data)

    def get_chunk(self) -> list[T]:
        return _copy(self._chunk)

    def _push_to_data(self, element: T):
        self._data.append(element)
        if self._max_size < 2:
            return
        if len(self._data) >= self._max_size:
            self._data = self._compressor(self._data, int(len(self._data) * .5))
            self._chunk_size *= 2

    def append(self, element: T):
        self._file.write(self._stringifier(element))
        if self._chunk_size == 1:
            return self._push_to_data(element)
        self._chunk.append(element)
        if len(self._chunk) >= self._chunk_size:
            for e in self._compressor(self._chunk, self._chunk_scale):
                self._push_to_data(e)
            self._chunk.clear()