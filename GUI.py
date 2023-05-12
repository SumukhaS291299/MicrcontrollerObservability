import tkinter
from tkinter.filedialog import askopenfilename

import pandas as pd

from main import PlotCSVData

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
    global HeadEntry, DefaultValueX, DefaultValueY, file
    plotter = PlotCSVData(
        file, str(HeadEntry.get()))
    plot = plotter.ShowSingleGraph(x_plot=str(DefaultValueX.get()), y_plot=str(DefaultValueY.get()))
    plot.show()


def GetMultiGraph():
    # Replace with multi value and df.head
    global MultiGraphfile, HeadEntry_MultiGraph, YPlot_Box
    plotter = PlotCSVData(
        MultiGraphfile, str(HeadEntry_MultiGraph.get()))
    selected_tuple = YPlot_Box.curselection()
    selected = []
    for indx in selected_tuple:
        selected.append(YPlot_Box.get(indx))
    plot = plotter.ShowMultiGraph(selected)
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
    global MultiGraphfile, HeadEntry_MultiGraph, YPlot_Box
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
    DoneButton = tkinter.Button(MultiGraph, text="Done", command=GetMultiGraph)
    DoneButton.pack(side=tkinter.BOTTOM, pady=10)


def GetAnimationGraph():
    # Replace with multi value and df.head
    global GraphAnimationFile, HeadEntry_AnimGraph, PlotBufferEntry, PauseIntervalSelector, YPlot_Box_Anim
    plotter = PlotCSVData(
        GraphAnimationFile, str(HeadEntry_AnimGraph.get()))
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


def Quit():
    exit(0)


def MainLoop():
    global canvas, root
    root = tkinter.Tk()
    root.title("S√PyPlots")
    root.geometry('640x480')
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
    QuitButton = tkinter.Button(root, text="Quit", bd="5", command=Quit)
    QuitButton.pack(side=tkinter.BOTTOM, pady=10)
    root.mainloop()


MainLoop()
