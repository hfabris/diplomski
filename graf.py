from PyQt5.QtWidgets import *   #QWidget, QApplication, QStyleFactory, QDesktopWidget, QGridLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from os import environ
import networkx as nx
import json
import network
import random
import time


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

class PrettyWidget(QWidget):

    def __init__(self, network_info, components_possitions, attacker_progress):


        super(PrettyWidget, self).__init__()
        font = QFont()
        font.setPointSize(16)
        self.network_info = network_info
        self.attacker_progress = attacker_progress
        
        self.height = int(components_possitions["dimensions"]["height"])
        self.width = int(components_possitions["dimensions"]["width"])
        self.possitions = components_possitions["components"]
        
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, self.height, self.width)
        self.center()
        self.setWindowTitle('Network Plot')

        grid = QGridLayout()
        self.setLayout(grid)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 1, 2, 8, 9)

        # Create network graph from network informations
        self.g = make_network(self.network_info, self.possitions, self.height, self.width)

        self.network_info.add_graph(self.g)

        # Create scrollbar with buttons for getting user components informations
        # Add scrollbar to the left side of the grid
        user = ["\n".join(comp.name.split("_")) for comp in self.network_info.user_components]
        self.create_component_group_box(user)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)

        # self.create_legend_group_box()
        # buttonLayout.addLayout(self.legend_layout)
        
        grid.addLayout(buttonLayout, 0, 0, 6, 2)

        self.create_legend_group_box()
        grid.addLayout(self.legend_layout, 6, 0, 2,2)

        self.create_upper_bar()
        grid.addLayout(self.horizontal_layout, 0, 2, 1, 7)


        # user = ["\n".join(comp.name.split("_")) for comp in self.network_info.user_components]
        # self.create_component_group_box(user)
        # buttonLayout = QVBoxLayout()
        # buttonLayout.addWidget(self.verticalGroupBox)
        # grid.addLayout(buttonLayout, 0, 0, 6, 2)

        # self.create_upper_bar()
        # grid.addLayout(self.horizontal_layout, 0, 2, 1, 1)



        self.showMaximized()

    def create_upper_bar(self):
        self.horizontal_layout = QGridLayout()
        font = QFont()
        font.setBold(True)

        strategy_layout = QHBoxLayout()

        strategy_label = QLabel()
        strategy_label.setFont(font)
        strategy_label.setText("\tSelect attacker strategy: ")
        strategy_layout.addWidget(strategy_label)

        strategy_combo = QComboBox(self)
        for strategy in self.attacker_progress:
            strategy_combo.addItem(strategy)
            game = self.attacker_progress[strategy]
        strategy_layout.addWidget(strategy_combo)

        self.horizontal_layout.addLayout(strategy_layout, 0, 0)

        game_layout = QHBoxLayout()

        game_label = QLabel()
        game_label.setFont(font)
        game_label.setText("\tSelect attacker game: ")
        game_layout.addWidget(game_label)

        game_combo = QComboBox(self)
        for i in game:
            game_combo.addItem(str(i))
            round = game[i]
        game_layout.addWidget(game_combo)

        self.horizontal_layout.addLayout(game_layout, 0, 1)

        round_layout = QHBoxLayout()
        
        round_label = QLabel()
        round_label.setFont(font)
        round_label.setText("\tSelect attacker round: ")
        round_layout.addWidget(round_label)

        strategy = strategy_combo.currentText()
        game = int(game_combo.currentText())
        round_combo = QComboBox(self)
        for round in self.attacker_progress[strategy][game]: 
            round_combo.addItem(str(round))
        round_combo.activated.connect(lambda: self.show_round(strategy_combo.currentText(), int(game_combo.currentText()), int(round_combo.currentText())))
        round_layout.addWidget(round_combo)

        game_combo.activated.connect(lambda: self.refresh_round(strategy_combo.currentText(), int(game_combo.currentText()), round_combo))

        self.horizontal_layout.addLayout(round_layout, 0, 2)

        emulate_button = QPushButton("Emulate")
        self.horizontal_layout.addWidget(emulate_button, 0, 3)
        emulate_button.clicked.connect(lambda: self.emulate(strategy_combo.currentText(), int(game_combo.currentText())))
        
        exit_button = QPushButton("Exit")
        self.horizontal_layout.addWidget(exit_button, 0 ,4)
        exit_button.clicked.connect(lambda:self.close())

        self.show_round(strategy_combo.currentText(), int(game_combo.currentText()), int(round_combo.currentText()))

    def create_legend_group_box(self):
        
        self.legend_layout = QVBoxLayout()
        
        colors = [ "skyblue", "red", "green", "yellow", "cyan", "gray"]
        texts = [ "network components", "user componnets", "attacker has foothold on component", "attacker enumerated component",
            "attacker has escalated priviledges on component", "attacker has exfiltrated data from component"]
        
        combinations = zip(colors, texts)
        
        layout = QGridLayout()
        
        font = QFont()
        font.setBold(True)
        
        text_label = QLabel()
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(font)
        text_label.setText("colour")
        layout.addWidget(text_label, 0, 0)

        text_label = QLabel()
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(font)
        text_label.setText("colour meaning")
        layout.addWidget(text_label, 0, 1)
        
        for color, text in zip(colors, texts):
            
            i = colors.index(color)
            
            color_label = QLabel()
            color_label.setAlignment(Qt.AlignCenter)
            color_label.setAutoFillBackground(True)
            palette = QPalette()
            palette.setColor(QPalette.Background, QColor(color))
            color_label.setPalette(palette)
            color_label.setText(color)
            layout.addWidget(color_label, i+1, 0)
            
            text_label = QLabel()
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setWordWrap(True)
            text_label.setText(text)
            layout.addWidget(text_label, i+1, 1)
            
        self.legend_layout.addLayout(layout)

        
        text_label = QLabel()
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(font)
        text_label.setText("Attacker action: ")
        self.legend_layout.addWidget(text_label)

        self.attacker_action = QLabel()
        self.attacker_action.setAlignment(Qt.AlignCenter)
        self.attacker_action.setFont(font)
        self.attacker_action.setText(" ")
        self.legend_layout.addWidget(self.attacker_action)


    def emulate(self, strategy, game):
        
        rounds = int(list(self.attacker_progress[strategy][game].keys())[-1])

        for round in range(10):
            # print(round)
            self.show_round(strategy, game, round)
            time.sleep(1)

    def refresh_round(self, strategy, game, widget):

        widget.clear()

        for round in self.attacker_progress[strategy][game]: 
            widget.addItem(str(round))


    def show_round(self, strategy, game, round):
        # print("Selected strategy is {}, game {}, round {}".format(strategy, game, round))
        game = int(game)        

        user = ["\n".join(comp.name.split("_")) for comp in self.network_info.user_components]
        user_g = nx.subgraph(self.g,user)

        action, knowledge, compromise = self.attacker_progress[strategy][game][round].values()

        self.attacker_action.setText("Round: " + str(round) + "\naction: " + action[0] + " on component " + action[1])
        self.attacker_action.setWordWrap(True)

        footholds = set([x.name.split(" ")[0] for x in compromise["footholds"]])
        footholds = ["\n".join(x.split("_")) for x in footholds]
        footholds_subgraph = nx.subgraph(self.g, footholds)

        enumerated = set([x.name.split(" ")[0] for x in compromise["enumerated"]])
        enumerated = ["\n".join(x.split("_")) for x in enumerated]
        enumerated_subgraph = nx.subgraph(self.g, enumerated)

        escalated = set([x.name.split(" ")[0] for x in compromise["escalated"]])
        escalated = ["\n".join(x.split("_")) for x in escalated]
        escalated_subgraph = nx.subgraph(self.g, escalated)

        exfiltrated = set([x.name.split(" ")[0] for x in compromise["exfiltrated"]])
        exfiltrated = ["\n".join(x.split("_")) for x in exfiltrated]
        exfiltrated_subgraph = nx.subgraph(self.g, exfiltrated)

        # Plot network
        node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in self.g.nodes(data=True)}
        edge_col = [e[2]['attr_dict']['color'] for e in self.g.edges(data=True)]

        nx.draw_networkx(self.g, pos=node_pos, edge_color=edge_col, node_size=500, alpha=.99, node_color="r",
                         with_labels=True, bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.35'), node_shape='s' )

        nx.draw_networkx(user_g, pos=node_pos, edge_color=edge_col, node_size=100, alpha=.99, node_color='blue',
                         with_labels=True, bbox=dict(facecolor="r", edgecolor='black', boxstyle='round,pad=0.35'), node_shape='s' )

        nx.draw_networkx(footholds_subgraph, pos=node_pos, edge_color=edge_col, node_size=100, alpha=.99, node_color='green',
                         with_labels=True, bbox=dict(facecolor="g", edgecolor='black', boxstyle='round,pad=0.35'), node_shape='s' )

        nx.draw_networkx(escalated_subgraph, pos=node_pos, edge_color=edge_col, node_size=100, alpha=.99, node_color='green',
                         with_labels=True, bbox=dict(facecolor="cyan", edgecolor='black', boxstyle='round,pad=0.35'), node_shape='s' )

        nx.draw_networkx(enumerated_subgraph, pos=node_pos, edge_color=edge_col, node_size=100, alpha=.99, node_color='green',
                         with_labels=True, bbox=dict(facecolor="yellow", edgecolor='black', boxstyle='round,pad=0.35'), node_shape='s' )

        nx.draw_networkx(exfiltrated_subgraph, pos=node_pos, edge_color=edge_col, node_size=100, alpha=.99, node_color='green',
                         with_labels=True, bbox=dict(facecolor="gray", edgecolor='black', boxstyle='round,pad=0.35'), node_shape='s' )

        labels = nx.get_edge_attributes(self.g, 'num_connections')
        plt.title('Network', size=15)
        plt.axis("off")
        
        self.canvas.draw()
        self.canvas.flush_events()


    # Create new scrollbar, at the top of the scrollbar add label to describe the actions
    # For every node in graph, add button to get informations about that node
    def create_component_group_box(self,graph):        
        scrolllayout = QVBoxLayout()
        
        info_label = QLabel()
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setText("Press the button to get\ncomponent informations")
        scrolllayout.addWidget(info_label)

        scrollwidget = QWidget()
        scrollwidget.setLayout(scrolllayout)

        self.verticalGroupBox = QScrollArea()
        self.verticalGroupBox.setWidgetResizable(True)  # Set to make the inner widget resize with scroll area
        self.verticalGroupBox.setWidget(scrollwidget)
        
        for i in graph:
            i = "_".join(i.split("\n"))
            groupbox = QPushButton(i)
            groupbox.setObjectName(i)
            scrolllayout.addWidget(groupbox)
            groupbox.clicked.connect(self.submitCommand)
 
 
    # Create popup window, set window size and show the popup
    def create_popout(self, component):
        self.exPopup = popupWidget(component)
        self.exPopup.show() 


    #build and plot network
    def submitCommand(self):
        caller_name = self.sender().text()

        for component in self.network_info.get_components():
            if caller_name == component.name:
                # create_popup(component)
                self.create_popout(component)
                break


    # Possition widget at the center of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show()



# Create popup window with component informations
class popupWidget(QWidget):
    def __init__(self, component):
        super().__init__()
        self.component = component
        self.initUI()

    def initUI(self):
        layout = QScrollArea(self)
        layout.setWidgetResizable(True)

        component_label = QLabel(self.component.name)
        
        text = self.component.get_info()
        
        font = self.font()
        font.setPointSize(10)
        component_label.setFont(font)
        component_label.setText(text)
        component_label.setStyleSheet("padding :15px")
        component_label.adjustSize()

        layout.setMinimumWidth(component_label.width())
        layout.setMinimumHeight(component_label.height())
        layout.setWidget(component_label)



# Make network graph from network informations
# Create new graph and add components from the networks as graph nodes
# For every connected component, add edge between those two components
# Add component possition in the graph as coordinates X and Y
# return created network graph
def make_network(network_list, possitions, height, width):

    gr = nx.DiGraph()

    for component in network_list.get_components():
        name = component.name
        rename = "\n".join(name.split("_"))
        gr.add_node(rename)
        connected = component.connected_components
        for connected_component in connected:
            connected_component = "\n".join(connected_component.split("_"))
            gr.add_edge(rename, connected_component, attr_dict = {'color' : "blue"})
        dic = {}
        if possitions.get(component.name, "") == "":
            dic['X'] = random.randint(1,height-1)
            dic['Y'] = random.randint(1,width-1)
        else:
            x,y = possitions[component.name].split(",")
            dic['X'] = int(x)
            dic['Y'] = int(y)
        gr.nodes[rename].update(dic)

    return gr

# vizualize network
def vizualize(network1, components_possitions, attacker_progress):

    import sys
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = PrettyWidget(network1, components_possitions, attacker_progress)
    screen.show()
    sys.exit(app.exec_())


def main():
    with open("model_sustava.txt") as model:
        network1 = json.loads(model.read())
    vizualize(network.network_model(network1))

if __name__ == '__main__':
    main()
