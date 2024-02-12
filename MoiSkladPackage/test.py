import asyncio

dict_1 = dict({"a": "x", "b": "y"})
dict_2 = dict({"x": 5, "y": 6})
res = {t: dict_2[l] for t, l in dict_1.items()}
print(res)