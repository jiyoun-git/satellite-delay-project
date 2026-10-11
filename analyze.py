import pandas as pd

# 5주차에서 만든 결과 파일을 표(DataFrame)로 불러옴
df = pd.read_csv("rtt_results.csv")

# 1차 시도 제외 (DNS 조회 시간이 섞여 있어서 순수 handshake 시간이 아님)
df_filtered = df[df["trial"] != 1]

# 서버별로 묶어서 2~5차 평균 연결 시간 계산
avg_by_server = (
    df_filtered.groupby(["server", "location", "country"])["time_ms"]
    .mean()
    .reset_index()
    .rename(columns={"time_ms": "avg_time_ms"})
)

print(avg_by_server)

# 나중에 그래프 그릴 때 다시 불러오기 쉽도록 별도 CSV로도 저장
avg_by_server.to_csv("avg_by_server.csv", index=False)
print("\n완료! 서버별 평균이 avg_by_server.csv 파일에 저장되었습니다.")
