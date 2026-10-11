import pandas as pd
import plotly.express as px

# 각 도시의 위도, 경도 (add_distance.py에서 쓴 것과 동일)
CITY_COORDS = {
    "서울": (37.5665, 126.9780), "대전": (36.3504, 127.3845), "청주": (36.6424, 127.4890),
    "도쿄": (35.6762, 139.6503), "베이징": (39.9042, 116.4074), "뭄바이": (19.0760, 72.8777),
    "싱가포르": (1.3521, 103.8198), "옥스퍼드": (51.7520, -1.2577), "뮌헨": (48.1351, 11.5820),
    "파리": (48.8566, 2.3522), "모스크바": (55.7558, 37.6173), "볼로냐": (44.4949, 11.3426),
    "케임브리지": (42.3736, -71.1097), "스탠퍼드": (37.4275, -122.1697), "토론토": (43.6532, -79.3832),
    "멕시코시티": (19.4326, -99.1332), "상파울루": (-23.5505, -46.6333), "부에노스아이레스": (-34.6037, -58.3816),
    "케이프타운": (-33.9249, 18.4241), "카이로": (30.0444, 31.2357), "라고스": (6.5244, 3.3792),
    "시드니": (-33.8688, 151.2093), "오클랜드": (-36.8485, 174.7633),
}

df = pd.read_csv("avg_with_distance.csv")

# 측정 실패(NaN)한 서버는 지도에서 제외
df = df.dropna(subset=["avg_time_ms"])

# location(도시 이름)을 기준으로 위도, 경도 열 추가
df["lat"] = df["location"].apply(lambda city: CITY_COORDS[city][0])
df["lon"] = df["location"].apply(lambda city: CITY_COORDS[city][1])

# 지도에 서버 위치를 점으로 표시. 점 색깔 = 연결 시간(ms), 점 크기도 연결 시간에 비례
fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    color="avg_time_ms",
    size="avg_time_ms",
    hover_name="server",
    hover_data={"location": True, "distance_km": True, "avg_time_ms": ":.1f", "lat": False, "lon": False},
    color_continuous_scale="YlOrRd",  # 노란색(빠름) ~ 빨간색(느림)
    projection="natural earth",
    title="서버 위치별 평균 TCP 연결 시간 (ms)",
)

# 서울(측정 기준점)을 별도로 파란 점으로 표시
# 점 옆에 이미 이름(text)이 표시되므로 범례(legend)는 끔 - 컬러바 제목과 겹치는 것 방지
fig.add_scattergeo(
    lat=[37.5665], lon=[126.9780],
    mode="markers+text",
    marker=dict(size=14, color="blue", symbol="star"),
    text=["서울 (측정 지점)"],
    textposition="bottom center",
    name="측정 기준점",
    showlegend=False,
)

fig.update_layout(height=600, margin=dict(t=60))

fig.write_html("distance_map.html")
print("완료. distance_map.html 파일로 인터랙티브 지도 저장함.")
print("웹 브라우저로 파일 열어서 확인 후, 보고서에 넣을 화면 캡처함.")
