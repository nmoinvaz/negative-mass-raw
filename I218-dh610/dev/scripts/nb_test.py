import numpy as np
from pol import *
y = np.random.randn(8)
try:
    print(rhs4(2.0, y, 0.49, 6.0, -0.3, 0.19)[:3])
except Exception as e:
    import traceback; traceback.print_exc()
try:
    print(rhs4(np.float64(2.0), y, 0.49, 6.0, -0.3, 0.19)[:3])
except Exception as e:
    print("np.float64 version failed:", type(e), e)
