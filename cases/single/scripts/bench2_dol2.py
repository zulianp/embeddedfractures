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

if len(argv) < 6:
	print(f'usage: {argv[0]} <input_mesh_flow> <input_mesh_conc> <output_csv_col1> <output_csv_col2 <output_csv_col3>')
	exit()

path_matrix_flow=argv[1]
path_matrix_conc=argv[2]
path_csv_col1=argv[3]
path_csv_col2=argv[4]
path_csv_col3=argv[5]

# create a new 'IOSS Reader'
matrix_flowe = IOSSReader(registrationName='matrix_flow.e', FileName=[path_matrix_flow])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
matrix_floweDisplay = Show(matrix_flowe, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
matrix_floweDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(matrix_floweDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
matrix_floweDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# get opacity transfer function/opacity map for 'vtkBlockColors'
vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

# get 2D transfer function for 'vtkBlockColors'
vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(registrationName='PlotOverLine1', Input=matrix_flowe)

# Properties modified on plotOverLine1
plotOverLine1.Point1 = [0.0, 100.0, 100.0]
plotOverLine1.Point2 = [100.0, 0.0, 0.0]

# show data in view
plotOverLine1Display = Show(plotOverLine1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
plotOverLine1Display.Representation = 'Surface'

# Create a new 'Line Chart View'
lineChartView1 = CreateView('XYChartView')

# show data in view
plotOverLine1Display_1 = Show(plotOverLine1, lineChartView1, 'XYChartRepresentation')

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=lineChartView1, layout=layout1, hint=0)

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesOpacity = ['arc_length', '1', 'ids', '1', 'object_id', '1', 'pressure', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine1Display_1.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'arc_length', '0', 'ids', '0', 'object_id', '0', 'pressure', '0', 'vtkValidPointMask', '0']
plotOverLine1Display_1.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'arc_length', '1', 'ids', '1', 'object_id', '1', 'pressure', '1', 'vtkValidPointMask', '1']
plotOverLine1Display_1.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'arc_length', '2', 'ids', '2', 'object_id', '2', 'pressure', '2', 'vtkValidPointMask', '2']
plotOverLine1Display_1.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'arc_length', '0', 'ids', '0', 'object_id', '0', 'pressure', '0', 'vtkValidPointMask', '0']
plotOverLine1Display_1.SeriesMarkerSize = ['Points_Magnitude', '4', 'Points_X', '4', 'Points_Y', '4', 'Points_Z', '4', 'arc_length', '4', 'ids', '4', 'object_id', '4', 'pressure', '4', 'vtkValidPointMask', '4']

# update the view to ensure updated data information
lineChartView1.Update()

# save data
SaveData(path_csv_col1, proxy=plotOverLine1, ChooseArraysToWrite=1,
    PointDataArrays=['arc_length', 'pressure'],
    AddMetaData=0)

# create a new 'IOSS Reader'
matrix_transporte = IOSSReader(registrationName='matrix_transport.e', FileName=[path_matrix_conc])

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# set active view
SetActiveView(renderView1)

