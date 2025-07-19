import pandas as pd

file_path = "TOTAL_sp_ta_medical_ifo.csv"

# Read the CSV file
df = pd.read_csv(file_path, encoding= "euc-kr")
print(df.head())
print(df.columns)
print(df.shape)
print(df.info())

# '종별코드명' 열에 '약국'이라는 단어가 있는 행만 선택
df_pharmacy = df[df['종별코드명'].str.contains('약국', na=False)]

print(df_pharmacy.head())  # 잘 필터링됐는지 앞부분만 확인!

# '시군구명' 열에 '천안서북구'만 선택
df_seobuk = df_pharmacy[df_pharmacy['시군구명'] == '천안서북구']

print(df_seobuk.head())  # 잘 필터링됐나 확인!

# 저장 예시
df_seobuk.to_csv("cheonan_seobuk_pharmacy.csv", index=False, encoding="utf-8-sig")

