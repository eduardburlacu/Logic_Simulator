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
        super().__init__(parent, -1,
                         attribList=[wxcanvas.WX_GL_RGBA,
                                     wxcanvas.WX_GL_DOUBLEBUFFER,
                                     wxcanvas.WX_GL_DEPTH_SIZE, 16, 0])
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

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def render(self, text):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Draw specified text at position (10, 10)
        self.render_text(text, 10, 10)

        # Draw a sample signal trace
        GL.glColor3f(0.0, 0.0, 1.0)  # signal trace is blue
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(10):
            x = (i * 20) + 10
            x_next = (i * 20) + 30
            if i % 2 == 0:
                y = 75
            else:
                y = 100
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()

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

        size = self.GetClientSize()
        text = "".join(["Canvas redrawn on paint event, size is ",
                        str(size.width), ", ", str(size.height)])
        self.render(text)

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""
        text = ""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            text = "".join(["Mouse button pressed at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.ButtonUp():
            text = "".join(["Mouse button released at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Leaving():
            text = "".join(["Mouse left canvas at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join(["Mouse dragged to: ", str(event.GetX()),
                            ", ", str(event.GetY()), ". Pan is now: ",
                            str(self.pan_x), ", ", str(self.pan_y)])
        if event.GetWheelRotation() < 0:
            self.zoom *= (1.0 + (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Negative mouse wheel rotation. Zoom is now: ",
                            str(self.zoom)])
        if event.GetWheelRotation() > 0:
            self.zoom /= (1.0 - (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Positive mouse wheel rotation. Zoom is now: ",
                            str(self.zoom)])
        if text:
            self.render(text)
        else:
            self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        GL.glColor3f(0.0, 0.0, 0.0)  # text is black
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12

        for character in text:
            if character == '\n':
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
        self.remove_button = wx.Button(self, wx.ID_ANY, "Remove")
        self.add_button = wx.Button(self, wx.ID_ANY, "Add")
        
        # Dropdown list options
        dropdown_options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
        self.dropdown = wx.ComboBox(self, wx.ID_ANY, choices=dropdown_options, style=wx.CB_READONLY)
        self.dropdown.Bind(wx.EVT_COMBOBOX, self.on_dropdown)

        # List to display added options
        self.added_list = wx.ListBox(self, wx.ID_ANY)
        
        # Create the list control for items with on/off states
        self.list_ctrl = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.list_ctrl.InsertColumn(0, 'Input', width=140)
        self.list_ctrl.InsertColumn(1, 'State', width=60)

        # Add sample items to the list control
        for i in range(5):
            index = self.list_ctrl.InsertItem(i, f'Switch {i+1}')
            self.list_ctrl.SetItem(index, 1, 'Off')

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.continue_button.Bind(wx.EVT_BUTTON,
											self.on_continue_button)
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_button)
        self.remove_button.Bind(wx.EVT_BUTTON, self.on_remove_button)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_list_item_activated)
        self.added_list.Bind(wx.EVT_LISTBOX, self.on_listbox_selection)
		
        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        dropdown_sizer = wx.BoxSizer(wx.HORIZONTAL)

        main_sizer.Add(self.canvas, 5, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(side_sizer, 1, wx.ALL, 5)

		# ---Button Configuration
        button_sizer1.Add(self.run_button, 1, wx.ALL, 0)
        button_sizer1.Add(self.continue_button, 1, wx.ALL, 0)
        button_sizer2.Add(self.add_button, 1, wx.ALL, 0)
        button_sizer2.Add(self.remove_button, 1, wx.ALL, 0)

		# ---Simulation Cycles
        side_sizer.Add(self.textC, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(self.spin, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(button_sizer1, 1, wx.EXPAND | wx.ALL, 10)
        
        # ---Monitors
        side_sizer.Add(self.textM, 1, wx.EXPAND | wx.ALL, 10)
        dropdown_sizer.Add(self.dropdown, 1, wx.EXPAND | wx.ALL, 10)
        dropdown_sizer.Add(self.added_list, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(dropdown_sizer, 1, wx.EXPAND | wx.ALL, 10)
        side_sizer.Add(button_sizer2, 1, wx.EXPAND | wx.ALL, 10)
        
        # ---Set Switches
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
        text = "".join(["New spin control value: ", str(spin_value)])
        self.canvas.render(text)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        text = "Run button pressed."
        self.canvas.render(text)

    def on_continue_button(self, event):
        """Handle the event when the user clicks the continue button."""
        text = "Continue button pressed."
        self.canvas.render(text)

    def on_remove_button(self, event):
        """Handle the event when the user clicks the remove button."""
        text = "Remove button pressed."
        self.canvas.render(text)

    def on_add_button(self, event):
        """Handle the event when the user clicks the add button."""
        text = "Add button pressed."
        self.canvas.render(text)

    def on_list_item_activated(self, event):
        """Handle the event when a list item is activated (double-clicked)."""
        index = event.GetIndex()
        current_state = self.list_ctrl.GetItem(index, 1).GetText()
        new_state = 'On' if current_state == 'Off' else 'Off'
        self.list_ctrl.SetItem(index, 1, new_state)
        self.canvas.render(f"Item {index+1} state changed to: {new_state}")

    def on_text_box(self, event):
        """Handle the event when the user enters text."""
        text_box_value = self.text_box.GetValue()
        text = "".join(["New text box value: ", text_box_value])
        self.canvas.render(text)

    def on_dropdown(self, event):
        """Handle the event when the user selects an option from the dropdown list."""
        selection = self.dropdown.GetStringSelection()
        text = f"Dropdown selection changed to: {selection}"
        self.canvas.render(text)

    def on_listbox_selection(self, event):
        """Handle the event when a selection is made in the listbox."""
        selection = event.GetString()
        text = f"Listbox selection changed to: {selection}"
        self.canvas.render(text)