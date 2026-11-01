import math

C = 299792.458       # 광속 (km/s)
R = 6371             # 지구 반지름 (km)

satellites = {
    "저궤도 (550 km)": 550,
    "정지궤도 (35,786 km)": 35786,
}

# 앙각: 지상에서 위성을 올려다보는 각도 (90도 = 머리 바로 위, 0도 = 지평선)
elevations = [90, 60, 45, 30, 10]


def slant_range_km(altitude_km, elevation_deg):
    """지상 관측자에서 위성까지의 실제 직선 거리(km)"""
    e = math.radians(elevation_deg)
    return math.sqrt((R + altitude_km) ** 2 - (R * math.cos(e)) ** 2) - R * math.sin(e)


for name, h in satellites.items():
    print(f"[{name}]")
    for elev in elevations:
        d = slant_range_km(h, elev)
        one_hop_ms = d / C * 1000
        print(f"  앙각 {elev:>2}도: 거리 {d:>9,.0f} km, 지상->위성 {one_hop_ms:7.2f} ms")
    print()
