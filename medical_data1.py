# ----------------------------------------
# 📌 1) pandas 도구 불러오기
# ----------------------------------------
import pandas as pd

# ----------------------------------------
# 📌 2) CSV 파일 경로 설정 & 불러오기
# ----------------------------------------
# 파일 경로: 같은 폴더에 있으면 파일명만!
file_path = "cheonan_seobuk_pharmacy.csv"

# CSV 파일 열기 (한글 깨짐 방지)
df = pd.read_csv(file_path, encoding="utf-8-sig")

# ----------------------------------------
# 📌 3) 표가 잘 열렸는지 확인하기
# ----------------------------------------
print("\n✅ [데이터 앞부분 미리보기]")
print(df.head())

# ----------------------------------------
# 📌 4) 열 이름(컬럼) 확인
# ----------------------------------------
print("\n✅ [열 이름]")
print(df.columns)

# ----------------------------------------
# 📌 5) 표 크기 확인 (행, 열)
# ----------------------------------------
print("\n✅ [데이터 크기]")
print(df.shape)  # (행, 열)

# ----------------------------------------
# 📌 6) 데이터 요약 정보 확인 (데이터 타입 & 결측치)
# ----------------------------------------
print("\n✅ [데이터 요약 정보]")
print(df.info())

# ----------------------------------------
# 📌 7) 결측치(빈칸) 개수 확인
# ----------------------------------------
print("\n✅ [결측치 개수]")
print(df.isnull().sum())

# ----------------------------------------
# 📌 8) 약국 이름만 고유하게 확인
# ----------------------------------------
print("\n✅ [약국 이름 목록]")
print(df['병원명'].unique())

# ----------------------------------------
# 📌 9) 위도/경도가 없는 약국만 확인
# ----------------------------------------
missing_coords = df[df['위도'].isnull() | df['경도'].isnull()]

print("\n✅ [위도/경도 없는 약국]")
print(missing_coords)

# ----------------------------------------
# 📌 10) 위도/경도가 있는 약국만 따로 저장하기
# ----------------------------------------
filtered = df.dropna(subset=['위도', '경도'])

print(f"\n✅ [위도/경도 있는 약국 개수] : {filtered.shape[0]}개")

# 새 파일로
