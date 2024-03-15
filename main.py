import json
import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon,LineString,MultiLineString,MultiPoint
from shapely import get_coordinates,count_coordinates
import networkx as nx
from scipy.spatial import cKDTree

DEGREE_TO_KM=111.32
def get_points(data,sample=None):
    points=[]
    for index,feature in enumerate(data['features']):
        
        l=None
        if feature['geometry']['type']=='LineString':
            l=LineString(feature['geometry']['coordinates'])

        elif feature['geometry']['type']=='MultiLineString':
            l=MultiLineString(feature['geometry']['coordinates'])
        elif   feature['geometry']['type']=='Point':
            l=Point(feature['geometry']['coordinates'])
        coords=get_coordinates(l).tolist()
        points.extend(coords)
    return points

#plot geometries from geoJSON    
def plot_graph(data,ax,label,c='b',sample=None):
    scatter=False
    length=len(data['features'])
    orig=data['features']
    if sample:
       orig=np.random.choice(data['features'],sample)
   
    for index,feature in enumerate(orig):
        l=None
        if feature['geometry']['type']=='LineString':
            l=LineString(feature['geometry']['coordinates'])

        elif feature['geometry']['type']=='MultiLineString':
            l=MultiLineString(feature['geometry']['coordinates'])
        elif   feature['geometry']['type']=='Point':
            l=Point(feature['geometry']['coordinates'])
            scatter=True
        coords=get_coordinates(l).tolist()
        
        x,y=zip(*coords)
        if index==0:
            if scatter is True:
                ax.plot(x, y, c=c, label=label,marker='o', linestyle='None')
            else:
                ax.plot(x, y, c=c, label=label)
        else:
            if scatter is True:
                ax.plot(x, y, c=c,marker='o', linestyle='None')
            else:
                ax.plot(x, y, c=c)
        return ax

#from geoJSON to a graph
def convert_to_graph(data,file_name='graph.json'):
    total_index=0
    g=nx.Graph()
    for index,feature in enumerate(data['features']):
        l=None
        if feature['geometry']['type']=='LineString':
            l=LineString(feature['geometry']['coordinates'])

        elif feature['geometry']['type']=='MultiLineString':
            l=MultiLineString(feature['geometry']['coordinates'])
        elif   feature['geometry']['type']=='Point':
            l=Point(feature['geometry']['coordinates'])
        coords=get_coordinates(l).tolist()

        for index_inner,point in enumerate(coords):
           
           if (index_inner>0):
                g.add_node(total_index+index_inner-1,pos=(coords[index_inner-1][0],coords[index_inner-1][1]))
                g.add_node(total_index+index_inner,pos=(coords[index_inner][0],coords[index_inner][1]))
                g.add_edge(total_index+index_inner-1, total_index+index_inner, weight=np.linalg.norm(np.array(coords[index_inner-1])-np.array(coords[index_inner])))
        total_index+=len(coords)
    return g
#generate all plots
def generate_allPlots():
    bike_path=json.load(open('sherbrooke/Pistes_cyclables.geojson', 'r'))
    road=json.load(open('sherbrooke/Segments_de_rue.geojson', 'r'))
    address=json.load(open('sherbrooke/Adresses.geojson', 'r'))
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    ax.set_title('Sherbrooke')
    _=plot_graph(bike_path, ax, label="Pistes_cyclables", c='r')
    _=plot_graph(road, ax, label="Segments_de_rue", c='b')
    _=plot_graph(address, ax, label="Address", c='y', sample=100)
    plt.legend()
    fig.savefig('graph.png')

def pick_random_work_location(data,seed=10):
    np.random.seed(seed)
    random_data=np.random.choice(data['features'])
    return np.array(random_data['geometry']['coordinates'])

def find_closest_node(graph,coord):
    pos=nx.get_node_attributes(graph,'pos')
    distance=10000
    closest=None
    for p in pos:
        pos[p]=np.array(pos[p])
        if np.linalg.norm(pos[p]-coord)<distance:
            distance=np.linalg.norm(pos[p]-coord)
            closest=p

    return closest

def propose_address(coord,choosen_nodes,within=1):
    address=json.load(open('sherbrooke/Adresses.geojson', 'r'))
    

def plot_with_graph(graph,closest,coord,path_to_choose=None):
    work=nx.Graph()
    work.add_node(0,pos=coord)
    fig, axs = plt.subplots()
    nx.draw_networkx_nodes(work, pos=nx.get_node_attributes(work,'pos'),node_size=100, ax=axs, node_color='m')
    nx.draw(graph, pos=nx.get_node_attributes(graph,'pos'),node_size=1, ax=axs, node_color='r')
    H = nx.subgraph(graph, [closest])
    nx.draw(H, pos=nx.get_node_attributes(H, 'pos'), ax=axs, node_size=100, node_color='g')
    if  path_to_choose:
        I= nx.subgraph(graph, path_to_choose)
        nx.draw_networkx_edges(I, pos=nx.get_node_attributes(I, 'pos'), ax=axs, width=5, edge_color='k')
    plt.show()


def propose_address(target,address_data,within=0.0001):
  
    print (len(address_data['features']))
    propose_address=[]
    for index,address in enumerate(address_data['features']):
        address=np.array(address['geometry']['coordinates'])
        coord= np.array(address)
        if (np.linalg.norm(coord-target)*DEGREE_TO_KM<within):
            propose_address.append(address_data['features'][index]['properties']['ADRESSE'])
        
    return propose_address   
     
if __name__=='__main__':
   
    # #to generate the plot
    # #generate_allPlots()
   
    files=['sherbrooke/Pistes_cyclables.geojson', 'sherbrooke/Segments_de_rue.geojson', 'sherbrooke/Adresses.geojson']
    colors=['r', 'b', 'y']
    address=json.load(open(files[2], 'r'))
    #random work location
    coord=pick_random_work_location(address,seed=100)
    
    data=json.load(open(files[0], 'r'))
    #bike graph    
    graph=convert_to_graph(data)

    #find the closest node to the chosen work location
    closest=find_closest_node(graph, coord)
    
    source=graph.nodes(closest)
    pos=nx.get_node_attributes(graph,'pos')
    #find all shortest paths from the chosen node with a given cutoff
    path=nx.single_source_shortest_path(graph,closest,cutoff=100000)
    
    shortest_distance=10000
    path_to_choose=None
    max_km=10
    min_km=0.1
    #find distances between nodes
    for node in path:
        tmp=node
        distance=0
        for index,j in enumerate(path[node]):
            if index>0:
    
                from_node=np.array(pos[path[node][index-1]])
                to_node=np.array(pos[path[node][index]])
                distance+=np.linalg.norm(from_node-to_node)
                
        if (distance*DEGREE_TO_KM>min_km and distance*DEGREE_TO_KM<max_km) or distance<shortest_distance:
            shortest_distance=distance
            target=node
            path_to_choose=path[node]
        
plot_with_graph(graph, closest, coord, path_to_choose)


  
    
 
    
    


