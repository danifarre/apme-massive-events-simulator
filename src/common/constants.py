WIDTH, HEIGHT = 800, 600

# Dimensiones de las zonas
STAGE_HEIGHT = 80  # Altura del escenario (parte superior)
SIDE_ZONE_WIDTH = 150  # Ancho de cada zona lateral
SIDE_ZONE_TOTAL_HEIGHT = HEIGHT - STAGE_HEIGHT
HALF_SIDE_ZONE = SIDE_ZONE_TOTAL_HEIGHT // 2  # Para dividir zonas laterales en dos (baño y bar)

# Parámetros de comportamiento y grupos
NUM_AGENTS = 3000
GROUP_SIZE_MIN = 1
GROUP_SIZE_MAX = 5

# Probabilidad de que un grupo en la pista decida ir al baño o bar en cada frame
PROB_GROUP_MOVE = 0.001

# Probabilidad de que un agente (no líder) se separe temporalmente
PROB_SEPARATION = 0.0002

# Tiempo de separación temporal (frames) y de espera en baño/bar
SEPARATION_TIME_MIN = 60
SEPARATION_TIME_MAX = 180
WAIT_TIME_MIN = 60
WAIT_TIME_MAX = 180

# Velocidad de movimiento de los agentes
AGENT_SPEED = 2
