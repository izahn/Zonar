# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# DeleteFromBigDataStore.py
# Created on: 2017-04-12 10:15:47.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# Local variables:
AllTimeWL = "Hosted\\AllTimeWL\\AllTimeWL"
AllTimeWL__2_ = AllTimeWL

# Process: Delete Rows
arcpy.DeleteRows_management(AllTimeWL)

