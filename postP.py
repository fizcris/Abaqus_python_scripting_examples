 # coding=utf-8
from abaqus import *
from abaqusConstants import *
import os

import displayGroupOdbToolset as dgo

if 'JobName' not in locals():
    JobName = 'Probeta_2'


jobFileName = 'C:/temp/{}.odb'.format(JobName)
resultsFileName = "{}.csv".format(JobName)


#Open results file
o1 = session.openOdb(name=jobFileName)
session.viewports['Viewport: 1'].setValues(displayedObject=o1)

# Create viewport session
session.viewports['Viewport: 1'].setValues(
    displayedObject=session.mdbData['Model-1'])
##################      Filter Nodes         ##################
leaf = dgo.LeafFromNodeSets(nodeSets=('PART-1-1.GALGA', ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
#: Warning: Display groups containing only nodes are not supported in contour plot mode. Select a different plot mode and activate node symbols and/or labels to see the selected nodes.
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    UNDEFORMED, ))

#################      Create results.csv         ##################
session.viewports['Viewport: 1'].makeCurrent()


session.fieldReportOptions.setValues(reportFormat=COMMA_SEPARATED_VALUES)
session.writeFieldReport(fileName=resultsFileName, append=OFF,
    sortItem='Node Label', odb=o1, step=0, frame=1, outputPosition=NODAL,
    variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), ), ('LAYER_1',
    TOP)), ), stepFrame=SPECIFY)

##################      Extract Media from .csv        ##################
import csv
sumatorio =0.0
puntos=0.0

with open(resultsFileName,'rt')as f:
    #Sikp header
    data = csv.reader(f)
    next(data)
    for row in data:
        sumatorio += float(row[-1])
        puntos +=1

tensionMediaS11 = (sumatorio/puntos)
numNodos = len (part1.nodes)
numElementos = len (part1.elements)

resultado = {"name": JobName, "#Nodos": numNodos,
            "#elementos":numElementos,  "tensionMediaS11": tensionMediaS11,}
print resultado