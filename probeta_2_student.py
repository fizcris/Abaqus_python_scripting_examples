from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from regionToolset import *
from visualization import *
from connectorBehavior import *
import time

##################      Helper garbage colect. funct.         ##################
JobName = 'Probeta_2'
# Clear problematic files
if os.path.isfile(JobName + '.lck') == True:
    os.remove(JobName + '.lck')
# os.remove(JobName+'.023')

##################      Create Model         ##################
mdb.models['Model-1'].Material(name='Acero')
mdb.models['Model-1'].materials['Acero'].Elastic(table=((211000.0, 0.33),))

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
                        offsetField='', offsetType=TOP_SURFACE, region=Region(
        faces=part1.faces.getSequenceFromMask(
            mask=('[#3ff ]',), )), sectionName='Section-1', thicknessAssignment=
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
for i in range(9):
    x = 11.0 + i * 20.0
    # Create partition plane
    part1.DatumPlaneByPrincipalPlane(offset=x, principalPlane=YZPLANE)
    if i == 0 or i == 1 or i == 9: continue;
    part1.PartitionFaceByDatumPlane(datumPlane=part1.datums[part1.datums.items()[-1][0]], faces=part1.faces)

# for i in range(9):
# x = 21 + i * 20.0
# # Create partition plane
# part1.DatumPlaneByPrincipalPlane(offset=x, principalPlane=YZPLANE)
# if i == 1 or i==3 or i==5 or i==7:  continue;
# part1.PartitionFaceByDatumPlane(datumPlane=part1.datums[part1.datums.items()[-1][0]], faces=part1.faces)

# Create partition plane in y
for i in range(6):
    y = 9.5 + i * 10.0
    # Create partition plane
    part1.DatumPlaneByPrincipalPlane(offset=y, principalPlane=XZPLANE)
    if i == 0 or i == 2 or i == 4 or i == 6:  continue;
    part1.PartitionFaceByDatumPlane(datumPlane=part1.datums[part1.datums.items()[-1][0]], faces=part1.faces)

######### Partition for BC
# Create partition plane
part1.DatumPlaneByPrincipalPlane(offset=34.0, principalPlane=YZPLANE)
part1.PartitionFaceByDatumPlane(datumPlane=part1.datums[part1.datums.items()[-1][0]], faces=part1.faces)

#########  Mesh

part1.seedPart(deviationFactor=0.14, minSizeFactor=0.13, size=14.0)
part1.setMeshControls(algorithm=MEDIAL_AXIS, regions=part1.faces)
part1.setMeshControls(elemShape=QUAD, regions=part1.faces, algorithm=ADVANCING_FRONT
                      , allowMapped=True)
mdb.models['Model-1'].parts['Part-1'].generateMesh()

##################      Create BC          ##################
mdb.models['Model-1'].EncastreBC(createStepName='Initial', localCsys=None,
                                 name='BC-1', region=Region(
        faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.getSequenceFromMask(
            mask=('[#800000b ]',), ),
        edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
            mask=('[#13004c71 #0:4 #60000000 #2 ]',), ),
        vertices=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.getSequenceFromMask(
            mask=('[#a01461 #0:3 #280000 ]',), )))

##################      Create Load  Step         ##################
mdb.models['Model-1'].StaticStep(description='Aplicacion presion', name='Step-1',
                                 previous='Initial')

##################      Create Load          ##################
fuerza = 14.86  # N
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1',
                               distributionType=UNIFORM, field='', magnitude=fuerza / ((pi) * ((15 ** 2) - (8 ** 2))),
                               name='Load-1', region=
                               Region(
                                   side1Faces=mdb.models['Model-1'].rootAssembly.instances[
                                       'Part-1-1'].faces.getSequenceFromMask(
                                       mask=('[#80000 #80 ]',), )))

##################      Create Job/s          ##################
# Check student
numNodes = len(part1.nodes);
if numNodes > 1000:
    print("Number of nodes ({}) must be below 1000 for student version".format(numNodes))
else:
    ######### Job 1
    mdb.Job(atTime=None, contactPrint=OFF, description='Simulacion-1', echoPrint=
    OFF, explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF
            , memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, name=
            'Job-1', nodalOutputPrecision=SINGLE, queue=None, resultsFormat=ODB,
            scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)

    # Submit Job 1
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)

    mdb.models['Model-1'].parts['Part-1'].RemoveFaces(deleteCells=False, faceList=
    mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(mask=(
        '[#800000b ]',), ))