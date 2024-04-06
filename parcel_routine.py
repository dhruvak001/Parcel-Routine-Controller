import heapq
from collections import deque


class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        heapq.heappush(self.heap, -item)  # Negate the item for max heap

    def pop(self):
        return -heapq.heappop(self.heap)  # Negate the result for max heap

    def is_empty(self):
        return len(self.heap) == 0

    def parent(self, i):
        return (i - 1) // 2

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def get_max(self):
        if self.heap:
            return self.heap[0]
        return None

    def extract_max(self):
        if not self.heap:
            return None
        max_item = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.min_heapify(0)  # Use min_heapify instead of max_heapify
        return max_item

    def max_heapify(self, i):  # Change method name to min_heapify
        l = self.left(i)
        r = self.right(i)
        smallest = i  # Change variable name to smallest

        if l < len(self.heap) and self.heap[l] > self.heap[smallest]:  # Change comparison operator
            smallest = l
        if r < len(self.heap) and self.heap[r] > self.heap[smallest]:  # Change comparison operator
            smallest = r

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.min_heapify(smallest)  # Change method name

    def insert(self, item):
        self.heap.append(item)
        i = len(self.heap) - 1
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:  # Change comparison operator
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)



class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []

    def add_edge(self, source, destination, min_freight_cars_to_move, max_parcel_capacity):
        if source not in self.vertices:
            self.vertices[source] = Vertex(source, min_freight_cars_to_move, max_parcel_capacity, self)
        if destination not in self.vertices:
            self.vertices[destination] = Vertex(destination, min_freight_cars_to_move, max_parcel_capacity, self)

        self.vertices[source].add_neighbor(destination)
        self.vertices[destination].add_neighbor(source)

        self.edges.append((source, destination))

    def bfs(self, source, destination):
        visited = set()
        queue = deque([[source]])
        if source == destination:
            return [source]
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node not in visited:
                neighbors = self.vertices[node].neighbors
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    if neighbor == destination:
                        return new_path
                visited.add(node)
        return []

    def dfs(self, source, destination):
        visited = set()
        stack = [(source, [source])]  # Keep track of the path
        while stack:
            current, path = stack.pop()
            if current not in visited:
                visited.add(current)
                if current == destination:
                    return path  # Return the path if the destination is reached
                neighbors = self.vertices[current].neighbors
                for neighbor in neighbors:
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))  # Update the path
        return []
    
    def groupFreightCars(self):
        for vertex in self.vertices.values():
            vertex.groupFreightCars()

    def moveTrains(self):
        for vertex in self.vertices.values():
            vertex.moveTrains()


