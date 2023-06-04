from flask import Flask, render_template

app = Flask(__name__)

X = None
Y = None


@app.route("/")
def plotData():
    return render_template("plot.html", xList=X, yjson=Y)


def StartServer():
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
        print("X", X)
        print("Y", Y)


def run():
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    StartServer()
    run()
