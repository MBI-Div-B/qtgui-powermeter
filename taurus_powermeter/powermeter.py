import sys
from taurus.external.qt import Qt
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus.qt.qtgui.input import TaurusValueSpinBox, TaurusValueLineEdit, TaurusValueCheckBox
from taurus.qt.qtgui.compact.basicswitcher import TaurusLabelEditRW, TaurusBoolRW
from taurus_pyqtgraph import TaurusTrend
from taurus.core.util.argparse import get_taurus_parser

def main():
    parser = get_taurus_parser()
    parser.set_usage('python powermeter.py [domain/family/member]')
    parser.set_description('Taurus GUI for Coherent PowerMax and EnergyMax powermeters')
    
    app = TaurusApplication(sys.argv, cmd_line_parser=parser, app_name='Coherent Powermeter')
    args = app.get_command_line_args()

    try:
        tango_device = args[0]
    except IndexError:
        print('tango device must be provided as argument!')
        return
    # Define the layout and panels

    parent = Qt.QWidget()
    parent_layout = Qt.QVBoxLayout()
    parent_layout.setSpacing(0)
    parent_layout.setContentsMargins(0, 0, 0, 0)
    parent.setLayout(parent_layout)

    parent.setWindowTitle("Power meter")
    parent.setFont(Qt.QFont('Arial',12))
    parent.setMinimumSize(1000,300)    

    header = Qt.QFrame()
    header_layout = Qt.QHBoxLayout()
    header_layout.setSpacing(0)
    header_layout.setContentsMargins(0, 0, 0, 0)
    header.setLayout(header_layout)

    bottom = Qt.QFrame()
    bottom_layout = Qt.QHBoxLayout()
    bottom_layout.setSpacing(0)
    bottom_layout.setContentsMargins(0, 0, 0, 0)
    bottom.setLayout(bottom_layout)

    parameters = Qt.QFrame()
    parameters_layout = Qt.QVBoxLayout()
    parameters_layout.setSpacing(0)
    parameters_layout.setContentsMargins(0, 0, 0, 0)
    parameters.setLayout(parameters_layout)

    plotpanel = Qt.QFrame()
    plotpanel_layout = Qt.QVBoxLayout()
    plotpanel_layout.setSpacing(5)
    plotpanel_layout.setContentsMargins(5, 5, 5, 5)
    plotpanel.setLayout(plotpanel_layout)


    # Fill the panels with content

    
    # Header

    # Sensor information
    sensor = Qt.QFrame()
    sensor_box = Qt.QVBoxLayout()
    sensor_box.setSpacing(0)
    sensor_box.setContentsMargins(5, 5, 5, 5)
    sensor.setLayout(sensor_box)
    sensor.setMaximumSize(400,50)

    sensor_box.addWidget(compact_attribute(tango_device+'/Device', show_label=False, highlight_status=False, inline=True))
    sensor_box.addWidget(compact_attribute(tango_device+'/SerialNumber', show_label=True, highlight_status=False, inline=True))

    # Power reading
    power = Qt.QFrame()
    power_box = Qt.QVBoxLayout()
    power_box.setSpacing(5)
    power_box.setContentsMargins(5, 5, 5, 5)
    power.setLayout(power_box)

    power_box.addWidget(compact_attribute(tango_device+'/Value', inline=True))
    power.setFont(Qt.QFont('Arial',48))
    
    header_layout.addWidget(sensor, 1)
    header_layout.addWidget(power, 2)

    # Bottom

    # Parameters panel

    # Settings
    settings = Qt.QFrame()
    settings_box = Qt.QVBoxLayout()
    settings_box.setSpacing(5)
    settings_box.setContentsMargins(5, 5, 5, 5)
    settings.setLayout(settings_box)

    settings_box.addWidget(compact_rw_attribute(tango_device+'/Wavelength'))
    settings_box.addWidget(switch(tango_device+'/Gain_onoff'))
    settings_box.addWidget(compact_rw_attribute(tango_device+'/Gain_factor', show_label=False, inline=True))
    settings_box.addWidget(compact_rw_attribute(tango_device+'/Polling'))

    # Statistics
    stats = Qt.QFrame()
    stats_box = Qt.QGridLayout()
    stats_box.setSpacing(5)
    stats_box.setContentsMargins(5, 5, 5, 5)
    stats.setLayout(stats_box)

    stats_box.addWidget(compact_attribute(tango_device+'/Statistics_mean'),3,0)
    stats_box.addWidget(compact_attribute(tango_device+'/Statistics_std'),3,1)
    stats_box.addWidget(compact_attribute(tango_device+'/Statistics_min'),4,0)
    stats_box.addWidget(compact_attribute(tango_device+'/Statistics_max'),4,1)
    stats_box.addWidget(compact_attribute(tango_device+'/Statistics_bsize'),5,0)


    parameters_layout.addStretch()
    parameters_layout.addWidget(settings)
    parameters_layout.addWidget(stats)


    # Plot panel

    plot = TaurusTrend()
    model = [tango_device+'/Value']
    plot.setModel(model)
    
    try:
        plot.loadConfigFile('TaurusTrend.pck')
    except:
        pass

    plotpanel_layout.addWidget(plot)


    # Add parameters and plotpanel to bottom layout
    bottom_layout.addWidget(parameters)
    bottom_layout.addWidget(plotpanel, 1)

    # Add header and bottom panel to parent layout
    parent_layout.addWidget(header)
    parent_layout.addWidget(bottom)

    parent.show()
    sys.exit(app.exec_())




def compact_attribute(address, show_label=True, highlight_status=True, inline=False):
    attr = Qt.QFrame()
    if inline==True:
        attr_format = Qt.QHBoxLayout()
    else:
        attr_format = Qt.QVBoxLayout()
    attr_format.setSpacing(0)
    attr_format.setContentsMargins(0, 0, 0, 0)
    attr.setLayout(attr_format)

    label, value = TaurusLabel(), TaurusLabel()

    label.model, label.bgRole = address+'#label', ''
    value.model = address

    if highlight_status==False:
        value.bgRole = ''

    if show_label==True:
        attr_format.addWidget(label)

    attr_format.addWidget(value)

    return attr

def compact_rw_attribute(address, show_label=True, highlight_status=True, inline=False):
    attr = Qt.QFrame()
    if inline==True:
        attr_format = Qt.QHBoxLayout()
    else:
        attr_format = Qt.QVBoxLayout()
    attr_format.setSpacing(0)
    attr_format.setContentsMargins(0, 0, 0, 0)
    attr.setLayout(attr_format)

    label, value = TaurusLabel(), TaurusLabelEditRW()

    label.model, label.bgRole = address+'#label', ''
    value.model = address

    if show_label==True:
        attr_format.addWidget(label)

    attr_format.addWidget(value)

    return attr

def switch(address):
    attr = Qt.QFrame()
    attr_format = Qt.QHBoxLayout()
    attr_format.setSpacing(0)
    attr_format.setContentsMargins(0, 0, 0, 0)
    attr.setLayout(attr_format)

    label, value = TaurusLabel(), TaurusBoolRW()

    label.model, label.bgRole = address+'#label', ''
    value.model = address

    attr_format.addWidget(value)
    attr_format.addWidget(label)

    return attr

if __name__ == "__main__": main()