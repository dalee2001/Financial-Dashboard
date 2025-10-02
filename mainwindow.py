# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from ui_form import Ui_MainWindow

# ------------------ Example spending data ------------------
monthly_spending = {
    "January": {"Food": 50, "Entertainment": 20, "Transport": 15, "Bills": 15},
    "February": {"Food": 40, "Entertainment": 25, "Transport": 20, "Bills": 15},
    "March": {"Food": 55, "Entertainment": 15, "Transport": 15, "Bills": 15},
    "April": {"Food": 45, "Entertainment": 20, "Transport": 20, "Bills": 15},
    # Add remaining months as needed
}

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # --------- Buttons Setup ---------
        months = [
            ("January", self.ui.januaryButton),
            ("February", self.ui.februaryButton),
            ("March", self.ui.marchButton),
            ("April", self.ui.aprilButton),
            ("May", self.ui.mayButton),
            ("June", self.ui.juneButton),
            ("July", self.ui.julyButton),
            ("August", self.ui.augustButton),
            ("September", self.ui.septemberButton),
            ("October", self.ui.octoberButton),
            ("November", self.ui.novemberButton),
            ("December", self.ui.decemberButton)
        ]

        # Connect each button to updateMonth function and set hand cursor
        for month_name, button in months:
            button.clicked.connect(lambda checked, m=month_name: self.updateMonth(m))
            button.setCursor(Qt.PointingHandCursor)

        # --------- Matplotlib Pie Chart Setup ---------
        # Create figure and axes (ax is the chart area)
        self.figure, self.ax = plt.subplots()
        # Wrap the figure in a Qt widget so it can be displayed in the UI
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(150, 150)  # Set fixed size of the pie chart

        # Create vertical layout for pie chart and labels
        self.chart_layout = QVBoxLayout(self.ui.pieChartWidget)
        # Add canvas to the layout
        self.chart_layout.addWidget(self.canvas, alignment=Qt.AlignHCenter)

        # Container for labels in two columns
        self.labels_widget = QWidget()
        self.labels_layout = QHBoxLayout(self.labels_widget)
        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()
        self.labels_layout.addLayout(self.left_column)
        self.labels_layout.addLayout(self.right_column)
        # Add the labels container below the chart
        self.chart_layout.addWidget(self.labels_widget)

        # Set default month
        self.current_month = "January"
        self.updateMonth(self.current_month)

    def updateMonth(self, month):
        self.current_month = month

        # ---------- Update cash flow label ----------
        self.ui.cashFlowLabel.setText(f"My Cash Flow for {month}")
        self.ui.cashFlowLabel.adjustSize()  # Adjust size in case text changes

        # ---------- Update pie chart ----------
        self.ax.clear()  # Clear previous chart before drawing a new one

        # Get spending data for the selected month
        data = monthly_spending.get(month, {})
        categories = list(data.keys())  # ["Food", "Entertainment", ...]
        values = list(data.values())    # [50, 20, 15, 15]


        # Hex code colors for pie chart
        # Pastel Red - #DE5B5B
        # Pastel Blue - #5B8BDE
        # Pastel Purple - #7A5BDE
        # Pastel Yellow - #DEDE5B

        # Set custom colors for pie chart slices
        colors = ["#DE5B5B", "#5B8BDE", "#7A5BDE", "#DEDE5B"]

        # Draw donut pie chart
        wedges, texts = self.ax.pie(
            values,              # Slice sizes
            labels=None,         # No text directly on slices
            startangle=90,       # Rotate chart so first slice starts at top (12 o'clock)
            wedgeprops=dict(width=0.4, edgecolor=None),  # Width=0.4 makes a donut
            colors=colors        # Custom slice colors
        )

        # Make chart circular
        self.ax.set_aspect("equal")
        # Transparent figure background
        self.figure.patch.set_alpha(0)
        # Transparent axes background
        self.ax.set_facecolor("none")
        # Hide axes ticks/lines
        self.ax.axis("off")
        # Render chart
        self.canvas.draw()

        # ---------- Update labels ----------
        # Clear old labels first
        for layout in [self.left_column, self.right_column]:
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

        total = sum(values)  # Total spending for calculating percentages
        half = (len(categories) + 1) // 2  # Split categories into two columns
        left_items = list(zip(wedges[:half], categories[:half], values[:half]))
        right_items = list(zip(wedges[half:], categories[half:], values[half:]))

        # Add left column labels
        for wedge, cat, val in left_items:
            percent = int((val / total) * 100)  # Convert to integer percent
            label = QLabel(f"{percent}% {cat}")  # Create QLabel for this category
            rgba = wedge.get_facecolor()  # Get the color of the slice
            # Convert RGBA to hex string for Qt stylesheet
            hex_color = "#{:02x}{:02x}{:02x}".format(
                int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255)
            )
            label.setStyleSheet(f"color: {hex_color}; font-size: 10pt;")
            self.left_column.addWidget(label)

        # Add right column labels
        for wedge, cat, val in right_items:
            percent = int((val / total) * 100)
            label = QLabel(f"{percent}% {cat}")
            rgba = wedge.get_facecolor()
            hex_color = "#{:02x}{:02x}{:02x}".format(
                int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255)
            )
            label.setStyleSheet(f"color: {hex_color}; font-size: 10pt;")
            self.right_column.addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
