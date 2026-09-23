import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")


# --------------------------------------------------
# 데이터 주소
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/"
    "greatsong/modudata/main/data/kobis_movies.csv"
)


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일을 날짜형으로 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 여러 장르가 "|" 또는 "/"로 연결된 경우
    # 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split(r"[|/]")
        .str[0]
        .str.strip()
    )

    # 빈 장르는 미상으로 처리
    df.loc[
        df["genre"].isin(["", "nan", "None"]),
        "genre"
    ] = "미상"

    return df


# --------------------------------------------------
# 데이터 로드
# --------------------------------------------------
try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.code(str(e))
    st.stop()


st.caption(
    f"1년간 박스오피스 10위권에 든 영화 중 "
    f"이 기간에 개봉한 {len(df):,}편의 영화 데이터입니다."
)


# ==================================================
# 그래프 1
# ==================================================
st.header("1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화편수"]


fig = px.pie(
    genre_count,
    names="장르",
    values="영화편수",
    hole=0.5,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    legend_title_text="장르",
    margin=dict(
        t=60,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# 그래프로 알 수 있는 것
# --------------------------------------------------
st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "1년간 10위권에 진입한 영화가 어떤 장르에 많이 분포했는지 알 수 있습니다."
)


# --------------------------------------------------
# 원본 데이터
# --------------------------------------------------
with st.expander("📋 데이터 원본 보기"):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
