from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Plotter:
    def __init__(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

    def get_canvas(self):
        return self.canvas

    def plot_comparison(self, results):
        labels = ["Construction", "Maintenance", "Repair", "Demolition", "Environmental", "Social", "User"]
        steel_costs = [results[0][i + 1] for i in range(len(labels))]
        concrete_costs = [results[1][i + 1] for i in range(len(labels))]

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        x = range(len(labels))
        bar_width = 0.35

        ax.bar(x, steel_costs, width=bar_width, label="Steel", color="blue")
        ax.bar([p + bar_width for p in x], concrete_costs, width=bar_width, label="Concrete", color="orange")

        ax.set_xticks([p + bar_width / 2 for p in x])
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_ylabel("Cost (₹)")
        ax.set_title("Cost Comparison: Steel vs. Concrete")
        ax.legend()

        self.canvas.draw()

    def export_plot(self, file_path):
        self.figure.savefig(file_path)