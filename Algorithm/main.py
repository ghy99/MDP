import sys
import time
from typing import List
import pickle
import socket
import constants
from Misc.positioning import Position
from Misc.direction import Direction
from ConnectionToRpi.rpi_client import RPiClient
from ConnectionToRpi.rpi_server import RPiServer
from Grid.obstacle import Obstacle
from commands.go_straight_command import StraightCommand
from commands.scan_obstacle_command import ScanCommand
from pygame_app import AlgoMinimal


class Main:
    def __init__(self):
        self.client = None
        self.commands = None
        self.count = 0

    def parse_obstacle_data(self, data) -> List[Obstacle]:
        obs = []
        # [[x, y, orient, index], [x, y, orient, index]]
        for obstacle_params in data:
            obs.append(Obstacle(Position(obstacle_params[0],
                                         obstacle_params[1],
                                         Direction(obstacle_params[2])),
                                obstacle_params[3]))
        return obs

    def run_simulator(self):
        # Fill in obstacle positions with respect to lower bottom left corner.
        # (x-coordinate, y-coordinate, Direction)
        # obstacles = [[15, 75, 0, 0]]
        # obs = parse_obstacle_data(obstacles)
        obs = self.parse_obstacle_data([])
        # app = AlgoSimulator(obs)
        # app.init()
        # app.execute()

    def run_minimal(self, also_run_simulator, dummydata):
        # Create a client to connect to the RPi.

        # print(constants.PC_HOST)
        # if self.client is None:
        #     print(f"Attempting to connect to {constants.RPI_HOST}:{constants.RPI_PORT}")
        #     self.client = RPiClient(constants.RPI_HOST, constants.RPI_PORT)
        #     #     Wait to connect to RPi.
        #     while True:
        #         try:
        #             self.client.connect()
        #             break
        #         except OSError:
        #             pass
        #         except KeyboardInterrupt:
        #             self.client.close()
        #             sys.exit(1)
        #     print("Connected to RPi!\n")
        #
        # # Wait for message from RPI
        # print("Waiting to receive data from RPi...")
        # d = self.client.receive_message()
        print("Decoding data from RPi:")
        d = dummydata.decode('utf-8')
        to_return = []
        if d[0:4] == 'ALG:':
            d = d[4:]
            d = d.split(';')
            # now split into separate obstacles
            # last will be split into empty string therefore ignore
            for x in range(0, len(d) - 1):
                d_split = d[x].split(',')
                # d_split now holds the 4 values that are needed to create one obstacle
                temp = []
                for y in range(0, len(d_split)):
                    # means it's x or y coordinate so multiply by 10 to correspond to correct coordinate
                    if y <= 1:
                        temp.append(int(d_split[y]) * 10)
                    elif y == 2:
                        if d_split[y] == 'N':
                            temp.append(90)
                        elif d_split[y] == 'S':
                            temp.append(-90)
                        elif d_split[y] == 'E':
                            temp.append(0)
                        else:
                            temp.append(180)
                    else:
                        temp.append(int(d_split[y]))
                to_return.append(temp)
                print(to_return)
            self.decision(self.client, to_return, also_run_simulator)
        else:
            # this would be strings such as NONE, DONE, BULLSEYE
            print(d)
            self.decision(self.client, d, also_run_simulator)

    def decision(self, client, data, also_run_simulator):
        def isvalid(img):
            # Obstacle string 11-39
            checklist = [str(i) for i in range(41)]
            if img in checklist:
                return True
            return False

        # Obstacle list
        if isinstance(data[0], list):
            obstacles = self.parse_obstacle_data(data)
            # if also_run_simulator:
            #     app = AlgoSimulator(obstacles)
            #     app.init()
            #     app.execute()
            app = AlgoMinimal(obstacles)
            # app.init()
            # populates the Hamiltonian object with all the commands necessary to reach the objects
            app.execute()
            # Send the list of commands over.
            obs_priority = app.robot.hamiltonian.get_simple_hamiltonian()
            print(obs_priority)
            print("Sending list of commands to RPi...")
            self.commands = app.robot.convert_all_commands()
            print(self.commands)
            # if len(self.commands) != 0:
            #     client.send_message(self.commands)
            # else:
            #     print("ERROR!! NO COMMANDS TO SEND TO RPI")

        elif isinstance(data[0], str):
            # means its NONE
            client.send_message([StraightCommand(-10).convert_to_message(),
                                 ScanCommand(data[2]).convert_to_message(),
                                 StraightCommand(10).convert_to_message()])

        #
        # # String commands from Rpi
        # elif isinstance(data[0], str):
        #     # Check valid image taken
        #     if isvalid(data[0]):
        #         if self.count == 0:
        #             if len(self.commands) != 0:
        #                 if "STM:pn\n" in self.commands:
        #                     sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #                     self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #                 else:
        #                     sent_commands = self.commands
        #                 print(sent_commands)
        #                 print(self.commands)
        #                 client.send_message(sent_commands)
        #
        #         elif self.count == 1:
        #             self.count = 0
        #             amended_commands = ["STM:w010n\n"]
        #             if len(self.commands) != 0:
        #                 if "STM:pn\n" in self.commands:
        #                     sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #                     self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #                 else:
        #                     sent_commands = self.commands
        #                 amended_commands = amended_commands + sent_commands
        #                 print("Amended commands: ", amended_commands)
        #                 print(self.commands)
        #                 client.send_message(amended_commands)
        #
        #         elif self.count == 2:
        #             self.count = 0
        #             amended_commands = ["STM:w020n\n"]
        #             if len(self.commands) != 0:
        #                 if "STM:pn\n" in self.commands:
        #                     sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #                     self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #                 else:
        #                     sent_commands = self.commands
        #                 amended_commands = amended_commands + sent_commands
        #                 print("Amended commands: ", amended_commands)
        #                 print(self.commands)
        #                 client.send_message(amended_commands)
        #
        #     # Start sending algo commands
        #     elif data[0] == "START":
        #         if len(self.commands) != 0:
        #             sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #             self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #             print(sent_commands)
        #             print(self.commands)
        #             client.send_message(sent_commands)
        #             # client.close()
        #
        #     # Not valid data
        #     elif data[0] == "bullseye":
        #         print("Sending list of commands to RPi...")
        #         fixed_commands = ["STM:Ln\n", "STM:w060n\n", "STM:ln\n", "STM:w025n\n", "STM:ln\n", "STM:pn\n"]
        #         print(fixed_commands)
        #         client.send_message(fixed_commands)
        #
        #     # If no image taken
        #     elif data[0] == "-1":
        #         if self.count == 2:
        #             self.count = 0
        #             amended_commands = ["STM:w020n\n"]
        #             if len(self.commands) != 0:
        #                 if "STM:pn\n" in self.commands:
        #                     sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
        #                     self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
        #                 else:
        #                     sent_commands = self.commands
        #                 amended_commands = amended_commands + sent_commands
        #                 print("Amended commands: ", amended_commands)
        #                 print(self.commands)
        #                 client.send_message(amended_commands)
        #
        #         else:
        #             self.count += 1
        #             correction_commands = ["STM:s010n\n", "STM:pn\n"]
        #             print(correction_commands)
        #             client.send_message(correction_commands)

    def run_rpi(self):
        while True:
            x = 'ALG:10,17,S,0;17,17,W,1;2,16,S,2;16,4,S,3;13,1,W,4;6,6,N,5;9,11,W,6;3,3,E,7;'.encode('utf-8')
            self.run_minimal(False,x)
            break
            # time.sleep(5)


def initialize():
    algo = Main()
    algo.run_rpi()


def sim():
    algo = Main()
    algo.run_simulator()


def test():
    print('start test')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("192.168.17.1", 6000))
    print("connected")
    server.send("12345")
    msg = server.recv(1024)
    print(msg.decode("utf-8"))


if __name__ == '__main__':
    """
    Simulator 
    Rpi Connection
    """
    # sim()
    initialize()
    # test()
