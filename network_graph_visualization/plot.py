import sys
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly
import plotly.offline as py
import plotly.io as pio


class GraphNetwork: 
    """An object that builds a network graph in Plotly with Networkx including functions that display node and edge attributes.

    Object requires a graph built with Networkx. If node and edge attributes are to be added to the visualization those attributes need to be added to the graph.   
    """

    def __init__(self, G):

        self.G = G  

        # Get the location of the nodes
        self.pos = nx.spring_layout(self.G) 

    
    def trace_nodes(self, node_color_variable=None, node_text=None):
        """Create a function to build a dictionary to trace nodes, including the color and text when hovering over an edge.          

        :param node_color_variable: The name of the variable that distinguishes nodes by color. 
            The values of the colors are represented as integers. 
            Default equals None when no color is assigned to the nodes.
        :type node_color_variable: str
        :param node_text: The hover text corresponding to each node. 
            The list of strings consists of multiple node attributes each attribute separated by <br> to indicate a new line.
            The list should be ordered by the order in which the nodes appear as in G.nodes().
            The default node text equals None, which means that the name of the node is used when hovering over the node.
        :type node_text: list of strings
        """

        # color nodes by category (where category is a number)
        if node_color_variable:
            node_colors = list(nx.get_node_attributes(self.G, node_color_variable).values())
        else:
            node_colors = []

        # set node text
        if node_text:
            node_text = node_text
        else:
            node_text = []
            for node in self.G.nodes():
                node_text.append("Name: " + node)
        
        # Extract node positions by coordinates
        Xn = [self.pos[k][0] for k in self.pos.keys()]
        Yn = [self.pos[k][1] for k in self.pos.keys()]

        self.trace_nodes = dict(
                                type='scatter',
                                x=Xn, 
                                y=Yn,
                                mode="markers",
                                marker=dict(size=10, color=node_colors),
                                hoverinfo='text',
                                text=node_text
                                )


    def trace_edges(self, edge_text=None, edge_attribute=None):
        """Create a function to build a dictionary to trace edges, including the text when hovering over an edge.        

        :param edge_text: The hover text corresponding to each edge. 
            The list of strings consists of multiple edge attributes each attribute separated by <br> to indicate a new line.
            The list should be ordered by the order in which the edges appear as in G.edges().
        :type edge_text: list of strings, default=None
        :param edge_attribute: The name of the variable to show as a single edge attribute when hovering over the edge.
            When edge_text equals None AND edge_attribute equals None, no edge attributes are shown.  
        :type edge_attribute: str, default=None
        """

        # set edge text
        if edge_text:
            hover_info = 'text'
            edge_text = edge_text
            hover_template = None
        elif edge_attribute:
            hover_info = 'text'
            edge_text = nx.get_edge_attributes(self.G, edge_attribute)
            edge_text = list(edge_text.values())
            hover_template = '{}: %{edge_text}'.format(edge_attribute)
        else:
            hover_info = None
            edge_text = None
            hover_template = None

        Xe=[]
        Ye=[]
        Xtext = []
        Ytext = []

        for e in self.G.edges():
                Xe.extend([self.pos[e[0]][0], self.pos[e[1]][0], None])
                Ye.extend([self.pos[e[0]][1], self.pos[e[1]][1], None])
                Xtext.append((self.pos[e[0]][0] + self.pos[e[1]][0])/2)
                Ytext.append((self.pos[e[0]][1] + self.pos[e[1]][1])/2)

        self.trace_edges = dict(
                                type='scatter',
                                mode='lines',
                                x=Xe,
                                y=Ye,
                                line=dict(width=1, color='#555555')
                                )

        self.trace_edge_text = dict(
                                    type='scatter',
                                    mode='markers',
                                    x=Xtext,
                                    y=Ytext,
                                    marker_size=0.5,
                                    hoverinfo=hover_info,
                                    text=edge_text,
                                    hovertemplate=hover_template
                                    )


    def visualization_attributes(self, title=str):
        """Set axis attributes. 
        
        Default to hiding axis lines, hiding grid, hiding ticklabels.

        Paramaters
        ------------------
        :param title: Title of the graph network plot.
        :type title: str
        :param showline: Defaults to False
        :type showline: bool
        :param zeroline: Defaults to False
        :type zeroline: bool
        :param showgrid: Defaults to False
        :type showgrid: bool
        :param showticklabels: Defaults to False
        :type showticklabels: bool
        :param width: Width of the plot.
        :type width: int
        :param height: Height of the plot.
        :type height: int
        :param autosize: Defaults to False
        :type autosize: bool
        :param showlegend: Defaults to False
        :type showlegend: bool
        :param margin: l=40,r=40,b=85,t=100,pad=0
        :type margin: dictionary of key : int value pairs
        :param hovermode: When hovermode equals 'closest' a single hover label appears for the point directly underneath the cursor.
            Defaults to 'closest'.
        :type hovermode: {'closest'}
        :param plot_bgcolor: Set background color.
            Defaults to '#ffffff'
        :type plot_bgcolor: str
        """

        axis = dict(
                    showline=False, # hide axis line, grid, ticklabels, title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    title='' 
                    )

        self.layout = dict(
                           title=title,  
                           width=600,
                           height=600,
                           autosize=False,
                           showlegend=False,
                           xaxis=axis,
                           yaxis=axis,
                           margin=dict(l=40,r=40,b=85,t=100,pad=0,),
                           hovermode='closest',
                           plot_bgcolor='#ffffff', #set background color            
                           )


    def draw_network(self, graph_filename='graph.html'):
        """Draw the network.

        :param graph_filename: Name and location of the filename as 'html'.
        :type graph_filename: str, default='graph.html'
        :return: Output file with '.html' extension.
        """
        
        fig = dict(
                    data=[
                         self.trace_nodes,
                         self.trace_edges, 
                         self.trace_edge_text
                         ],
                    layout=self.layout
                    )

        pio.write_html(fig, graph_filename) 


# if __name__ == '__main__':
#     plot = GraphNetwork(G)
#     plot.trace_edges()
#     plot.trace_nodes()
#     plot.visualization_attributes()
#     plot.draw_network()