class Vertex:
    def __init__(self, name, min_freight_cars_to_move, max_parcel_capacity, graph):
        self.name = name
        self.freight_cars = []
        self.neighbors = []
        self.trains_to_move = None
        self.min_freight_cars_to_move = min_freight_cars_to_move
        self.max_parcel_capacity = max_parcel_capacity
        self.parcel_destination_heaps = {}
        self.sealed_freight_cars = []
        self.all_parcels = []
        self.graph = graph  


    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def get_all_current_parcels(self):
        all_parcels = []
        for freight_car in self.freight_cars:
            all_parcels.extend(freight_car.parcels)
        return all_parcels

    def clean_unmoved_freight_cars(self):
        for freight_car in self.freight_cars:
            if not freight_car.moved:
                self.loadParcel(freight_car.parcels)
                freight_car.parcels = []
                freight_car.destination_city = None
                freight_car.next_link = None

    def loadParcel(self, parcel):
        #for parcel in parcels:
        if parcel.destination not in self.parcel_destination_heaps:
            self.parcel_destination_heaps[parcel.destination] = MaxHeap()
        self.parcel_destination_heaps[parcel.destination].insert(parcel)

    def loadFreightCars(self):
        for destination, heap in self.parcel_destination_heaps.items():
            while not heap.is_empty():
                available_freight_cars = [car for car in self.freight_cars if len(car.parcels) < self.max_parcel_capacity]
                if not available_freight_cars:
                    break  # No available freight cars, stop loading parcels

                parcels_to_load = [heap.extract_max() for _ in range(self.max_parcel_capacity)]
                for car in available_freight_cars:
                    parcels_for_car = parcels_to_load[: self.max_parcel_capacity - len(car.parcels)]
                    car.load_parcel(parcels_for_car)
                    parcels_to_load = parcels_to_load[len(parcels_for_car):]

                # Create new freight cars if there are remaining parcels to load
                while parcels_to_load:
                    new_freight_car = FreightCar(self.max_parcel_capacity)
                    parcels_for_new_car = parcels_to_load[: self.max_parcel_capacity]
                    new_freight_car.load_parcel(parcels_for_new_car)
                    self.freight_cars.append(new_freight_car)
                    parcels_to_load = parcels_to_load[len(parcels_for_new_car):]
        
    def groupFreightCars(self):
        grouped_cars = []
        
        for freight_car in self.freight_cars:
            if not freight_car.moved:
                group = [freight_car]
                
                for other_car in self.freight_cars:
                    if (
                        other_car != freight_car
                        and not other_car.moved
                        and other_car.destination_city == freight_car.destination_city
                    ):
                        group.append(other_car)
                        if len(group) == self.min_freight_cars_to_move:
                            
                            grouped_cars.append(group)
                            break
                if len(group) < self.min_freight_cars_to_move:
                    grouped_cars.append([freight_car])

        for group in grouped_cars:
            destination = group[0].destination_city
            for freight_car in group:
                dfs_path = self.dfs(freight_car.current_location, destination)
                if dfs_path:
                    freight_car.next_link = dfs_path[1]
                    freight_car.moved = True

    def moveTrains(self):
        moved_freight_cars = []  # Temporary list to store moved freight cars
        for freight_car in self.freight_cars:
            destination_vertex = None  # Initialize before the loop
            if freight_car.next_link:
                destination = freight_car.next_link
                destination_vertex = self.graph.vertices.get(destination)  # Use get to handle None case
                if destination_vertex and len(destination_vertex.trains_to_move) >= self.min_freight_cars_to_move:
                    train = destination_vertex.trains_to_move[: self.min_freight_cars_to_move]
                    for car in train:
                        car.current_location = destination
                        car.moved = True
                        car.destination_city = None
                        car.next_link = None
                        moved_freight_cars.append(car)
                        # Remove moved freight cars from the source vertex's freight_cars list
                        self.freight_cars.remove(car)

        # Call the move method for each moved freight car
        for freight_car in moved_freight_cars:
            freight_car.move(freight_car.current_location)  # Use the current location as the argument

        # Check if moved_freight_cars is not empty before referencing it
        if moved_freight_cars:
            # Get the destination_vertex for the first moved car (assuming all moved cars have the same destination)
            destination_vertex = self.graph.vertices.get(moved_freight_cars[0].current_location)
            if destination_vertex is not None:
                # Add moved freight cars to the destination vertex's list
                destination_vertex.freight_cars.extend(moved_freight_cars)
                # Remove moved freight cars from the destination vertex's trains_to_move list
                destination_vertex.trains_to_move = [
                    car for car in destination_vertex.trains_to_move if car not in moved_freight_cars
                ]

class FreightCar:
    def __init__(self, max_parcel_capacity):
        self.max_parcel_capacity = max_parcel_capacity
        self.parcels = []
        self.destination_city = None
        self.next_link = None
        self.current_location = None
        self.moved = False

    def load_parcel(self, parcels):
        self.parcels.extend(parcels)

    def can_move(self):
        return len(self.parcels) == self.max_parcel_capacity

    def move(self, destination):
        self.current_location = destination
        self.moved = True
        self.destination_city = None
        self.next_link = None

        # Update the loop to correctly set the 'delivered' attribute
        for parcel in self.parcels:
            parcel.current_location = destination
            parcel.delivered = True  # Move this line inside the loop

        self.parcels = []

class Parcel:
    def __init__(self, time_tick, parcel_id, origin, destination, priority):
        self.time_tick = time_tick
        self.parcel_id = parcel_id
        self.origin = origin
        self.destination = destination
        self.priority = priority
        self.delivered = False
        self.current_location = origin

    def __lt__(self, other):
        return self.priority < other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __ne__(self, other):
        return self.priority != other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __ge__(self, other):
        return self.priority >= other.priority


