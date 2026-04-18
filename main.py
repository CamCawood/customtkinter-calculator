import customtkinter as ct


class Settings:
    """Store fonts and colour values used by the calculator UI."""

    def __init__(self):
        """Initialise all theme fonts and colours."""
        self.RESULT_FONT = ct.CTkFont(family="Arial", size=50)
        self.BUTTON_FONT = ct.CTkFont(family="Arial", size=30)

        self.ROOT_BG = "#0d0d0d"
        self.FRAME_BG = "#1a1a1a"
        self.FRAME_BORDER = "#f5c518"
        self.LABEL_BG = "#1a1a1a"
        self.LABEL_TEXT = "#f5f5f5"
        self.BUTTON_BG = "#2b2f36"
        self.BUTTON_HOVER = "#3a3f47"
        self.BUTTON_TEXT = "#f5f5f5"
        self.OP_ACTIVE = "#f5c518"
        self.OP_INACTIVE = "#2b2f36"


class CalculatorLogic:
    """Handle the calculator's arithmetic operations."""

    def __init__(self):
        """Create mappings between operation symbols and their functions."""
        self.operations = ["+", "-", "x", "÷"]
        self.operation_func_list = [
            self.add,
            self.subtract,
            self.multiply,
            self.divide
        ]
        self.operations_func_dict = {
            op: self.operation_func_list[k]
            for k, op in enumerate(self.operations)
        }

    def add(self, number1, number2):
        """Return the sum of two numbers."""
        return number1 + number2

    def subtract(self, number1, number2):
        """Return the result of subtracting number2 from number1."""
        return number1 - number2

    def multiply(self, number1, number2):
        """Return the product of two numbers."""
        return number1 * number2

    def divide(self, number1, number2):
        """Return the result of dividing number1 by number2.

        Returns:
            str | float: 'Error' if dividing by zero, otherwise the quotient.
        """
        if number2 == 0:
            return "Error"
        return number1 / number2


class WidgetFactory:
    """Create and return CustomTkinter widgets for the calculator."""

    def __init__(self, main):
        """Store references to the main app, root window, and settings."""
        self.main = main
        self.root = self.main.root
        self.settings = self.main.settings

    def create_label(self, master, **label_details):
        """Create, place, and return a styled label.

        Args:
            master: Parent widget for the label.
            **label_details: Label configuration such as text, size, and grid position.

        Returns:
            ct.CTkLabel: The created label widget.
        """
        label = ct.CTkLabel(
            master=master,
            text=label_details.get("text"),
            font=self.settings.RESULT_FONT,
            width=label_details.get("width"),
            height=label_details.get("height"),
            anchor="e",
            bg_color=self.settings.LABEL_BG,
            text_color=self.settings.LABEL_TEXT
        )
        label_coords = label_details.get("coords")
        label.grid(
            row=label_coords[0],
            column=label_coords[1],
            columnspan=label_details.get("columnspan")
        )
        return label

    def create_frame(self, master, **frame_details):
        """Create, place, and return a styled frame.

        Args:
            master: Parent widget for the frame.
            **frame_details: Frame configuration such as size and grid position.

        Returns:
            ct.CTkFrame: The created frame widget.
        """
        frame = ct.CTkFrame(
            master=master,
            border_color=self.settings.FRAME_BORDER,
            border_width=2,
            width=frame_details.get("width"),
            height=frame_details.get("height"),
            fg_color=self.settings.FRAME_BG
        )
        frame_coords = frame_details.get("coords")
        frame.grid(
            row=frame_coords[0],
            column=frame_coords[1],
            columnspan=frame_details.get("columnspan")
        )
        return frame

    def create_button(self, master, width=90, height=70, **button_details):
        """Create, place, and return a styled button.

        Args:
            master: Parent widget for the button.
            width: Button width.
            height: Button height.
            **button_details: Button configuration such as text, command, and grid position.

        Returns:
            ct.CTkButton: The created button widget.
        """
        button = ct.CTkButton(
            master=master,
            text=button_details.get("text"),
            font=self.settings.BUTTON_FONT,
            width=width,
            height=height,
            command=button_details.get("command"),
            fg_color=self.settings.BUTTON_BG,
            hover_color=self.settings.BUTTON_HOVER,
            text_color=self.settings.BUTTON_TEXT
        )
        button_coords = button_details.get("coords")
        button.grid(
            row=button_coords[0],
            column=button_coords[1],
            padx=button_details.get("padx"),
            pady=button_details.get("pady"),
            columnspan=button_details.get("columnspan")
        )
        return button


