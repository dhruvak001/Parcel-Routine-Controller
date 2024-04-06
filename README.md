# Parcel Routine Controller

The Parcel Routing Controller (PRC) is a Python program designed to simulate the routing and delivery of parcels in a transportation network. It utilizes various data structures and algorithms to efficiently manage freight cars, parcels, and their movement between different locations in the network.

## Usage:

- Initialize a PRC object with parameters for minimum freight cars to move and maximum parcel capacity per freight car.
- Create the transportation network graph using the create_graph method, providing the path to the graph file.
- Process parcel bookings using the process_parcels method, specifying the path to the booking file.
- Run the simulation using the run_simulation method, optionally specifying the time tick until which to run.
- Check simulation results and status using various methods such as all_parcels_delivered, get_stranded_parcels, etc.

## Note:

- Ensure that the graph file and booking file paths are correct and contain valid data.
- Customize the simulation parameters, such as minimum freight cars to move and maximum parcel capacity, as needed.
- Modify the sample code to fit your specific transportation network and parcel routing requirements.






### Code Overview:

MaxHeap:
Implements a max heap data structure with methods for pushing, popping, and extracting the maximum element.
Used in the PRC for managing parcels based on priority.

Graph:
Represents the transportation network as a graph with vertices and edges.
Provides methods to add edges, perform breadth-first search (BFS), depth-first search (DFS), and manage freight cars within vertices.

Vertex:
Represents a location (e.g., city) in the transportation network.
Stores information about freight cars, parcels, and their movement within the vertex.
Includes methods for grouping freight cars, loading parcels, and moving trains.

FreightCar:
Represents a freight car used for transporting parcels.
Contains attributes such as maximum parcel capacity, current location, destination, and a list of parcels.
Includes methods for loading parcels, determining movement feasibility, and updating the current location.

Parcel:
Represents a parcel to be transported within the transportation network.
Contains attributes such as time tick, parcel ID, origin, destination, priority, and delivery status.
Implements comparison methods based on priority for sorting.

PRC:
Acts as the main controller for the parcel routing simulation.
Manages the graph, freight cars, parcels, and the simulation process.
Includes methods for processing parcels, running the simulation, checking convergence, and obtaining simulation status.
