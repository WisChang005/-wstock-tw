# WStock Taiwan - 台灣股票小工具

### 取得當前開盤狀態

```python3
from wstock_tw import wstock

wstock.open_state  # True or False
```


### 股票類型屬於 - 上市(TWSE) 或 上櫃(TPEX)

```python3
from wstock_tw import wstock

# 益登科技
"3048" in wstock.tpex
"3048" in wstock.twse
```