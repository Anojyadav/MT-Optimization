from GenerateOrderList import GenerateOrderList
from AntTour import AntTour
import copy
import math
import random


class CapacityVehicleRoutingPickupDelivery(GenerateOrderList):

    def __init__(self, colony_size, steps, robot_parameters):
        super().__init__()
        self.colony_size = colony_size
        self.steps = steps
        self.robot_parameters = robot_parameters
        self.robot_name_list = None
        self.total_distance_travelled = 0.0
        self.best_tour = [0]
        self.best_distance = float("inf")
        self.best_robot_parameters = [0]

    def sort_in(self):

        self.robot_parameters.sort(key=lambda x: x['Capacity'], reverse=True)

    def check_robot_capacity(self, a, c):

        k = []
        for s in c:
            if all(elem in a for elem in s['pick_drop']):
                continue
            else:
                k.append(s['total_demand_tour'])
        return k

    def random_shuffle_(self):

        robot_list = []
        while True:
            robot_parameters_ = copy.deepcopy(self.robot_parameters)
            n = len(robot_list)
            if n >= math.factorial(len(robot_parameters_)):
                break
            else:
                random.shuffle(robot_parameters_)
                if robot_parameters_ not in robot_list:
                    robot_list.append(robot_parameters_)
        return robot_list

    def main(self):

        nodes_location, demand_list, pick_drop_list = self.generate_order_list()
        robot_parameter_list = self.random_shuffle_()
        for robot_list in robot_parameter_list:
            demand_list_ = copy.deepcopy(demand_list)
            total_distance = 0
            tour_list = []
            tour_nodes = []
            for robot in robot_list:

                if robot['Capacity'] < min(self.check_robot_capacity(tour_nodes, pick_drop_list)):
                    tour_list.append(None)
                    tour_nodes.extend([0])
                    continue

                else:
                    tour = AntTour(colony_size=self.colony_size, steps=self.steps, nodes_location=nodes_location,
                                   demand_list=demand_list_, robot_capacity=robot['Capacity'],
                                   pick_drop_list=pick_drop_list)
                    a, c, d = tour.run()
                    total_distance += round(d, 2)
                    tour_list.append(a)
                    tour_nodes.extend(a)
                    for ele in a:
                        if ele != 0:
                            demand_list_[ele] = float('inf')
                    if min(demand_list_[1:]) == float('inf'):
                        break

            if total_distance < self.best_distance:
                self.best_tour = tour_list
                self.best_distance = round(total_distance, 3)
                self.best_robot_parameters = robot_list
        print("total distance traveled {}".format(self.best_distance))
        print("best robot sequence parameter {}".format(self.best_robot_parameters))
        print("best tour for all robot based on seq {}".format(self.best_tour))


if __name__ == '__main__':
    colony_size = 5
    steps = 50
    robot_parameters = [{'name': 'Captain', 'Capacity': 5}, {'name': 'Cob', 'Capacity': 12},
                        {'name': 'Davy', 'Capacity': 20}]
    cvrp = CapacityVehicleRoutingPickupDelivery(colony_size, steps, robot_parameters)
    cvrp.main()
