import datetime
import time
import grpc

import sys
import clock_pb2
import clock_pb2_grpc


def get_time_offset(stub, client_id):
    local_time = time.time()

    print(sys.argv, len(sys.argv), len(sys.argv) == 3)

    if len(sys.argv) == 3:
        print(sys.argv[2])
        local_time += int(sys.argv[2])

    request = clock_pb2.TimeOffsetRequest(timestamp=local_time, client_id=client_id)
    response = stub.GetTimeOffset(request)
    return response.offset


def get_synchronized_time(stub, client_id):
    request = clock_pb2.SynchronizedTimeRequest(client_id=client_id)
    response = stub.GetSynchronizedTime(request)
    return response.time


def run_client(client_id):
    channel = grpc.insecure_channel('localhost:50051')
    stub = clock_pb2_grpc.ClockServiceStub(channel)
    offset = get_time_offset(stub, client_id)

    while True:
        local_time = datetime.datetime.fromtimestamp(get_synchronized_time(stub, client_id))
        synchronized_time = datetime.datetime.fromtimestamp(get_synchronized_time(stub, client_id) - offset)
        print(f"[{client_id}] Sincronizado: {synchronized_time} | Local: {local_time}")
        time.sleep(1)


if __name__ == '__main__':
    print(sys.argv[1])
    run_client(sys.argv[1])
