import pygame
from tkinter import filedialog
import numpy as np
import networkx as nx
from Moran.graph import MoranGraphGenerator
from Moran.graph import GraphType
from Moran.MoranTools import MoranGraph, MoranSimulation

pygame.init()
from Prefabs.topbar import Topbar
from Prefabs.sidebar import Sidebar
from Prefabs.graphWindow import GraphWindow
from Prefabs.graphWindow import Mode
from Prefabs.bottomside import BottomSidebar
from Prefabs.bottomleft import BottomLeftSidebar
from Prefabs.node import Node
import globals 

screen = pygame.display.set_mode([1920, 1080])

# Instantiate UI Surfaces
topbar = Topbar()
sidebar = Sidebar(screen)
bottomSidebar = BottomSidebar(screen)
bottomleft = BottomLeftSidebar(screen)
graphWindow = GraphWindow(screen)

# Instantiate MoranGraphGenerator
graphGenerator = MoranGraphGenerator(0,10)
simdata = []

dataArray = [] #Holds adjacency array from opened file.
nodelist = [] #Holds all instantiated nodes
cf = 0
animDelay = 0
lframe = 0

G = nx.barabasi_albert_graph(10, 3)
positions = nx.spring_layout(G) #Positions nodes using spring_layout

for node, pos in positions.items():
    x, y = pos
    nX = int(x * graphWindow.zoom + (1/2) * graphWindow.width + graphWindow.panX)
    nY = int(y * graphWindow.zoom + (1/2) * graphWindow.height + graphWindow.panY)
    nodelist.append(Node(nX,nY, node))

def openFile():
    global G, positions, nodelist
    filepath = filedialog.askopenfile(title="Select a File", filetypes=[("All Files","*.*")])

    if filepath:
        print(f"Selected file {filepath}")
        dataArray = np.loadtxt(filepath)
        print("Loaded Array")
        print(dataArray)

        G = nx.Graph()
        numOfNodes = dataArray.shape[0]
        G.add_nodes_from(range(numOfNodes))

        for i in range(numOfNodes):
            for j in range(i + 1, numOfNodes):
                if dataArray[i,j] == 1:
                    G.add_edge(i, j)
        
        positions = nx.spring_layout(G)

        nodelist = []
        for node, pos in positions.items():
            x, y = pos
            nX = int(x * graphWindow.zoom + (1/2) * graphWindow.width + graphWindow.panX)
            nY = int(y * graphWindow.zoom + (1/2) * graphWindow.height + graphWindow.panY)
            nodelist.append(Node(nX,nY, node))


    else:
        print("No file selected.")

def loadPreset():
    global G,positions,nodelist
    print(topbar.presetTextBox.text)
    if str.isdigit(topbar.presetTextBox.text):
        val = int(topbar.presetTextBox.text)
        print(val)
        if val >= 1 and val < 11:
            graphGenerator = MoranGraphGenerator(GraphType(val), 10)
            G = graphGenerator.getGraph()
            print(G)
            positions = nx.spring_layout(G)
            nodelist = []
            for node, pos in positions.items():
                x, y = pos
                nX = int(x * graphWindow.zoom + (1/2) * graphWindow.width + graphWindow.panX)
                nY = int(y * graphWindow.zoom + (1/2) * graphWindow.height + graphWindow.panY)
                nodelist.append(Node(nX,nY, node))

def addNode():
    graphWindow.mode = Mode.ADD_NODE

def linkNode():
    graphWindow.mode = Mode.LINK_NODE_ONE

def mutate():
    if globals.selectedNode != -1:
        nodelist[globals.selectedNode].mutant = not nodelist[globals.selectedNode].mutant

def simulate():
    global simdata,nodelist
    infected = []
    for node in nodelist:
        if node.mutant == True:
            infected.append(node.id)
    moranGraph = MoranGraph(G,float(bottomSidebar.relativeFitnessTextBox.text),infected)
    sim = MoranSimulation(moranGraph)
    sim.run(1)
    simdata = sim.simulationMemory
    lastFrameNum = simdata.__len__()
    for node in nodelist:
        node.mutant = False

    for i in simdata[-1]:
        nodelist[i].mutant = True

    bottomleft.framesText.text = str(lastFrameNum)
    bottomleft.currentFrameText.text = str(lastFrameNum-1)
    # print(simdata)

def back():
    global nodelist,simdata
    if simdata.__len__() != 0 :
        bottomleft.currentFrameText.text = "0"
        for node in nodelist:
            node.mutant = False

        for i in simdata[0]:
            nodelist[i].mutant = True
        left()

def end():
    global nodelist,simdata
    if simdata.__len__() != 0 :
        bottomleft.currentFrameText.text = str(simdata.__len__() - 1);
        for node in nodelist:
            node.mutant = False

        for i in simdata[0]:
            nodelist[i].mutant = True
        right()

def left():
    global nodelist,simdata
    currentFrame = int(bottomleft.currentFrameText.text)
    currentFrame -= 1
    if simdata.__len__() != 0 :
        if currentFrame < 0:
            currentFrame = 0
        bottomleft.currentFrameText.text = str(currentFrame)
        for node in nodelist:
            node.mutant = False

        for i in simdata[currentFrame]:
            nodelist[i].mutant = True

