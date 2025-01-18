from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QSplitter, QWidget, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from plot import Plotter
from database import DatabaseManager
from calculations import CostCalculator


class BridgeCostApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steel vs. Concrete Bridge Cost Analysis")
        self.setGeometry(100, 100, 1200, 700)

        # Initialize components
        self.database_manager = DatabaseManager("bridge_costs.db")
        self.cost_calculator = CostCalculator(self.database_manager)
        self.plotter = Plotter()

        # Set up the UI
        self.initialize_ui()

    def initialize_ui(self):
        """Set up the main user interface."""
        # Create a splitter for dynamic resizing
        main_splitter = QSplitter(Qt.Horizontal)

        # Input Section
        self.input_section = QWidget()
        self.input_layout = QVBoxLayout(self.input_section)
        self.add_input_fields()
        main_splitter.addWidget(self.input_section)

        # Plot Section
        self.plot_section = QWidget()
        self.plot_layout = QVBoxLayout(self.plot_section)
        self.plot_canvas = self.plotter.create_canvas()
        self.plot_layout.addWidget(self.plot_canvas)
        main_splitter.addWidget(self.plot_section)

        # Output Section
        self.output_section = QWidget()
        self.output_layout = QVBoxLayout(self.output_section)
        self.add_output_table()
        main_splitter.addWidget(self.output_section)

        # Configure resizing behavior
        main_splitter.setStretchFactor(0, 1)  # Input section stretch factor
        main_splitter.setStretchFactor(1, 2)  # Plot section stretch factor
        main_splitter.setStretchFactor(2, 1)  # Output section stretch factor

        # Set the splitter as the central widget
        self.setCentralWidget(main_splitter)

    def add_input_fields(self):
        """Create and add input fields for user inputs."""
        self.input_layout.addWidget(QLabel("Bridge Parameters"))

        # Span Length Input
        self.span_length_input = QLineEdit()
        self.span_length_input.setPlaceholderText("Enter span length (m)")
        self.input_layout.addWidget(QLabel("Span Length (m):"))
        self.input_layout.addWidget(self.span_length_input)

        # Width Input
        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Enter bridge width (m)")
        self.input_layout.addWidget(QLabel("Width (m):"))
        self.input_layout.addWidget(self.width_input)

        # Traffic Volume Input
        self.traffic_volume_input = QLineEdit()
        self.traffic_volume_input.setPlaceholderText("Enter traffic volume (vehicles/day)")
        self.input_layout.addWidget(QLabel("Traffic Volume (vehicles/day):"))
        self.input_layout.addWidget(self.traffic_volume_input)

        # Design Life Input
        self.design_life_input = QLineEdit()
        self.design_life_input.setPlaceholderText("Enter design life (years)")
        self.input_layout.addWidget(QLabel("Design Life (years):"))
        self.input_layout.addWidget(self.design_life_input)

        # Calculate Button
        self.calculate_button = QPushButton("Calculate Costs")
        self.calculate_button.clicked.connect(self.calculate_costs)
        self.input_layout.addWidget(self.calculate_button)

    def add_output_table(self):
        """Create and add the results table."""
        self.output_layout.addWidget(QLabel("Cost Breakdown Results"))

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)  # Adjust columns for results table
        self.results_table.setHorizontalHeaderLabels([
            "Cost Type", "Steel Cost", "Concrete Cost"
        ])
        self.output_layout.addWidget(self.results_table)

    def calculate_costs(self):
        """Calculate costs based on user input."""
        try:
            # Parse inputs
            span_length = float(self.span_length_input.text())
            width = float(self.width_input.text())
            traffic_volume = float(self.traffic_volume_input.text())
            design_life = int(self.design_life_input.text())

            # Perform calculations
            results = self.cost_calculator.compute_costs(
                span_length, width, traffic_volume, design_life
            )

            # Display results
            self.populate_results_table(results)
            self.update_plot(results)

        except ValueError:
            # Handle invalid input
            self.show_error_message("Invalid input. Please enter valid numbers.")

    def populate_results_table(self, results):
        """Fill the results table with calculated data."""
        self.results_table.setRowCount(len(results))
        for i, (cost_type, steel_cost, concrete_cost) in enumerate(results):
            self.results_table.setItem(i, 0, QTableWidgetItem(cost_type))
            self.results_table.setItem(i, 1, QTableWidgetItem(f"{steel_cost:.2f}"))
            self.results_table.setItem(i, 2, QTableWidgetItem(f"{concrete_cost:.2f}"))

    def update_plot(self, results):
        """Update the plot with calculated data."""
        labels = [row[0] for row in results]
        steel_costs = [row[1] for row in results]
        concrete_costs = [row[2] for row in results]

        self.plotter.plot_comparison(steel_costs, concrete_costs, labels)

    def show_error_message(self, message):
        """Display an error message to the user."""
        error_label = QLabel(message)
        error_label.setStyleSheet("color: red; font-weight: bold;")
        self.input_layout.addWidget(error_label)
