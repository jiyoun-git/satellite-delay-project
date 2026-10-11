import pandas as pd
from math import radians, sin, cos, asin, sqrt

# 측정 기준점: 서울 (우리 컴퓨터가 있는 위치)
ORIGIN_LAT, ORIGIN_LON = 37.5665, 126.9780

# 각 도시의 위도, 경도 (location 열의 이름과 맞춰둠)
CITY_COORDS = {
    "서울": (37.5665, 126.9780),
    "대전": (36.3504, 127.3845),
    "청주": (36.6424, 127.4890),
    "도쿄": (35.6762, 139.6503),
    "베이징": (39.9042, 116.4074),
    "뭄바이": (19.0760, 72.8777),
    "싱가포르": (1.3521, 103.8198),
    "옥스퍼드": (51.7520, -1.2577),
    "뮌헨": (48.1351, 11.5820),
    "파리": (48.8566, 2.3522),
    "모스크바": (55.7558, 37.6173),
    "볼로냐": (44.4949, 11.3426),
    "케임브리지": (42.3736, -71.1097),
    "스탠퍼드": (37.4275, -122.1697),
    "토론토": (43.6532, -79.3832),
    "멕시코시티": (19.4326, -99.1332),
    "상파울루": (-23.5505, -46.6333),
    "부에노스아이레스": (-34.6037, -58.3816),
    "케이프타운": (-33.9249, 18.4241),
    "카이로": (30.0444, 31.2357),
    "라고스": (6.5244, 3.3792),
    "시드니": (-33.8688, 151.2093),
    "오클랜드": (-36.8485, 174.7633),
}


def haversine_km(lat1, lon1, lat2, lon2):
    """두 지점(위도, 경도) 사이의 지구 표면 거리(km)를 구하는 함수. 하버사인 공식 사용."""
    R = 6371  # 지구 반지름(km)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


df = pd.read_csv("avg_by_server.csv")

# location(도시 이름)을 기준으로 거리(km) 계산해서 새 열로 추가
df["distance_km"] = df["location"].apply(
    lambda city: round(haversine_km(ORIGIN_LAT, ORIGIN_LON, *CITY_COORDS[city]), 1)
)

# 거리순으로 정렬해서 보기 좋게 출력
df_sorted = df.sort_values("distance_km")
print(df_sorted)

df_sorted.to_csv("avg_with_distance.csv", index=False)
print("\n완료! avg_with_distance.csv 파일에 저장되었습니다.")
