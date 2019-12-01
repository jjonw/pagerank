import copy

import matplotlib.pyplot as plt
import networkx as nx


class PageRank(object):
    """docstring for PageRank"""
    def __init__(self, nodes, edges, alpha, epsilon):
        self.epsilon = epsilon # acceptable error
        self.nodes = nodes
        self.edges = edges
        self.graph = nx.DiGraph()
        self.alpha = alpha    # teleport
        

    def make_matrix(self, graph):
        return nx.incidence_matrix(G = graph, oriented = True)

    def print_matrix(self):
        print(self.make_matrix(self.graph).todense())

    def create_graph(self):
        self.graph.add_nodes_from(self.nodes)
        self.graph.add_edges_from(self.edges)

    def show_graph(self):
        pos = nx.layout.spring_layout(self.graph)
        nx.draw(self.graph, pos, node_size=3000, 
            arrow_size=6000, with_labels=True)
        plt.show()

    def sum_node_pr(self, graph_, node):
        # Returns the sum of (nodes/out_degree)
        sum_pr = 0

        for into, out in list(graph_.in_edges(node)):
            L_j = graph_.out_degree(into)
            sum_pr += (graph_.nodes[into]['PR'] / L_j)

        return sum_pr

    # def get_max_pr_from_nodes(self, graph_):
    #     # Returns the maximum PR value of the graph
    #     return max(dict(graph_.nodes.data()).items(), 
    #         key=lambda x: x[1]['PR'])[1]['PR']

    # def get_min_pr_from_nodes(self, graph_):
    #     # Returns the minimum PR value of the graph
    #     return min(dict(graph_.nodes.data()).items(), 
    #         key=lambda x: x[1]['PR'])[1]['PR']

    def is_dangling_node(self, node):
        # Returns True if the node has no out
        # edges
        return True and not self.graph.out_degree(node)

    def dangling_node_correction(self, d_node):
        # If a node is dangling node, add edges from 
        # this node to every other node
        qnt_pages = len(list(self.graph.nodes))

        for node in list(self.graph.nodes):
            if node != d_node:
                self.graph.add_edge(d_node, node)

    def normalize_values(self):
        # Normalize PR values between 0-1 with
        # PR_i = PR_i / sum(PR)
        sum_of = 0
        for node in self.graph.nodes:
            sum_of += self.graph.nodes[node]['PR']

        for node in self.graph.nodes:
            self.graph.nodes[node]['PR'] = (
                self.graph.nodes[node]['PR'] / sum_of)

    def print_pagerank(self, iteraction, current_error):
        # Show nodes PR values and its sum
        print("-------------------------------------------")
        print("### Iteraction ", iteraction)
        print("### Error: ", current_error)

        sum_pr_values = 0
        for node in list(self.graph.nodes):
            print("Node: ", node, " -> PR: ", self.graph.nodes[node]['PR'])
            sum_pr_values += self.graph.nodes[node]['PR']

        print("Sum of PR values: ", sum_pr_values)

    def build_pagerank(self, 
                        dangling_correction = False,
                        last_pr_value = False,
                        normalize_values = False):
        # Calculate pagerank and show it
        qnt_pages = len(list(self.graph.nodes))

        if dangling_correction is True:
            for node in self.graph.nodes:
                if self.is_dangling_node(node):
                    self.dangling_node_correction(node)

        error = None
        iteraction = 1
        
        while error is None or error > self.epsilon:
            if iteraction == 1:
                for node in list(self.graph.nodes):
                    self.graph.nodes[node]['PR'] = 1/qnt_pages
            else:
                # deepcopy is necessary as python only bindes the 
                # variables
                old_graph = copy.deepcopy(self.graph)

                for node in list(self.graph.nodes):
                    # if False use the current iteraction as PR values
                    # else use the old iteraction values
                    if last_pr_value is False:
                        sum_pr = self.sum_node_pr(self.graph, node)
                    else:
                        sum_pr = self.sum_node_pr(old_graph, node)
                    
                    self.graph.nodes[node]['PR'] = ((self.alpha / qnt_pages) \
                                                + ((1 - self.alpha) * sum_pr))
            
            if iteraction > 1:
                error = None
                for node in self.graph.nodes:
                    e = abs(self.graph.nodes[node]['PR'] - old_graph.nodes[node]['PR'])
                    if error is None or error < e:
                        error = e
            
            ## Normalize values to sum to 1 after converging
            if error is not None and error < self.epsilon and normalize_values is True:
                self.normalize_values()

            self.print_pagerank(iteraction, error)

            iteraction += 1
