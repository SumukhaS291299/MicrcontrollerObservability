from main import PlotCSVData

plotter = PlotCSVData(
    r"C:\Users\User\PycharmProjects\VechDectCount\venv\Lib\site-packages\sklearn\datasets\data\iris.csv", "Iris")
# plotter1 = PlotCSVData(
#     r"D:\DataVisualiser\venv\Lib\site-packages\matplotlib\mpl-data\sample_data\percent_bachelors_degrees_women_usa.csv",
#     "new")

# plot = plotter.ShowSingleGraph(x_plot="auto", y_plot="setosa")
# plot = plotter.ShowSingleGraph(x_plot="auto", y_plot="versicolor")
# plot = plotter.ShowSingleGraph(x_plot="auto", y_plot="virginica")
# plot = plotter1.ShowSingleGraph(x_plot="auto", y_plot="Year")
# plot = plotter1.ShowSingleGraph(x_plot="auto", y_plot="Agriculture")
# 
# plot.show()

# plot = ShowSingleGraph(
#     r"C:\Users\User\PycharmProjects\VechDectCount\venv\Lib\site-packages\sklearn\datasets\data\iris.csv",
#     "auto", "setosa", "IRIS")
# plot.show()
# plot = plotter.ShowMultiGraph(
#     ["setosa", "versicolor", "virginica"])
# plot = plotter1.ShowMultiGraph(
#     ["Year", "Agriculture", "Architecture", "Art and Performance", "Biology"])
# plot.show()
# plot = ShowSingleGraph(
#     r"C:\Users\User\PycharmProjects\VechDectCount\venv\Lib\site-packages\sklearn\datasets\data\iris.csv",
#     "auto", "versicolor", "IRIS")
# plot = ShowSingleGraph(
#     r"C:\Users\User\PycharmProjects\VechDectCount\venv\Lib\site-packages\sklearn\datasets\data\iris.csv",
#     "auto", "virginica", "IRIS")
# plot = ShowAnimatedGraph(
#     r"C:\Users\User\PycharmProjects\VechDectCount\venv\Lib\site-packages\sklearn\datasets\data\iris.csv",
#     ["virginica", "setosa", "versicolor"],
#     "IRIS")
# plot = ShowAnimatedGraph(
#     r"D:\DataVisualiser\venv\Lib\site-packages\matplotlib\mpl-data\sample_data\percent_bachelors_degrees_women_usa.csv",
#     ["Year", "Agriculture", "Architecture", "Art and Performance", "Biology", "Business",
#      "Communications and Journalism", "Computer Science", "Education", "Engineering", "English", "Foreign Languages",
#      "Health Professions", "Math and Statistics", "Physical Sciences", "Psychology", "Public Administration"],
#     "Data")
# plot = ShowMultiGraph(r"D:\DataVisualiser\venv\Lib\site-packages\matplotlib\mpl-data\sample_data\msft.csv",
#                       ["Open", "High", "Low", "Close"], "Data")
# plot.show()
plotter.ShowAnimatedGraph(["setosa", "versicolor", "virginica"], pauseInterval=plotter.SLOW)
# plotter1.ShowAnimatedGraph(["Year", "Agriculture", "Architecture", "Art and Performance", "Biology"],
#                            pauseInterval=plotter.MID)
# D:\DataVisualiser\venv\Lib\site-packages\matplotlib\mpl-data\sample_data\msft.csv
# D:\DataVisualiser\venv\Lib\site-packages\matplotlib\mpl-data\sample_data\percent_bachelors_degrees_women_usa.csv
# plot.show()
