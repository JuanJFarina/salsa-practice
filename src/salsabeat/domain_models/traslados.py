from .positions import Positions
from .steps import Step

dile_que_no = Step(
    name="Dile que no",
    start_position=[Positions.CERRADA_AGARRADA, Positions.CERRADA_SUELTA],
    end_position=[Positions.ABIERTA],
)

dile_que_no_giro = Step(
    name="Dile que no con giro",
    start_position=[Positions.CERRADA_AGARRADA, Positions.CERRADA_SUELTA],
    end_position=[Positions.ABIERTA],
)

desplazamiento = Step(
    name="Desplazamiento",
    start_position=[Positions.CERRADA_AGARRADA, Positions.CERRADA_SUELTA],
    end_position=[Positions.CERRADA],
)

tornillo = Step(
    name="Tornillo",
    start_position=[Positions.CERRADA_AGARRADA, Positions.CERRADA_SUELTA],
    end_position=[Positions.BASICAS],
)

tornillo_con_freno = Step(
    name="Tornillo con freno",
    start_position=[Positions.OPUESTA],
    end_position=[Positions.BASICAS],
)

dile_que_si = Step(
    name="Dile que si",
    start_position=[Positions.CERRADA_AGARRADA],
    end_position=[Positions.CERRADA],
)

prima_cerrada = Step(
    name="Prima",
    start_position=[Positions.CERRADA_AGARRADA],
    end_position=[Positions.ABIERTA_IZQUIERDA],
)

prima_abierta = Step(
    name="Prima",
    start_position=[Positions.ABIERTA_IZQUIERDA],
    end_position=[Positions.ABIERTA_IZQUIERDA],
)

hermana = Step(
    name="Hermana",
    start_position=[Positions.ABIERTA_IZQUIERDA],
    end_position=[Positions.BASICAS],
)
