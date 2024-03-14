import time
from concurrent import futures
import grpc
import clock_pb2
import clock_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ClockSyncServicer(clock_pb2_grpc.ClockSyncServicer):
    def __init__(self):
        self.client_times = []

    def GetTime(self, request, context):
        return clock_pb2.TimeResponse(server_time=int(time.time() * 1000))

    def AdjustTime(self, request, context):
        avg_time = sum(self.client_times) // len(self.client_times)
        adjustment = avg_time - request.client_time
        return clock_pb2.AdjustResponse(success=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    clock_pb2_grpc.add_ClockSyncServicer_to_server(ClockSyncServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started!")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
