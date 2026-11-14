import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams["font.family"] = "Malgun Gothic"  # 한글 폰트 (윈도우: 맑은 고딕)
plt.rcParams["axes.unicode_minus"] = False

C = 299792.458  # 광속 (km/s)

# ── 1. 지구 안: rtt_results.csv에서 실제 측정한 평균 연결 시간 (≈ 1 RTT) ──
df = pd.read_csv("rtt_results.csv")
df = df[df["trial"] != 1].dropna(subset=["time_ms"])
avg = df.groupby(["server", "country"])["time_ms"].mean().reset_index()
cdn_suspects = ["nus.edu.sg", "sorbonne-universite.fr", "auckland.ac.nz",
                "utoronto.ca", "mit.edu"]
domestic = avg[avg["country"] == "한국"]
overseas = avg[avg["country"] != "한국"]
overseas_clean = overseas[~overseas["server"].isin(cdn_suspects)]

# ── 2. 위성·달·화성: 거리 ÷ 광속으로 계산한 RTT (이론상 최소값) ──
# 위성: 지상 -> 위성 -> 지상이 한 방향, 왕복(RTT)은 이 경로를 두 번 지나므로 고도 x 4
leo_rtt = 550 * 4 / C
geo_rtt = 35786 * 4 / C
moon_rtt = 371_236 * 2 / C
mars_near_rtt = 56_909_620 * 2 / C
mars_far_rtt = 400_190_463 * 2 / C

# (이름, RTT(초), 종류) - 지구에서 멀어지는 순서
rows = [
    ("지구 안\n국내", domestic["time_ms"].mean() / 1000, "측정"),
    ("지구 안\n해외 전체", overseas["time_ms"].mean() / 1000, "측정"),
    ("지구 안\n해외(CDN 제외)", overseas_clean["time_ms"].mean() / 1000, "측정"),
    ("저궤도\n(550 km)", leo_rtt, "계산"),
    ("정지궤도\n(35,786 km)", geo_rtt, "계산"),
    ("달", moon_rtt, "계산"),
    ("화성\n가까울 때", mars_near_rtt, "계산"),
    ("화성\n멀 때", mars_far_rtt, "계산"),
]


def fmt(sec):
    if sec < 1:
        return f"{sec * 1000:,.1f} ms"
    if sec < 60:
        return f"{sec:,.2f} 초"
    return f"{sec / 60:,.1f} 분"


# ── 3. 표 출력 ──
base = rows[0][1]
print(f"{'구분':<20}{'RTT':>12}{'국내 대비':>14}{'기본 SYN 재전송(RTO 1초) 기준':>32}")
for name, rtt, kind in rows:
    if rtt > 127:
        status = "연결 실패 (127초 초과)"
    elif rtt > 1:
        status = "연결 성공, 불필요한 재전송 발생"
    else:
        status = "연결 성공, 재전송 없음"
    print(f"{name.replace(chr(10), ' '):<18}{fmt(rtt):>12}{rtt / base:>13,.1f}배   {status}")

# ── 4. 그래프: 세로축 로그 스케일, 측정값은 색 채움, 계산값은 빗금 ──
colors = {"지구 안": "#4C78A8", "위성": "#54A24B", "달": "#F58518", "화성": "#E45756"}


def color_of(name):
    for key in colors:
        if name.startswith(key) or (key == "위성" and name.startswith(("저궤도", "정지궤도"))):
            return colors[key]


fig, ax = plt.subplots(figsize=(11, 5.5))
for i, (name, rtt, kind) in enumerate(rows):
    ax.bar(i, rtt, color=color_of(name), hatch="//" if kind == "계산" else None,
           edgecolor="white" if kind == "계산" else None, linewidth=0)
    ax.text(i, rtt * 1.2, fmt(rtt), ha="center", fontsize=9)

ax.set_xticks(range(len(rows)))
ax.set_xticklabels([r[0] for r in rows])
ax.set_yscale("log")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
ax.axhline(1, color="gray", linestyle=":", linewidth=1)
ax.text(-0.45, 1 * 1.15, "초기 RTO 1초", ha="left", fontsize=9, color="gray")
ax.axhline(127, color="gray", linestyle="--", linewidth=1)
ax.text(-0.45, 127 * 1.15, "리눅스 기본 SYN 포기 시간 127초", ha="left", fontsize=9, color="gray")
ax.set_ylabel("RTT (초, 로그 스케일)")
ax.set_title("지구 안·위성·달·화성의 왕복 지연(RTT) 종합 비교")
ax.set_ylim(top=max(r[1] for r in rows) * 6)
ax.legend(handles=[Patch(facecolor="#999999", label="실제 측정값"),
                   Patch(facecolor="#999999", hatch="//", edgecolor="white", label="거리로 계산한 이론 최소값")],
          loc="upper left")
plt.tight_layout()
plt.savefig("overall_compare.png", dpi=150)
plt.show()
