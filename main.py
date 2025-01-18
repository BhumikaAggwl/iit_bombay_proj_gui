import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QGridLayout
from PyQt5.QtCore import Qt
from database import DatabaseManager
from calculations import CostCalculator
from plot import Plotter

class BridgeCostApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steel vs. Concrete Bridge Cost Comparison")
        self.setGeometry(100, 100, 1200, 600)

        # Main Layout
        main_layout = QHBoxLayout()

        # Left Dock: Input Parameters
        self.input_widget = QWidget()
        self.input_layout = QVBoxLayout()
        self.input_widget.setLayout(self.input_layout)
        main_layout.addWidget(self.input_widget)

        self.create_input_fields()

        # Center: Bar Plot
        self.plot_widget = QWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_widget.setLayout(self.plot_layout)
        main_layout.addWidget(self.plot_widget)

        self.plotter = Plotter()
        self.canvas = self.plotter.get_canvas()
        self.plot_layout.addWidget(self.canvas)

        # Right Dock: Output Table
        self.output_widget = QWidget()
        self.output_layout = QVBoxLayout()
        self.output_widget.setLayout(self.output_layout)
        main_layout.addWidget(self.output_widget)

        self.create_output_table()

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Initialize Database and Calculator
        self.db_manager = DatabaseManager("bridge_costs.db")
        self.calculator = CostCalculator(self.db_manager)

    def create_input_fields(self):
        grid = QGridLayout()

        # Labels and Inputs
        grid.addWidget(QLabel('Span Length (m):'), 0, 0)
        self.span_length_input = QLineEdit()
        grid.addWidget(self.span_length_input, 0, 1)

        grid.addWidget(QLabel('Width (m):'), 0, 2)
        self.width_input = QLineEdit()
        grid.addWidget(self.width_input, 0, 3)

        grid.addWidget(QLabel('Traffic Volume (vehicles/day):'), 1, 0)
        self.traffic_volume = QLineEdit()
        grid.addWidget(self.traffic_volume, 1, 1)

        grid.addWidget(QLabel('Design Life (years):'), 1, 2)
        self.design_life = QLineEdit()
        grid.addWidget(self.design_life, 1, 3)

        # Perform Calculation Button
        self.calculate_button = QPushButton('Calculate Costs')
        self.calculate_button.clicked.connect(self.calculate_costs)
        grid.addWidget(self.calculate_button, 2, 0, 1, 4)

        self.input_layout.addLayout(grid)
        self.result_label = QLabel('')
        self.input_layout.addWidget(self.result_label)

    def create_output_table(self):
        self.output_layout.addWidget(QLabel("Cost Comparison Table", alignment=Qt.AlignCenter))

        self.output_table = QTableWidget()
        self.output_table.setColumnCount(3)
        self.output_table.setHorizontalHeaderLabels(["Cost Component", "Steel Bridge (₹)", "Concrete Bridge (₹)"])
        self.output_layout.addWidget(self.output_table)

        self.export_button = QPushButton("Export Plot as PNG")
        self.export_button.clicked.connect(self.export_plot)
        self.output_layout.addWidget(self.export_button)

    def calculate_costs(self):
        try:
            span_length = float(self.span_length_input.text())
            width = float(self.width_input.text())
            traffic_volume = float(self.traffic_volume.text())
            design_life = int(self.design_life.text())
        except ValueError:
            self.result_label.setText("Error: Please enter valid numerical inputs.")
            return

        results = self.calculator.calculate_costs(span_length, width, traffic_volume, design_life)
        self.populate_output_table(results)
        self.plotter.plot_comparison(results)

    def populate_output_table(self, results):
        cost_components = ["Construction Cost", "Maintenance Cost", "Repair Cost", "Demolition Cost",
                           "Environmental Cost", "Social Cost", "User Cost", "Total Cost"]

        self.output_table.setRowCount(len(cost_components))

        for i, component in enumerate(cost_components):
            self.output_table.setItem(i, 0, QTableWidgetItem(component))
            self.output_table.setItem(i, 1, QTableWidgetItem(f"{results[0][i + 1]:,.2f}"))
            self.output_table.setItem(i, 2, QTableWidgetItem(f"{results[1][i + 1]:,.2f}"))

    def export_plot(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png)", options=options)
        if file_path:
            self.plotter.export_plot(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BridgeCostApp()
    window.show()
    sys.exit(app.exec_())