Systematic-uncertainty tools
============================

Heppy provides tools to explore and treat the systematic variations of histograms. This notably means combining multiple systematic variations into a single combined systematic. Some examples include:

- Combining the members of a PDF set into the PDF uncertainty
- Adding several uncorrelated uncertainties in quadrature to get a resulting net uncertainty
- Combining a set of bootstrap replicas into a final uncertainty
- Taking the envelope of perturbative QCD scale variations to get an estimate of the fixed-order calculation uncertainty
- etc.

The basic usage is:

1. Create any number of ``heppy.uncertainty.model`` instances that specify *which* variations should be combined and *how*.
2. Call ``heppy.uncertainty.combine_copy``, taking as arguments a histogram and a list of uncertainty models, to return a copy of the histogram where the combination models have been applied to the variations.

.. automodule:: heppy.uncertainty
    :members:
    :undoc-members:
