Plotting
========

2D plotting (histograms as lines, points, or bands)
---------------------------------------------------

2D plotting, i.e. plotting of 1D histograms. A single histogram stack as well as any number of individual histograms visualised as curves, points, bands can be shown. Any number of panels (called "pads" in ROOT) can be included in a single figure.

The function for making a 2D plot is ``make_figure``.

A special convenience function for plotting a breakdown of the uncertainties of a single histogram called ``make_uncertainty_breakdown`` is also provided.

.. autofunction:: heppy.make_figure

.. autoclass:: heppy.panel

.. autofunction:: heppy.make_uncertainty_breakdown



3D plotting (histogram as heatmap)
----------------------------------

3D plotting, i.e. plotting of 2D histograms. Only a single histogram can be put into each plot. The histogram contents can be printed onto the histogram in a nicely formatted way for better readability.

.. autofunction:: heppy.make_heatmap

.. autoclass:: heppy.TextFormatter
    :members:
