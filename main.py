import numpy
import pandas as pd
import scipy
import serial
from matplotlib import pyplot
from serial.tools import list_ports


class Addons:

    @staticmethod
    def AvailableAddons():
        availableAddons = ["Integration", "differentiation"]
        return availableAddons

    def integrate(self, X: numpy.ndarray, Y: numpy.ndarray, save="None", type="cumulative_trapezoid"):
        integral = scipy.integrate.cumulative_trapezoid(y=Y, x=X)
        pyplot.figure()
        pyplot.title("Integral graph")
        pyplot.plot(integral)
        pyplot.figure()
        pyplot.title("Area marking")
        # TODO Check and add filter if auto and x values are different
        pyplot.fill_between(x=X, y1=Y, color='purple')  # alpha=0.5


class PlotCSVData:

    def __init__(self, csv_dir, identifier, PyplotStyle, Utils: dict):
        pyplot.style.use(PyplotStyle)
        self.csv_dir = csv_dir
        self.identifier = identifier
        self.SLOW = 1
        self.FAST = 0.05
        self.MID = 0.525
        self.utils = Utils
        self.adds = Addons()

    def CheckAddons(self, selectedAddons):
        AvailableList = Addons.AvailableAddons()
        try:
            for i in selectedAddons.get("addons"):
                subsetselection = []
                if i in AvailableList:
                    subsetselection.append(i)
                return subsetselection
        except:
            # print("Nothing was selected")
            return []

    def ShowSingleGraph(self, x_plot: str, y_plot: str):
        df = pd.read_csv(self.csv_dir)
        pyplot.figure(self.identifier)
        pyplot.xlabel(x_plot)
        pyplot.ylabel(y_plot)
        y = df[y_plot].tolist()
        x = []
        if x_plot != "auto":
            x = df[x_plot].tolist()
        else:
            x = range(0, len(y))
        x = numpy.array(x)
        y = numpy.array(y)
        # fg = pyplot.figure(num=identifier, figsize=(width,height))
        pyplot.plot(x, y)
        pyplot.title(self.identifier)
        addonsSel = self.CheckAddons(self.utils)
        if addonsSel != []:
            try:
                if "Integration" in addonsSel:
                    self.adds.integrate(X=x, Y=y)
            except Exception as e:
                print("Could not use the addon", e)
        return pyplot

    def ShowMultiGraph(self, y_plots: list):
        df = pd.read_csv(self.csv_dir)
        pyplot.figure(self.identifier)
        pyplot.xlabel("Auto-increment")
        pyplot.ylabel(' '.join(y_plots))
        addonsSel = self.CheckAddons(self.utils)
        for yplot in y_plots:
            y = df[yplot].tolist()
            y = numpy.array(y)
            pyplot.plot(y)
            if addonsSel != []:
                try:
                    if "Integration" in addonsSel:
                        self.adds.integrate(X=numpy.array(range(len(y))), Y=y)
                except Exception as e:
                    print("Could not use the addon", e)
        pyplot.title(self.identifier)
        return pyplot

    def ShowAnimation(self, arr: list[list], plotBuffer: int, pauseInterval: int):
        col = 0
        row = 0
        col2D = 0
        while row <= (len(arr)):
            pyplot.plot(arr[row][:col])
            col = col + plotBuffer
            row = row + 1
            pyplot.show(block=False)
            pyplot.pause(pauseInterval)
            if col <= len(arr[0]) and row == len(arr):
                row = 0
            else:
                if col >= len(arr[0]):
                    break
                else:
                    continue

    def ShowAnimatedGraph(self, y_plots: list, plotBuffer=2, pauseInterval=2):
        buffer = 2
        df = pd.read_csv(self.csv_dir)
        pyplot.figure(self.identifier)
        pyplot.xlabel("Auto-increment")
        pyplot.ylabel(' '.join(y_plots))
        Make2DList = []
        for plots in y_plots:
            Make2DList.append(df[plots].tolist())
        y_nparr = numpy.array(Make2DList)
        pyplot.xlim(0, len(Make2DList[0]) + buffer)
        pyplot.ylim(numpy.amin(y_nparr) - buffer, numpy.amax(y_nparr) + buffer)
        # print(Make2DList)
        self.ShowAnimation(Make2DList, plotBuffer, pauseInterval)


class PlotSerialData:
    def ListAvailablePorts(self):
        ports = serial.tools.list_ports.comports()
        ComPorts = {}
        for port, desc, hwid in sorted(ports):
            ComPorts[port] = [desc, hwid]
        return ComPorts

    def AllComPortsDisplay(self):
        ComDef = self.ListAvailablePorts()
        ComPortsAll = ComDef.keys()
        DisplaySting = ''
        DisplaySting += "######################" + "\n"
        for com in ComPortsAll:
            DisplaySting += "COM port: " + str(com) + "\n"
            try:
                DisplaySting += "COM Description: " + ComDef[com][0] + "\n"
            except Exception as E:
                print(E)
            try:
                DisplaySting += "Hardware Identification: " + ComDef[com][1] + "\n"
            except Exception as E:
                print(E)
            DisplaySting += "######################" + "\n"
        return DisplaySting

    def __init__(self):
        self.AllComPortsDisplay()

    def RecieveData(self, COM, BaudRate=9600):
        data = serial.Serial(port=COM, baudrate=BaudRate)
        return data
        # while True:
        #     yield data.readline().decode().replace("\n", "")

    # def ShowPlot(self):

    def Plotter(self, title: str, rawData: dict, cmd: str, limit: int):
        if cmd == "data":
            try:
                pyplot.legend(list(rawData.keys()))
                pyplot.title(title)
                # pyplot.xlim(0, limit)
                pyplot.pause(0.00000001)
                for it, head in enumerate(rawData.keys()):
                    headData = numpy.array(rawData[head])
                    pyplot.plot(headData)
                pyplot.show(block=False)
                # pyplot.pause(1)
            except:
                self.PlotValidator(len(rawData))
        elif cmd == "clear":
            pyplot.cla()
            # TODO Exit if the user wants to quit !

    def Formatter(self):
        raise NotImplemented

    def PlotValidator(self, Lenght: int):
        if Lenght % 2 == 0:
            print("Data Validation successful")
        else:
            print("Format error", Lenght)
            raise TypeError
