# Bridge Cost Comparison Application

## Overview
This application allows users to compare the costs of steel and concrete bridges based on various cost categories such as construction, maintenance, repair, and more. It provides a user-friendly GUI, detailed breakdown tables, and interactive plots.

## Features
- Input parameters like span length, width, traffic volume, and design life.
- Bar plot comparing costs of steel and concrete bridges.
- Dynamic resizing of GUI components.
- Export plot as an image.

---

## Setup Instructions

### Prerequisites
Ensure the following are installed:
1. Python (version 3.8 or above)
2. `pip` (Python package manager)
3. SQLite3 (for database handling)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-repo>/bridge-cost-comparison.git
   cd bridge-cost-comparison
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify the SQLite database file (`bridge_costs.db`) exists in the root folder.

4. Run the application:
   ```bash
   python main.py
   ```

---

## File Structure and Descriptions

### Python Files
- **`main.py`**:
  The entry point of the application. Initializes the GUI and handles user interactions.

- **`plot.py`**:
  Contains the `Plotter` class to generate and update bar plots.

- **`database.py`**:
  Handles all database operations, such as fetching cost data for calculations.

- **`calculations.py`**:
  Implements the `CostCalculator` class to perform cost estimations based on user inputs.

### Supporting Files
- **`bridge_costs.db`**:
  SQLite database containing pre-populated cost data for various categories.

- **`requirements.txt`**:
  Lists the Python packages required to run the application.

### Additional Resources
- **`README.md`**:
  Provides setup and usage instructions.

---

## Usage Instructions
1. Launch the application using the command:
   ```bash
   python main.py
   ```

2. Enter the required inputs (e.g., span length, width, traffic volume).

3. Click the **Calculate Costs** button to view:
   - Cost comparison bar plot.
   - Detailed breakdown table.

4. Use the **Export Plot as PNG** button to save the bar chart.

---

## Contributing
Feel free to contribute to this project by creating pull requests or submitting issues.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
