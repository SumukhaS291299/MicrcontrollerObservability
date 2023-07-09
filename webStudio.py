import os
import subprocess

import numpy
import streamlit as st
from pandas import DataFrame


class WebPlot:

    def __init__(self,number:int,port=5000):
        self.number = number
        self.port = port

    def Plot(self,col:int,df:DataFrame,plotList:list):
        TotalCols = int(self.number/col) + 1
        stcolums = []
        for i in range(TotalCols):
            stcolums.append(st.columns(col))
        cur = 0
        colindx = 0
        for i in range(self.number):
            if cur >= col:
                cur = 0
                colindx += 1
            y = df[plotList[i]].tolist()
            y = numpy.array(y)
            with stcolums[colindx][cur]:
                st.line_chart(y)
            cur += 1
        web = subprocess.run(f"streamlit run webStudio.py --server.port {self.port}",shell=True,capture_output=True,text=True)
        print("STDOUT: ",web.stdout)
        print("STDERR: ",web.stderr)


# wp = WebPlot(3)
# df = pandas.read_csv(r"C:\Users\User\PycharmProjects\VechDectCount\venv\Lib\site-packages\sklearn\datasets\data\irisWhat.csv")
# wp.Plot(2,df,["setosa","versicolor","virginica"])
