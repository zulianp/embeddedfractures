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
	print(f'usage: {argv[0]} <input_mesh> <output_csv>')
	exit()

path_matrix=argv[1]
path_csv=argv[2]

# create a new 'IOSS Reader'
matrix_flowe = IOSSReader(registrationName='matrix_flow.e', FileName=[path_matrix])

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

# set active source
SetActiveSource(plotOverLine1)

# show data in view
plotOverLine1Display = Show(plotOverLine1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
plotOverLine1Display.Representation = 'Surface'

# show data in view
plotOverLine1Display = Show(plotOverLine1, renderView1, 'GeometryRepresentation')

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

# save data
SaveData(path_csv, proxy=plotOverLine1, ChooseArraysToWrite=1,
    PointDataArrays=['arc_length', 'pressure'],
    AddMetaData=0)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1091, 1262)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [0.5, 0.5, 4.275309792344299]
renderView1.CameraFocalPoint = [0.5, 0.5, 0.5]
renderView1.CameraParallelScale = 0.9846162698882537


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