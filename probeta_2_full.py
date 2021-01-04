 # coding=utf-8
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
import mesh
from job import *
from sketch import *
from regionToolset import *
from visualization import *
from connectorBehavior import *
import  regionToolset
import time

##################      Helper garbage colect. funct.         ##################
if 'JobName' not in locals():
    JobName = 'Probeta_2'
# Clear problematic files
if os.path.isfile(JobName + '.lck') == True:
    os.remove(JobName + '.lck')
# os.remove(JobName+'.023')

##################      Create Material         ##################
if 'mYoung' not in locals():
    mYoung = 211000.0
if 'mPoiss' not in locals():
    mPoiss = 0.33

mdb.models['Model-1'].Material(name='Acero')
mdb.models['Model-1'].materials['Acero'].Elastic(table=((mYoung, mPoiss),))

##################      Create Model         ##################
# Define base measures [In mm]
height = 80.0
width = 200.0


# Custom function to create circles by diameter
def CircleByDiameter(x, y, d):
    return mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(x, y),
                                                                                 point1=(x + (d / 2.0), y))


# Create constrained sketch
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)

# Create rectangle
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0, 0),
                                                        point2=(width, height))
# Create set 1 of holes
for i in range(3):
    y = (i + 1) * 20.0;
    CircleByDiameter(31.0, y, 5.0)
    CircleByDiameter(31.0 + 40, y, 5.0)
    CircleByDiameter(31.0 + 40 * 2, y, 5.0)
    CircleByDiameter(31.0 + 40.0 * 3.0, y, 5.0)
    if y == 40.0: continue;
    CircleByDiameter(31.0 + 40.0 * 4.0, y, 5.0)

# Create force hole
CircleByDiameter(190.5, 40.0, 8.0)

# Create set 2 of holes
for i in range(4):
    y = 9.5 + (i) * 20.0;
    CircleByDiameter(11.0, y, 5.0)
    CircleByDiameter(11.0 + 40.0, y, 5.0)
    CircleByDiameter(11.0 + 40.0 * 2.0, y, 5.0)
    CircleByDiameter(11.0 + 40.0 * 3.0, y, 5.0)
    CircleByDiameter(11.0 + 40.0 * 4.0, y, 5.0)

##################      Create Part         ##################
part1 = mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
DEFORMABLE_BODY)

# Assign sketch to part
part1.BaseShell(sketch=mdb.models['Model-1'].sketches['__profile__'])

##################      Create Assembly         ##################
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', part=part1)
mdb.models['Model-1'].rootAssembly.regenerate()

##################      Create Section         ##################
mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION,
                                              integrationRule=SIMPSON, material='Acero', name='Section-1',
                                              nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT,
                                              preIntegrate=OFF, temperature=GRADIENT, thickness=2.0, thicknessField='',
                                              thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
# Assign section
part1.SectionAssignment(offset=0.0,
                        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        faces=part1.faces), sectionName='Section-1', thicknessAssignment=
                        FROM_SECTION)

##################      Mesh         ##################
######### Partition Load
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=10.77, name='__profile__',
                                        sheetSize=430.81,
                                        transform=part1.MakeSketchTransform(sketchPlane=part1.faces[0],
                                                                            sketchPlaneSide=SIDE1,
                                                                            sketchOrientation=RIGHT,
                                                                            origin=(0.0, 0.0, 0.0)))
part1.projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
CircleByDiameter(190.5, 40.0, 15.0)
part1.PartitionFaceBySketch(faces=part1.faces, sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
######### Partition Load Cell Sensor
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=10.77, name='__profile__',
                                        sheetSize=430.81,
                                        transform=part1.MakeSketchTransform(sketchPlane=part1.faces[0],
                                                                            sketchPlaneSide=SIDE1,
                                                                            sketchOrientation=RIGHT,
                                                                            origin=(0.0, 0.0, 0.0)))
part1.projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].rectangle(
    point1=(111 - 1.5, 40 - 2.5 - ((3.0 - 1.6) / 2.0) - 1.6),
    point2=(111 + 1.5, 40 - 2.5 - (3.0 - 1.6) / 2.0))
