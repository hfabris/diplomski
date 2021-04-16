from PyQt5.QtWidgets import *   #QWidget
from PyQt5.QtGui import *       #QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import tkinter as tk
from tkinter import ttk

import json
import network

koordinate = {
    "backup_server" : (200,100),
    "private_web_server" : (200,200),
    "database_server" : (200,300),
    "domain_controler" : (200,400),
    "datacenter_switch" : (400,300),
    "core_router" : (600,300),
    "dmz_switch" : (600,200),
    "wan_switch" : (800,300),
    "regional_branch_switch" : (1000,300),
    "distribution_switch" : (600,400),
    "access_switch_IT" : (800,500),
    "access_switch_management" : (600,500),
    "access_switch_accounting" : (400,500),
    "dns_server" : (400,200),
    "mail_server" : (400,100),
    "public_web_server" : (600,100),
    "bank_counters" : (1200,200),
    "regional_admin_workstation" : (1200,300),
    "bank_officer_workstation" : (1200,400),
    "sec_op_workstation" : (1000,500),
    "admin_workstation" : (1000,600),
    "developer_workstation" : (800,600),
    "manager_workstation" : (600,600),
    "accountant_workstation" : (400,600)
}

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


        g, user = make_network(self.network_info)
        
        self.createVerticalGroupBox(user)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)
        grid.addLayout(buttonLayout, 0, 0, 9, 2)
        
        user_g = nx.subgraph(g,user)
        
        # Plot network
        node_pos = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}
        node_shp = {node[0]: node[1]['shape'] for node in g.nodes(data=True)}
        edge_col = [e[2]['attr_dict']['color'] for e in g.edges(data=True)]
        nx.draw_networkx(g, pos=node_pos, edge_color=edge_col, node_size=500, alpha=.99, node_color='red',
                         with_labels=True, bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'), node_shape='h' )
        nx.draw_networkx(user_g, pos=node_pos, edge_color=edge_col, node_size=100, alpha=.99, node_color='blue',
                         with_labels=True, bbox=dict(facecolor="r", edgecolor='black', boxstyle='round,pad=0.2'), node_shape='s' )
        labels = nx.get_edge_attributes(g, 'num_connections')
        nx.draw_networkx_edge_labels(g, pos=node_pos, edge_labels=labels, font_color='black', alpha=.2)
        plt.title('Network', size=15)
        plt.axis("off")

        # self.cid = self.figure.canvas.mpl_connect('button_press_event', onclick)
        self.canvas.draw_idle()

    def createVerticalGroupBox(self,graph):
        # self.verticalGroupBox = QScrollArea()        
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
 
    def create_popout(self, name):
        self.exPopup = popupWidget(name)
        self.exPopup.setGeometry(200, 300, 100, 100)
        self.exPopup.show() 
        
    #build and plot network
    def submitCommand(self):
        caller_name = self.sender().text()
        
        for component in self.network_info.get_components():
            if caller_name == component.get_name():
                create_popup(component)
                # self.create_popout(component.get_name())
                break
        


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show()




class popupWidget(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.initUI()

    def initUI(self):
        lblName = QLabel(self.name, self)




def create_popup(component):
    
    msg = '''
    Component name: 
        {}
    IP address:     
        {}
    software:       
        {}
    accounts:       
        {}
    domain:         
        {}
    '''.format(component.get_name(), component.get_ip_address(), "\n".join(software for software in component.get_software()), 
    "\n".join(account for account in component.get_accounts()), "\n".join(domain for domain in component.get_domains()))
    
    popup = tk.Tk()
    popup.wm_title("Component informations")
    NORM_FONT= ("Verdana", 10)
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def make_network(network_list):

    gr = nx.DiGraph()
    
    user = ["\n".join(comp.get_name().split("_")) for comp in network_list.get_user_components()]
    
    for component in network_list.get_components():
        name = component.get_name()
        rename = "\n".join(name.split("_"))
        gr.add_node(rename, pos=koordinate[name])
        connected = component.get_connected_components()
        for connected_component in connected:
            connected_component = "\n".join(connected_component.split("_"))
            gr.add_edge(rename, connected_component, attr_dict = {'color' : "blue"})
        dic = {}
        dic['X'], dic['Y'] = koordinate[name]
        if component.is_network_component():
            dic['shape'] = 'h'
        else:
            dic['shape'] = 's'
        gr.nodes[rename].update(dic)
    
    return gr, user


def vizualize(network1):

    import sys
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
