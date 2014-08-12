###############################################################################
##
## Copyright (C) 2014, NYU Center for Urban Science and Progress (NYU CUSP). 
## All rights reserved.
## Contact: huy.vo@nyu.edu
## Modified for Urban Computing Skills Lab, CUSP-GX-1000 Assignment purpose by drp354@nyu.edu
##
## This file is part of the Urban Computing Skills Lab, CUSP-GX-1000.
##
## "Redistribution and use in source and binary forms, with or without 
## modification, are permitted provided that the following conditions are met:
##
##  - Redistributions of source code must retain the above copyright notice, 
##    this list of conditions and the following disclaimer.
##  - Redistributions in binary form must reproduce the above copyright 
##    notice, this list of conditions and the following disclaimer in the 
##    documentation and/or other materials provided with the distribution.
##  - Neither the name of NYU-Poly nor the names of its 
##    contributors may be used to endorse or promote products derived from 
##    this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
## THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
## PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
## OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
## WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
## OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
###############################################################################

import shapefile, sys
import matplotlib.pyplot as m_plot
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.ticker import MaxNLocator

if __name__=='__main__':
    if len(sys.argv)!=3:
        print 'Usage: python %s <SHAPEFILE_PREFIX> <OUTPUT_PDF>' % sys.argv[0]
        sys.exit(1)

    # We are creating a figure of size 4.5" by 7.2". This "tall" ratio
    # was due to the boundary of the shapefile
    fig = m_plot.figure(figsize=(4.5, 7.2))

    # We create a centered plot title with a specific font size
    fig.suptitle('New York City Street Maps', fontsize=20)

    # We add a plot to position '111', please note that '111' means
    # that our layout is a 1x1 cell and the subplot will be in the
    # first position. Likewise, a '212' value would mean that we're
    # creating a 2x1 (two row, one column) layout and putting our plot
    # on the second (2) slot, which is on the second row. You can play
    # around with this to get a sense of the layout.
    ax = fig.add_subplot(111, aspect='equal')

    # Now, we move on to reading the shapefile, very simple, just use
    # the Reader class. This would return an object where we can get
    # shape data from.
    sf = shapefile.Reader(sys.argv[1])

    # As we all know, a shapefile consists of a list of shapes and
    # meta-data (i.e. a record) associated with each shape. For our
    # dataset, the shapes are all polylines. To iterate through all
    # shapes and records, we may use the shapeRecords function as
    # follows:
    #i=0;
    for sr in sf.shapeRecords():

        # Now, each 'sr' object would contains two members: 'shape'
        # and 'record', as their names suggest, containing the shape
        # geometry and the record meta data.
        #
        # We first assign a value of '0.8' to color, which is a light
        # gray-ish color.
        color = '0.8'

        # Next, we're parsing the record information to determine the
        # shape color. Since the 5th field of the record (numbering
        # from 1), aka "LeftCounty", specifying one of the county
        # where this street segment belongs, we just need to check if
        # its value is "New York" to determine if the segment belongs
        # to Manhattan.
        #
        # NOTE: NYC is divided into five boroughs, each belongs to a
        # different county: Manhattan (New York), Brooklyn (Kings),
        # Queens (Queens), Bronx (Bronx), Staten Island (Richmond).
        #
        # If a shape belongs to Manhattan, we assign a different color
        
        #Modified for highlighting only the highway
        if sr.record[1]!='      ':
            color='orange'
        
        # It's time to draw the shape on our plot. A shape in a
        # shapefile consists a list of vertices (points) and a list of
        # parts which is a partition of the points, where each
        # partition should be rendered as an independent object. Each
        # partition is just an index number pointing to the location
        # of the point that marks the beginning of this partition. By
        # looking at a partition and the partition right after that,
        # we would know exactly the points that is needed to be
        # rendered for the first partition. For example, given:
        #
        # parts = [0, 16, 40]
        #
        # The first part would consist points 0 to 15
        # The second part would consists points 16 to 39
        # The third part would consists poitns 40 to the rest
        #
        # However, it should be noted that, the last part would not
        # have the information on "part after next" since it's the
        # last of the array. Therefore, we would create a new 'parts'
        # list, and append "-1" to the last element to make sure that
        # it knows its last element.
        parts = list(sr.shape.parts) + [-1]

        # Now rendering the shapes are straight forward. We iterate
        # through all the parts, using the parts index to fetch the
        # appropriate points and create Path and PathPatch. Then we
        # just need to add the patch the plot.
        for i in xrange(len(sr.shape.parts)):
            path = Path(sr.shape.points[parts[i]:parts[i+1]])
            patch = PathPatch(path, edgecolor=color, facecolor='none', lw=0.5, aa=True)
            ax.add_patch(patch)

    # We use the information on the shapefile bounding box to set
    # limits for the X and Y axis
    ax.set_xlim(sf.bbox[0], sf.bbox[2])
    ax.set_ylim(sf.bbox[1], sf.bbox[3])

    # We want to make sure that there's only 3 ticks on the X axis due
    # to the size ratio
    ax.xaxis.set_major_locator(MaxNLocator(3))

    # Now save the plot to the supplied filename
    fig.savefig(sys.argv[2])
