import json
import pickle
import sys
import tkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import pandas
import pandas as pd
from matplotlib import pyplot
from tabulate import tabulate

from main import Addons
from main import PlotCSVData
from main import PlotSerialData

StartAnimCount = 0
LoadingX = 150


def LoadingAnimation():
    global canvas, root, LoadingX
    if LoadingX <= 250:
        canvas.delete("all")
        canvas.create_text(LoadingX, 150, text="/", fill="purple", font=('Helvetica 30 bold'))
        LoadingX = LoadingX + 20
        root.after(300, LoadingAnimation)
    else:
        canvas.create_text(150, 150, text="Loaded Graphs...", fill="purple", font=('Helvetica 16 bold'))
        root.after(400, canvas.destroy)


def CanvasStartAnimation():
    global canvas, StartAnimCount, root
    canvas.delete("all")
    canvas.create_text(150, 20, text="An open-source plotter by Sumukha S", fill="green", font=('Helvetica 11 bold'))
    if StartAnimCount <= 6:
        if (StartAnimCount % 2) == 0:
            canvas.create_text(150, 150, text="/", fill="purple", font=('Helvetica 30 bold'))
        else:
            canvas.create_text(150, 150, text="-", fill="purple", font=('Helvetica 30 bold'))
        StartAnimCount = StartAnimCount + 1
        root.after(300, CanvasStartAnimation)
    else:
        root.after(300, LoadingAnimation)


def GetSingleGraph():
    # Replace with multi value and df.head
    global HeadEntry, DefaultValueX, DefaultValueY, file, StyleSelected, utilsDict
    plotter = PlotCSVData(
        file, str(HeadEntry.get()), PyplotStyle=StyleSelected, Utils=utilsDict)
    plot = plotter.ShowSingleGraph(x_plot=str(DefaultValueX.get()), y_plot=str(DefaultValueY.get()))
    plot.show()


def GetMultiGraph():
    # Replace with multi value and df.head
    global MultiGraphfile, HeadEntry_MultiGraph, YPlot_Box, StyleSelected, utilsDict,WebMultiColnInput
    plotter = PlotCSVData(
        MultiGraphfile, str(HeadEntry_MultiGraph.get()), PyplotStyle=StyleSelected, Utils=utilsDict)
    selected_tuple = YPlot_Box.curselection()
    selected = []
    for indx in selected_tuple:
        selected.append(YPlot_Box.get(indx))
    plot = plotter.ShowMultiGraph(selected)
    try:
        with open("Columns.txt", "wb") as webcols:
            pickle.dump(int(WebMultiColnInput.get()), webcols)
    except Exception as e:
        print(e)
    plot.show()


def CallSingleGraph():
    global HeadEntry, DefaultValueX, DefaultValueY, file
    # Do only for CSV files
    SingleGraph = tkinter.Tk()
    SingleGraph.title("S√PyPlots")
    SingleGraph.geometry('640x480')
    file = askopenfilename()
    file = file.replace("\\", "//")
    csv_readFile = pd.read_csv(file)
    PlotValues = csv_readFile.columns.values.tolist()
    SingleGraph.focus()
    Title = tkinter.Label(SingleGraph, text="Welcome to Single X-Y Plots", font=("Terminal", 25))
    Title.pack(side=tkinter.TOP, pady=5)
    fileLabel = tkinter.Label(SingleGraph, text="File Selected: " + file, font=("Terminal", 17))
    fileLabel.pack(pady=5, padx=5)
    HeadLabel = tkinter.Label(SingleGraph, text="Plot Headings", font=("Terminal", 17))
    HeadLabel.pack(pady=20, padx=5)
    HeadEntry = tkinter.Entry(SingleGraph)
    HeadEntry.pack(padx=10, pady=2)
    XplotValues = PlotValues.copy()
    XplotValues.append("auto")
    YplotValues = PlotValues.copy()
    XPlot_Label = tkinter.Label(SingleGraph, text="X Axis Plot", font=("Terminal", 17))
    XPlot_Label.pack(padx=20, pady=5)
    DefaultValueX = tkinter.StringVar(SingleGraph)
    DefaultValueX.set("Select an Option")
    DefaultValueY = tkinter.StringVar(SingleGraph)
    DefaultValueY.set("Select an Option")
    XPlot_Entry = tkinter.OptionMenu(SingleGraph, DefaultValueX, *XplotValues)
    XPlot_Entry.pack()
    YPlot_Label = tkinter.Label(SingleGraph, text="Y Axis Plot", font=("Terminal", 17))
    YPlot_Label.pack(padx=20, pady=5)
    YPlot_Entry = tkinter.OptionMenu(SingleGraph, DefaultValueY, *YplotValues)
    YPlot_Entry.pack()
    DoneButton = tkinter.Button(SingleGraph, text="Done", command=GetSingleGraph)
    DoneButton.pack(side=tkinter.BOTTOM, pady=10)


