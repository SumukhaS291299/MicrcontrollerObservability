import numpy
import pandas as pd
import serial
from matplotlib import pyplot
from serial.tools import list_ports


class PlotCSVData:

    def __init__(self, csv_dir, identifier):
        self.csv_dir = csv_dir
        self.identifier = identifier
        self.SLOW = 1
        self.FAST = 0.05
        self.MID = 0.525

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
        try:
            with open("web.txt", "w") as w:
                w.write("X: " + str(list(x)) + "\n")
                w.write("Y: " + str(list(y)))
        except Exception as E:
            print(E)
        x = numpy.array(x)
        y = numpy.array(y)
        # fg = pyplot.figure(num=identifier, figsize=(width,height))
        pyplot.plot(x, y)
        pyplot.title(self.identifier)
        return pyplot

    def ShowMultiGraph(self, y_plots: list):
        df = pd.read_csv(self.csv_dir)
        pyplot.figure(self.identifier)
        pyplot.xlabel("Auto-increment")
        pyplot.ylabel(' '.join(y_plots))
        for yplot in y_plots:
            y = df[yplot].tolist()
            y = numpy.array(y)
            pyplot.plot(y)
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

    def __init__(self):
        ComDef = self.ListAvailablePorts()
        ComPortsAll = ComDef.keys()
        print("######################")
        for com in ComPortsAll:
            print("COM port: ", com)
            try:
                print("COM Description: ", ComDef[com][0])
            except Exception as E:
                print(E)
            try:
                print("Hardware Identification: ", ComDef[com][1])
            except Exception as E:
                print(E)
            print("######################")

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

# s = PlotSerialData()
# # Default Format
# PlotDict = {}
# while True:
#     data = s.RecieveData("COM3")
#     data = data.readline().decode().replace("\n", '').replace("\r", '').strip()
#     data_formatted = data.split(" ")
#     for itter in range(len(data_formatted)):
#         try:
#             if itter % 2 == 0:
#                 PlotDict.setdefault(data_formatted[itter], []).append(float(data_formatted[itter + 1]))
#                 try:
#                     if len(PlotDict.get(data_formatted[len(data_formatted) - 2])) > 50:  # Get Key of Last Set
#                         PlotDict = {}
#                         print(PlotDict)
#                         # TODO Remove (50/2) number of elements by [n:] if 50/2 is reached give limit as the same
#                         s.Plotter("MPU6050 Data", PlotDict, "clear", 50)
#                 except:
#                     pass
#         except Exception as e:
#             print(e)
#     with open("DataBackup.json", "w") as backupFile:
#         json.dump(PlotDict, backupFile, indent=4)
#     print(PlotDict)
#     s.Plotter("MPU6050 Data", PlotDict, "data", limit=50)