part1.PartitionFaceBySketch(faces=part1.faces, sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

######### Partitions for mesh
# Create partition plane in x
for i in range(10):
    x = 11.0 + i * 20.0
    # Create partition plane
    part1.DatumPlaneByPrincipalPlane(offset=x, principalPlane=YZPLANE)
    if i == 1: continue;
    part1.PartitionFaceByDatumPlane(datumPlane=part1.datums[part1.datums.items()[-1][0]], faces=part1.faces)

for i in range(9):
    x = 21 + i * 20.0
    # Create partition plane
    part1.DatumPlaneByPrincipalPlane(offset=x, principalPlane=YZPLANE)
    # if i == 1:  continue;
    part1.PartitionFaceByDatumPlane(datumPlane=part1.datums[part1.datums.items()[-1][0]], faces=part1.faces)

# Create partition plane in y
for i in range(7):
    y = 9.5 + i * 10.0
    # Create partition plane
    part1.DatumPlaneByPrincipalPlane(offset=y, principalPlane=XZPLANE)
    # if i == 0 or i == 2 or i == 4 or i == 6:  continue;
    part1.PartitionFaceByDatumPlane(datumPlane=part1.datums[part1.datums.items()[-1][0]], faces=part1.faces)

######### Partition for BC
# Create partition plane
part1.DatumPlaneByPrincipalPlane(offset=34.0, principalPlane=YZPLANE)
part1.PartitionFaceByDatumPlane(datumPlane=part1.datums[part1.datums.items()[-1][0]], faces=part1.faces)

#########  Mesh
if 'elemSize' not in locals():
    elemSize = 1
if 'deviationFactor' not in locals():
    deviationFactor = 0.08
part1.seedPart(deviationFactor=deviationFactor, minSizeFactor=0.05, size=elemSize)
part1.setMeshControls(elemShape=QUAD, regions=part1.faces, algorithm=mesh.MEDIAL_AXIS,
                      allowMapped=True)
#########  Set element type
elemType1 = mesh.ElemType(elemCode=mesh.S4R, elemLibrary=STANDARD,
    secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=mesh.S3, elemLibrary=STANDARD)


pickedRegions =(part1.faces, )
part1.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
part1.generateMesh()

##################      Create BC          ##################
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=(
    '[#800048bf #120001 #2400006 #600 #c05000 #4 ]', ), )
e1 = a.instances['Part-1-1'].edges
edges1 = e1.getSequenceFromMask(mask=(
    '[#1c771dce #81f0001c #3 #0 #7e #7800000 #3',
    ' #3f00 #0 #3078000 #0 #3f8000 #0:2 #3ee0000', ' #e0000 #3 ]', ), )
v1 = a.instances['Part-1-1'].vertices
verts1 = v1.getSequenceFromMask(mask=(
    '[#43162cc #21f00 #0 #f #f0000007 #0 #e00', ' #3e0000 #0 #3f00 ]', ), )
region = regionToolset.Region(vertices=verts1, edges=edges1, faces=faces1)
mdb.models['Model-1'].EncastreBC(name='BC-2', createStepName='Initial',
    region=region, localCsys=None)

##################      Create Load  Step         ##################
mdb.models['Model-1'].StaticStep(description='Aplicacion presion', name='Step-1',
                                 previous='Initial')

##################      Create Load          ##################
  # N
##################      Helper garbage colect. funct.         ##################
if 'fuerza' not in locals():
    fuerza = 14.86

mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1',
                               distributionType=UNIFORM, field='',
                               magnitude=fuerza / ((pi) * (((15.0 / 2.0) ** 2) - ((8.0 / 2.0) ** 2))),
                               name='Load-1', region=
                               Region(
                                   side1Faces=mdb.models['Model-1'].rootAssembly.instances[
                                       'Part-1-1'].faces.getSequenceFromMask(
                                       mask=('[#0:2 #180000 #0 #1000000 #20 ]',), )))

##################      Data extraction        ##################
#########  Create Set for Load cell
part1.Set(faces=part1.faces.getSequenceFromMask(mask=('[#0:4 #20000000 #10 ]', ),),
          name='Galga')


#########  Create Field Output Request
mdb.models['Model-1'].FieldOutputRequest(createStepName='Step-1',
                                        name='F-Output-2', rebar=EXCLUDE,
                                        region=mdb.models['Model-1'].rootAssembly.allInstances['Part-1-1'].sets['Galga'],
                                        sectionPoints=DEFAULT, variables=('S', 'E'))
##################      Create Job/s          ##################
# Check student
numNodes = len(part1.nodes);

######### Job 1
mdb.Job(atTime=None, contactPrint=OFF, description=JobName, echoPrint=
OFF, explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF
        , memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, name=
        JobName, nodalOutputPrecision=SINGLE, queue=None, resultsFormat=ODB,
        scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)

# Submit Job 1
mdb.jobs[JobName].submit(consistencyChecking=OFF)
mdb.jobs[JobName].waitForCompletion()