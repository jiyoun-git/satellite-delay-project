import socket
import time


def measure_connect_time(host, port=80, timeout=5):
    # 1. 소켓 만들기: IPv4(AF_INET) + TCP(SOCK_STREAM) 방식
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)  # 5초 안에 안 되면 포기

    start = time.perf_counter()      # 시간 측정 시작
    try:
        sock.connect((host, port))   # 여기서 3-way handshake가 실제로 일어남
        end = time.perf_counter()    # handshake가 끝난 순간
        elapsed_ms = (end - start) * 1000
        print(f"{host}:{port} 연결 시간 = {elapsed_ms:.2f} ms")
        return elapsed_ms
    except socket.timeout:
        print(f"{host}:{port} 연결 시간 초과")
        return None
    finally:
        sock.close()  # 소켓 정리 (전화 끊기)


if __name__ == "__main__":
    measure_connect_time("www.google.com", 80)

