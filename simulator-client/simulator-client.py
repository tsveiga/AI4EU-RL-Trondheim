import json
import grpc
import time

import simulator_pb2
import simulator_pb2_grpc


def main():
    sim_channel = grpc.insecure_channel("localhost:50055", options=[
        ('grpc.max_send_message_length', 1000 * 1024 * 1024),
        ('grpc.max_receive_message_length', 1000 * 1024 * 1024)
        ])
    # sim_channel = grpc.insecure_channel('localhost:'+str(config['simulator-grpcport']))
    sim_request_stub = simulator_pb2_grpc.SimulatorStub(sim_channel)

    StartDate = "2020-02-01"
    EndDate = "2020-02-02"
    DensityPerc = 1

    # Start Simulation
    initRequest = simulator_pb2.InitRequest(
        StartDate=StartDate, EndDate=EndDate, DensityPerc=DensityPerc
    )
    emissionsState = sim_request_stub.start_simulation(initRequest)
    # guijob = gui_request_stub.requestSudokuEvaluation(initRequest)

    emissions = emissionsState.emissions

    stepMsg = simulator_pb2.StepRequest()
    stepMsg.numSteps = 10

    for key, value in emissions.items():
        stepMsg.cell_state[key] = 1

    while not emissionsState.hasEnded:
        try:
            
            emissionsState = sim_request_stub.step(stepMsg)

            print(emissionsState.emissions)

        #
        except Exception as e:
            print("Got an exception ", str(e))
            # do not spam
            time.sleep(2)


main()
