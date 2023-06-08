from search.algorithms import State
from search.map import Map
import getopt
import sys

import heapq


# Heuristic function, returns the h(n) of a given state and goal.
def heuristics(state, goal):
    
    goalX = goal.get_x()
    goalY = goal.get_y()
    diffX = abs(state.get_x() - goalX)
    diffY = abs(state.get_y() - goalY)
    
    minimum = min(diffX,diffY)
    hVal = (1.5 * minimum) + abs(diffX-diffY)

    return hVal

# A* Search, returns the cost. 
def a_star_search(map, start, goal, index):
    """
    This function implements the A* search algorithm. It takes as input a map, a start state, and a goal state. 
    It returns the cost of the solution path, as well as the number of nodes expanded. 
    """
    OPEN=[]
    CLOSED={}
    
    
    startHVal = heuristics(start, goal)
    start.set_cost(start.get_g()+startHVal)
   
    heapq.heappush(OPEN,start)
    CLOSED[start.state_hash()]= start 
    
    
    #
    while OPEN:
        
        current = heapq.heappop(OPEN)
        
        if current == goal:
            # plot map when done
            map.plot_map(CLOSED, start, goal, 'a_star_map {idx}'.format(idx=index))
            return CLOSED[current.state_hash()].get_cost(), len(CLOSED)
        
        else:
            children = map.successors(current)
            
            for child in children:
                    
                child_h_val = heuristics(child, goal)
                
                child.set_cost(child.get_g() + child_h_val)
                
                if child.state_hash() not in CLOSED:
                    
                    CLOSED[child.state_hash()] = child
                    heapq.heappush(OPEN, child)

                elif child.state_hash() in CLOSED and child.get_cost() < CLOSED[child.state_hash()].get_cost():
                
                    CLOSED[child.state_hash()] = child
                    heapq.heappush(OPEN, child)
                    
    return -1 , len(CLOSED)

# bi-directional A* search
def bi_a_star(map, start, goal, index):
    
    OPENf=[]
    OPENb =[]
    CLOSEDf ={}
    CLOSEDb={}
    
    forwardStartHVal = heuristics(start, goal)
    backwardStartHVal = heuristics(goal, start)
    
    start.set_cost(start.get_g()+forwardStartHVal)
    goal.set_cost(goal.get_g()+backwardStartHVal)
   
    # push the nodes into open list
    heapq.heappush(OPENf, start)
    heapq.heappush(OPENb, goal)
    
    CLOSEDf[start.state_hash()]= start
    CLOSEDb[goal.state_hash()]= goal
    
    cost = float('inf')
    
    while OPENf and OPENb:
        
        if cost <= min(OPENf[0].get_cost(), OPENb[0].get_cost()):
            # combines the two dictionaries
            CLOSED = {**CLOSEDf, **CLOSEDb}
            map.plot_map(CLOSED, start, goal, 'bi_a_star_map {idx}'.format(idx=index))
            return cost, len(CLOSED)
        
        # forward search
        if OPENf[0].get_cost() < OPENb[0].get_cost():
            
            current = heapq.heappop(OPENf)
            children = map.successors(current)
            
            for child in children:
                
                childHVal = heuristics(child, goal)
                
                child.set_cost(child.get_g() + childHVal)
                childHash = child.state_hash()
                
                if childHash in CLOSEDb:
                    cost = min(cost, CLOSEDb[childHash].get_g() + child.get_g())

                if childHash not in CLOSEDf:
                    
                    CLOSEDf[childHash] = child
                    heapq.heappush(OPENf, child)
                    
                if childHash in CLOSEDf and child.get_cost() < CLOSEDf[childHash].get_cost():
                    
                    CLOSEDf[childHash] = child
                    heapq.heappush(OPENf, child)
                    
                    
        elif OPENf[0].get_cost() >= OPENb[0].get_cost():
            #backward search
            current = heapq.heappop(OPENb)
            
            children = map.successors(current)
            
            for child in children:
                
                childHash = child.state_hash()
                
                childHVal = heuristics(child, start)
                child.set_cost(child.get_g() + childHVal)
                
                if childHash in CLOSEDf:
                    cost = min(cost, CLOSEDf[childHash].get_g() + child.get_g())
                
                if childHash not in CLOSEDb:
                    
                    heapq.heappush(OPENb, child)
                    CLOSEDb[childHash] = child
                
                if childHash in CLOSEDb and child.get_cost() < CLOSEDb[childHash].get_cost():
                    
                    heapq.heappush(OPENb, child)
                   
                    CLOSEDb[childHash]= child
                
    return -1, len(CLOSEDf)+len(CLOSEDb)

