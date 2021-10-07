import json
import grpc
import time

import simulator_pb2
import simulator_pb2_grpc

import numpy as np

import matplotlib.pyplot as plt

# Just as an example, define here a cell of interest. The script will track its history during the episode and plot it in the end
cell_to_plot = 'poly_162'

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

    cell_history = []

    while not emissionsState.hasEnded:
        try:

            emissionsState = sim_request_stub.step(stepMsg)

            cell_history.append(emissionsState.emissions[cell_to_plot])
        #
        except Exception as e:
            print("Got an exception ", str(e))
            # do not spam
            time.sleep(2)

    # In the end we can plot the pollution history for the cell of interest
    plt.plot(cell_history)
    plt.title('Results for cell' + cell_to_plot)
    plt.show()

main()