# show data in view
matrix_transporteDisplay = Show(matrix_transporte, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
matrix_transporteDisplay.Representation = 'Surface'

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
lineChartView1.Update()

# set scalar coloring
ColorBy(matrix_transporteDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
matrix_transporteDisplay.SetScalarBarVisibility(renderView1, True)

# hide data in view
Hide(matrix_flowe, renderView1)

animationScene1.GoToLast()

# create a new 'Plot Over Line'
plotOverLine2 = PlotOverLine(registrationName='PlotOverLine2', Input=matrix_transporte)

# Properties modified on plotOverLine2
plotOverLine2.Point1 = [0.0, 100.0, 100.0]
plotOverLine2.Point2 = [100.0, 0.0, 100.0]

# show data in view
plotOverLine2Display = Show(plotOverLine2, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
plotOverLine2Display.Representation = 'Surface'

# Create a new 'Line Chart View'
lineChartView2 = CreateView('XYChartView')

# show data in view
plotOverLine2Display_1 = Show(plotOverLine2, lineChartView2, 'XYChartRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=lineChartView2, layout=layout1, hint=1)

# Properties modified on plotOverLine2Display_1
plotOverLine2Display_1.SeriesOpacity = ['arc_length', '1', 'concentration', '1', 'ids', '1', 'object_id', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine2Display_1.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'arc_length', '0', 'concentration', '0', 'ids', '0', 'object_id', '0', 'vtkValidPointMask', '0']
plotOverLine2Display_1.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'arc_length', '1', 'concentration', '1', 'ids', '1', 'object_id', '1', 'vtkValidPointMask', '1']
plotOverLine2Display_1.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'arc_length', '2', 'concentration', '2', 'ids', '2', 'object_id', '2', 'vtkValidPointMask', '2']
plotOverLine2Display_1.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'arc_length', '0', 'concentration', '0', 'ids', '0', 'object_id', '0', 'vtkValidPointMask', '0']
plotOverLine2Display_1.SeriesMarkerSize = ['Points_Magnitude', '4', 'Points_X', '4', 'Points_Y', '4', 'Points_Z', '4', 'arc_length', '4', 'concentration', '4', 'ids', '4', 'object_id', '4', 'vtkValidPointMask', '4']

# update the view to ensure updated data information
lineChartView1.Update()

# update the view to ensure updated data information
lineChartView2.Update()

# save data
SaveData(path_csv_col2, proxy=plotOverLine2, ChooseArraysToWrite=1,
    PointDataArrays=['concentration'],
    AddMetaData=0)

# set active source
SetActiveSource(matrix_transporte)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=plotOverLine2)

# create a new 'Plot Over Line'
plotOverLine3 = PlotOverLine(registrationName='PlotOverLine3', Input=matrix_transporte)

# set active view
SetActiveView(renderView1)

# Properties modified on plotOverLine3
plotOverLine3.Point1 = [0.0, 100.0, 80.0]
plotOverLine3.Point2 = [100.0, 0.0, 20.0]

# show data in view
plotOverLine3Display = Show(plotOverLine3, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
plotOverLine3Display.Representation = 'Surface'

# Create a new 'Line Chart View'
lineChartView3 = CreateView('XYChartView')

# show data in view
plotOverLine3Display_1 = Show(plotOverLine3, lineChartView3, 'XYChartRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=lineChartView3, layout=layout1, hint=3)

# Properties modified on plotOverLine3Display_1
plotOverLine3Display_1.SeriesOpacity = ['arc_length', '1', 'concentration', '1', 'ids', '1', 'object_id', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine3Display_1.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'arc_length', '0', 'concentration', '0', 'ids', '0', 'object_id', '0', 'vtkValidPointMask', '0']
plotOverLine3Display_1.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'arc_length', '1', 'concentration', '1', 'ids', '1', 'object_id', '1', 'vtkValidPointMask', '1']
plotOverLine3Display_1.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'arc_length', '2', 'concentration', '2', 'ids', '2', 'object_id', '2', 'vtkValidPointMask', '2']
plotOverLine3Display_1.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'arc_length', '0', 'concentration', '0', 'ids', '0', 'object_id', '0', 'vtkValidPointMask', '0']
plotOverLine3Display_1.SeriesMarkerSize = ['Points_Magnitude', '4', 'Points_X', '4', 'Points_Y', '4', 'Points_Z', '4', 'arc_length', '4', 'concentration', '4', 'ids', '4', 'object_id', '4', 'vtkValidPointMask', '4']

# update the view to ensure updated data information
lineChartView1.Update()

# update the view to ensure updated data information
lineChartView2.Update()

# update the view to ensure updated data information
lineChartView3.Update()

# resize frame
layout1.SetSplitFraction(0, 0.7373271889400922)

# save data
SaveData(path_csv_col3, proxy=plotOverLine3, ChooseArraysToWrite=1,
    PointDataArrays=['concentration'],
    AddMetaData=0)

# set active view
SetActiveView(renderView1)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1705, 1256)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [50.0, 50.0, 384.60652149512316]
renderView1.CameraFocalPoint = [50.0, 50.0, 50.0]
renderView1.CameraParallelScale = 86.60254037844386


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