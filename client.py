import grpc
import clock_pb2
import clock_pb2_grpc


def get_time(stub):
    response = stub.GetTime(clock_pb2.TimeRequest(client_time=int(time.time() * 1000)))
    return response.server_time


def adjust_time(stub, client_time):
    response = stub.AdjustTime(clock_pb2.AdjustRequest(client_time=client_time))
    if response.success:
        print("Time adjusted successfully.")
    else:
        print("Failed to adjust time.")


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = clock_pb2_grpc.ClockSyncStub(channel)

    client_time = get_time(stub)
    adjust_time(stub, client_time)


if __name__ == '__main__':
    run()
