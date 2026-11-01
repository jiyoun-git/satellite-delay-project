from skyfield.api import load

C = 299792.458  # 광속 (km/s)

# 1. 시간 도구와 천체력(행성·달 위치 데이터) 불러오기
ts = load.timescale()
eph = load("de421.bsp")  # 처음 실행하면 자동으로 다운로드됨 (약 17MB)

earth = eph["earth"]
moon = eph["moon"]

# 2. 지금 이 순간, 지구에서 달을 바라봤을 때의 거리
t = ts.now()
distance_km = earth.at(t).observe(moon).distance().km

# 3. 거리 ÷ 광속 = 편도 전파 지연, 왕복은 2배
one_way_s = distance_km / C
round_trip_s = one_way_s * 2

print(f"측정 시각(UTC): {t.utc_strftime('%Y-%m-%d %H:%M:%S')}")
print(f"지구-달 거리: {distance_km:,.0f} km")
print(f"편도 지연: {one_way_s:.3f} 초")
print(f"왕복(RTT) 지연: {round_trip_s:.3f} 초")
