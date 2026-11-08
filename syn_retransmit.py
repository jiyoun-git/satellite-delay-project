import pandas as pd

C = 299792.458  # 광속 (km/s)

INITIAL_RTO = 1       # SYN 재전송 타임아웃 초기값(초). 표준(RFC 6298)이 권장하는 값
DEFAULT_RETRIES = 6   # 리눅스의 기본 SYN 재시도 횟수


def simulate(rtt, retries=DEFAULT_RETRIES, rto0=INITIAL_RTO):
    """SYN을 보낸 뒤 SYN+ACK가 rtt초 만에 돌아온다고 할 때의 결과를 계산.
    재전송 간격은 1초 -> 2초 -> 4초 ... 처럼 매번 2배로 늘어남 (패킷 손실은 없다고 가정)."""
    retransmit_times = []
    t, rto = 0, rto0
    for _ in range(retries):
        t += rto                      # 이 시각까지 응답이 없으면 SYN을 다시 보냄
        retransmit_times.append(t)
        rto *= 2
    give_up_time = t + rto            # 마지막 재전송 뒤에도 기다리다가 포기하는 시각
    success = rtt <= give_up_time
    spurious = sum(1 for x in retransmit_times if x < rtt)  # 응답이 오기 전에 이미 보낸 재전송 수
    return success, spurious, retransmit_times, give_up_time


def min_retries_needed(rtt):
    """연결이 성공하려면 SYN 재시도를 최소 몇 번까지 허용해야 하는지"""
    n = 0
    while not simulate(rtt, retries=n)[0]:
        n += 1
    return n


def fmt(sec):
    if sec < 1:
        return f"{sec * 1000:,.1f} ms"
    if sec < 60:
        return f"{sec:,.2f} 초"
    return f"{sec / 60:,.1f} 분"


# ── 시나리오별 RTT ──
df = pd.read_csv("rtt_results.csv")
df = df[df["trial"] != 1].dropna(subset=["time_ms"])
slowest_earth = df.groupby("server")["time_ms"].mean().max() / 1000  # 지구 안에서 가장 느린 서버

cases = {
    "지구 안 - 가장 느린 서버": slowest_earth,
    "달 (오늘 기준)": 371_236 / C * 2,
    "화성 - 가장 가까울 때": 56_909_620 / C * 2,
    "화성 - 가장 멀 때": 400_190_463 / C * 2,
}

print(f"가정: 초기 RTO {INITIAL_RTO}초, 재전송마다 2배, 기본 재시도 {DEFAULT_RETRIES}회")
_, _, times, give_up = simulate(0)
print(f"기본 설정의 SYN 재전송 시각: {', '.join(f'{x}초' for x in times)} / {give_up}초에 연결 포기")
print()

for name, rtt in cases.items():
    ok, spurious, _, _ = simulate(rtt)
    need = min_retries_needed(rtt)
    print(f"[{name}] RTT {fmt(rtt)}")
    if ok:
        print(f"  기본 설정: 연결 성공 ({fmt(rtt)} 후 완료), 불필요한 SYN 재전송 {spurious}회")
    else:
        print(f"  기본 설정: 연결 실패 ({give_up}초 뒤 포기, RTT가 포기 시간보다 김)")
    print(f"  연결이 성공하려면 SYN 재시도를 최소 {need}회까지 허용해야 함 "
          f"(그때 불필요한 재전송 {simulate(rtt, retries=need)[1]}회)")
    print()
