from enum import Enum


class Position: ...


class Cerrada(Position): ...


class Abierta(Position): ...


class Frenada(Position): ...


class Espalda(Position): ...


class Agarrada(Cerrada): ...


class Suelta(Cerrada): ...


class Paralelas(Abierta): ...


class Izquierda(Abierta): ...


class Derecha(Abierta): ...


class DerechaOpuesta(Abierta): ...


class IzquierdaOpuesta(Abierta): ...


class DerechaAmbasOpuestas(Abierta): ...


class IzquierdaAmbasOpuestas(Abierta): ...


class DerechaAmbasCruzadas(Abierta): ...


class IzquierdaAmbasCruzadas(Abierta): ...


class Setenta(Abierta): ...


class Positions(Enum):
    POSITION = Position()
    ABIERTA = Abierta()
    CERRADA = Cerrada()
    FRENADA = Frenada()
    ESPALDA = Espalda()
    CERRADA_AGARRADA = Agarrada()
    CERRADA_SUELTA = Suelta()
    ABIERTA_PARALELAS = Paralelas()
    ABIERTA_IZQUIERDA = Izquierda()
    ABIERTA_DERECHA = Derecha()
    ABIERTA_IZQUIERDA_OPUESTA = IzquierdaOpuesta()
    ABIERTA_DERECHA_OPUESTA = DerechaOpuesta()
    ABIERTA_IZQUIERDA_AMBAS_OPUESTAS = IzquierdaAmbasOpuestas()
    ABIERTA_DERECHA_AMBAS_OPUESTAS = DerechaAmbasOpuestas()
    ABIERTA_IZQUIERDA_AMBAS_CRUZADAS = IzquierdaAmbasCruzadas()
    ABIERTA_DERECHA_AMBAS_CRUZADAS = DerechaAmbasCruzadas()
    ABIERTA_SETENTA = Setenta()
