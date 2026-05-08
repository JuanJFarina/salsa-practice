from enum import Enum


class Basicas:
    """Basic positions don't require previous steps and can be arranged immediately inbetween steps"""


class Setenta:
    """Setenta position require the specific setup for setenta moves"""


class Frenada:
    """Frenada position require the partner to be setup backwards to you"""


class Espalda:
    """Espalda position requires you to be setup backwards to your partner"""


class Opuesta:
    """Opuesta position is a hugging position where you grab the partner's left hand with yours, thus requiring a specific setup"""


class Cerrada(Basicas):
    """Cerrada positions involve non-setup hugging positions"""


class Abierta(Basicas):
    """Abierta positions involve non-setup open positions"""


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


class Positions(Enum):
    BASICAS = Basicas()
    ABIERTA = Abierta()
    SETENTA = Setenta()
    CERRADA = Cerrada()
    FRENADA = Frenada()
    ESPALDA = Espalda()
    OPUESTA = Opuesta()
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
