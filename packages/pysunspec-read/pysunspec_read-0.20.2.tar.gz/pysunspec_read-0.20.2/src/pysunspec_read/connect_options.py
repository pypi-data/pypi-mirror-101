from dataclasses import dataclass
from typing import Any


@dataclass
class ConnectOptionsTcp:
    slave_id: int = 1
    ip_address: str = None
    ip_port: int = None
    timeout: str = None
    ctx: Any = None
    max_count: int = None
    test: bool = None


@dataclass
class ConnectOptionsRtu:
    slave_id: int = 1
    name: str = None
    baudrate: str = None
    parity: str = None
    timeout: str = None
    ctx: Any = None
    max_count: int = None


@dataclass
class ConnectOptionsFile:
    name: str = None
    addr: int = 40000


@dataclass
class ConnectOptions:
    file: ConnectOptionsFile = None
    tcp: ConnectOptionsTcp = None
    rtu: ConnectOptionsRtu = None
