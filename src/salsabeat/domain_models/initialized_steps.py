from .positions import Positions
from .steps import Step

giro_simple = Step(
    name="Giro Simple",
    start_position=[Positions.POSITION],
    end_position=[Positions.CERRADA, Positions.ABIERTA],
)

giro_setenta = Step(
    name="Giro de Setenta",
    start_position=[Positions.ABIERTA_PARALELAS, Positions.FRENADA],
    end_position=[Positions.ABIERTA_SETENTA],
)

giro_sombrero = Step(
    name="Giro de Sombrero",
    start_position=[Positions.ABIERTA_DERECHA_AMBAS_OPUESTAS],
    end_position=[Positions.ABIERTA_IZQUIERDA_AMBAS_OPUESTAS],
)

cosela = Step(
    name="Cosela",
    start_position=[Positions.ABIERTA_DERECHA_AMBAS_OPUESTAS],
    end_position=[Positions.CERRADA],
)

giro_juntos = Step(
    name="Giro Juntos",
    start_position=[Positions.ABIERTA_DERECHA_OPUESTA],
    end_position=[Positions.ABIERTA],
)
