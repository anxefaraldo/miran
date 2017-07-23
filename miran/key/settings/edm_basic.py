# ================================ #
# KEY ESTIMATION ANALYSIS SETTINGS #
# ================================ #



# Analysis Parameters
# -------------------
SAMPLE_RATE = 44100
DETUNING_CORRECTION = False
PCP_THRESHOLD = None
WINDOW_SIZE = 4096
HOP_SIZE = 4096
WINDOW_SHAPE = 'hann'
MIN_HZ = 27.5  # A-1
MAX_HZ = 3500  # 7 octavas
HPCP_SIZE = 12
HPCP_REFERENCE_HZ = 440
HPCP_WEIGHT_WINDOW_SEMITONES = 1  # semitones
HPCP_WEIGHT_TYPE = 'cosine'  # {'none', 'cosine', 'squaredCosine'}
HPCP_NORMALIZE = False

# Scope and Key Detector Method
# -----------------------------
DURATION = None  # analyse first n seconds of each track (None = full track)
OFFSET = 0
ANALYSIS_TYPE = 'global'  # {'local', 'global'}
N_WINDOWS = 100  # if ANALYSIS_TYPE is 'local'
WINDOW_INCREMENT = 100  # if ANALYSIS_TYPE is 'local'
KEY_PROFILE = 'krumhansl'
USE_THREE_PROFILES = False
WITH_MODAL_DETAILS = False
