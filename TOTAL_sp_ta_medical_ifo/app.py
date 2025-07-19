# ----------------------------------------
# 📂 폐의약품 수거 약국 찾기 Streamlit 예제
# ----------------------------------------

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# ----------------------------------------
# 1) 페이지 기본 설정
# ----------------------------------------
# 웹 브라우저 탭 이름, 아이콘, 화면 레이아웃 넓게 설정!
st.set_page_config(
    page_title="폐의약품 수거 약국 찾기",
    page_icon="💊",
    layout="wide"
)

# 화면에 큰 제목과 설명문 쓰기!
st.title("💊 폐의약품 수거 약국 찾기")
st.markdown("원하는 폐의약품을 선택하면 해당 약국을 표와 지도에서 확인할 수 있어요!")

# ----------------------------------------
# 2) CSV 데이터 불러오기 함수
# ----------------------------------------
# @st.cache_data : 데이터 기억해서 새로고침해도 빨라요!
@st.cache_data
def load_data():
    # 저장한 CSV 파일을 utf-8-sig로 읽어오기
    df = pd.read_csv("cheonan_seobuk_pharmacy_with_items.csv", encoding="utf-8-sig")
    return df

df = load_data()

# ----------------------------------------
# 3) 수거약품목 카테고리 만들기
# CSV에 들어있는 모든 수거약품목을 한 번에 모아서 중복 없이!
# ----------------------------------------
all_items = []
# '수거약품목' 열의 값들을 쉼표로 나눠서 리스트에 넣기
df['수거약품목'].dropna().apply(lambda x: all_items.extend([i.strip() for i in x.split(',')]))
# set() 으로 중복 제거 후 다시 리스트로
categories = list(sorted(set(all_items)))

# ----------------------------------------
# 4) 체크박스로 약품목 선택하기
# ----------------------------------------
st.subheader("♻️ 수거 약품목 선택 (최대 3개)")
cols = st.columns(3)  # 3열로 체크박스 배치
selected = []  # 선택된 약품목 저장할 리스트

# 카테고리 하나씩 돌면서 체크박스 만들기!
for i, cat in enumerate(categories):
    if cols[i % 3].checkbox(cat):
        selected.append(cat)

# 선택한 약품목이 3개 초과면 오류 메시지 출력!
if len(selected) > 3:
    st.error("❗ 최대 3개까지만 선택할 수 있어요.")
    selected = selected[:3]  # 3개 초과되면 잘라버리기

# ----------------------------------------
# 5) 선택된 약품목으로 데이터 필터링
# ----------------------------------------
if selected:
    # 수거약품목에 선택된 단어 중 하나라도 들어있는 데이터만 남기기
    mask = df['수거약품목'].apply(lambda x: any(tag in str(x) for tag in selected))
    result = df[mask]

    # 선택 결과 요약 메시지
    st.success(f"선택한 약품목: {selected} → 약국 {len(result)}곳")

    # 필터링된 약국 표 보여주기
    st.dataframe(result[['병원명', '주소', '전화번호', '수거약품목']], use_container_width=True)

    # ----------------------------------------
    # 6) 지도에 선택된 약국 위치 표시
    # ----------------------------------------
    st.subheader("📍 약국 위치 지도")

    # 위도/경도 값 없는 데이터는 제외
    coords = result.dropna(subset=['위도', '경도'])

    if not coords.empty:
        # folium으로 빈 지도 만들기
        m = folium.Map()

        # 선택된 좌표 범위로 지도를 딱 맞게 확대/축소
        bounds = [
            [coords['위도'].min(), coords['경도'].min()],
            [coords['위도'].max(), coords['경도'].max()]
        ]
        m.fit_bounds(bounds)

        # 약국 하나씩 돌면서 핀 꽂기!
        for _, row in coords.iterrows():
            folium.Marker(
                [row['위도'], row['경도']],  # 핀 찍을 위치
                popup=f"{row['병원명']}<br>{row['수거약품목']}",  # 클릭하면 말풍선
                tooltip=row['병원명']  # 마우스 올리면 이름 보이기
            ).add_to(m)

        # 완성된 지도 Streamlit에 띄우기!
        folium_static(m, width=800, height=500)
    else:
        # 위치 좌표가 없으면 안내 메시지
        st.info("위치 정보가 없습니다!")

else:
    # 아무 약품목도 선택 안 했으면 안내 메시지
    st.info("위쪽에서 수거 약품목을 선택해주세요!")
