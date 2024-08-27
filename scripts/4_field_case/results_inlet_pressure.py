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
	print(f'usage: {argv[0]}  <input_mesh> <output_csv> ')
	exit()

path_matrix=argv[1]
path_csv=argv[2]

matrix_flowe = IOSSReader(registrationName='matrix_flow.e', FileName=[path_matrix])

# create a new 'IOSS Reader'

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

# Properties modified on matrix_flowe
matrix_flowe.ElementBlocks = []

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on matrix_flowe
matrix_flowe.SideSets = ['surface_1', 'surface_2']

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=matrix_flowe)

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

# get animation scene
animationScene1 = GetAnimationScene()

animationScene1.Play()

animationScene1.GoToFirst()

# set active view
SetActiveView(renderView1)

# set active source
SetActiveSource(matrix_flowe)

# set scalar coloring
ColorBy(matrix_floweDisplay, ('POINTS', 'pressure'))

# rescale color and/or opacity maps used to include current data range
matrix_floweDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
matrix_floweDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'pressure'
pressureLUT = GetColorTransferFunction('pressure')

# get opacity transfer function/opacity map for 'pressure'
pressurePWF = GetOpacityTransferFunction('pressure')

# get 2D transfer function for 'pressure'
pressureTF2D = GetTransferFunction2D('pressure')

# set active view
SetActiveView(spreadSheetView1)

# set active source
SetActiveSource(integrateVariables1)

# save data
SaveData(path_csv, proxy=integrateVariables1, ChooseArraysToWrite=1,
    PointDataArrays=['pressure'],
    AddMetaData=0)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1241, 1256)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [3.497701484667223, -4.014970961207725, 0.9949041575280038]
renderView1.CameraFocalPoint = [0.5, 1.125, 0.49999966665999995]
renderView1.CameraViewUp = [0.20237236630888172, 0.2101234493101632, 0.9565006855222548]
renderView1.CameraParallelScale = 1.5597502123205909


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