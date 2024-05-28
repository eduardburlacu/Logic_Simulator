"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import wx
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser


class MyGLCanvas(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters
    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render(self, text): Handles all drawing operations.

    on_paint(self, event): Handles the paint event.

    on_size(self, event): Handles the canvas resize event.

    on_mouse(self, event): Handles mouse events.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.
    """

    def __init__(self, parent, devices, monitors):
        """Initialise canvas properties and useful variables."""
        super().__init__(
            parent,
            -1,
            attribList=[
                wxcanvas.WX_GL_RGBA,
                wxcanvas.WX_GL_DOUBLEBUFFER,
                wxcanvas.WX_GL_DEPTH_SIZE,
                16,
                0,
            ],
        )
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise variables for zooming
        self.zoom = 1

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

        # Colours for signals

        self.RED = (1.0, 0.0, 0.0)
        self.GREEN = (0.0, 1.0, 0.0)
        self.BLUE = (0.0, 0.0, 1.0)
        self.colours = [self.RED, self.GREEN, self.BLUE]
        self.signals_list = []

        self.TEXT_COLOUR = (0.0, 0.0, 0.0)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def draw_signal(self, signal, colour, position):
        """Draw the given signal."""
        GL.glColor3f(colour[0], colour[1], colour[2])
        GL.glBegin(GL.GL_LINE_STRIP)

        for i in range(len(signal)):
            x = (i * 50) + 30
            x_next = (i * 50) + 80
            y = 430 + 50 * int(signal[i]) - 100 * position
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()

    def get_signals(self):
        """Render all the signals and labels."""
        for i in range(len(self.signals_list)):
            self.draw_signal(self.signals_list[i][1], self.colours[i % 3], i)
            self.render_text(self.signals_list[i][0], 10, 450 - 100 * i)

    def render(self, signals_list):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Update signal list and draw signals
        if signals_list is not None:
            self.signals_list = signals_list
        self.get_signals()

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        self.render(self.signals_list)

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
        if event.GetWheelRotation() < 0:
            self.zoom *= 1.0 + (
                event.GetWheelRotation() / (10 * event.GetWheelDelta())
            )
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
        if event.GetWheelRotation() > 0:
            self.zoom /= 1.0 - (
                event.GetWheelRotation() / (10 * event.GetWheelDelta())
            )
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False

        self.render(self.signals_list)
        self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        GL.glColor3f(
            self.TEXT_COLOUR[0], self.TEXT_COLOUR[1], self.TEXT_COLOUR[2]
        )
        GL.glRasterPos2f(x_pos, y_pos)

        # Choose a font and size
        font = GLUT.GLUT_BITMAP_HELVETICA_12

        for character in text:
            if character == "\n":
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.

    Parameters
    ----------
    title: title of the window.

    Public methods
    --------------
    on_menu(self, event): Event handler for the file menu.

    on_spin(self, event): Event handler for when the user changes the spin
                           control value.

    on_run_button(self, event): Event handler for when the user clicks the run
                                button.

    on_text_box(self, event): Event handler for when the user enters text.
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))

        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_ABOUT, "&About")
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)

        # Configure the widgets
        self.textC = wx.StaticText(self, wx.ID_ANY, "Simulation Cycles")
        self.spin = wx.SpinCtrl(self, wx.ID_ANY, "10")
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.continue_button = wx.Button(self, wx.ID_ANY, "Continue")
        self.textM = wx.StaticText(self, wx.ID_ANY, "Monitors")
        self.textMs = wx.StaticText(self, wx.ID_ANY, 13*" "
                                    + "Available" + 30*" " + "Current")
        self.remove_button = wx.Button(self, wx.ID_ANY, "Remove")
        self.add_button = wx.Button(self, wx.ID_ANY, "Add")
        self.textS = wx.StaticText(self, wx.ID_ANY, "Switches")

        # Assign variable to the other modules
        self.names = names
        self.devices = devices
        self.monitors = monitors
        self.network = network
        self.running = False
        self.monitored_list = self.get_monitored_devices_list(devices, names)
        self.devices_list = self.get_devices(devices, names)
        self.signals_list = self.get_signals_list(names, self.spin.GetValue())

        non_monitored_devices = []
        all_devices = self.get_devices(devices, names)
        for device in all_devices:
            if device[0] not in self.monitored_list:
                non_monitored_devices.append(device[0])

        # Dropdown list options

        self.dropdown = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY,
                                    choices=non_monitored_devices)
        self.dropdown.Bind(wx.EVT_COMBOBOX, self.on_dropdown)

        # List to display added options
        added_options = self.monitored_list
        self.added_list = wx.ListBox(self, wx.ID_ANY, choices=added_options)
        self.added_list.Bind(wx.EVT_LISTBOX, self.on_listbox_selection)

        # Create the list control for items with on/off states
        self.list_ctrl = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT
                                     | wx.LC_HRULES | wx.LC_VRULES)
        self.list_ctrl.InsertColumn(0, 'Input', width=140)
        self.list_ctrl.InsertColumn(1, 'State', width=60)

        # Add sample items to the list control
        device_list = self.devices_list

        for i in range(len(device_list)):
            if device_list[i][1] == 'SWITCH':
                if device_list[i][2] == 1:
                    index = self.list_ctrl.InsertItem(i, device_list[i][0])
                    self.list_ctrl.SetItem(index, 1, 'On')
                else:
                    index = self.list_ctrl.InsertItem(i, device_list[i][0])
                    self.list_ctrl.SetItem(index, 1, 'Off')

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.continue_button.Bind(wx.EVT_BUTTON, self.on_continue_button)
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_button)
        self.remove_button.Bind(wx.EVT_BUTTON, self.on_remove_button)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED,
                            self.on_list_item_activated)

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        dropdown_sizer = wx.BoxSizer(wx.HORIZONTAL)

        main_sizer.Add(self.canvas, 5, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(side_sizer, 1, wx.ALL, 5)

        # Button Configuration
        button_sizer1.Add(self.run_button, 1, wx.ALL, 0)
        button_sizer1.Add(self.continue_button, 1, wx.ALL, 0)
        button_sizer2.Add(self.add_button, 1, wx.ALL, 0)
        button_sizer2.Add(self.remove_button, 1, wx.ALL, 0)

        # Simulation Cycles
        side_sizer.Add(self.textC, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(self.spin, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(button_sizer1, 1, wx.EXPAND | wx.ALL, 10)

        # Monitors with Dropdown List and Added List
        side_sizer.Add(self.textM, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(self.textMs, 1, wx.EXPAND | wx.ALL, 10)
        dropdown_sizer.Add(self.dropdown, 1, wx.EXPAND | wx.ALL, 10)
        dropdown_sizer.Add(self.added_list, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(dropdown_sizer, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(button_sizer2, 1, wx.EXPAND | wx.ALL, 10)

        # Set Switches
        side_sizer.Add(self.textS, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(self.list_ctrl, 3, wx.EXPAND | wx.ALL, 10)

        self.SetSizeHints(600, 600)
        self.SetSizer(main_sizer)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)
        if Id == wx.ID_ABOUT:
            wx.MessageBox("Logic Simulator\nCreated by Mojisola Agboola\n2017",
                          "About Logsim", wx.ICON_INFORMATION | wx.OK)

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.spin.GetValue()

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        # Reset monitors
        self.monitors.reset_monitors()
        # Restart devices
        self.devices.cold_startup()

        # Record signals for monitored devices
        self.signals_list = self.get_signals_list(
            self.names, self.spin.GetValue()
        )

        # Render the canvas, set to running
        self.canvas.render(self.signals_list)
        self.running = True

    def on_continue_button(self, event):
        """Handle the event when the user clicks the continue button."""
        if not self.running:
            self.on_run_button("")
            return
        self.signals_list = self.get_signals_list(
            self.names, self.spin.GetValue()
        )
        self.canvas.render(self.signals_list)

    def on_add_button(self, event):
        """Handle the event when the user clicks the add button."""
        selection = self.dropdown.GetStringSelection()

        if selection and selection not in self.added_list.GetItems():
            index = self.dropdown.FindString(selection)

            # Add the device to monitors
            device_id = self.names.query(selection.split(".")[0])
            output_id = None
            if len(selection.split(".")) == 2:
                if selection.split(".")[1] == 'Q':
                    output_id = 12
                elif selection.split(".")[1] == 'QBAR':
                    output_id = 13
            if device_id is not None:
                self.monitors.make_monitor(device_id, output_id,
                                           self.spin.GetValue())

            self.dropdown.Delete(index)
            self.added_list.Append(selection)
        if not selection:
            print("Nothing to add...")
        if not self.running:
            return
        self.signals_list = self.on_run_button("")
        self.canvas.render(self.signals_list)

    def on_remove_button(self, event):
        """Handle the event when the user clicks the remove button."""
        selection = self.added_list.GetSelection()
        if selection != wx.NOT_FOUND:
            item = self.added_list.GetString(selection)

            # Remove the device from monitors
            device_id = self.names.query(item.split(".")[0])
            output_id = None
            if len(item.split(".")) == 2:
                if item.split(".")[1] == 'Q':
                    output_id = 12
                elif item.split(".")[1] == 'QBAR':
                    output_id = 13

            if device_id is not None:
                self.monitors.remove_monitor(device_id,
                                             output_id)

            self.added_list.Delete(selection)
            self.dropdown.Append(item)
        if not self.running:
            return
        self.signals_list = self.on_run_button("")
        self.canvas.render(self.signals_list)

    def get_signals_list(self, names, cycle_count):
        """Return a list of lists of the signals of the monitors."""
        signals_list = []
        self.run(cycle_count)
        for id_pair in self.monitors.monitors_dictionary.items():
            signal = []

            if id_pair[0][1] == 12:
                signal.append(names.get_name_string(id_pair[0][0]) + ".Q")
            elif id_pair[0][1] == 13:
                signal.append(
                    names.get_name_string(id_pair[0][0]) + ".QBAR"
                )
            else:
                signal.append(names.get_name_string(id_pair[0][0]))
            signal.append(id_pair[1])
            signals_list.append(signal)
        return signals_list

    def run(self, cycles):
        """Run the circuit for a given number of cycles."""
        for _ in range(cycles):
            if self.network.execute_network():
                self.monitors.record_signals()

    def get_devices(self, devices, names):
        """Return a list of lists, with each element having id, name, value."""
        all_devices_list = []
        for device in devices.devices_list:
            # Unique condition for DTYPE
            if self.get_device_string(device.device_kind) == ("DTYPE"):
                device_list = []
                id = device.device_id

                # D.Q
                if (device.device_id, 12) in self.monitors.monitors_dictionary:
                    device_list.append(names.get_name_string(id) + ".Q")
                    device_list.append(
                        self.get_device_string(device.device_kind))
                    device_list.append(devices.get_property(id))
                    all_devices_list.append(device_list)
                    device_list = []

                # D.QBAR
                if (device.device_id, 13) in self.monitors.monitors_dictionary:
                    device_list.append(names.get_name_string(id) + ".QBAR")
                    device_list.append(
                        self.get_device_string(device.device_kind))
                    device_list.append(devices.get_property(id))
                    all_devices_list.append(device_list)

            # Rest of devices
            else:
                device_list = []
                id = device.device_id
                device_list.append(names.get_name_string(id))
                device_list.append(
                    self.get_device_string(device.device_kind))
                device_list.append(devices.get_property(id))

                all_devices_list.append(device_list)
        return all_devices_list

    def get_monitored_devices_list(self, devices, names):
        """Return a list of monitored devices."""
        monitored_devices = []
        for id_pair in self.monitors.monitors_dictionary.items():
            if id_pair[0][1]:
                if id_pair[0][1] == 12:
                    monitored_devices.append(
                        names.get_name_string(id_pair[0][0]) + ".Q"
                    )
                elif id_pair[0][1] == 13:
                    monitored_devices.append(
                        names.get_name_string(id_pair[0][0]) + ".QBAR"
                    )
            else:
                monitored_devices.append(names.get_name_string(id_pair[0][0]))

        return monitored_devices

    def get_device_string(self, device_index):
        """Return string device name matching with the number."""
        name = ["AND", "OR", "NAND", "NOR",
                "XOR", "CLOCK", "SWITCH", "DTYPE"]
        if device_index in range(8):
            return name[device_index]
        else:
            return str(device_index)

    def on_dropdown(self, event):
        """Handle the event when the user selects an option from the list."""
        selection = self.dropdown.GetStringSelection()

    def on_listbox_selection(self, event):
        """Handle the event when a selection is made in the listbox."""
        selection = event.GetString()

    def on_list_item_activated(self, event):
        """Handle the event when a list item is activated (double-clicked)."""
        index = event.GetIndex()
        current_state = self.list_ctrl.GetItem(index, 1).GetText()
        new_state = 'On' if current_state == 'Off' else 'Off'
        self.list_ctrl.SetItem(index, 1, new_state)

        # Update the state of the switch in the devices
        switch_name = self.list_ctrl.GetItem(index, 0).GetText()
        name_id = self.names.query(switch_name)
        if name_id is not None:
            if new_state == 'On':
                self.devices.set_switch(name_id, 1)
            elif new_state == 'Off':
                self.devices.set_switch(name_id, 0)

        # Update the canvas if the circuit has been run
        if not self.running:
            return
        # self.signals_list = self.on_run_button("")
        # self.canvas.render(self.signals_list)
