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

if len(argv) < 4:
	print(f'usage: {argv[0]}  <input_mesh> <output_csv1> <output_csv2> ')
	exit()

path_matrix=argv[1]
path_csv1=argv[2]
path_csv2=argv[3]

# create a new 'IOSS Reader'
matrix_transporte = IOSSReader(registrationName='matrix_transport.e', FileName=[path_matrix])

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
matrix_transporteDisplay = Show(matrix_transporte, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
matrix_transporteDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(matrix_transporteDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
matrix_transporteDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# get opacity transfer function/opacity map for 'vtkBlockColors'
vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

# get 2D transfer function for 'vtkBlockColors'
vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')

# Properties modified on matrix_transporte
matrix_transporte.ElementBlocks = ['block_2']

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=matrix_transporte)

# Properties modified on calculator1
calculator1.ResultArrayName = 'porosity33'
calculator1.Function = '0.25'

# show data in view
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'

# hide data in view
Hide(matrix_transporte, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'porosity33'
porosity33LUT = GetColorTransferFunction('porosity33')

# get opacity transfer function/opacity map for 'porosity33'
porosity33PWF = GetOpacityTransferFunction('porosity33')

# get 2D transfer function for 'porosity33'
porosity33TF2D = GetTransferFunction2D('porosity33')

# create a new 'Calculator'
calculator2 = Calculator(registrationName='Calculator2', Input=calculator1)

# Properties modified on calculator2
calculator2.ResultArrayName = 'col2'
calculator2.Function = 'concentration*porosity33'

# show data in view
calculator2Display = Show(calculator2, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator2Display.Representation = 'Surface'

# hide data in view
Hide(calculator1, renderView1)

# show color bar/color legend
calculator2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'col2'
col2LUT = GetColorTransferFunction('col2')

# get opacity transfer function/opacity map for 'col2'
col2PWF = GetOpacityTransferFunction('col2')

# get 2D transfer function for 'col2'
col2TF2D = GetTransferFunction2D('col2')

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=calculator2)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
integrateVariables1Display = Show(integrateVariables1, spreadSheetView1, 'SpreadSheetRepresentation')

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

# update the view to ensure updated data information
spreadSheetView1.Update()

# create a new 'Plot Data Over Time'
plotDataOverTime1 = PlotDataOverTime(registrationName='PlotDataOverTime1', Input=integrateVariables1)

# set active source
SetActiveSource(plotDataOverTime1)

# show data in view
plotDataOverTime1Display = Show(plotDataOverTime1, spreadSheetView1, 'SpreadSheetRepresentation')

# Create a new 'Quartile Chart View'
quartileChartView1 = CreateView('QuartileChartView')

# show data in view
plotDataOverTime1Display_1 = Show(plotDataOverTime1, quartileChartView1, 'QuartileChartRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=quartileChartView1, layout=layout1, hint=2)

# Properties modified on plotDataOverTime1Display_1
plotDataOverTime1Display_1.SeriesOpacity = ['col2 (stats)', '1', 'concentration (stats)', '1', 'porosity33 (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display_1.SeriesPlotCorner = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'col2 (stats)', '0', 'concentration (stats)', '0', 'porosity33 (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display_1.SeriesLineStyle = ['N (stats)', '1', 'Time (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'col2 (stats)', '1', 'concentration (stats)', '1', 'porosity33 (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display_1.SeriesLineThickness = ['N (stats)', '2', 'Time (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'col2 (stats)', '2', 'concentration (stats)', '2', 'porosity33 (stats)', '2', 'vtkValidPointMask (stats)', '2']
plotDataOverTime1Display_1.SeriesMarkerStyle = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'col2 (stats)', '0', 'concentration (stats)', '0', 'porosity33 (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display_1.SeriesMarkerSize = ['N (stats)', '4', 'Time (stats)', '4', 'X (stats)', '4', 'Y (stats)', '4', 'Z (stats)', '4', 'col2 (stats)', '4', 'concentration (stats)', '4', 'porosity33 (stats)', '4', 'vtkValidPointMask (stats)', '4']

# update the view to ensure updated data information
quartileChartView1.Update()

# Properties modified on plotDataOverTime1Display_1
plotDataOverTime1Display_1.SeriesVisibility = ['col2 (stats)', 'porosity33 (stats)']

# Properties modified on plotDataOverTime1Display_1
plotDataOverTime1Display_1.SeriesVisibility = ['col2 (stats)']

# set active source
SetActiveSource(plotDataOverTime1)

# create a new 'IOSS Reader'
matrix_transporte_1 = IOSSReader(registrationName='matrix_transport.e', FileName=[path_matrix])

# set active view
SetActiveView(renderView1)

# set active source
SetActiveSource(matrix_transporte_1)

# show data in view
matrix_transporte_1Display = Show(matrix_transporte_1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
matrix_transporte_1Display.Representation = 'Surface'

# hide data in view
Hide(matrix_transporte_1, renderView1)

# split cell
layout1.SplitVertical(1, 0.5)

# set active view
SetActiveView(None)

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.AxesGrid = 'Grid Axes 3D Actor'
renderView2.StereoType = 'Crystal Eyes'
renderView2.CameraFocalDisk = 1.0
renderView2.LegendGrid = 'Legend Grid Actor'
renderView2.BackEnd = 'OSPRay raycaster'
renderView2.OSPRayMaterialLibrary = materialLibrary1

# show data in view
matrix_transporte_1Display_1 = Show(matrix_transporte_1, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
matrix_transporte_1Display_1.Representation = 'Surface'

# add view to a layout so it's visible in UI
AssignViewToLayout(view=renderView2, layout=layout1, hint=4)

# reset view to fit data
renderView2.ResetCamera(False, 0.9)

# set active source
SetActiveSource(matrix_transporte_1)

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=matrix_transporte_1)

# set active source
SetActiveSource(matrix_transporte_1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# change representation type
matrix_transporte_1Display_1.SetRepresentationType('Outline')

# set active source
SetActiveSource(slice1)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice1.SliceType)

# show data in view
slice1Display = Show(slice1, renderView2, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'

# set active source
SetActiveSource(matrix_transporte_1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# set scalar coloring
ColorBy(matrix_transporte_1Display_1, ('POINTS', 'concentration'))

# rescale color and/or opacity maps used to include current data range
matrix_transporte_1Display_1.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
matrix_transporte_1Display_1.SetScalarBarVisibility(renderView2, True)

# get color transfer function/color map for 'concentration'
concentrationLUT = GetColorTransferFunction('concentration')

# get opacity transfer function/opacity map for 'concentration'
concentrationPWF = GetOpacityTransferFunction('concentration')

# get 2D transfer function for 'concentration'
concentrationTF2D = GetTransferFunction2D('concentration')

# change representation type
matrix_transporte_1Display_1.SetRepresentationType('Surface')

# set active source
SetActiveSource(slice1)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice1.SliceType)

# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [60.0, 0.0, 100.0]

# show data in view
slice1Display = Show(slice1, renderView2, 'GeometryRepresentation')

# hide data in view
Hide(matrix_transporte_1, renderView2)

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Calculator'
calculator3 = Calculator(registrationName='Calculator3', Input=slice1)

# Properties modified on calculator3
calculator3.ResultArrayName = 'frac_thikness'
calculator3.Function = '1e-2'

# show data in view
calculator3Display = Show(calculator3, renderView2, 'GeometryRepresentation')

# trace defaults for the display properties.
calculator3Display.Representation = 'Surface'

# hide data in view
Hide(slice1, renderView2)

# show color bar/color legend
calculator3Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# get color transfer function/color map for 'frac_thikness'
frac_thiknessLUT = GetColorTransferFunction('frac_thikness')

# get opacity transfer function/opacity map for 'frac_thikness'
frac_thiknessPWF = GetOpacityTransferFunction('frac_thikness')

# get 2D transfer function for 'frac_thikness'
frac_thiknessTF2D = GetTransferFunction2D('frac_thikness')

# create a new 'Calculator'
calculator4 = Calculator(registrationName='Calculator4', Input=calculator3)

# Properties modified on calculator4
calculator4.ResultArrayName = 'col2'
calculator4.Function = 'frac_thikness*concentration'

# show data in view
calculator4Display = Show(calculator4, renderView2, 'GeometryRepresentation')

# trace defaults for the display properties.
calculator4Display.Representation = 'Surface'

# hide data in view
Hide(calculator3, renderView2)

# show color bar/color legend
calculator4Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Integrate Variables'
integrateVariables2 = IntegrateVariables(registrationName='IntegrateVariables2', Input=calculator4)

# Create a new 'SpreadSheet View'
spreadSheetView2 = CreateView('SpreadSheetView')
spreadSheetView2.ColumnToSort = ''
spreadSheetView2.BlockSize = 1024

# show data in view
integrateVariables2Display = Show(integrateVariables2, spreadSheetView2, 'SpreadSheetRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView2, layout=layout1, hint=4)

# update the view to ensure updated data information
spreadSheetView1.Update()

# update the view to ensure updated data information
quartileChartView1.Update()

# update the view to ensure updated data information
spreadSheetView2.Update()

# set active view
SetActiveView(spreadSheetView1)

# destroy spreadSheetView1
Delete(spreadSheetView1)
del spreadSheetView1

# close an empty frame
layout1.Collapse(5)

# set active view
SetActiveView(quartileChartView1)

# set active view
SetActiveView(renderView1)

# destroy renderView1
Delete(renderView1)
del renderView1

# close an empty frame
layout1.Collapse(3)

# resize frame
layout1.SetSplitFraction(0, 0.6790490341753344)

# create a new 'Plot Data Over Time'
plotDataOverTime2 = PlotDataOverTime(registrationName='PlotDataOverTime2', Input=integrateVariables2)

# Create a new 'Quartile Chart View'
quartileChartView2 = CreateView('QuartileChartView')

# show data in view
plotDataOverTime2Display = Show(plotDataOverTime2, quartileChartView2, 'QuartileChartRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=quartileChartView2, layout=layout1, hint=0)

# Properties modified on plotDataOverTime2Display
plotDataOverTime2Display.SeriesOpacity = ['col2 (stats)', '1', 'concentration (stats)', '1', 'frac_thikness (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime2Display.SeriesPlotCorner = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'col2 (stats)', '0', 'concentration (stats)', '0', 'frac_thikness (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime2Display.SeriesLineStyle = ['N (stats)', '1', 'Time (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'col2 (stats)', '1', 'concentration (stats)', '1', 'frac_thikness (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime2Display.SeriesLineThickness = ['N (stats)', '2', 'Time (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'col2 (stats)', '2', 'concentration (stats)', '2', 'frac_thikness (stats)', '2', 'vtkValidPointMask (stats)', '2']
plotDataOverTime2Display.SeriesMarkerStyle = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'col2 (stats)', '0', 'concentration (stats)', '0', 'frac_thikness (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime2Display.SeriesMarkerSize = ['N (stats)', '4', 'Time (stats)', '4', 'X (stats)', '4', 'Y (stats)', '4', 'Z (stats)', '4', 'col2 (stats)', '4', 'concentration (stats)', '4', 'frac_thikness (stats)', '4', 'vtkValidPointMask (stats)', '4']

# update the view to ensure updated data information
quartileChartView1.Update()

# update the view to ensure updated data information
spreadSheetView2.Update()

# update the view to ensure updated data information
quartileChartView2.Update()

# resize frame
layout1.SetSplitFraction(1, 0.865934065934066)

# Properties modified on plotDataOverTime2Display
plotDataOverTime2Display.SeriesVisibility = ['col2 (stats)', 'frac_thikness (stats)']

# Properties modified on plotDataOverTime2Display
plotDataOverTime2Display.SeriesVisibility = ['col2 (stats)']

# set active source
SetActiveSource(integrateVariables2)

# set active source
SetActiveSource(calculator4)

# Properties modified on calculator4
calculator4.ResultArrayName = 'col3'

# update the view to ensure updated data information
quartileChartView1.Update()

# update the view to ensure updated data information
renderView2.Update()

# update the view to ensure updated data information
spreadSheetView2.Update()

# update the view to ensure updated data information
quartileChartView2.Update()

# set active source
SetActiveSource(plotDataOverTime2)

# save data
SaveData(path_csv1, proxy=plotDataOverTime2, WriteTimeSteps=1,
    ChooseArraysToWrite=1,
    RowDataArrays=['Time','avg(col3)'],
    FieldAssociation='Row Data',
    AddMetaData=0)

# set active source
SetActiveSource(plotDataOverTime1)

# save data
SaveData(path_csv2, proxy=plotDataOverTime1, WriteTimeSteps=1,
    ChooseArraysToWrite=1,
    RowDataArrays=['Time','avg(col2)'],
    FieldAssociation='Row Data')

# set active source
SetActiveSource(calculator4)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1511, 1244)

#-----------------------------------
# saving camera placements for views



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