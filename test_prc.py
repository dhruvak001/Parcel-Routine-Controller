from lab7_1 import PRC

def test_case_1():
    prc = PRC(2, 2)
    prc.create_graph('samples/2/graph.txt')
    prc.process_parcels('samples/2/bookings.txt')
    prc.run_simulation(3)

    # Print the status of 'P2Ludhiana4'
    # print("Status of 'P2Ludhiana4':", prc.status_of_parcel('P2Ludhiana4'))
    
    # # # Print the state of parcels and the list of stranded parcels
    # print("State of parcels:", prc.get_state_of_parcels())
    # print("Stranded parcels:", prc.get_stranded_parcels())
    
    assert prc.all_parcels_delivered() == False
    prc.run_simulation(4)

    assert 'P2Ludhiana4' not in prc.get_stranded_parcels()

    # Print the status of 'P2Ludhiana4'
    # print("Status of 'P2Ludhiana4':", prc.status_of_parcel('P2Ludhiana4'))
    
    # # # Print the state of parcels and the list of stranded parcels
    # print("State of parcels:", prc.get_state_of_parcels())
    # print("Stranded parcels:", prc.get_stranded_parcels())
    
    assert 'P2Ludhiana4' not in prc.get_stranded_parcels()
    # delete the prc object
    del prc

def test_case_2():
    # create a PRC object
    prc = PRC(5,5)
    # create a graph
    prc.create_graph('samples/5/graph.txt')
    prc.process_parcels('samples/5/bookings.txt')
    prc.run_simulation(4)
    assert prc.all_parcels_delivered() == False
    assert 'P31' not in prc.get_delivered_parcels()
    print(prc.get_delivered_parcels())
    print(len(prc.get_parcels_delivered_upto_time_tick(3)))
    assert len(prc.get_parcels_delivered_upto_time_tick(3)) == 25

def test_case_3():
    # create a PRC object
    prc = PRC(2, 2)
    # create a graph
    prc.create_graph('samples/1/graph.txt')
    prc.process_parcels('samples/1/bookings.txt')
    prc.run_simulation(20)
    print(prc.time_tick, " => test 3 passed")
    assert prc.time_tick < 20
    
def test_case_4():
    # create a PRC object
    prc = PRC(5,5)
    # create a graph
    prc.create_graph('samples/3/graph.txt')
    prc.process_parcels('samples/3/bookings.txt')

    # read the graph file and check if the graph is created correctly
    assert len(prc.graph.vertices) == 30

    assert len(prc.graph.edges) == 119
    # print(prc.graph.vertices)
    # print(prc.graph.edges)
    print(" => test 4 passed")

def test_case_5():

    # create a PRC object
    prc = PRC(5,5)
    # create a graph
    prc.create_graph('samples/4/graph.txt')
    prc.process_parcels('samples/4/bookings.txt')

    # check bfs 
    assert prc.graph.bfs('Mumbai', 'Ahmedabad') == ['Mumbai', 'Nashik', 'Ahmedabad']

    print(prc.graph.bfs('Mumbai', 'Ahmedabad'), "=> test 5 passed")

def test_case_6():

    # create a PRC object
    prc = PRC(5,5)
    # create a graph
    prc.create_graph('samples/4/graph.txt')
    prc.process_parcels('samples/4/bookings.txt')
    print(prc.graph.dfs('Chennai',"Rohtak"))
    assert "Tirupati" not in prc.graph.dfs('Chennai', "Rohtak")
    print(prc.graph.dfs('Chennai',"Rohtak"),"=> test 6 passed")



# run the test cases
test_case_1()
test_case_2()
test_case_3()
test_case_4()
test_case_5()
test_case_6()