def mm(map, start, goal, index):
    
    OPENf = []
    OPENb = []
    CLOSEDf = {}
    CLOSEDb = {}
    
    startHVal = heuristics(start, goal)
    goalHVal = heuristics(goal, start)
    
    pForward = max(start.get_g()+ startHVal, (2* start.get_g()))
    pBackward = max(goal.get_g()+ goalHVal, (2* goal.get_g()))
    
    start.set_cost(pForward)
    goal.set_cost(pBackward)
    
    heapq.heappush(OPENf, start)
    heapq.heappush(OPENb, goal)
    
    CLOSEDf[start.state_hash()] = start
    CLOSEDb[goal.state_hash()] =goal
    
    cost = float('inf')
    
    while OPENf and OPENb:
         
        if cost <= min(OPENf[0].get_cost(), OPENb[0].get_cost()):
            
            CLOSED = {**CLOSEDf, **CLOSEDb}
            map.plot_map(CLOSED, start, goal, 'mm{idx}'.format(idx=index))
            return cost, len(CLOSED)
        
        if OPENf[0].get_cost() < OPENb[0].get_cost():
            #Forward Expansion
            
            current = heapq.heappop(OPENf)
            children = map.successors(current)
            
            
            for child in children:
                
                childHash = child.state_hash()
                childHVal = heuristics(child, goal)
                # min of f val or 2*g val
                child.set_cost(max(child.get_g() + childHVal, (2* child.get_g())))
                
                if childHash in CLOSEDb:
                    cost = min(cost, CLOSEDb[childHash].get_g() + child.get_g())
                    
                if childHash not in CLOSEDf:
                    
                    heapq.heappush(OPENf, child)
                    CLOSEDf[childHash] = child
                    
                if childHash in CLOSEDf and child.get_g() < CLOSEDf[childHash].get_g():
                    
                    heapq.heappush(OPENf, child)
                    CLOSEDf[childHash] = child
        else: 
            # backward expansion
            
            current = heapq.heappop(OPENb)
            children = map.successors(current)
            
            for child in children:
                
                childHash = child.state_hash()
                childHVal = heuristics(child, start)
                child.set_cost(max(child.get_g() + childHVal, (2* child.get_g())))
                
                if childHash in CLOSEDf:
                    cost = min(cost, CLOSEDf[childHash].get_g() + child.get_g())
                    
                if childHash not in CLOSEDb:
                    
                    heapq.heappush(OPENb, child)
                    CLOSEDb[childHash] = child
                    
                if childHash in CLOSEDb and child.get_g() < CLOSEDb[childHash].get_g():
                    
                    heapq.heappush(OPENb, child)
                    CLOSEDb[childHash] = child
    
    return -1 , len(CLOSEDf) + len(CLOSEDb)
    

def main():
    """
    Function for testing your implementation. Run it with a -help option to see the options available. 
    """
    optlist, _ = getopt.getopt(sys.argv[1:], 'h:m:r:', ['testinstances', 'plots', 'help'])

    plots = False
    for o, _ in optlist:
        if o in ("-help"):
            print("Examples of Usage:")
            print("Solve set of test instances: main.py --testinstances")
            print("Solve set of test instances and generate plots: main.py --testinstances --plots")
            exit()
        elif o in ("--plots"):
            plots = True
    test_instances = "test-instances/testinstances.txt"
    gridded_map = Map("dao-map/brc000d.map")
    
    nodes_expanded_biastar = []   
    nodes_expanded_astar = []   
    nodes_expanded_mm = []
    
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
       
    for i in range(0, len(start_states) ):   

        start = start_states[i]
        goal = goal_states[i]
    
        cost, expanded_astar = a_star_search(gridded_map, start, goal, i) # Replace None, None with a call to your implementation of A*
        nodes_expanded_astar.append(expanded_astar)

        if cost != solution_costs[i]:
            print("There is a mismatch in the solution cost found by A* and what was expected for the problem:")
            print("Start state: ", start)
            print("Goal state: ", goal)
            print("Solution cost encountered: ", cost)
            print("Solution cost expected: ", solution_costs[i])
            print()

        cost, expanded_mm = mm(gridded_map, start, goal, i)# Replace None, None with a call to your implementation of MM
        nodes_expanded_mm.append(expanded_mm)
        
        if cost != solution_costs[i]:
            print("There is a mismatch in the solution cost found by MM and what was expected for the problem:")
            print("Start state: ", start)
            print("Goal state: ", goal)
            print("Solution cost encountered: ", cost)
            print("Solution cost expected: ", solution_costs[i])
            print()

        cost, expanded_biastar = bi_a_star(gridded_map, start, goal, i) # Replace None, None with a call to your implementation of Bi-A*
        nodes_expanded_biastar.append(expanded_biastar)
        
        if cost != solution_costs[i]:
            print("There is a mismatch in the solution cost found by Bi-A* and what was expected for the problem:")
            print("Start state: ", start)
            print("Goal state: ", goal)
            print("Solution cost encountered: ", cost)
            print("Solution cost expected: ", solution_costs[i])
            print()
    
    print('Finished running all tests. The implementation of an algorithm is likely correct if you do not see mismatch messages for it.')

    if plots:
        from search.plot_results import PlotResults
        plotter = PlotResults()
        plotter.plot_results(nodes_expanded_mm, nodes_expanded_astar, "Nodes Expanded (MM)", "Nodes Expanded (A*)", "nodes_expanded_mm_astar")
        plotter.plot_results(nodes_expanded_mm, nodes_expanded_biastar, "Nodes Expanded (MM)", "Nodes Expanded (Bi-A*)", "nodes_expanded_mm_biastar")
        

if __name__ == "__main__":
    main()