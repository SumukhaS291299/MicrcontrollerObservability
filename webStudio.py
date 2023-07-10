import os
import pickle

import numpy
import pandas
import streamlit as st

df = pandas.DataFrame()
plotList = []
col = 0

def Plot():
    with open("dataframe.txt", "rb") as dfpickle:
        df = pickle.load(dfpickle)
    with open("PLOTS.txt", "rb") as AllPlotsListpickle:
        plotList = pickle.load(AllPlotsListpickle)
    with open("Columns.txt", "rb") as webcols:
        col = pickle.load(webcols)
    number = len(plotList)
    TotalCols = int(number/col) + 1
    stcolums = []
    for i in range(TotalCols):
        stcolums.append(st.columns(col))
    cur = 0
    colindx = 0
    for i in range(number):
        if cur >= col:
            cur = 0
            colindx += 1
        y = df[plotList[i]].tolist()
        y = numpy.array(y)
        with stcolums[colindx][cur]:
            st.line_chart(y)
        cur += 1

Plot()
