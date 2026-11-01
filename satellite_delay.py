C = 299792.458  # 광속 (km/s)

# 위성 종류별 고도 (km). 지상 바로 위(천정)에 위성이 있다고 가정한 가장 단순한 경우
satellites = {
    "저궤도 (LEO, 예: 스타링크)": 550,
    "정지궤도 (GEO)": 35786,
}

for name, altitude_km in satellites.items():
    # 지상 -> 위성 한 구간의 편도 지연
    one_hop_s = altitude_km / C
    # 지상 -> 위성 -> 지상: 위성이 중계해서 반대편 지상으로 데이터를 전달하는 한 방향 경로
    one_way_s = one_hop_s * 2
    # 요청을 보내고 응답을 받는 왕복(RTT): 위 경로를 두 번 지남
    rtt_s = one_way_s * 2

    print(f"[{name}] 고도 {altitude_km:,} km")
    print(f"  지상 -> 위성 (한 구간): {one_hop_s * 1000:.2f} ms")
    print(f"  지상 -> 위성 -> 지상 (한 방향): {one_way_s * 1000:.2f} ms")
    print(f"  왕복(RTT): {rtt_s * 1000:.2f} ms")
    print()
