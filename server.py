import datetime
import time
from concurrent import futures

import grpc

import clock_pb2
import clock_pb2_grpc


class ClockService(clock_pb2_grpc.ClockServiceServicer):
    def __init__(self):
        self.offsets = {}

    def GetTimeOffset(self, request, context):
        client_time = request.timestamp
        server_time = time.time()
        offset = (server_time - client_time) / 2
        self.offsets[request.client_id] = offset
        return clock_pb2.TimeOffsetResponse(offset=offset)

    def GetSynchronizedTime(self, request, context):
        if request.client_id not in self.offsets:
            return clock_pb2.SynchronizedTimeResponse(time=0)

        offset = self.offsets[request.client_id]
        synchronized_time = time.time() + offset
        print(f"[{request.client_id}] {datetime.datetime.fromtimestamp(synchronized_time)} | (Tempo: {synchronized_time}, diferença: {offset})")
        return clock_pb2.SynchronizedTimeResponse(time=synchronized_time)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    clock_pb2_grpc.add_ClockServiceServicer_to_server(ClockService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
