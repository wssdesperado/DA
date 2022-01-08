import pandas as pd
import csv
import networkx as nx
import matplotlib.pyplot as plt
import community
import argparse
def build_network(required_date):
    # Network rules :   Each node represents one state. If the difference between the
    # hospital capacity of the state A and state B is within a specific value,
    # then regard them as similar states and draw a edge from node A to node B.
    # The weight of each edge is determined by the difference of two nodes' willingness.
    # This network is based on one specific date.
    Mydata = pd.read_csv('../dataset/labeled.csv',sep=',')
    dic = {}
    state_mapping = {}
    did = 1
    record = []
    for i in range(len(Mydata['date'])):
        if Mydata['date'][i] == required_date:
            state, willing, capcity = Mydata['state'][i], Mydata['willingness'][i], Mydata['hospitalBeds capacity'][i]
            state_mapping[state] = did
            dic[did] = [willing,capcity]
            did += 1
    with open('../dataset/network.csv','w+',newline='') as f:
        # write the graph and each edge's weight into file
        csv_write = csv.writer(f)
        for i in dic.keys():
            record.append(i)
            for j in [other for other in dic.keys() if other not in record]:
                if abs(dic[i][1]- dic[j][1]) <= 3000:
                    # if the difference of nodes' hospital capacity is within 3000, then connecting them.
                    data = [ i, j, int(abs(dic[i][0]-dic[j][0]) * 5)+2]
                    csv_write.writerow(data)
    f.close()
    with open('../dataset/state_mapping.txt','w+') as f:
        f.write(str(state_mapping))
    f.close()
def network():
    G = nx.Graph()

    plt.rcParams['savefig.dpi'] = 250
    with open('../dataset/network.csv', 'r') as f:
        for line in f:
            data = line.strip().split(',')
            source = int(data[0])
            target = int(data[1])
            weight = int(data[2])
            G.add_edge(source, target, weight=weight)
    ####### VISUALIZE NETWORK
    # Draw the network using the default settings
    # We are using a small subgraph so we can draw it quickly.
    small_G = G.subgraph([i for i in range(0,100)])  # this gets the subgraph of G for
    #nodes 0-99
    nx.draw(small_G)
    plt.show()
    # Draw, but change some drawing properties
    nx.draw(small_G, node_color='blue', node_size=15, alpha=0.5, arrowsize=5)
    plt.show()
    ####### COMPUTE & PRINT NETWORK STATS
    # Prints summary information about the graph
    print(nx.info(G))
    # Print the degree of each node
    print("Node, Degree")
    for v in list(small_G.nodes()):
        print('{}, {}'.format(v, small_G.degree[v]))
    # Compute and print other stats
    nbr_nodes = len(small_G.nodes())
    nbr_edges = len(small_G.edges())
    print("Number of nodes:", nbr_nodes)
    print("Number of edges:", nbr_edges)
    # find the number of CCs
    nbr_components = nx.number_connected_components(small_G)
    print("Number of connected components:", nbr_components)
    ds = nx.density(small_G)
    print("Network density:", ds)
    CC = nx.average_clustering(G)
    print("Network Cluster coefficient:", CC)
    # Compute betweeness centralities and then store the value with each node in the
    # networkx graph
    centralities = nx.betweenness_centrality(small_G)
    print()
    print("Betweeness of each node")
    for node in list(small_G.nodes()):
        print(centralities[node])
    #####################
    # Clustering
    #####################
    # Conduct modularity clustering
    # Create an unweighted version of G because modularity works only on graphs with
    # non-negative edge weights
    unweighted_SG = nx.Graph()
    for u, v in small_G.edges():
        unweighted_SG.add_edge(u, v)
    partition = community.best_partition(unweighted_SG)
    # Print clusters (You will get a list of each node with the cluster you are in)
    print()
    print("Clusters")
    print(partition)
    # Get the values for the clusters and select the node color based on the cluster
    # value
    values = [partition.get(node) for node in unweighted_SG.nodes()]
    nx.draw_spring(unweighted_SG, cmap = plt.get_cmap('jet'), node_color = values,
    node_size=10, with_labels=False)
    plt.show()
    # Determine the final modularity value of the network
    modValue = community.modularity(partition, unweighted_SG)
    print("modularity: {}".format(modValue))
def main():
    parser = argparse.ArgumentParser(description='date')
    parser.add_argument('date', type=str)
    build_network(parser.parse_args().date)

    network()
if __name__ == '__main__':
    main()
