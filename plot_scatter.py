import pandas as pd
import matplotlib.pyplot as plt

# 한글이 그래프에서 깨지지 않도록 폰트 설정 (Windows 기본 한글 폰트)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("avg_with_distance.csv")

# 측정 실패(NaN)한 서버는 그래프에서 제외
df = df.dropna(subset=["avg_time_ms"])

# 광속 한계선: 광케이블 속 신호 속도를 약 200,000km/s로 가정
# 왕복(거리 x 2)을 가는 데 걸리는 최소 시간(ms)을 거리별로 계산
FIBER_SPEED_KM_PER_MS = 200  # 200,000km/s = 200km/ms
df["min_possible_ms"] = (df["distance_km"] * 2) / FIBER_SPEED_KM_PER_MS

# 실제 측정값이 이론적 최소 시간보다 작으면 "이상치"로 표시 (물리적으로 불가능한 값)
df["is_outlier"] = df["avg_time_ms"] < df["min_possible_ms"]

normal = df[~df["is_outlier"]]
outliers = df[df["is_outlier"]]

plt.figure(figsize=(9, 6))

# 광속 한계선 (거리가 커질수록 최소 시간도 커지는 직선)
distance_range = df["distance_km"].sort_values()
min_line = (distance_range * 2) / FIBER_SPEED_KM_PER_MS
plt.plot(distance_range, min_line, "--", color="gray", label="광속 한계선 (이론적 최소 시간)")

# 정상 범위 서버들 (파란 점)
plt.scatter(normal["distance_km"], normal["avg_time_ms"], color="steelblue", label="측정 서버 (정상 범위)")

# 이상치 서버들 (빨간 점, 물리적으로 불가능한 값)
if len(outliers) > 0:
    plt.scatter(outliers["distance_km"], outliers["avg_time_ms"], color="crimson", marker="x", s=100,
                label="이상치 (광속 한계선 아래, CDN 의심)")
    for _, row in outliers.iterrows():
        plt.annotate(row["location"], (row["distance_km"], row["avg_time_ms"]),
                     textcoords="offset points", xytext=(8, 5), fontsize=9, color="crimson")

plt.xlabel("거리 (km)")
plt.ylabel("평균 연결 시간 (ms)")
plt.title("거리 vs TCP 연결(handshake) 시간")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("distance_vs_time.png", dpi=150)
print("완료! distance_vs_time.png 파일로 그래프가 저장되었습니다.")

if len(outliers) > 0:
    print("\n이상치로 분류된 서버:")
    print(outliers[["server", "location", "distance_km", "avg_time_ms", "min_possible_ms"]])
