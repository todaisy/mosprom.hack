import pandas as pd, sys
p = "classifier.csv"
df = pd.read_csv(p)
need_cols = {"text","label"}
assert need_cols.issubset(df.columns), f"Нужны колонки {need_cols}, нашли {set(df.columns)}"
bad = df[~df["label"].isin(["it","hr","buh"])]
print("Размер:", len(df))
print("Распределение:\n", df["label"].value_counts())
if not bad.empty:
    print("\n⚠️ Некорректные метки (исправь на it/hr/buh):")
    print(bad[["text","label"]].head(20).to_string(index=False))