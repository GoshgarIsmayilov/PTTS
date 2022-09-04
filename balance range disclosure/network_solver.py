import time
import random
import subprocess
from ortools.graph import pywrapgraph
import graphviz

"""
CONSTANT PARAMETERS
"""
VISIBILITY = 0.5
TOTAL_SUPPLY = 1000000
NUMBER_OF_ADDRESS = 100000
NUMBER_OF_TRANSACTION = 100
NUMBER_OF_RUN = 20
PNS_VERSION = 0   # 0: PNS-Seq, 1: PNS-Omp, 2: PNS-Omp-Avx2
IS_VERBOSE_ENABLED = False
IS_GRAPHVIZ_ENABLED = False
IS_LOGGING_ENABLED = False


class Node:
    """
    Node class with id and balance represents user in blockchain.
    """
    def __init__(self, _id, balance):
        self.id = _id
        self.balance = balance

class Edge:
    """
    Edge class with id, sender, receiver and amount represents transaction in blockchain.
    """
    def __init__(self, _id, sender, receiver, amount):
        self.id = _id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        
        
def generate_users(): 
    """
    It generates nodes (users) with respect to the given number of addresses.
    
    Parameters
    ----------

    Returns
    -------
    users (List[Node]): list of nodes (users)

    """
    users = [Node(0, TOTAL_SUPPLY)]
    users += [Node(i, 0) for i in range(1, NUMBER_OF_ADDRESS)]
    return users


def generate_transactions(users: list):
    """
    It generates edges (transactions) with respect to the given number of transactions.
    
    Parameters
    ----------
    users (List[Node]): list of nodes (users)

    Returns
    -------
    transactions (List[Edge]): list of edges (transactions)

    """
    transactions = []
    
    senders = set([users[0]])
    
    for i in range(0, NUMBER_OF_TRANSACTION):
    
        sender = random.choice(tuple(senders))
        
        receiver = random.choice(users)
        while sender.id == receiver.id:
            receiver = random.choice(users)
        
        amount = random.randint(1, sender.balance)
        
        sender.balance -= amount
        receiver.balance += amount
        
        if sender.balance == 0:
            senders.remove(sender)
   
        senders.add(receiver)
        if len(senders) > 1000:
            sender_to_delete = random.sample(senders, 1)[0]
            senders.remove(sender_to_delete)
        
        transactions.append(Edge(i, sender, receiver, amount)) 

    return transactions


        
def generate_open_transactions(transactions: list):
    """
    It generates open edges (transactions) with respect to the given visibility ratio.
    The amounts of open transactions are visible.
    
    Parameters
    ----------
    transactions (List[Edge]): list of edges (transactions)

    Returns
    -------
    open_transactions (List[Edge]): list of open edges (transactions)

    """
    open_transactions = random.sample(transactions, int(len(transactions) * VISIBILITY))
    return open_transactions


def print_users_and_transactions(users: list, transactions: list, open_transactions: list):
    """
    It prints users, transactions and open transactions.
    
    Parameters
    ----------
    users (List[Node]): list of nodes (users)
    transactions (List[Edge]): list of edges (transactions)
    open_transactions (List[Edge]): list of open edges (transactions)

    Returns
    -------

    """
    if IS_VERBOSE_ENABLED:
        print("\nUSERS:")
        for user in users:
            print(user.id, user.balance)
        
        print("\nTRANSACTIONS:")
        for transaction in transactions:
            print(transaction.sender.id, transaction.receiver.id, transaction.amount)
            
        print("\nOPEN TRANSACTIONS:")
        for open_transaction in open_transactions:
            print(open_transaction.sender.id, open_transaction.receiver.id, open_transaction.amount)


def log_transactions(transactions: list):
    """
    It logs transactions.
    
    Parameters
    ----------
    transactions (List[Edge]): list of edges (transactions)

    Returns
    -------

    """
    if IS_LOGGING_ENABLED:
        file = open("transactions_log_" + str(NUMBER_OF_ADDRESS) + "_" + str(NUMBER_OF_TRANSACTION) + "_" + str(VISIBILITY) + ".txt", "w")
        file.write("Sender -> Receiver: Amount\n")
        for transaction in transactions:
            file.write(str(transaction.sender.id) + " -> " + str(transaction.receiver.id) + " : " + str(transaction.amount) + "\n")
        