class Main:
    """Run the calculator application and manage its state."""

    def __init__(self):
        """Initialise the main window, helper classes, and calculator state."""
        self.root = ct.CTk()
        self.settings = Settings()
        self.root.configure(fg_color=self.settings.ROOT_BG)
        self.root.title("Calculator")

        self.calculator_logic = CalculatorLogic()
        self.widget_factory = WidgetFactory(self)

        self.op_button_list = []
        self.current_operation_func = None
        self.current_op_button = None
        self.first_result = None
        self.just_calculated = False

    def run(self):
        """Build the UI and start the main event loop."""
        height = 90

        self.result_frame = self.widget_factory.create_frame(
            master=self.root,
            coords=(0, 0),
            columnspan=5,
            height=height,
            width=400
        )
        self.result_label = self.widget_factory.create_label(
            master=self.root,
            text="",
            coords=(0, 0),
            height=height - 10,
            width=370,
            columnspan=5
        )

        self.widget_factory.create_button(
            master=self.root,
            text="CE",
            coords=(2, 1),
            padx=5,
            pady=5,
            command=self.clear_entry_button_command
        )

        self.widget_factory.create_button(
            master=self.root,
            text="C",
            coords=(2, 2),
            padx=5,
            pady=5,
            command=self.clear_button_command
        )

        column = 0
        row = 2
        number_buttons = [7, 8, 9, 4, 5, 6, 1, 2, 3]

        for i in range(9):
            if (column % 3) == 0:
                row += 1
                column = 0
            column += 1

            self.widget_factory.create_button(
                master=self.root,
                text=number_buttons[i],
                coords=(row, column),
                padx=5,
                pady=5,
                command=lambda b=number_buttons[i]: self.number_button_command(b)
            )

        self.widget_factory.create_button(
            master=self.root,
            text="0",
            coords=(6, 2),
            padx=5,
            pady=5,
            command=self.zero_button_command
        )

        self.widget_factory.create_button(
            master=self.root,
            text=".",
            coords=(6, 1),
            padx=5,
            pady=5,
            command=self.decimal_button_command
        )

        self.widget_factory.create_button(
            master=self.root,
            text="=",
            coords=(6, 3),
            padx=5,
            pady=5,
            columnspan=2,
            width=200,
            command=self.equal_command
        )

        for i in range(len(self.calculator_logic.operations)):
            op_button = self.widget_factory.create_button(
                master=self.root,
                text=self.calculator_logic.operations[i],
                coords=(i + 2, 4),
                padx=5,
                pady=5,
            )
            op_button.configure(
                command=lambda op=self.calculator_logic.operations[i], b=op_button:
                self.operation_button_command(op, b)
            )
            self.op_button_list.append(op_button)

        self.root.mainloop()

    def number_button_command(self, button_number):
        """Append a number to the display.

        If a calculation was just completed and there is no active operation,
        start a new number entry first.
        """
        if self.just_calculated and self.current_operation_func is None:
            self.result_label.configure(text="")
            self.just_calculated = False

        current_result = self.result_label.cget("text") + str(button_number)
        self.result_label.configure(text=current_result)

    def operation_button_command(self, operation, op_button):
        """Store the current number and selected operation.

        Args:
            operation: The chosen operator symbol.
            op_button: The operator button widget that was pressed.
        """
        current_text = self.result_label.cget("text")
        if not current_text:
            return

        for b in self.op_button_list:
            b.configure(fg_color=self.settings.OP_INACTIVE)

        self.first_result = current_text
        self.current_operation_func = self.calculator_logic.operations_func_dict.get(operation)
        self.current_op_button = op_button
        self.current_op_button.configure(fg_color=self.settings.OP_ACTIVE)
        self.result_label.configure(text="")
        self.just_calculated = False

    def equal_command(self):
        """Perform the selected operation using the stored and current values."""
        if self.current_operation_func is None or self.first_result is None:
            return

        second_result = self.result_label.cget("text")
        if not second_result:
            return

        calculation = self.current_operation_func(
            float(self.first_result),
            float(second_result)
        )

        if self.current_op_button is not None:
            self.current_op_button.configure(fg_color=self.settings.OP_INACTIVE)

        if calculation == "Error":
            self.result_label.configure(text=calculation)
            self.first_result = None
        else:
            if calculation == int(calculation):
                calculation = int(calculation)

            self.result_label.configure(text=str(calculation))
            self.first_result = str(calculation)

        self.current_operation_func = None
        self.current_op_button = None
        self.just_calculated = True

    def zero_button_command(self):
        """Append zero only when it makes sense to do so."""
        result = self.result_label.cget("text")

        if self.just_calculated and self.current_operation_func is None:
            self.result_label.configure(text="")
            self.just_calculated = False
            result = ""

        if result:
            self.number_button_command("0")

    def decimal_button_command(self):
        """Add a decimal point to the current entry if one is not already present."""
        result = self.result_label.cget("text")

        if self.just_calculated and self.current_operation_func is None:
            self.result_label.configure(text="")
            self.just_calculated = False
            result = ""

        if "." not in result:
            if result:
                self.result_label.configure(text=result + ".")
            else:
                self.result_label.configure(text="0.")

    def clear_entry_button_command(self):
        """Clear only the current display entry."""
        self.result_label.configure(text="")

    def clear_button_command(self):
        """Reset the full calculator state and clear the display."""
        if self.current_op_button is not None:
            self.current_op_button.configure(fg_color=self.settings.BUTTON_BG)

        self.current_op_button = None
        self.current_operation_func = None
        self.first_result = None
        self.just_calculated = False
        self.result_label.configure(text="")


Main().run()