def CallMultiGraph():
    global MultiGraphfile, HeadEntry_MultiGraph, YPlot_Box, utilsDict,WebMultiColnInput
    # Do only for CSV files
    MultiGraph = tkinter.Tk()
    MultiGraph.title("S√PyPlots")
    MultiGraph.geometry('640x480')
    MultiGraphfile = askopenfilename()
    MultiGraphfile = MultiGraphfile.replace("\\", "//")
    csv_readFile = pd.read_csv(MultiGraphfile)
    PlotValues = csv_readFile.columns.values.tolist()
    MultiGraph.focus()
    Title = tkinter.Label(MultiGraph, text="Welcome to Multi Plot Graph", font=("Terminal", 25))
    Title.pack(side=tkinter.TOP, pady=5)
    fileLabel = tkinter.Label(MultiGraph, text="File Selected: " + MultiGraphfile, font=("Terminal", 17))
    fileLabel.pack(pady=5, padx=5)
    HeadLabel = tkinter.Label(MultiGraph, text="Plot Headings", font=("Terminal", 17))
    HeadLabel.pack(pady=20, padx=5)
    HeadEntry_MultiGraph = tkinter.Entry(MultiGraph)
    HeadEntry_MultiGraph.pack(padx=10, pady=2)
    XplotValues = PlotValues.copy()
    XplotValues.append("auto")
    YplotValues = PlotValues.copy()
    XPlot_Label = tkinter.Label(MultiGraph, text="X Axis Plot: Auto Scale(Default)", font=("Terminal", 17))
    XPlot_Label.pack(padx=20, pady=5)
    YPlot_Label = tkinter.Label(MultiGraph, text="Y Axis Plot [MultiSelect: ON,Scroll:ON]", font=("Terminal", 17))
    YPlot_Label.pack(padx=20, pady=5)
    YPlot_Box = tkinter.Listbox(MultiGraph, selectmode=tkinter.MULTIPLE, height=6)
    for col in YplotValues:
        YPlot_Box.insert(tkinter.END, col)
    YPlot_Box.pack()
    CheckWebAddon = utilsDict.get("addons")
    print(CheckWebAddon)
    try:
        WebLayout = tkinter.Label(MultiGraph, text="Number of Columns for the Web layout ", font=("Terminal", 17))
        WebLayout.pack(padx=20, pady=5)
        if "Multi Graph Web plot" in CheckWebAddon:
            WebMultiColnInput = tkinter.Scale(MultiGraph, from_=1,
                                       to=20,
                                       orient="horizontal")
            WebMultiColnInput.pack()
    except Exception as e:
        print(e)
    DoneButton = tkinter.Button(MultiGraph, text="Done", command=GetMultiGraph)
    DoneButton.pack(side=tkinter.BOTTOM, pady=10)


