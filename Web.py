import threading
import time

from flask import Flask, render_template

app = Flask(__name__)

XRead = None
YRead = None
X = None
Y = None

event = threading.Event()


def CheckFileChanges():
    print("Started Looking for changes...")
    while True:
        global XRead, YRead
        with open("Web.txt", "r") as readF:
            lines = readF.readlines()
        for line in lines:
            line = line.replace("\n", "")
            if "X:" in line:
                XRead = line[2:]
            if "Y:" in line:
                YRead = line[3:]
        if X == XRead and Y == YRead:
            print("No change found...")
        else:
            print("Change Found")
            event.set()
        time.sleep(2)


@app.route("/")
def plotData():
    return render_template("plot.html", xList=X, yjson=Y)


def UpdateValues():
    print("Waiting for trigger")
    event.wait(120)
    print("Updating Server about changes..")
    global X, Y
    with open("web.txt", "r") as r:
        lines = r.readlines()
    # print(lines)
    for line in lines:
        line = line.replace("\n", "")
        if "X:" in line:
            X = line[2:]
        if "Y:" in line:
            Y = line[3:]
        # print("X", X)
        # print("Y", Y)


def PerformChanges():
    while True:
        print("Changes Found ?", event.is_set())
        if event.is_set():
            print("Event was set")
            UpdateValues()
            print(X, XRead)
            event.clear()
        time.sleep(10)


def run():
    app.run(host="0.0.0.0", port=8080, debug=False)


if __name__ == "__main__":
    Check = threading.Thread(target=CheckFileChanges)
    Check.start()
    fileC = threading.Thread(target=PerformChanges)
    fileC.start()
    run()
