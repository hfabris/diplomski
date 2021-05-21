from PyQt5.QtWidgets import *   #QWidget, QApplication, QStyleFactory, QDesktopWidget, QGridLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from os import environ
import networkx as nx
import json
import network

koordinate = {
    "backup_server" : (100,100),
    "private_web_server" : (100,200),
    "database_server" : (100,300),
    "domain_controler" : (100,400),
    "datacenter_switch" : (300,300),
    "core_router" : (600,300),
    "dmz_switch" : (600,200),
    "wan_switch" : (850,300),
    "Zagreb_regional_branch_switch" : (850,200),
    "Split_regional_branch_switch" : (1050,300),
    "Rijeka_regional_branch_switch" : (1050,450),
    "distribution_switch" : (600,400),
    "access_switch_IT" : (400,500),
    "access_switch_management" : (600,500),
    "access_switch_accounting" : (800,500),
    "dns_server" : (400,200),
    "mail_server" : (400,100),
    "public_web_server" : (600,100),
    "Zagreb_bank_counters" : (850,100),
    "Zagreb_regional_admin_workstation" : (1050,100),
    "Zagreb_bank_officer_workstation" : (1050,200),
    "Split_bank_counters" : (1350,200),
    "Split_regional_admin_workstation" : (1350,300),
    "Split_bank_officer_workstation" : (1350,400),
    "Rijeka_bank_counters" : (1350,500),
    "Rijeka_regional_admin_workstation" : (1350,600),
    "Rijeka_bank_officer_workstation" : (1050,600),
    "sec_op_workstation" : (200,500),
    "admin_workstation" : (200,600),
    "developer_workstation" : (400,600),
    "manager_workstation" : (600,600),
    "accountant_workstation" : (800,600)
}

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

class PrettyWidget(QWidget):

    def __init__(self, network_info):


        super(PrettyWidget, self).__init__()
        font = QFont()
        font.setPointSize(16)
        self.network_info = network_info
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 1400, 700)
        self.center()
        self.setWindowTitle('Network Plot')

        grid = QGridLayout()
        self.setLayout(grid)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 2, 9, 9)

        # Create network graph from network informations
        g = make_network(self.network_info)

        self.network_info.add_graph(g)

        # Make subgraph consisting of user components
        user = ["\n".join(comp.get_name().split("_")) for comp in self.network_info.get_user_components()]
        user_g = nx.subgraph(g,user)

        # Create scrollbar with buttons for getting user components informations
        # Add scrollbar to the left side of the grid
        self.createVerticalGroupBox(user)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)
        grid.addLayout(buttonLayout, 0, 0, 6, 2)


        # Plot network
        node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
        edge_col = [e[2]['attr_dict']['color'] for e in g.edges(data=True)]
        nx.draw_networkx(g, pos=node_pos, edge_color=edge_col, node_size=500, alpha=.99, node_color='red',
                         with_labels=True, bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'), node_shape='h' )
        nx.draw_networkx(user_g, pos=node_pos, edge_color=edge_col, node_size=100, alpha=.99, node_color='blue',
                         with_labels=True, bbox=dict(facecolor="r", edgecolor='black', boxstyle='round,pad=0.2'), node_shape='s' )
        labels = nx.get_edge_attributes(g, 'num_connections')
        plt.title('Network', size=15)
        plt.axis("off")

        self.showMaximized()

        self.canvas.draw_idle()

    # Create new scrollbar, at the top of the scrollbar add label to describe the actions
    # For every node in graph, add button to get informations about that node
    def createVerticalGroupBox(self,graph):        
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
            if caller_name == component.get_name():
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
        component_label = QLabel(self.component.get_name(), self)
        
        text = '''
        Component name: {}
        Connected components: {}
        Component ip address: {}
        Installed software on component: {}
        Accounts on component: {}
        Component domain: {}
        '''.format(self.component.get_name(), "", "", "", "", "")
        
        font = self.font()
        font.setPointSize(10)
        component_label.setFont(font)
        component_label.setText(text)
        component_label.setStyleSheet("padding :15px")
        component_label.adjustSize()



# Make network graph from network informations
# Create new graph and add components from the networks as graph nodes
# For every connected component, add edge between those two components
# Add component possition in the graph as coordinates X and Y
# return created network graph
def make_network(network_list):

    gr = nx.DiGraph()

    for component in network_list.get_components():
        name = component.get_name()
        rename = "\n".join(name.split("_"))
        gr.add_node(rename, pos=koordinate[name])
        connected = component.connected_components
        for connected_component in connected:
            connected_component = "\n".join(connected_component.split("_"))
            gr.add_edge(rename, connected_component, attr_dict = {'color' : "blue"})
        dic = {}
        dic['X'], dic['Y'] = koordinate[name]
        gr.nodes[rename].update(dic)

    return gr

# vizualize network
def vizualize(network1):

    import sys
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = PrettyWidget(network1)
    screen.show()
    sys.exit(app.exec_())


def main():
    with open("model_sustava.txt") as model:
        network1 = json.loads(model.read())
    vizualize(network.network_model(network1))

if __name__ == '__main__':
    main()