def GetAnimationGraph():
    # Replace with multi value and df.head
    global GraphAnimationFile, HeadEntry_AnimGraph, PlotBufferEntry, PauseIntervalSelector, YPlot_Box_Anim
    plotter = PlotCSVData(
        GraphAnimationFile, str(HeadEntry_AnimGraph.get()), PyplotStyle=StyleSelected, Utils={})
    selected_tuple = YPlot_Box_Anim.curselection()
    selected = []
    for indx in selected_tuple:
        selected.append(YPlot_Box_Anim.get(indx))
    pause = str(PauseIntervalSelector.get())
    # Come with Bettter Sol
    PI = 2
    if pause == "SLOW":
        PI = plotter.SLOW
    elif pause == "MID":
        PI = plotter.MID
    else:
        PI = plotter.FAST
    plotter.ShowAnimatedGraph(selected, plotBuffer=int(PlotBufferEntry.get()),
                              pauseInterval=PI)


def CallAnimation():
    global GraphAnimationFile, HeadEntry_AnimGraph, PlotBufferEntry, PauseIntervalSelector, YPlot_Box_Anim
    # Do only for CSV files
    GrapAnimation = tkinter.Tk()
    GrapAnimation.title("S√PyPlots")
    GrapAnimation.geometry('640x480')
    GraphAnimationFile = askopenfilename()
    GraphAnimationFile = GraphAnimationFile.replace("\\", "//")
    csv_readFile = pd.read_csv(GraphAnimationFile)
    PlotValues = csv_readFile.columns.values.tolist()
    GrapAnimation.focus()
    Title = tkinter.Label(GrapAnimation, text="Welcome to Graph Animations", font=("Terminal", 25))
    Title.pack(side=tkinter.TOP, pady=5)
    fileLabel = tkinter.Label(GrapAnimation, text="File Selected: " + GraphAnimationFile, font=("Terminal", 17))
    fileLabel.pack(pady=5, padx=5)
    HeadLabel = tkinter.Label(GrapAnimation, text="Plot Headings", font=("Terminal", 17))
    HeadLabel.pack(pady=20, padx=5)
    HeadEntry_AnimGraph = tkinter.Entry(GrapAnimation)
    HeadEntry_AnimGraph.pack(padx=10, pady=2)
    PlotBufferLabel = tkinter.Label(GrapAnimation, text="Number of datapoints to capture per itteration (Ex: 1,2 etc)",
                                    font=("Terminal", 17))
    PlotBufferLabel.pack(pady=20, padx=5)
    PlotBufferEntry = tkinter.Entry(GrapAnimation)
    PlotBufferEntry.pack(padx=10, pady=2)
    PauseIntervalLabel = tkinter.Label(GrapAnimation,
                                       text="The pause(sleep) interval after every itteration",
                                       font=("Terminal", 17))
    PauseIntervalLabel.pack(pady=20, padx=5)

    AnimationTypes = []
    AnimationTypes.append("SLOW")
    AnimationTypes.append("MID")
    AnimationTypes.append("FAST")
    PauseIntervalSelector = tkinter.StringVar(GrapAnimation)
    PauseIntervalSelector.set("Select an Option")
    PauseIntervalEntry = tkinter.OptionMenu(GrapAnimation, PauseIntervalSelector, *AnimationTypes)
    PauseIntervalEntry.pack()

    YplotValues = PlotValues.copy()
    XPlot_Label = tkinter.Label(GrapAnimation, text="X Axis Plot: Auto Scale(Default)", font=("Terminal", 17))
    XPlot_Label.pack(padx=20, pady=5)
    YPlot_Label = tkinter.Label(GrapAnimation, text="Y Axis Plot [MultiSelect: ON,Scroll:ON]", font=("Terminal", 17))
    YPlot_Label.pack(padx=20, pady=5)
    YPlot_Box_Anim = tkinter.Listbox(GrapAnimation, selectmode=tkinter.MULTIPLE, height=6)
    for col in YplotValues:
        YPlot_Box_Anim.insert(tkinter.END, col)
    YPlot_Box_Anim.pack()
    DoneButton = tkinter.Button(GrapAnimation, text="Done", command=GetAnimationGraph)
    DoneButton.pack(side=tkinter.BOTTOM, pady=10)


