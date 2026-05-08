from .positions import Positions
from .steps import Step

giro_simple = Step(  # no prepara para enchufa
    name="Giro simple",
    start_position=[
        Positions.ABIERTA_IZQUIERDA,
        Positions.ABIERTA_DERECHA,
        Positions.ABIERTA_IZQUIERDA_OPUESTA,
        Positions.ABIERTA_DERECHA_OPUESTA,
    ],
    end_position=[Positions.BASICAS],
)

giro_enchufa = Step(  # prepara para enchufa
    name="Giro para enchufa",
    start_position=[
        Positions.ABIERTA_IZQUIERDA,
        Positions.ABIERTA_DERECHA,
        Positions.ABIERTA_IZQUIERDA_OPUESTA,
        Positions.ABIERTA_DERECHA_OPUESTA,
    ],
    end_position=[Positions.BASICAS],
)

giro_setenta = Step(
    name="Giro de setenta",
    start_position=[Positions.ABIERTA_PARALELAS, Positions.FRENADA],
    end_position=[Positions.SETENTA],
)

giro_sombrero = Step(
    name="Giro de sombrero",
    start_position=[Positions.ABIERTA_DERECHA_AMBAS_OPUESTAS],
    end_position=[Positions.ABIERTA_IZQUIERDA_AMBAS_OPUESTAS],
)

cosela = Step(
    name="Cosela",
    start_position=[Positions.ABIERTA_DERECHA_AMBAS_OPUESTAS],
    end_position=[Positions.CERRADA],
)

giro_juntos = Step(
    name="Giro juntos",
    start_position=[Positions.ABIERTA_DERECHA_OPUESTA],
    end_position=[Positions.ABIERTA],
)

giro_pidiendo_mano = Step(
    name="Giro pidiendo mano",
    start_position=[Positions.ABIERTA_IZQUIERDA],
    end_position=[Positions.ABIERTA_DERECHA],
)