class PRC:
    def __init__(self, min_freight_cars_to_move=5, max_parcel_capacity=5):
        self.graph = Graph()
        self.freight_cars = []
        self.parcels = {}
        self.parcels_with_time_tick = {}
        self.min_freight_cars_to_move = min_freight_cars_to_move
        self.max_parcel_capacity = max_parcel_capacity
        self.time_tick = 1

        self.old_state = None
        self.new_state = None

        self.max_time_tick = 10

    def get_state_of_parcels(self):
        state = {x.parcel_id: x.current_location for x in self.parcels.values()}
        #print("State of parcels:", state)
        return state

    def process_parcels(self, booking_file_path):
        with open(booking_file_path, 'r') as file:
            for line in file:
                if line.strip():
                    time_tick, parcel_id, origin, destination, priority = line.split()
                    parcel = Parcel(int(time_tick), parcel_id, origin, destination, int(priority))
                    self.parcels[parcel_id] = parcel
                    if int(time_tick) not in self.parcels_with_time_tick:
                        self.parcels_with_time_tick[int(time_tick)] = []
                    self.parcels_with_time_tick[int(time_tick)].append(parcel)

    def get_new_bookings_at_time_tick_at_vertex(self, time_tick, vertex):
        return self.parcels_with_time_tick.get(time_tick, [])

    def run_simulation(self, run_till_time_tick=None):

        self.old_state = self.get_state_of_parcels()  # Initialize with an empty dictionary
        self.new_state = self.get_state_of_parcels()
        while not (run_till_time_tick is None or self.time_tick >= run_till_time_tick):

            for vertex in self.graph.vertices.values():
                # Move trains first, then group freight cars, and finally clean unmoved freight cars
                vertex.moveTrains()
                vertex.groupFreightCars()
                vertex.clean_unmoved_freight_cars()

            # Update the delivered status for each parcel when a freight car is moved
            for vertex in self.graph.vertices.values():
                for freight_car in vertex.freight_cars:
                    freight_car.move(vertex.name)


            self.old_state = self.new_state  # Update previous state
            self.new_state = self.get_state_of_parcels()
            if not (run_till_time_tick is None or self.time_tick >= run_till_time_tick):
                self.time_tick += 1
        self.time_tick = self.time_tick - 1

    def convergence_check(self, previous_state, current_state):
        # print("Previous state:", previous_state)
        # print("Current state:", current_state)

        # Check if all parcels are delivered or if there are stranded parcels
        if self.all_parcels_delivered() or self.get_stranded_parcels():
            return False

        # Check if the states are the same
        return previous_state == current_state

    def all_parcels_delivered(self):
        return all(parcel.delivered for _, parcel in self.parcels.items())

    def get_delivered_parcels(self):
        return [parcel.parcel_id for parcel in self.parcels.values() if parcel.delivered]

    def get_parcels_delivered_upto_time_tick(self, time_tick):
        return [parcel.parcel_id for parcel in self.parcels.values() if parcel.time_tick <= time_tick and parcel.delivered]

    def get_stranded_parcels(self):
        return [parcel.parcel_id for parcel in self.parcels.values() if not parcel.delivered]

    def status_of_parcels_at_time_tick(self, time_tick):
        return [(parcel.parcel_id, parcel.current_location, parcel.delivered) for parcel in self.parcels.values()
                if parcel.time_tick <= time_tick and not parcel.delivered]

    def status_of_parcel(self, parcel_id):
        return self.parcels[parcel_id].delivered, self.parcels[parcel_id].current_location


    def create_graph(self, graph_file_path):
        with open(graph_file_path, 'r') as file:
            for line in file:
                if line.strip():
                    source, destination = line.split()
                    self.graph.add_edge(source, destination, self.min_freight_cars_to_move, self.max_parcel_capacity)


if __name__ == "__main__":
    prc = PRC(2, 2)
    prc.create_graph('samples/2/graph.txt')
    prc.process_parcels('samples/2/bookings.txt')
    prc.run_simulation(3)
    print(prc.all_parcels_delivered(), ",", prc.get_stranded_parcels())
    assert prc.all_parcels_delivered() == False
    assert 'P2Ludhiana4' in prc.get_stranded_parcels()

    prc.run_simulation(4)
    assert 'P2Ludhiana4' not in prc.get_stranded_parcels()

    # delete the prc object
    del prc