def ReadLiveData():
    global s, DefaultCOM
    PlotDict = {}
    while True:
        data = s.RecieveData(str(DefaultCOM.get()))
        data = data.readline().decode().replace("\n", '').replace("\r", '').strip()
        data_formatted = data.split(" ")
        # print(data_formatted)
        for itter in range(len(data_formatted)):
            try:
                if itter % 2 == 0:
                    PlotDict.setdefault(data_formatted[itter], []).append(float(data_formatted[itter + 1]))
                    try:
                        if len(PlotDict.get(data_formatted[len(data_formatted) - 2])) > 300:  # Get Key of Last Set
                            PlotDict = {}
                            # print(PlotDict)
                            # TODO Remove (50/2) number of elements by [n:] if 50/2 is reached give limit as the same
                            s.Plotter("Clearing...", PlotDict, "clear", 300)
                    except:
                        pass
            except Exception as e:
                print(e)
        with open("DataBackup.json", "w") as backupFile:
            json.dump(PlotDict, backupFile, indent=4)
        # print(PlotDict)
        s.Plotter("Live Data", PlotDict, "data", limit=50)


def CallReadLiveData():
    global s, DefaultCOM
    print("Checking ComPorts...")
    s = PlotSerialData()
    Ports = s.ListAvailablePorts()
    tkinter.messagebox.showinfo(title="Available COM Ports", message=s.AllComPortsDisplay())
    s.ListAvailablePorts()
    ReadLiveDataWin = tkinter.Tk()
    ReadLiveDataWin.title("S√PyPlots")
    ReadLiveDataWin.geometry('640x480')
    Title = tkinter.Label(ReadLiveDataWin, text="Live Data Reader", font=("Terminal", 25))
    Title.pack(side=tkinter.TOP, pady=5)
    DefaultCOM = tkinter.StringVar(ReadLiveDataWin)
    DefaultCOM.set("Select an Option")
    comPorts = list(Ports.keys())
    COMOptionsBox = tkinter.OptionMenu(ReadLiveDataWin, DefaultCOM, *comPorts)
    COMOptionsBox.pack()
    DoneButton = tkinter.Button(ReadLiveDataWin, text="Done", command=ReadLiveData)
    DoneButton.pack(side=tkinter.BOTTOM, pady=10)


def about():
    msg = 'Developer: Sumukha S\nStable Release: Beta 1.3\nEmail: sumukhashivashankar@outlook.com\nPython Version: 3.11'
    tkinter.messagebox.showinfo(title="Software Version", message=msg)


def setOptions():
    # TODO Add Grid and other style options
    # TODO Add functional changes
    global DefaultStyle, opt, StyleSelected, addons, utilsDict
    UpdatedLable = tkinter.Label(opt, text="Updated values...", font=("Terminal", 15))
    UpdatedLable.pack()
    selected_tuple = addons.curselection()
    selected = []
    for indx in selected_tuple:
        selected.append(addons.get(indx))
    utilsDict = {"addons": selected}
    StyleSelected = str(DefaultStyle.get())
    opt.destroy()


def addonsManager():
    global utilsDict, StyleSelected, root
    addonManagerWin = tkinter.Toplevel(root)
    addonManagerWin.title("S√PyPlots")
    addonManagerWin.geometry('640x280')
    addonManagerWinTitle = tkinter.Label(addonManagerWin, text="Welcome to S√PyPlots Plugin Manager",
                                         font=("Terminal", 15))
    addonManagerWinTitle.pack()
    addonManagerWinTitle = tkinter.Label(addonManagerWin, text="",
                                         font=("Terminal", 11))
    addonManagerWinTitle.pack()
    addonManagerWinTitle.pack()
    StyleSelector = tkinter.Label(addonManagerWin, text=f"Selected Style = {StyleSelected}",
                                  font=("Terminal", 11))
    StyleSelector.pack()
    if utilsDict == {}:
        addonManagerWinNone = tkinter.Label(addonManagerWin, text="None of the Plugins or addons selected",
                                            font=("Terminal", 11))
        addonManagerWinNone.pack()
    else:
        addonsdf = pandas.DataFrame(utilsDict.get("addons"))
        addonstr = tabulate(addonsdf, headers=['Sl no.', 'Plugins Activated'], tablefmt='psql')
        addonManagerWinAvail = tkinter.Label(addonManagerWin, text=addonstr,
                                             font=("Terminal", 15))
        addonManagerWinAvail.pack()


