import socket
import time
import csv

# 측정할 서버 목록: (호스트 주소, 위치, 국가)
SERVERS = [
    ("snu.ac.kr", "서울", "한국"),
    ("yonsei.ac.kr", "서울", "한국"),
    ("korea.ac.kr", "서울", "한국"),
    ("kaist.ac.kr", "대전", "한국"),
    ("cbnu.ac.kr", "청주", "한국"),
    ("u-tokyo.ac.jp", "도쿄", "일본"),
    ("tsinghua.edu.cn", "베이징", "중국"),
    ("iitb.ac.in", "뭄바이", "인도"),
    ("nus.edu.sg", "싱가포르", "싱가포르"),
    ("ox.ac.uk", "옥스퍼드", "영국"),
    ("tum.de", "뮌헨", "독일"),
    ("sorbonne-universite.fr", "파리", "프랑스"),
    ("msu.ru", "모스크바", "러시아"),
    ("unibo.it", "볼로냐", "이탈리아"),
    ("mit.edu", "케임브리지", "미국"),
    ("stanford.edu", "스탠퍼드", "미국"),
    ("utoronto.ca", "토론토", "캐나다"),
    ("unam.mx", "멕시코시티", "멕시코"),
    ("usp.br", "상파울루", "브라질"),
    ("uba.ar", "부에노스아이레스", "아르헨티나"),
    ("uct.ac.za", "케이프타운", "남아공"),
    ("cu.edu.eg", "카이로", "이집트"),
    ("unilag.edu.ng", "라고스", "나이지리아"),
    ("sydney.edu.au", "시드니", "호주"),
    ("auckland.ac.nz", "오클랜드", "뉴질랜드"),
]

PORT = 80          # 지난주와 동일하게 HTTP 포트 사용
TRIALS = 5          # 서버 1곳당 5번씩 반복 측정
TIMEOUT = 5          # 5초 안에 연결 안 되면 포기
OUTPUT_FILE = "rtt_results.csv"


def measure_once(host, port=PORT, timeout=TIMEOUT):
    """서버 1곳에 1번 접속해서 연결 시간(ms)을 재는 함수. 지난주 measure.py와 거의 같음."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    start = time.perf_counter()
    try:
        sock.connect((host, port))        # 여기서 3-way handshake 발생
        end = time.perf_counter()
        return (end - start) * 1000       # ms 단위로 변환
    except (socket.timeout, OSError):
        # 타임아웃되거나, 호스트를 못 찾거나, 연결이 거부된 경우 모두 여기로 옴
        return None
    finally:
        sock.close()


def main():
    # newline="" 와 encoding="utf-8"은 한글이 깨지지 않고 줄바꿈이 꼬이지 않게 하기 위한 옵션
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["server", "location", "country", "trial", "time_ms"])  # 헤더(제목) 행

        total = len(SERVERS) * TRIALS
        done = 0

        for host, location, country in SERVERS:
            for trial in range(1, TRIALS + 1):
                elapsed = measure_once(host)
                done += 1

                if elapsed is None:
                    print(f"[{done}/{total}] {host} ({location}) 시도 {trial}: 실패(타임아웃/연결거부)")
                    writer.writerow([host, location, country, trial, ""])
                else:
                    print(f"[{done}/{total}] {host} ({location}) 시도 {trial}: {elapsed:.2f} ms")
                    writer.writerow([host, location, country, trial, f"{elapsed:.2f}"])

                f.flush()  # 중간에 멈춰도 그때까지 측정한 데이터는 CSV에 남도록 즉시 저장

    print(f"\n완료! 결과가 {OUTPUT_FILE} 파일에 저장되었습니다.")


if __name__ == "__main__":
    main()
