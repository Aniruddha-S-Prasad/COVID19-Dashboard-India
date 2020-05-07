import numpy as np
from typing import NamedTuple


class DataContainer(NamedTuple):
    dates: list
    offset_days: int
    np_data: np.ndarray
    members = {'total_count': 0,
               'active_cases': 1,
               'beta': 2,
               'gamma': 3,
               'reproductive_number': 4}