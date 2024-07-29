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
	print(f'usage: {argv[0]}  <input_mesh> <output_csv> <block_number>')
	exit()

path_matrix=argv[1]
path_csv=argv[2]
block_input=argv[3] #/IOSS/element_blocks/block_1
block_number = ('/IOSS/element_blocks/unnamed_block_id_%s' %(block_input))
#block_number = '/IOSS/element_blocks/unnamed_block_id_7'
print(block_number)

# create a new 'IOSS Reader'
fracture_transporte = IOSSReader(registrationName='fracture_transport.e', FileName=[path_matrix])

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
fracture_transporteDisplay = Show(fracture_transporte, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
fracture_transporteDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(fracture_transporteDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
fracture_transporteDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# get opacity transfer function/opacity map for 'vtkBlockColors'
vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

# get 2D transfer function for 'vtkBlockColors'
vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')

# create a new 'Extract Block'
extractBlock1 = ExtractBlock(registrationName='ExtractBlock1', Input=fracture_transporte)

# Properties modified on extractBlock1
extractBlock1.Selectors = [block_number]

# show data in view
extractBlock1Display = Show(extractBlock1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
extractBlock1Display.Representation = 'Surface'

# hide data in view
Hide(fracture_transporte, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(extractBlock1Display, ('POINTS', 'concentration'))

# rescale color and/or opacity maps used to include current data range
extractBlock1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
extractBlock1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'concentration'
concentrationLUT = GetColorTransferFunction('concentration')

# get opacity transfer function/opacity map for 'concentration'
concentrationPWF = GetOpacityTransferFunction('concentration')

# get 2D transfer function for 'concentration'
concentrationTF2D = GetTransferFunction2D('concentration')

animationScene1.GoToFirst()

animationScene1.GoToFirst()

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=extractBlock1)

# Create a new 'SpreadSheet View'
spreadSheetView2 = CreateView('SpreadSheetView')
spreadSheetView2.ColumnToSort = ''
spreadSheetView2.BlockSize = 1024

# show data in view
integrateVariables1Display = Show(integrateVariables1, spreadSheetView2, 'SpreadSheetRepresentation')

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView2, layout=layout1, hint=1)

# update the view to ensure updated data information
spreadSheetView2.Update()

# create a new 'Plot Data Over Time'
plotDataOverTime1 = PlotDataOverTime(registrationName='PlotDataOverTime1', Input=integrateVariables1)

# Create a new 'Quartile Chart View'
quartileChartView2 = CreateView('QuartileChartView')

# show data in view
plotDataOverTime1Display = Show(plotDataOverTime1, quartileChartView2, 'QuartileChartRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=quartileChartView2, layout=layout1, hint=4)

# Properties modified on plotDataOverTime1Display
plotDataOverTime1Display.SeriesOpacity = ['concentration (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display.SeriesPlotCorner = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display.SeriesLineStyle = ['N (stats)', '1', 'Time (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'concentration (stats)', '1', 'vtkValidPointMask (stats)', '1']
plotDataOverTime1Display.SeriesLineThickness = ['N (stats)', '2', 'Time (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'concentration (stats)', '2', 'vtkValidPointMask (stats)', '2']
plotDataOverTime1Display.SeriesMarkerStyle = ['N (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'concentration (stats)', '0', 'vtkValidPointMask (stats)', '0']
plotDataOverTime1Display.SeriesMarkerSize = ['N (stats)', '4', 'Time (stats)', '4', 'X (stats)', '4', 'Y (stats)', '4', 'Z (stats)', '4', 'concentration (stats)', '4', 'vtkValidPointMask (stats)', '4']

# find view
spreadSheetView1 = FindViewOrCreate('SpreadSheetView1', viewtype='SpreadSheetView')

# update the view to ensure updated data information
spreadSheetView1.Update()

# find view
quartileChartView1 = FindViewOrCreate('QuartileChartView1', viewtype='QuartileChartView')

# update the view to ensure updated data information
quartileChartView1.Update()

# update the view to ensure updated data information
quartileChartView2.Update()

# save data
SaveData(path_csv, proxy=plotDataOverTime1, ChooseArraysToWrite=1,
    RowDataArrays=['Time', 'avg(concentration)'],
    FieldAssociation='Row Data',
    AddMetaData=0)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1681, 1179)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [2014.7474198973127, 1814.0181088662148, 4564.751703618234]
renderView1.CameraFocalPoint = [-75.0, 800.0, 200.0]
renderView1.CameraViewUp = [-0.06144730182286946, 0.978302553353816, -0.19785940260723905]
renderView1.CameraParallelScale = 1304.0542267497372


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