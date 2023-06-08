from search.algorithms import State
from search.map import Map
import getopt
import sys

import heapq 

def dijkstra(map, start, goal):
    
    OPEN = [] 
    CLOSED = {}
    expandedNodes = 0

 
    heapq.heappush(OPEN, start)
    CLOSED[start.state_hash()] = start
                
    while OPEN:
        
        current = heapq.heappop(OPEN)
        if current == goal:
            map.plot_map(CLOSED, start, goal, 'dijkstra_map')
            return CLOSED[current.state_hash()].get_g(), expandedNodes
       
        children = map.successors(current)
       
        for child in children:
            
            if child.state_hash() not in CLOSED:
                CLOSED[child.state_hash()] = child
                heapq.heappush(OPEN, child)
                expandedNodes +=1
                
            if child.state_hash() in CLOSED and child.get_g() < CLOSED[child.state_hash()].get_g():
                CLOSED[child.state_hash()] = child
                heapq.heapify(OPEN)
    return -1, expandedNodes

def bibs(map, start, goal):
    
    OPEN_forward = []
    OPEN_backward =[]

    CLOSED_forward = {}
    CLOSED_backward = {}
  
    
    cost = float("inf")
   
    expandedNodes = 0
    expandedNodes2 =0 
    
    heapq.heappush(OPEN_forward, start)
    heapq.heappush(OPEN_backward, goal)
    
    CLOSED_forward[start.state_hash()] = start
    CLOSED_backward[goal.state_hash()] = goal
    
    
    
    while OPEN_forward and OPEN_backward:
        
        if cost <= OPEN_forward[0].get_g() + OPEN_backward[0].get_g():
            
            CLOSED = {**CLOSED_forward, **CLOSED_backward}
            
            map.plot_map(CLOSED, start, goal, 'bibs_map')
            
            return cost, expandedNodes+expandedNodes2
        
        # foward expansion and search

        if OPEN_forward[0].get_g() < OPEN_backward[0].get_g():
            
            current = heapq.heappop(OPEN_forward)
            children = map.successors(current)
           
            for child in children:
                childHash = child.state_hash()
                
                if childHash in CLOSED_backward:
                    cost = min(child.get_g() + CLOSED_backward[childHash].get_g(), cost)
                    
                if childHash not in CLOSED_forward:
                    
                    heapq.heappush(OPEN_forward, child)
                    CLOSED_forward[childHash] = child
                    expandedNodes +=1
               
                if childHash in CLOSED_forward and child.get_g() < CLOSED_forward[child.state_hash()].get_g():
                    
                    CLOSED_forward[childHash].set_g(child.get_g())
                    heapq.heappush(OPEN_forward, child)
                    # heapq.heapify(OPEN_forward)
        
        else:
            # backward expansion
            current = heapq.heappop(OPEN_backward)
            children = map.successors(current)
            
            for child in children:
                childHash = child.state_hash()
                
                if childHash in CLOSED_forward:
                    cost = min(child.get_g() + CLOSED_forward[childHash].get_g(),cost)
                    
                if childHash not in CLOSED_backward:
                    heapq.heappush(OPEN_backward, child)
                    CLOSED_backward[childHash] = child
                   
                    expandedNodes2 +=1
                    
                if childHash in CLOSED_backward and child.get_g() < CLOSED_backward[childHash].get_g():
                    
                    CLOSED_backward[childHash].set_g(child.get_g())
                    heapq.heappush(OPEN_backward, child)
                    # heapq.heapify(OPEN_backward)
                       
    return -1, expandedNodes

def main():
    """
    Function for testing your A* and Dijkstra's implementation. There is no need to edit this file.
    Run it with a -help option to see the options available. 
    """
    optlist, _ = getopt.getopt(sys.argv[1:], 'h:m:r:', ['testinstances', 'plots', 'help'])

    plots = False
    for o, a in optlist:
        if o in ("-help"):
            print("Examples of Usage:")
            print("Solve set of test instances: main.py --testinstances")
            print("Solve set of test instances and generate plots: main.py --testinstances --plots")
            exit()
        elif o in ("--plots"):
            plots = True
        elif o in ("--testinstances"):
            test_instances = "test-instances/testinstances.txt"
                              
    gridded_map = Map("dao-map/brc000d.map")
    
    nodes_expanded_dijkstra = []    
    nodes_expanded_bibs = []
    
    start_states = []
    goal_states = []
    solution_costs = []
       
    file = open(test_instances, "r")
    for instance_string in file:
        list_instance = instance_string.split(",")
        start_states.append(State(int(list_instance[0]), int(list_instance[1])))
        goal_states.append(State(int(list_instance[2]), int(list_instance[3])))
        
        solution_costs.append(float(list_instance[4]))
    file.close()
        
    for i in range(0, len(start_states)):    
        start = start_states[i]
        goal = goal_states[i]
    
        cost, expanded_diskstra = dijkstra(gridded_map, start, goal) # Implement here the call to your Dijkstra's implementation for start, goal, and gridded_map
        
        nodes_expanded_dijkstra.append(expanded_diskstra)

        if cost != solution_costs[i]:
            print("There is a mismatch in the solution cost found by Dijkstra and what was expected for the problem:")
            print("Start state: ", start)
            print("Goal state: ", goal)
            print("Solution cost encountered: ", cost)
            print("Solution cost expected: ", solution_costs[i])
            print()

        cost, expanded_astar = bibs(gridded_map, start, goal) # Implement here the call to your Bi-BS's implementation for start, goal, and gridded_map

        nodes_expanded_bibs.append(expanded_astar)
        
        if cost != solution_costs[i]:
            print("There is a mismatch in the solution cost found by Bi-HS and what was expected for the problem:")
            print("Start state: ", start)
            print("Goal state: ", goal)
            print("Solution cost encountered: ", cost)
            print("Solution cost expected: ", solution_costs[i])
            print()
    
    if plots:
        from search.plot_results import PlotResults
        plotter = PlotResults()
        plotter.plot_results(nodes_expanded_bibs, nodes_expanded_dijkstra, "Nodes Expanded (Bi-HS)", "Nodes Expanded (Dijkstra)", "nodes_expanded")
    
    print('Finished running all experiments.')

if __name__ == "__main__":
    main()