def options():
    global DefaultStyle, opt, addons
    opt = tkinter.Tk()
    opt.title("S√PyPlots")
    opt.geometry('640x480')
    optTitle = tkinter.Label(opt, text="Welcome to S√PyPlots", font=("Terminal", 25))
    optTitle.pack(side=tkinter.TOP, pady=5)
    plotStyles = pyplot.style.available
    DefaultStyle = tkinter.StringVar(opt)
    DefaultStyle.set("default")
    plotSytleOptions = tkinter.OptionMenu(opt, DefaultStyle, *plotStyles)
    plotSytleOptions.pack()
    # utils also called addons and used intechangably
    utils = Addons.AvailableAddons()
    addons = tkinter.Listbox(opt, selectmode=tkinter.MULTIPLE, height=6)
    for col in utils:
        addons.insert(tkinter.END, col)
    addons.pack()
    IntegrateWithRange = tkinter.Label(opt,
                                       text="Integrate with range only available with single graph(Plot X-Y Graph)",
                                       font=("Terminal", 11), highlightcolor="red")
    IntegrateWithRange.pack()
    IntegrateWithRange.pack()
    IntegrateWithRange = tkinter.Label(opt,
                                       text="Roots,Slope only available with single graph(Plot X-Y Graph) \nas the X-axis is dynamically sized",
                                       font=("Terminal", 11), highlightcolor="red")
    IntegrateWithRange.pack()
    WEBB = tkinter.Label(opt, text="Multi Graph Web plot[Works with Plot Multi-Plot Graph], \nis used to visualise multiple graphs on a webpage\nWe use Streamlit libraries for the web \ninterface, for more robust \noperations we recommend using the streamlit cli", font=("Terminal", 11))
    WEBB.pack(padx=20, pady=5)
    Done = tkinter.Button(opt, text="Done", bd="5", command=setOptions)
    Done.pack(padx=10, pady=20)


def Quit():
    sys.exit(0)


def MainLoop():
    global canvas, root, DefaultStyle, utilsDict, StyleSelected
    StyleSelected = 'default'
    utilsDict = {}
    root = tkinter.Tk()
    root.title("S√PyPlots")
    root.geometry('640x528')
    # Start Sequence
    Title = tkinter.Label(root, text="Welcome to S√PyPlots", font=("Terminal", 25))
    Title.pack(side=tkinter.TOP, pady=5)
    canvas = tkinter.Canvas(root, bg="cyan", height=300, width=300)
    canvas.pack(side=tkinter.TOP, pady=50)
    root.after(500, CanvasStartAnimation)
    SingleGraph = tkinter.Button(root, text="Plot X-Y Graph", bd="5", command=CallSingleGraph)
    SingleGraph.pack(padx=10, pady=20)
    MultiPlotGraph = tkinter.Button(root, text="Plot Multi-Plot Graph", bd="5", command=CallMultiGraph)
    MultiPlotGraph.pack(padx=10, pady=20)
    GraphAnimation = tkinter.Button(root, text="Graph animation", bd="5", command=CallAnimation)
    GraphAnimation.pack(padx=10, pady=20)
    GraphAnimation = tkinter.Button(root, text="Read Live Data", bd="5", command=CallReadLiveData)
    GraphAnimation.pack(padx=10, pady=20)
    OptionsButton = tkinter.Button(root, text="Options", bd="5", command=options)
    OptionsButton.pack(padx=10, pady=20)
    AddonsManager = tkinter.Button(root, text="Addons Manager", bd="5", command=addonsManager)
    AddonsManager.pack(padx=10, pady=20)
    About = tkinter.Button(root, text="About", bd="5", command=about)
    About.pack(side=tkinter.RIGHT, padx=20, pady=10)
    QuitButton = tkinter.Button(root, text="Quit", bd="5", command=Quit)
    QuitButton.pack(side=tkinter.LEFT, pady=10, padx=20)
    root.mainloop()


MainLoop()
