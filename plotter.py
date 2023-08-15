import matplotlib.pyplot as plt

class DataPlotter:
    def __init__(self):
        self.time_data = []
        self.horizontal_data = []
        self.vertical_data = []

        self.fig, (self.ax_horizontal, self.ax_vertical) = plt.subplots(2, 1, sharex=True)
        self.line_horizontal, = self.ax_horizontal.plot([], [], label='Horizontal')
        self.line_vertical, = self.ax_vertical.plot([], [], label='Vertical')

        self.ax_horizontal.set_ylabel('Horizontal EOG Signal')
        self.ax_horizontal.legend()

        self.ax_vertical.set_xlabel('Time')
        self.ax_vertical.set_ylabel('Vertical EOG Signal')
        self.ax_vertical.legend()

    def update_plot(self, time, horizontal, vertical):
        self.time_data.append(time)
        self.horizontal_data.append(horizontal)
        self.vertical_data.append(vertical)

        self.line_horizontal.set_data(self.time_data, self.horizontal_data)
        self.line_vertical.set_data(self.time_data, self.vertical_data)
        
        self.ax_horizontal.relim()
        self.ax_horizontal.autoscale_view()

        self.ax_vertical.relim()
        self.ax_vertical.autoscale_view()

        plt.pause(0.01)
