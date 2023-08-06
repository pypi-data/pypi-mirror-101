import abc
from typing import *
from typing import IO, BinaryIO
from io import UnsupportedOperation
import logging


class ScpiTransportBase(IO):
    # attribute default values
    transport_name: str = None
    transport_info: str = None
    transport_type: str = None

    encoding: str = 'iso-8859-15'
    newline: str = '\r\n'

    io: BinaryIO = None
    logger: logging.Logger

    @classmethod
    @abc.abstractmethod
    def discover(cls, **kwargs):
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__()

    def read(self, n: int = -1) -> Union[bytes, bytearray]:
        self.logger.debug(f'read: block with size of {n} bytes')
        return self.io.read(n)

    def write(self, s: Union[bytes, bytearray]) -> int:
        n = self.io.write(s)
        self.io.flush()
        self.logger.debug(f'write: block with size of {n} bytes')
        return n

    def readline(self, size: int = -1) -> str:
        data = self.io.readline(size)
        self.logger.debug(f'read line {str(bytes(data))[1:]}')
        return data.decode(self.encoding).rstrip(self.newline)

    def writeline(self, line: str) -> None:
        data = (line + self.newline).encode(self.encoding)
        self.logger.debug(f'write line {str(bytes(data))[1:]}')
        self.io.writelines([data])
        self.io.flush()

    def readlines(self, hint: int = ...) -> List[AnyStr]:
        raise UnsupportedOperation

    def writelines(self, lines: Iterable[AnyStr]) -> None:
        raise UnsupportedOperation

    def close(self) -> None:
        self.io.close()

    @property
    def closed(self) -> bool:
        return self.io.closed

    @property
    def mode(self) -> str:
        return self.io.mode

    @property
    def name(self) -> str:
        return self.io.name

    def isatty(self) -> bool:
        return self.io.isatty()

    def fileno(self) -> int:
        return self.io.fileno()

    def flush(self) -> None:
        return self.io.flush()

    def readable(self) -> bool:
        return self.io.readable()

    def seek(self, offset: int, whence: int = 0) -> int:
        return self.io.seek(offset, whence)

    def seekable(self) -> bool:
        return self.io.seekable()

    def tell(self) -> int:
        return self.io.tell()

    def truncate(self, size: Optional[int] = ...) -> int:
        return self.io.truncate(size)

    def writable(self) -> bool:
        return self.io.writable()

    def __next__(self) -> AnyStr:
        return self.io.__next__()

    def __iter__(self) -> Iterator[AnyStr]:
        return self.io.__iter__()

    def __enter__(self) -> IO[AnyStr]:
        return self.io.__enter__()

    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException],
                 traceback) -> Optional[bool]:
        return self.io.__exit__(t, value, traceback)

    def __del__(self):
        if self.io is not None:
            del self.io
        del self.logger

# TypeVar for type hinting subclasses of ScpiTransportBase
ScpiTransports = TypeVar('ScpiTransports', bound=ScpiTransportBase)
