# trace generated using paraview version 5.12.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 12
import sys
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

argv=sys.argv

if len(argv) < 3:
	print(f'usage: {argv[0]}  <input_mesh> <output_csv1>')
	exit()

path_matrix=argv[1]
path_csv1=argv[2]

# create a new 'IOSS Reader'
matrix_transporte = IOSSReader(registrationName='matrix_transport.e', FileName=[path_matrix])

# get active view
renderView2 = GetActiveViewOrCreate('RenderView')

# get display properties
matrix_transporteDisplay = GetDisplayProperties(matrix_transporte, view=renderView2)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# get opacity transfer function/opacity map for 'vtkBlockColors'
vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

# get 2D transfer function for 'vtkBlockColors'
vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on matrix_transporte
matrix_transporte.ElementBlocks = ['block_2']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.ElementBlocks = ['block_1', 'block_2']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.SideSets = ['surface_1']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.SideSets = ['surface_1', 'surface_2']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.ElementBlocks = ['block_2']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.ElementBlocks = ['block_1', 'block_2']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.ElementBlocks = ['block_2']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.SideSets = ['surface_2']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.SideSets = ['surface_1', 'surface_2']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.SideSets = ['surface_1']

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on matrix_transporte
matrix_transporte.ElementBlocks = []

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=matrix_transporte)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
integrateVariables1Display = Show(integrateVariables1, spreadSheetView1, 'SpreadSheetRepresentation')

# add view to a layout so it's visible in UI

# find view
spreadSheetView2 = FindViewOrCreate('SpreadSheetView2', viewtype='SpreadSheetView')

# update the view to ensure updated data information
spreadSheetView2.Update()

# update the view to ensure updated data information
spreadSheetView1.Update()

# create a new 'Plot Data Over Time'
plotDataOverTime1 = PlotDataOverTime(registrationName='PlotDataOverTime1', Input=integrateVariables1)

# Create a new 'Quartile Chart View'
quartileChartView1 = CreateView('QuartileChartView')

# show data in view
plotDataOverTime1Display = Show(plotDataOverTime1, quartileChartView1, 'QuartileChartRepresentation')

# add view to a layout so it's visible in UI

# Properties modified on plotDataOverTime1Display
plotDataOverTime1Display.SeriesOpacity = ['concentration (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display.SeriesPlotCorner = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display.SeriesLineStyle = ['N (stats)', '1', 'Time (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'concentration (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display.SeriesLineThickness = ['N (stats)', '2', 'Time (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'concentration (stats)', '2', 'vtkValidPointMask (stats)', '2']
plotDataOverTime1Display.SeriesMarkerStyle = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display.SeriesMarkerSize = ['N (stats)', '4', 'Time (stats)', '4', 'X (stats)', '4', 'Y (stats)', '4', 'Z (stats)', '4', 'concentration (stats)', '4', 'vtkValidPointMask (stats)', '4']

# update the view to ensure updated data information
spreadSheetView2.Update()

# set active view
SetActiveView(spreadSheetView2)

# destroy spreadSheetView2
Delete(spreadSheetView2)
del spreadSheetView2

# close an empty frame

# find view
renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

# set active view
SetActiveView(renderView1)

# destroy renderView1
Delete(renderView1)
del renderView1

# close an empty frame

# save data
SaveData(path_csv1, proxy=plotDataOverTime1, WriteTimeSteps=1,
    ChooseArraysToWrite=1,
    RowDataArrays=['Time', 'avg(concentration)'],
    FieldAssociation='Row Data',
    AddMetaData=0)

# set active view
SetActiveView(renderView2)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView2
renderView2.CameraPosition = [321.34265927538445, 193.1296082906069, 183.59865536376844]
renderView2.CameraFocalPoint = [50.0, 50.0, 50.0]
renderView2.CameraViewUp = [-0.32550076596440325, 0.8967971070373966, -0.29967348926113485]
renderView2.CameraParallelScale = 86.60254037844386


##--------------------------------------------
## You may need to add some code at the end of this python script depending on your usage, eg:
#
## Render all views to see them appears
# RenderAllViews()
#
## Interact with the view, usefull when running from pvpython
# Interact()
#
## Save a screenshot of the active view
# SaveScreenshot("path/to/screenshot.png")
#
## Save a screenshot of a layout (multiple splitted view)
# SaveScreenshot("path/to/screenshot.png", GetLayout())
#
## Save all "Extractors" from the pipeline browser
# SaveExtracts()
#
## Save a animation of the current active view
# SaveAnimation()
#
## Please refer to the documentation of paraview.simple
## https://kitware.github.io/paraview-docs/latest/python/paraview.simple.html
##--------------------------------------------