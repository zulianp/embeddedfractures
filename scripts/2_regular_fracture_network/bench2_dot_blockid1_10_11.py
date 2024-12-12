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

if len(argv) < 5:
	print(f'usage: {argv[0]}  <input_mesh> <output_csv> <output_csv> <output_csv> ')
	exit()

path_matrix=argv[1]
path_csv1=argv[2]
path_csv2=argv[3] #/IOSS/element_blocks/block_1
path_csv3=argv[4]

matrix_transporte = IOSSReader(registrationName='matrix_transport.e', FileName=[path_matrix])

# get active view
renderView2 = GetActiveViewOrCreate('RenderView')

# get the material library
materialLibrary1 = GetMaterialLibrary()

# get display properties
matrix_transporteDisplay = GetDisplayProperties(matrix_transporte, view=renderView2)

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

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=matrix_transporte)

# show data in view
clip1Display = Show(clip1, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display.Representation = 'Surface'

# hide data in view
Hide(matrix_transporte, renderView2)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip2.ClipType
clip1.ClipType.Normal = [-1.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip2 = Clip(registrationName='Clip2', Input=clip1)

# show data in view
clip2Display = Show(clip2, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip2Display.Representation = 'Surface'

# hide data in view
Hide(clip1, renderView2)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip2.ClipType
clip2.ClipType.Normal = [0.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip2.ClipType
clip2.ClipType.Normal = [0.0, 1.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip3 = Clip(registrationName='Clip3', Input=clip2)

# show data in view
clip3Display = Show(clip3, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip3Display.Representation = 'Surface'

# hide data in view
Hide(clip2, renderView2)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip3.ClipType
clip3.ClipType.Normal = [1.0, 0.0, 1.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip3.ClipType
clip3.ClipType.Normal = [0.0, 0.0, 1.0]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=clip3)

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

# set active view
SetActiveView(renderView2)

# set active source
SetActiveSource(matrix_transporte)

# update the view to ensure updated data information
spreadSheetView1.Update()

# set scalar coloring
ColorBy(matrix_transporteDisplay, ('POINTS', 'concentration'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView2)

# rescale color and/or opacity maps used to include current data range
matrix_transporteDisplay.RescaleTransferFunctionToDataRange(True, False)

# get color transfer function/color map for 'concentration'
concentrationLUT = GetColorTransferFunction('concentration')

# get opacity transfer function/opacity map for 'concentration'
concentrationPWF = GetOpacityTransferFunction('concentration')

# get 2D transfer function for 'concentration'
concentrationTF2D = GetTransferFunction2D('concentration')

# set active source
SetActiveSource(matrix_transporte)

# show data in view
matrix_transporteDisplay = Show(matrix_transporte, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
matrix_transporteDisplay.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# hide data in view
Hide(matrix_transporte, renderView2)

# set active source
SetActiveSource(clip3)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip3.ClipType)

# update the view to ensure updated data information
renderView2.Update()

# set scalar coloring
ColorBy(clip3Display, ('POINTS', 'concentration'))

# rescale color and/or opacity maps used to include current data range
clip3Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
clip3Display.SetScalarBarVisibility(renderView2, True)

# set active source
SetActiveSource(integrateVariables1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip3.ClipType)

# update the view to ensure updated data information
renderView2.Update()

animationScene1.Play()

# create a new 'Plot Data Over Time'
plotDataOverTime1 = PlotDataOverTime(registrationName='PlotDataOverTime1', Input=integrateVariables1)

# Create a new 'Quartile Chart View'
quartileChartView1 = CreateView('QuartileChartView')

# show data in view
plotDataOverTime1Display = Show(plotDataOverTime1, quartileChartView1, 'QuartileChartRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=quartileChartView1, layout=layout1, hint=1)

# Properties modified on plotDataOverTime1Display
plotDataOverTime1Display.SeriesOpacity = ['concentration (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display.SeriesPlotCorner = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display.SeriesLineStyle = ['N (stats)', '1', 'Time (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'concentration (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display.SeriesLineThickness = ['N (stats)', '2', 'Time (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'concentration (stats)', '2', 'vtkValidPointMask (stats)', '2']
plotDataOverTime1Display.SeriesMarkerStyle = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display.SeriesMarkerSize = ['N (stats)', '4', 'Time (stats)', '4', 'X (stats)', '4', 'Y (stats)', '4', 'Z (stats)', '4', 'concentration (stats)', '4', 'vtkValidPointMask (stats)', '4']

# update the view to ensure updated data information
spreadSheetView1.Update()

# update the view to ensure updated data information
quartileChartView1.Update()

# save data
SaveData(path_csv1, proxy=plotDataOverTime1, WriteTimeSteps=1,
    ChooseArraysToWrite=1,
    RowDataArrays=['Time','avg(concentration)'],
    FieldAssociation='Row Data',
    AddMetaData=0)

# set active view
SetActiveView(spreadSheetView1)

# destroy spreadSheetView1
Delete(spreadSheetView1)
del spreadSheetView1

# close an empty frame
layout1.Collapse(2)

# set active source
SetActiveSource(matrix_transporte)

# set active view
SetActiveView(renderView2)

# set active source
SetActiveSource(matrix_transporte)

# show data in view
matrix_transporteDisplay = Show(matrix_transporte, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
matrix_transporteDisplay.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# hide data in view
Hide(clip3, renderView2)

# create a new 'Clip'
clip4 = Clip(registrationName='Clip4', Input=matrix_transporte)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip4Display.Representation = 'Surface'

# hide data in view
Hide(matrix_transporte, renderView2)

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip4.ClipType
clip4.ClipType.Normal = [-1.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip5 = Clip(registrationName='Clip5', Input=clip4)

# show data in view
clip5Display = Show(clip5, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip5Display.Representation = 'Surface'

# hide data in view
Hide(clip4, renderView2)

# show color bar/color legend
clip5Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# set active source
SetActiveSource(clip4)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip5.ClipType)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip4.ClipType)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# Properties modified on clip5.ClipType
clip5.ClipType.Normal = [-1.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# hide data in view
Hide(clip4, renderView2)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# hide data in view
Hide(clip4, renderView2)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# set active source
SetActiveSource(clip4)

# Properties modified on clip4.ClipType
clip4.ClipType.Normal = [1.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# hide data in view
Hide(clip4, renderView2)

# set active source
SetActiveSource(clip4)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# hide data in view
Hide(clip4, renderView2)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# Properties modified on clip4.ClipType
clip4.ClipType.Normal = [-1.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# set active source
SetActiveSource(clip5)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip4.ClipType)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip5.ClipType)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip5.ClipType
clip5.ClipType.Normal = [1.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# hide data in view
Hide(clip4, renderView2)

# hide data in view
Hide(clip5, renderView2)

# set active source
SetActiveSource(clip4)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip5.ClipType)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip4.ClipType)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# reset view to fit data
renderView2.ResetCamera(False, 0.9)

# update the view to ensure updated data information
renderView2.Update()

# set active source
SetActiveSource(clip5)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip4.ClipType)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip5.ClipType)

# show data in view
clip5Display = Show(clip5, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip5Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# hide data in view
Hide(clip4, renderView2)

# set active source
SetActiveSource(clip4)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip5.ClipType)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip4.ClipType)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# hide data in view
Hide(clip4, renderView2)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# hide data in view
Hide(clip4, renderView2)

# show data in view
clip4Display = Show(clip4, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView2, True)

# hide data in view
Hide(clip4, renderView2)

# set active source
SetActiveSource(clip5)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip4.ClipType)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip5.ClipType)

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip6 = Clip(registrationName='Clip6', Input=clip5)

# show data in view
clip6Display = Show(clip6, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip6Display.Representation = 'Surface'

# hide data in view
Hide(clip5, renderView2)

# show color bar/color legend
clip6Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip6.ClipType
clip6.ClipType.Origin = [0.5, 0.5, 0.5]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip6.ClipType
clip6.ClipType.Normal = [1.0, 1.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip6.ClipType
clip6.ClipType.Normal = [0.0, 1.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip6.ClipType
clip6.ClipType.Normal = [0.0, -1.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip7 = Clip(registrationName='Clip7', Input=clip6)

# show data in view
clip7Display = Show(clip7, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip7Display.Representation = 'Surface'

# hide data in view
Hide(clip6, renderView2)

# show color bar/color legend
clip7Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip7.ClipType
clip7.ClipType.Normal = [1.0, 1.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip7.ClipType
clip7.ClipType.Normal = [0.0, 1.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip7.ClipType
clip7.ClipType.Origin = [0.5, 0.75, 0.5]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip8 = Clip(registrationName='Clip8', Input=clip7)

# show data in view
clip8Display = Show(clip8, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip8Display.Representation = 'Surface'

# hide data in view
Hide(clip7, renderView2)

# show color bar/color legend
clip8Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip8.ClipType
clip8.ClipType.Normal = [1.0, 0.0, 1.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip8.ClipType
clip8.ClipType.Normal = [0.0, 0.0, 1.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip8.ClipType
clip8.ClipType.Normal = [0.0, 0.0, -1.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip8.ClipType
clip8.ClipType.Origin = [0.625, 0.625, 0.75]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Integrate Variables'
integrateVariables2 = IntegrateVariables(registrationName='IntegrateVariables2', Input=clip8)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
integrateVariables2Display = Show(integrateVariables2, spreadSheetView1, 'SpreadSheetRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=1)

# update the view to ensure updated data information
spreadSheetView1.Update()

# create a new 'Plot Data Over Time'
plotDataOverTime2 = PlotDataOverTime(registrationName='PlotDataOverTime2', Input=integrateVariables2)

# Create a new 'Quartile Chart View'
quartileChartView2 = CreateView('QuartileChartView')

# show data in view
plotDataOverTime2Display = Show(plotDataOverTime2, quartileChartView2, 'QuartileChartRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=quartileChartView2, layout=layout1, hint=4)

# Properties modified on plotDataOverTime2Display
plotDataOverTime2Display.SeriesOpacity = ['concentration (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime2Display.SeriesPlotCorner = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime2Display.SeriesLineStyle = ['N (stats)', '1', 'Time (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'concentration (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime2Display.SeriesLineThickness = ['N (stats)', '2', 'Time (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'concentration (stats)', '2', 'vtkValidPointMask (stats)', '2']
plotDataOverTime2Display.SeriesMarkerStyle = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime2Display.SeriesMarkerSize = ['N (stats)', '4', 'Time (stats)', '4', 'X (stats)', '4', 'Y (stats)', '4', 'Z (stats)', '4', 'concentration (stats)', '4', 'vtkValidPointMask (stats)', '4']

# update the view to ensure updated data information
quartileChartView1.Update()

# update the view to ensure updated data information
quartileChartView2.Update()

# save data
SaveData(path_csv2, proxy=plotDataOverTime2, WriteTimeSteps=1,
    ChooseArraysToWrite=1,
    RowDataArrays=['Time','avg(concentration)'],
    FieldAssociation='Row Data',
    AddMetaData=0)

# set active source
SetActiveSource(matrix_transporte)

# set active view
SetActiveView(renderView2)

# set active source
SetActiveSource(matrix_transporte)

# show data in view
matrix_transporteDisplay = Show(matrix_transporte, renderView2, 'UnstructuredGridRepresentation')

# show color bar/color legend
matrix_transporteDisplay.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# update the view to ensure updated data information
quartileChartView2.Update()

# hide data in view
Hide(clip8, renderView2)

# set active view
SetActiveView(quartileChartView1)

# destroy quartileChartView1
Delete(quartileChartView1)
del quartileChartView1

# close an empty frame
layout1.Collapse(2)

# set active view
SetActiveView(quartileChartView2)

# destroy quartileChartView2
Delete(quartileChartView2)
del quartileChartView2

# close an empty frame
layout1.Collapse(6)

# set active view
SetActiveView(spreadSheetView1)

# destroy spreadSheetView1
Delete(spreadSheetView1)
del spreadSheetView1

# close an empty frame
layout1.Collapse(2)

# set active view
SetActiveView(renderView2)

# create a new 'Clip'
clip9 = Clip(registrationName='Clip9', Input=matrix_transporte)

# show data in view
clip9Display = Show(clip9, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip9Display.Representation = 'Surface'

# hide data in view
Hide(matrix_transporte, renderView2)

# show color bar/color legend
clip9Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip9.ClipType
clip9.ClipType.Origin = [0.75, 0.5, 0.5]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip9.ClipType
clip9.ClipType.Normal = [-1.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip10 = Clip(registrationName='Clip10', Input=clip9)

# show data in view
clip10Display = Show(clip10, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip10Display.Representation = 'Surface'

# hide data in view
Hide(clip9, renderView2)

# show color bar/color legend
clip10Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip10.ClipType
clip10.ClipType.Origin = [0.875, 0.75, 0.5]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip10.ClipType
clip10.ClipType.Normal = [1.0, 1.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip10.ClipType
clip10.ClipType.Normal = [0.0, 1.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip10.ClipType
clip10.ClipType.Normal = [0.0, -1.0, 0.0]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip11 = Clip(registrationName='Clip11', Input=clip10)

# show data in view
clip11Display = Show(clip11, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip11Display.Representation = 'Surface'

# hide data in view
Hide(clip10, renderView2)

# show color bar/color legend
clip11Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip11.ClipType
clip11.ClipType.Normal = [1.0, 0.0, 1.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip11.ClipType
clip11.ClipType.Normal = [0.0, 0.0, 1.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip11.ClipType
clip11.ClipType.Normal = [0.0, 0.0, -1.0]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Clip'
clip12 = Clip(registrationName='Clip12', Input=clip11)

# show data in view
clip12Display = Show(clip12, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip12Display.Representation = 'Surface'

# hide data in view
Hide(clip11, renderView2)

# show color bar/color legend
clip12Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip12.ClipType
clip12.ClipType.Normal = [1.0, 0.0, 1.0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on clip12.ClipType
clip12.ClipType.Normal = [0.0, 0.0, 1.0]

# update the view to ensure updated data information
renderView2.Update()

# create a new 'Integrate Variables'
integrateVariables3 = IntegrateVariables(registrationName='IntegrateVariables3', Input=clip12)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
integrateVariables3Display = Show(integrateVariables3, spreadSheetView1, 'SpreadSheetRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

# update the view to ensure updated data information
spreadSheetView1.Update()

# create a new 'Plot Data Over Time'
plotDataOverTime3 = PlotDataOverTime(registrationName='PlotDataOverTime3', Input=integrateVariables3)

# Create a new 'Quartile Chart View'
quartileChartView1 = CreateView('QuartileChartView')

# show data in view
plotDataOverTime3Display = Show(plotDataOverTime3, quartileChartView1, 'QuartileChartRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=quartileChartView1, layout=layout1, hint=2)

# Properties modified on plotDataOverTime3Display
plotDataOverTime3Display.SeriesOpacity = ['concentration (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime3Display.SeriesPlotCorner = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime3Display.SeriesLineStyle = ['N (stats)', '1', 'Time (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'concentration (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime3Display.SeriesLineThickness = ['N (stats)', '2', 'Time (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'concentration (stats)', '2', 'vtkValidPointMask (stats)', '2']
plotDataOverTime3Display.SeriesMarkerStyle = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime3Display.SeriesMarkerSize = ['N (stats)', '4', 'Time (stats)', '4', 'X (stats)', '4', 'Y (stats)', '4', 'Z (stats)', '4', 'concentration (stats)', '4', 'vtkValidPointMask (stats)', '4']

# save data
SaveData(path_csv3, proxy=plotDataOverTime3, WriteTimeSteps=1,
    ChooseArraysToWrite=1,
    RowDataArrays=['Time','avg(concentration)'],
    FieldAssociation='Row Data',
    AddMetaData=0)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1777, 1256)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView2
renderView2.CameraPosition = [-3.7538167775089484, 7.604104119547013, 2.8492580331293187]
renderView2.CameraFocalPoint = [0.5000000000000001, 0.4999999999999999, 0.49999999999999983]
renderView2.CameraViewUp = [0.5393334456453803, 0.5373507726269906, -0.6483622302119842]
renderView2.CameraParallelScale = 1.0392304845413265


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