def right():
    global nodelist,simdata
    currentFrame = int(bottomleft.currentFrameText.text)
    currentFrame += 1
    if simdata.__len__() != 0 :
        if currentFrame >= simdata.__len__():
            currentFrame = simdata.__len__()-1
        bottomleft.currentFrameText.text = str(currentFrame)
        for node in nodelist:
            node.mutant = False

        for i in simdata[currentFrame]:
            nodelist[i].mutant = True

def play():
    graphWindow.mode = Mode.PLAY_INIT
    


#Main Loop
running = True
while running:
    
    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                graphWindow.zoom += 10
            elif event.button == 5:  # Scroll down
                graphWindow.zoom -= 10
                if graphWindow.zoom < 1:
                    graphWindow.zoom = 1
            if graphWindow.mode == Mode.ADD_NODE:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    nodeID = nodelist.__len__()
                    nodelist.append(Node(x,y,nodeID))
                    oX = (x-(1/2) * graphWindow.width - graphWindow.panX)/graphWindow.zoom
                    oY = (y-(1/2) * graphWindow.height - graphWindow.panY)/graphWindow.zoom
                    positions[nodeID] = [oX,oY]
                    G.add_node(nodeID)
                    graphWindow.mode = Mode.NORMAL
                elif event.button == 3:
                    graphWindow.mode = Mode.NORMAL
            elif graphWindow.mode == Mode.LINK_NODE_PROCESS:
                if (graphWindow.linknode1 != None and graphWindow.linknode2 != None):
                    G.add_edge(graphWindow.linknode1,graphWindow.linknode2, weight=1)
                    graphWindow.linknode1 = None
                    graphWindow.linknode2 = None
                    graphWindow.mode = Mode.NORMAL


        # Prefab Callback Handling
        graphWindow.drag_to_pan(event)
        topbar.container.children[0].clickedCallback(event, openFile) # Open File Button
        topbar.container.children[1].clickedCallback(event) # Preset Textbox
        topbar.container.children[2].clickedCallback(event, loadPreset) # Load Preset Button
        sidebar.container.children[0].clickedCallback(event, addNode) # Add Node Button
        sidebar.container.children[1].clickedCallback(event, linkNode) # Link Node
        sidebar.container.children[2].clickedCallback(event, mutate) # Mutate
        bottomSidebar.container.children[1].clickedCallback(event) 
        bottomSidebar.container.children[3].clickedCallback(event)
        bottomSidebar.container.children[4].clickedCallback(event, simulate) # Simulate Button
        bottomleft.container.children[2].clickedCallback(event, back)
        bottomleft.container.children[3].clickedCallback(event, left)
        bottomleft.container.children[5].clickedCallback(event, right)
        bottomleft.container.children[6].clickedCallback(event, end)
        bottomleft.container.children[7].clickedCallback(event, play)

        for node in nodelist:
            node.move_node(event, positions, graphWindow)
            node.is_clicked(graphWindow,event)
        

    screen.fill((255,255,255))

    if graphWindow.mode == Mode.PLAY_INIT:
        cf = int(bottomleft.currentFrameText.text)
        animDelay = float(bottomSidebar.animationDelayTextBox.text)
        lframe = simdata.__len__()
        graphWindow.mode = Mode.PLAY

    if graphWindow.mode == Mode.PLAY:
        if cf < lframe:
            pygame.time.delay(int(animDelay * 1000))
            
            for node in nodelist:
                node.mutant = False

            for i in simdata[cf]:
                nodelist[i].mutant = True
            
            cf+=1
            bottomleft.currentFrameText.text = str(cf)
        else:
            graphWindow.mode = Mode.NORMAL

    #Draws Edges
    for edge in G.edges:
        pygame.draw.line(screen, (100,100,100), (positions[edge[0]][0] * graphWindow.zoom + (1/2 * graphWindow.width + graphWindow.panX), positions[edge[0]][1] * graphWindow.zoom + (1/2 * graphWindow.height + graphWindow.panY) ), (positions[edge[1]][0] * graphWindow.zoom + (1/2 * graphWindow.width + graphWindow.panX),positions[edge[1]][1] * graphWindow.zoom + (1/2 *graphWindow.height + graphWindow.panY)), 5)

    #Draws Nodes
    for node, pos in positions.items():
        int1, int2 = pos
        
        # x = int(int1 * graphWindow.zoom + (1/2) * graphWindow.width + graphWindow.panX)
        # y = int(int2 * graphWindow.zoom + (1/2) * graphWindow.height + graphWindow.panY)
        # pygame.draw.circle(screen, (255,0,0), (x, y), 20)
        nodelist[node].set_pos(int(int1 * graphWindow.zoom + (1/2) * graphWindow.width + graphWindow.panX),int(int2 * graphWindow.zoom + (1/2) * graphWindow.height + graphWindow.panY))
        nodelist[node].draw(screen)

    
    
   
    #Draws UI
    graphWindow.draw(screen)
    topbar.draw(screen)
    sidebar.draw(screen)
    bottomSidebar.draw(screen)
    bottomleft.draw(screen)

    #Refresh Screen
    pygame.display.flip()

pygame.quit()

