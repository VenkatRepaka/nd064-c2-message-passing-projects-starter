import grpc
import location_pb2
import location_pb2_grpc

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30055")
# channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

location = location_pb2.LocationMessage(
    person_id=10, longitude="74.55", latitude="66.29"
)

response = stub.Create(location)
print(response)
