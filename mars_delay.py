import numpy as np
from skyfield.api import load

C = 299792.458  # 광속 (km/s)

ts = load.timescale()
eph = load("de421.bsp")  # 달 때 받아둔 파일을 재사용함

earth = eph["earth"]
# de421에는 화성이 '화성계 무게중심'으로 들어 있음 (화성 본체와 차이는 아주 작음)
mars = eph["mars barycenter"]


def distance_km(t):
    """시각 t에 지구에서 화성을 바라봤을 때의 거리(km)"""
    return earth.at(t).observe(mars).distance().km


# 1. 지금 이 순간의 거리와 지연
d_now = distance_km(ts.now())
print("[지금]")
print(f"지구-화성 거리: {d_now:,.0f} km")
print(f"편도 지연: {d_now / C / 60:.1f} 분")
print(f"왕복(RTT) 지연: {d_now / C * 2 / 60:.1f} 분")

# 2. 2026년부터 약 15년간 하루 간격으로 거리를 구해 가장 가까울 때와 가장 멀 때를 찾기
days = 365 * 15
times = ts.utc(2026, 1, range(1, days + 1))
dists = distance_km(times)

i_min = int(np.argmin(dists))
i_max = int(np.argmax(dists))

print()
print("[2026~2040 범위에서 가장 가까울 때]")
print(f"날짜: {times[i_min].utc_strftime('%Y-%m-%d')}")
print(f"거리: {dists[i_min]:,.0f} km")
print(f"편도 지연: {dists[i_min] / C / 60:.1f} 분")

print()
print("[2026~2040 범위에서 가장 멀 때]")
print(f"날짜: {times[i_max].utc_strftime('%Y-%m-%d')}")
print(f"거리: {dists[i_max]:,.0f} km")
print(f"편도 지연: {dists[i_max] / C / 60:.1f} 분")