def set_network_parameters(transactions: list, open_transactions: list, cost: int, user_in_focus: Node):
    """
    It sets network parameters including unit_costs, start_nodes, end_nodes, 
    capacities and supplies.
    
    Parameters
    ----------
    transactions (List[Edge]): list of edges (transactions)
    open_transactions (List[Edge]): list of open edges (transactions)
    cost (int): cost for the edge between user in focus and sink node, -1 or 1
    user_in_focus (Node): user whose balance are in focus

    Returns
    -------
    unit_costs (list[int]): unit costs of the edges
    start_nodes (list[int]): start (head) nodes of the edges
    end_nodes (list[int]): end (tail) nodes of the edges
    capacities (list[int]): capacities edges can carry at most
    supplies (list[int]): supplies nodes can provide as positive or negative

    """
    unit_costs = [0] * (len(transactions) + NUMBER_OF_ADDRESS)
    unit_costs[len(transactions) + user_in_focus.id] = cost
 
    start_nodes = [transaction.sender.id for transaction in transactions] + list(range(NUMBER_OF_ADDRESS))
    
    end_nodes = [transaction.receiver.id for transaction in transactions] + [NUMBER_OF_ADDRESS] * NUMBER_OF_ADDRESS
    
    capacities = [TOTAL_SUPPLY] * (len(transactions) + NUMBER_OF_ADDRESS)
    for transaction in open_transactions:
        capacities[transaction.id] = 0
    
    supplies = [TOTAL_SUPPLY] + [0] * (NUMBER_OF_ADDRESS-1) + [-TOTAL_SUPPLY]
    for transaction in open_transactions:
        supplies[transaction.sender.id] -= transaction.amount
        supplies[transaction.receiver.id] += transaction.amount

    return unit_costs, start_nodes, end_nodes, capacities, supplies
   


def print_network_parameters(unit_costs: list, start_nodes: list, end_nodes: list, capacities: list, supplies: list):
    """
    It prints network parameters including unit_costs, start_nodes, end_nodes, 
    capacities and supplies.
    
    Parameters
    ----------
    unit_costs (list[int]): unit costs of the edges
    start_nodes (list[int]): start (head) nodes of the edges
    end_nodes (list[int]): end (tail) nodes of the edges
    capacities (list[int]): capacities edges can carry at most
    supplies (list[int]): supplies nodes can provide as positive or negative

    Returns
    -------

    """
    if IS_VERBOSE_ENABLED:
        print("\nNETWORK PARAMETERS:")
        print("Unit costs: ", unit_costs)
        print("Start nodes: ", start_nodes)
        print("End nodes: ", end_nodes)
        print("Capacities: ", capacities)
        print("Supplies: ", supplies)
 
    
def solve_network(unit_costs: list, start_nodes: list, end_nodes: list, capacities: list, supplies: list):
    """
    It solves the minimum cost flow network for the given network parameters.
    
    Parameters
    ----------
    unit_costs (list[int]): unit costs of the edges
    start_nodes (list[int]): start (head) nodes of the edges
    end_nodes (list[int]): end (tail) nodes of the edges
    capacities (list[int]): capacities edges can carry at most
    supplies (list[int]): supplies nodes can provide as positive or negative

    Returns
    -------
    min_cost_flow (object[SimpleMinCostFlow]): minimum cost flow network
    status (int): status of solution, 1 for success 
    
    """
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()
    
    for arc in zip(start_nodes, end_nodes, capacities, unit_costs):
        min_cost_flow.AddArcWithCapacityAndUnitCost(arc[0], arc[1], arc[2], arc[3])

    for count, supply in enumerate(supplies):
        min_cost_flow.SetNodeSupply(count, supply)

    status = min_cost_flow.Solve()
    return min_cost_flow, status


def print_flow_solution(min_cost_flow: object, status: int):
    """
    It prints the solution for the minimum cost flow network.
    
    Parameters
    ----------
    min_cost_flow (object[SimpleMinCostFlow]): minimum cost flow network
    status (int): status of solution, 1 for success 

    Returns
    -------
    
    """
    if IS_VERBOSE_ENABLED:
        if status == min_cost_flow.OPTIMAL:
            print("\nFLOW SOLUTION:")
            print('Minimum cost: ', min_cost_flow.OptimalCost())
            print('')
            print(' Arc   Flow / Capacity  Cost')
            for i in range(min_cost_flow.NumArcs()):
                cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
                print('%1s -> %1s    %3s   / %3s   %3s' %
                      (min_cost_flow.Tail(i), min_cost_flow.Head(i),
                       min_cost_flow.Flow(i), min_cost_flow.Capacity(i), cost))
     
    
