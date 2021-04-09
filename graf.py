from PyQt5.QtWidgets import *   #QWidget
from PyQt5.QtGui import *       #QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
import pandas as pd

import json
import network


# y = 0 - 1500
# x = 0 - 900

koordinate = {
    "backup_server" : (50,50),
    "private_web_server" : (50,100),
    "database_server" : (50,150),
    "domain_controler" : (50, 200),
    "datacenter_switch" : (100, 150),
    "core_router" : (150, 150),
    "dmz_switch" : (150, 100),
    "wan_switch" : (200,150),
    "regional_branch_switch" : (250,150),
    "distribution_switch" : (150,200),
    "access_switch_IT" : (200,250),
    "access_switch_management" : (150,250),
    "access_switch_accounting" : (100,250),
    "dns_server" : (100,100),
    "mail_server" : (100,50),
    "public_web_server" : (150,50),
    "bank_counters" : (300,100),
    "regional_admin_workstation" : (300,150),
    "bank_officer_workstation" : (300,200),
    "sec_op_workstation" : (250,250),
    "admin_workstation" : (250,300),
    "developer_workstation" : (200,300),
    "manager_workstation" : (150,300),
    "accountant_workstation" : (100,300)
}

class PrettyWidget(QWidget):

    def __init__(self):


        super(PrettyWidget, self).__init__()
        font = QFont()
        font.setPointSize(16)
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 1500, 900)
        self.center()
        self.setWindowTitle('Network Plot')

        grid = QGridLayout()
        self.setLayout(grid)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)


        g = make_network()

        # Plot network
        node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
        edge_col = [e[2]['attr_dict']['color'] for e in g.edges(data=True)]
        nx.draw_networkx(g, pos=node_pos, arrows=True, edge_color=edge_col, node_size=1700, alpha=.99, node_color='red',
                         with_labels=True, bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'), )
        labels = nx.get_edge_attributes(g, 'num_connections')
        nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
        plt.title('Network', size=15)
        plt.axis("off")

        self.canvas.draw_idle()

    #build and plot network

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def make_network():
    with open("model_sustava.txt") as model:
        network1 = json.loads(model.read())

    network_list = network.network_model(network1)

    gr = nx.DiGraph()
    
    for component in network_list.get_components():
        name = component.get_name()
        connected = component.get_connected_components()
        for connected_component in connected:
            gr.add_edge(name, connected_component, attr_dict = {'color' : "blue"})
        dic = {}
        dic['X'], dic['Y'] = koordinate[name]
        gr.nodes[name].update(dic)
    
    
    return gr


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = PrettyWidget()
    screen.show()
    sys.exit(app.exec_())


