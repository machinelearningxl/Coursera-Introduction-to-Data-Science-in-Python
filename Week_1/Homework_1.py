# @Author: Antero Maripuu Github:<machinelearningxl>
# @Date : 2019-07-15 17:55
# @Email:  antero.maripuu@gmail.com
# @Project: Coursera
# @Filename : Homework_1.py

import numpy as np
import pandas as pd

df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
print(df)
print()

print(df.rename(index=str, columns={"A": "a", "B": "c"}))