def draw_network_with_graphviz(users: list, start_nodes: list, end_nodes: list, open_transactions: list, user_in_focus: Node): 
    """
    It draws transaction graph and the minimum cost flow network with graphviz.
    
    Parameters
    ----------
    users (List[Node]): list of nodes (users)
    start_nodes (list[int]): start (head) nodes of the edges
    end_nodes (list[int]): end (tail) nodes of the edges
    open_transactions (List[Edge]): list of open edges (transactions)
    user_in_focus (Node): user whose balance are in focus

    Returns
    -------
    
    """
    if IS_GRAPHVIZ_ENABLED:
        dot_network = graphviz.Digraph('network')
        dot_transactions = graphviz.Digraph('transactions')
    
        for i in range(len(start_nodes)):
            if start_nodes[i] in end_nodes:
                dot_network.edge(str(start_nodes[i]), str(end_nodes[i]))
        for user in users: 
            if user.id in end_nodes:
                dot_network.node(str(user.id), style="filled", color="orange")
        dot_network.node(str(0), style="filled", color="black")
        dot_network.node(str(user_in_focus.id), style="filled", color="red")
        dot_network.node(str(NUMBER_OF_ADDRESS), style="filled", color="black")
        
        count = 0
        for i in range(len(start_nodes)): 
            if end_nodes[i] != NUMBER_OF_ADDRESS:
                dot_transactions.edge(str(start_nodes[i]), str(end_nodes[i]))
                count += 1
        for user in users: 
            if user.id in end_nodes:
                dot_transactions.node(str(user.id), style="filled", color="orange")   
        dot_transactions.node(str(0), style="filled", color="black")
        dot_transactions.node(str(user_in_focus.id), style="filled", color="red") 
        
        file_network = open("input_network.dot", "w")
        file_network.write(dot_network.source)
        
        file_transactions = open("input_transactions.dot", "w")
        file_transactions.write(dot_transactions.source)
        
        # dot -Tpdf input_network.dot > output.pdf
        # dot -Tpdf input_transactions.dot > output.pdf
        
        print(count)


def calculate_certainty_rate(minimum_value, maximum_value, user_in_focus):
    """
    It prints final ranges for the end of binary search. 
    
    Parameters
    ----------
    minimum_value (int): minimum possible balance for the node in focus
    maximum_value (int): maximum possible balance for the node in focus
    user_in_focus (Node): user whose balance are in focus

    Returns
    -------
    certainty_rate (float): certainty rate for the balance of user in focus 
    
    """
    is_correct = (minimum_value <= user_in_focus.balance <= maximum_value)
    
    certainty_rate = (TOTAL_SUPPLY - (maximum_value - minimum_value)) / TOTAL_SUPPLY
    
    print("\nFINAL RANGE: ", user_in_focus.balance, [minimum_value, maximum_value])
    print("IS CORRECT: ", is_correct)
    print("CERTAINTY RATE: ", certainty_rate)
    
    return certainty_rate
    

