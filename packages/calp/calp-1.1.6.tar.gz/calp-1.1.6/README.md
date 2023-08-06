# Calp - The easy calculation package

## Overview
Calp is a simple python package which is able to identify what calculation the user wants to do in a clean way

## Install
```cmd
pip install calp
```

### Quickstart
```python
import calp

exp0 = "43+32"
exp1 = "43-32"
exp2 = "43*32"
exp3 = "43/32"

for x in range(0, 4):
    print(calp.find(eval(f"exp{x}")))

# 75
# 11
# 1376
# 1.34375
```