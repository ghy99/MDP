import sys
import time
from typing import List
import pickle
import socket
# import settings
from pygame_app import AlgoSimulator, AlgoMinimal
from Algor import Direction
from entities.connection.rpi_client import RPiClient
from entities.connection.rpi_server import RPiServer
from entities.grid.obstacle import Obstacle


class Main:
    def __init__(self):
        self.client = None
        self.commands = None
        self.count = 0

    def parse_obstacle_data(self, data) -> List[Obstacle]:
        obs = []
        for obstacle_params in data:
            obs.append(Obstacle(obstacle_params[0],
                                obstacle_params[1],
                                Direction(obstacle_params[2]),
                                obstacle_params[3]))
        # [[x, y, orient, index], [x, y, orient, index]]
        return obs

    def run_simulator(self):
        # Fill in obstacle positions with respect to lower bottom left corner.
        # (x-coordinate, y-coordinate, Direction)
        # obstacles = [[15, 75, 0, 0]]
        # obs = parse_obstacle_data(obstacles)
        obs = self.parse_obstacle_data([])
        app = AlgoSimulator(obs)
        app.init()
        app.execute()

    def run_minimal(self, also_run_simulator):
        # Create a client to connect to the RPi.

        print(settings.PC_HOST)
        if self.client is None:
            print(
                f"Attempting to connect to {settings.RPI_HOST}:{settings.RPI_PORT}")
            self.client = RPiClient(settings.RPI_HOST, settings.RPI_PORT)
            #     Wait to connect to RPi.
            while True:
                try:
                    self.client.connect()
                    print('runs')
                    break
                except OSError:
                    pass
                except KeyboardInterrupt:
                    self.client.close()
                    sys.exit(1)
            print("Connected to RPi!\n")
            self.client.send_message(['1', '2', '3', '4', '5'])

        # # Wait for message from RPI
        # print("Waiting to receive data from RPi...")
        # d = self.client.receive_message()
        # print("Got data from RPi:")
        # d = d.decode('utf-8')
        # d = d.split(',')
        # print(d)
        # if len(d) != 1:
        #     print(d)
        #     data = []
        #     for i in range(0, len(d), 4):
        #         data.append(d[i:i + 4])
        #
        #     for i in range(len(data)):
        #         data[i][0] = 10 * int(data[i][0]) + 5
        #         # 200 - flip obstacle plot according to android
        #         data[i][1] = 200 - (10 * int(data[i][1])) - 5
        #         match data[i][2]:
        #             case 'N':
        #                 data[i][2] = 90
        #             case 'S':
        #                 data[i][2] = -90
        #             case 'E':
        #                 data[i][2] = 0
        #             case 'W':
        #                 data[i][2] = 180
        #         data[i][3] = int(data[i][3])
        # else:
        #     data = d
        #
        # print(data)
        #
        # # data = [[145, 35, 180, 0], [115, 85, 0, 1], [25, 155, -90, 2], [175, 175, 180, 3], [105, 115, 180, 4]]
        # self.decision(self.client, data, also_run_simulator)

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
            if also_run_simulator:
                app = AlgoSimulator(obstacles)
                app.init()
                app.execute()
            app = AlgoMinimal(obstacles)
            app.init()
            app.execute()
            # Send the list of commands over.
            obs_priority = app.robot.hamiltonian.get_simple_hamiltonian()
            print(obs_priority)
            obs_str = "RPI:PLOT,"
            for i in range(len(obs_priority)):
                if isinstance(obs_priority[i], Obstacle):
                    x = obs_priority[i].pos.x // settings.SCALING_FACTOR // 10
                    y = (200 - (obs_priority[i].pos.y //
                         settings.SCALING_FACTOR) - 5) // 10

                    if obs_priority[i].pos.direction == Direction.TOP:
                        direction = "N"
                    elif obs_priority[i].pos.direction == Direction.BOTTOM:
                        direction = "S"
                    elif obs_priority[i].pos.direction == Direction.RIGHT:
                        direction = "E"
                    elif obs_priority[i].pos.direction == Direction.LEFT:
                        direction = "W"
                    obs_str = obs_str + str(x) + "," + \
                        str(y) + "," + direction + ";"
            obs_str = obs_str[:-1] + "\n"
            print(obs_str)
            print("Sending list of commands to RPi...")
            self.commands = app.robot.convert_all_commands()
            self.commands.append("RPI:STOPPED\n")
            client.send_message([obs_str])

            # print("Sending list of commands to RPi...")
            # self.commands = app.robot.convert_all_commands()
            # self.commands.append("RPI:STOPPED\n")
            #
            # if len(self.commands) != 0:
            #     sent_commands = self.commands[:self.commands.index("STM:pn\n") + 1]
            #     self.commands = self.commands[self.commands.index("STM:pn\n") + 1:]
            #     print(sent_commands)
            #     print(self.commands)
            #     client.send_message(sent_commands)
            #     # client.close()

        # String commands from Rpi
        elif isinstance(data[0], str):
            # Check valid image taken
            if isvalid(data[0]):
                if self.count == 0:
                    if len(self.commands) != 0:
                        if "STM:pn\n" in self.commands:
                            sent_commands = self.commands[:self.commands.index(
                                "STM:pn\n") + 1]
                            self.commands = self.commands[self.commands.index(
                                "STM:pn\n") + 1:]
                        else:
                            sent_commands = self.commands
                        print(sent_commands)
                        print(self.commands)
                        client.send_message(sent_commands)

                elif self.count == 1:
                    self.count = 0
                    amended_commands = ["STM:w010n\n"]
                    if len(self.commands) != 0:
                        if "STM:pn\n" in self.commands:
                            sent_commands = self.commands[:self.commands.index(
                                "STM:pn\n") + 1]
                            self.commands = self.commands[self.commands.index(
                                "STM:pn\n") + 1:]
                        else:
                            sent_commands = self.commands
                        amended_commands = amended_commands + sent_commands
                        print("Amended commands: ", amended_commands)
                        print(self.commands)
                        client.send_message(amended_commands)

                elif self.count == 2:
                    self.count = 0
                    amended_commands = ["STM:w020n\n"]
                    if len(self.commands) != 0:
                        if "STM:pn\n" in self.commands:
                            sent_commands = self.commands[:self.commands.index(
                                "STM:pn\n") + 1]
                            self.commands = self.commands[self.commands.index(
                                "STM:pn\n") + 1:]
                        else:
                            sent_commands = self.commands
                        amended_commands = amended_commands + sent_commands
                        print("Amended commands: ", amended_commands)
                        print(self.commands)
                        client.send_message(amended_commands)

            # Start sending algo commands
            elif data[0] == "START":
                if len(self.commands) != 0:
                    sent_commands = self.commands[:self.commands.index(
                        "STM:pn\n") + 1]
                    self.commands = self.commands[self.commands.index(
                        "STM:pn\n") + 1:]
                    print(sent_commands)
                    print(self.commands)
                    client.send_message(sent_commands)
                    # client.close()

            # Not valid data
            elif data[0] == "bullseye":
                print("Sending list of commands to RPi...")
                fixed_commands = ["STM:Ln\n", "STM:w060n\n",
                                  "STM:ln\n", "STM:w025n\n", "STM:ln\n", "STM:pn\n"]
                print(fixed_commands)
                client.send_message(fixed_commands)

            # If no image taken
            elif data[0] == "-1":
                if self.count == 2:
                    self.count = 0
                    amended_commands = ["STM:w020n\n"]
                    if len(self.commands) != 0:
                        if "STM:pn\n" in self.commands:
                            sent_commands = self.commands[:self.commands.index(
                                "STM:pn\n") + 1]
                            self.commands = self.commands[self.commands.index(
                                "STM:pn\n") + 1:]
                        else:
                            sent_commands = self.commands
                        amended_commands = amended_commands + sent_commands
                        print("Amended commands: ", amended_commands)
                        print(self.commands)
                        client.send_message(amended_commands)

                else:
                    self.count += 1
                    correction_commands = ["STM:s010n\n", "STM:pn\n"]
                    print(correction_commands)
                    client.send_message(correction_commands)

    def run_rpi(self):
        while True:
            self.run_minimal(False)
            time.sleep(5)


def init():
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
    # init()
    test()


# if __name__ == "__main__":
#     bot = Robot()
#     # algo = Astar(bot)
#     # algo.runAlgo()
#     # algo = Astar(self.getCurrentPos(), self.grid)
# #     bot.callAlgo()
# # self.algo = Astar()
#     # grid, obstacles = app.initGrid()
#     # a = astarclass.Astar(settings.INITPOS, obstacles, grid, settings.GRID_LENGTH//settings.GRID_CELL_LENGTH)
#     # a.runAlgo(grid, obstacles)
#     sim = Simulation()
#     sim.runSimulation(bot)