def solve_with_pns(unit_costs, start_nodes, end_nodes, capacities, supplies):
    """
    It solves the network with parallel network simplex algorithm.
    (PNS-Seq, PNS-Omp, PNS-Omp-Avx2)
    
    Parameters
    ----------
    unit_costs (list[int]): unit costs of the edges
    start_nodes (list[int]): start (head) nodes of the edges
    end_nodes (list[int]): end (tail) nodes of the edges
    capacities (list[int]): capacities edges can carry at most
    supplies (list[int]): supplies nodes can provide as positive or negative

    Returns
    -------
    elapsed time (float): elapsed between to solve the network
    
    """
    file = open("pns/samples/balance_disclosure.min", "w")
    file.write("p min " + str(len(supplies)) + " " + str(len(unit_costs)) + "\n")
    
    for i in range(len(supplies)):
        file.write("n " + str(i + 1) + " " + str(supplies[i]) + "\n")

    for i in range(len(unit_costs)):
        file.write("a " + str(start_nodes[i] + 1) + " " + str(end_nodes[i] + 1) + " 0 " + str(capacities[i]) + " " + str(unit_costs[i]) +  "\n")
    file.close()

    if PNS_VERSION == 0:
        result = subprocess.run(['./pns/pns-seq', 'pns/samples/balance_disclosure.min'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    elif PNS_VERSION == 1:
        result = subprocess.run(['./pns/pns-omp', 'pns/samples/balance_disclosure.min'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    else:
        result = subprocess.run(['./pns/pns-omp-avx2', 'pns/samples/balance_disclosure.min'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    start_substring = "c Init Time           : "
    finish_substring = " ms"
    start_location = result.find(start_substring) + len(start_substring)
    offset = result[start_location:].find(finish_substring)
    pns_elapsed_init_time = int(result[start_location: start_location + offset]) / 1000
    
    start_substring = "c Time                : "
    finish_substring = " ms"
    start_location = result.find(start_substring) + len(start_substring)
    offset = result[start_location:].find(finish_substring)
    pns_elapsed_time = int(result[start_location: start_location + offset]) / 1000
    
    return pns_elapsed_init_time + pns_elapsed_time

    
def solve():
    """
    It solves the given minimum cost flow network with binary search. 
    
    Parameters
    ----------

    Returns
    -------
    """
    users = generate_users()
    
    start_time = time.time()
    
    transactions = generate_transactions(users)
    
    print("Graph Generation Elapsed Time: ", time.time() - start_time)
    
    open_transactions = generate_open_transactions(transactions)
    log_transactions(transactions)
    print_users_and_transactions(users, transactions, open_transactions)
    
    elapsed_times_google_or = []
    elapsed_times_pns = []
    certainty_rates = []
    
    users_in_focus = random.sample([user for user in users if user.balance > 0], NUMBER_OF_RUN)
    
    for run in range(NUMBER_OF_RUN):
        unit_costs, start_nodes, end_nodes, capacities, supplies = set_network_parameters(transactions, open_transactions, +1, users_in_focus[run])
        pns_elapsed_time_1 = solve_with_pns(unit_costs, start_nodes, end_nodes, capacities, supplies)
        
        print_network_parameters(unit_costs, start_nodes, end_nodes, capacities, supplies)
        start_time_1 = time.time()
        min_cost_flow, status = solve_network(unit_costs, start_nodes, end_nodes, capacities, supplies)
        end_time_1 = time.time()
        print_flow_solution(min_cost_flow, status)
        minimum_value = min_cost_flow.Flow(len(transactions) + users_in_focus[run].id) 
    
        unit_costs, start_nodes, end_nodes, capacities, supplies = set_network_parameters(transactions, open_transactions, -1, users_in_focus[run])
        pns_elapsed_time_2 = solve_with_pns(unit_costs, start_nodes, end_nodes, capacities, supplies)
        
        print_network_parameters(unit_costs, start_nodes, end_nodes, capacities, supplies)
        start_time_2 = time.time()
        min_cost_flow, status = solve_network(unit_costs, start_nodes, end_nodes, capacities, supplies)
        end_time_2 = time.time()
        print_flow_solution(min_cost_flow, status)
        maximum_value = min_cost_flow.Flow(len(transactions) + users_in_focus[run].id)
    
        draw_network_with_graphviz(users, start_nodes, end_nodes, open_transactions, users_in_focus[run])
        
        certainty_rate = calculate_certainty_rate(minimum_value, maximum_value, users_in_focus[run])
        certainty_rates.append(certainty_rate)
    
        elapsed_time_google_or = (end_time_1 - start_time_1) + (end_time_2 - start_time_2)
        elapsed_times_google_or.append(elapsed_time_google_or)
        
        elapsed_time_pns = pns_elapsed_time_1 + pns_elapsed_time_2
        elapsed_times_pns.append(elapsed_time_pns)
    
    print("\nAverage Elapsed Time Google-OR: ", sum(elapsed_times_google_or) / len(elapsed_times_google_or))
    print("Average Elapsed Time PNS: ", sum(elapsed_times_pns) / len(elapsed_times_pns))
    print("Average Certainty Rate: ", sum(certainty_rates) / len(certainty_rates))
            
if __name__ == '__main__':
    solve()
    
    