import pandas as pd

C = 299792.458  # 광속 (km/s)

# ── 1. 지구 안: 5주차에 측정한 rtt_results.csv에서 평균 연결 시간 구하기 ──
df = pd.read_csv("rtt_results.csv")
df = df[df["trial"] != 1]              # 1차 시도(DNS 조회 포함) 제외
df = df.dropna(subset=["time_ms"])     # 측정 실패한 서버 제외
avg = df.groupby(["server", "country"])["time_ms"].mean().reset_index()

# 6주차에서 광속 한계선보다 빠르게 나와 CDN이 의심된 서버 5곳
cdn_suspects = ["nus.edu.sg", "sorbonne-universite.fr", "auckland.ac.nz",
                "utoronto.ca", "mit.edu"]

domestic = avg[avg["country"] == "한국"]
overseas = avg[avg["country"] != "한국"]
overseas_clean = overseas[~overseas["server"].isin(cdn_suspects)]

# 연결 시간(connect()가 끝나기까지)은 거의 1 RTT이므로 평균값을 그대로 RTT로 사용 (ms -> 초)
earth = {
    f"지구 안 - 국내 평균 ({len(domestic)}곳)": domestic["time_ms"].mean() / 1000,
    f"지구 안 - 해외 전체 평균 ({len(overseas)}곳)": overseas["time_ms"].mean() / 1000,
    f"지구 안 - 해외 평균, CDN 의심 제외 ({len(overseas_clean)}곳)": overseas_clean["time_ms"].mean() / 1000,
}

# ── 2. 달·화성: 9주차에서 구한 거리로 왕복 시간(RTT) 계산 ──
space_km = {
    "달 (오늘 기준)": 371_236,
    "화성 - 가장 가까울 때 (2035-09-12)": 56_909_620,
    "화성 - 가장 멀 때 (2034-08-20)": 400_190_463,
}
space = {name: d / C * 2 for name, d in space_km.items()}  # 편도 x 2 = RTT

rtts = {**earth, **space}


def fmt(sec):
    if sec < 1:
        return f"{sec * 1000:,.1f} ms"
    if sec < 60:
        return f"{sec:,.2f} 초"
    return f"{sec / 60:,.1f} 분"


# ── 3. handshake 완료 시간 계산 ──
# 클라이언트 기준: SYN 보냄 -> SYN+ACK 받음 = 1 RTT  (connect()가 끝나는 시점)
# 서버 기준: 마지막 ACK까지 도착해야 연결 확립 = 1.5 RTT
base = rtts[list(earth)[0]]  # 국내 평균을 기준(1배)으로 삼음

print(f"{'구분':<42}{'RTT':>12}{'클라이언트 1 RTT':>18}{'서버 1.5 RTT':>16}{'국내 대비':>12}")
for name, rtt in rtts.items():
    print(f"{name:<40}{fmt(rtt):>12}{fmt(rtt):>18}{fmt(rtt * 1.5):>16}{rtt / base:>11,.0f}배")
