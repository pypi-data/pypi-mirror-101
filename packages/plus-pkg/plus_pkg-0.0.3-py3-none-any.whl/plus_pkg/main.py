from Orange.widgets.widget import OWWidget, Output
from Orange.widgets.widget import OWWidget, Input
from Orange.widgets import gui

class IntNumber(OWWidget):
    # Widget's name as displayed in the canvas
    name = "Integer Number"
    # Short widget description
    description = "Lets the user input a number"

    # An icon resource file path for this widget
    # (a path relative to the module where this widget is defined)
    icon = "../icons/number.svg"

    # Widget's outputs; here, a single output named "Number", of type int
    class Outputs:
        number = Output("Number", int)

def __init__(self):
    super().__init__()

    from AnyQt.QtGui import QIntValidator
    gui.lineEdit(self.controlArea, self, "number", "Enter a number",
                 box="Number",
                 callback=self.number_changed,
                 valueType=int, validator=QIntValidator())
    self.number_changed()

def number_changed(self):
    # Send the entered number on "Number" output
    self.Outputs.number.send(self.number)
class Print(OWWidget):
    name = "Print"
    description = "Print out a number"
    icon = "../icons/print.svg"

    class Inputs:
        number = Input("Number", int)

    want_main_area = False

    def __init__(self):
        super().__init__()
        self.number = None

        self.label = gui.widgetLabel(self.controlArea, "The number is: ??")

    @Inputs.number
    def set_number(self, number):
        """Set the input number."""
        self.number = number
        if self.number is None:
            self.label.setText("The number is: ??")
        else:
            self.label.setText("The number is {}".format(self.number))

class Adder(OWWidget):
    name = "Add two integers"
    description = "Add two numbers"
    icon = "../icons/plus.svg"

    class Inputs:
        a = Input("A", int)
        b = Input("B", int)

    class Outputs:
        sum = Output("A + B", int)

    want_main_area = False

    def __init__(self):
        super().__init__()
        self.a = None
        self.b = None

    @Inputs.a
    def set_A(self, a):
        """Set input 'A'."""
        self.a = a

    @Inputs.b
    def set_B(self, b):
        """Set input 'B'."""
        self.b = b

    def handleNewSignals(self):
        """Reimplemeted from OWWidget."""
        if self.a is not None and self.b is not None:
            self.Outputs.sum.send(self.a + self.b)
        else:
            # Clear the channel by sending `None`
            self.Outputs.sum.send(None)