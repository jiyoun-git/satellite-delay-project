import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"  # 한글 폰트 (윈도우: 맑은 고딕)
plt.rcParams["axes.unicode_minus"] = False

C = 299792.458  # 광속 (km/s)

# ── 1. 지구 안: rtt_results.csv 평균 (handshake_time.py와 같은 방식) ──
df = pd.read_csv("rtt_results.csv")
df = df[df["trial"] != 1].dropna(subset=["time_ms"])
avg = df.groupby(["server", "country"])["time_ms"].mean().reset_index()
cdn_suspects = ["nus.edu.sg", "sorbonne-universite.fr", "auckland.ac.nz",
                "utoronto.ca", "mit.edu"]
domestic = avg[avg["country"] == "한국"]
overseas = avg[avg["country"] != "한국"]
overseas_clean = overseas[~overseas["server"].isin(cdn_suspects)]

# ── 2. 달·화성: 거리로 RTT 계산 ──
rtts = {
    "지구 안\n국내": domestic["time_ms"].mean() / 1000,
    "지구 안\n해외 전체": overseas["time_ms"].mean() / 1000,
    "지구 안\n해외(CDN 제외)": overseas_clean["time_ms"].mean() / 1000,
    "달": 371_236 / C * 2,
    "화성\n가까울 때": 56_909_620 / C * 2,
    "화성\n멀 때": 400_190_463 / C * 2,
}


def fmt(sec):
    if sec < 1:
        return f"{sec * 1000:,.1f} ms"
    if sec < 60:
        return f"{sec:,.2f} 초"
    return f"{sec / 60:,.1f} 분"


# ── 3. 비교 표 (클라이언트 1 RTT / 서버 1.5 RTT) ──
base = rtts["지구 안\n국내"]
print(f"{'구분':<18}{'클라이언트(1 RTT)':>18}{'서버(1.5 RTT)':>16}{'국내 대비':>12}")
for name, rtt in rtts.items():
    print(f"{name.replace(chr(10), ' '):<16}{fmt(rtt):>16}{fmt(rtt * 1.5):>16}{rtt / base:>11,.0f}배")

# ── 4. 그래프: 값 차이가 너무 커서 세로축을 로그 스케일로 ──
names = list(rtts)
values = [v for v in rtts.values()]
colors = ["#4C78A8"] * 3 + ["#F58518"] + ["#E45756"] * 2

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(names, values, color=colors)
ax.set_yscale("log")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))  # 10^-1 대신 0.1처럼 표시
ax.axhline(127, color="gray", linestyle="--", linewidth=1)
ax.text(-0.4, 127 * 1.15, "리눅스 기본 SYN 포기 시간 (127초)", ha="left", fontsize=9, color="gray")
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, v * 1.2, fmt(v), ha="center", fontsize=9)
ax.set_ylabel("handshake 완료 시간, 클라이언트 기준 1 RTT (초, 로그 스케일)")
ax.set_title("지구 안·달·화성의 TCP handshake 완료 시간 비교")
ax.set_ylim(top=max(values) * 6)
plt.tight_layout()
plt.savefig("handshake_compare.png", dpi=150)
plt.show()
