# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Ml4Qgis
                                 A QGIS plugin
 Machine learning in QGIS.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-05-06
        copyright            : (C) 2023 by Mikhail Moskovchenko
        email                : moskovchenkomike@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Mikhail Moskovchenko'
__date__ = '2023-05-06'
__copyright__ = '(C) 2023 by Mikhail Moskovchenko'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import QgsProcessingProvider
from .ml4qgis_algorithm import (Ml4QgisAlgorithm, CondaSetupAlgorithm, PythonSetupAlgorithm,
                                DockerSetupAlgorithm, TempDirAlgorithm, 
                                Sentinel2Algorithm, LandsatAlgorithm, MosaicAlgorithm, NormalizeAlgorithm,
                                SegTilesAlgorithm, SegTrainAlgorithm, SegTestAlgorithm, SegMapAlgorithm)


class Ml4QgisProvider(QgsProcessingProvider):

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(DockerSetupAlgorithm())
        self.addAlgorithm(CondaSetupAlgorithm())
        self.addAlgorithm(PythonSetupAlgorithm())
        self.addAlgorithm(TempDirAlgorithm())
        self.addAlgorithm(Sentinel2Algorithm())
        self.addAlgorithm(LandsatAlgorithm())
        self.addAlgorithm(MosaicAlgorithm())
        self.addAlgorithm(NormalizeAlgorithm())
        self.addAlgorithm(SegTilesAlgorithm())
        self.addAlgorithm(SegTrainAlgorithm())
        self.addAlgorithm(SegTestAlgorithm())
        self.addAlgorithm(SegMapAlgorithm())
        #self.addAlgorithm(Ml4QgisAlgorithm())
        # add additional algorithms here
        # self.addAlgorithm(MyOtherAlgorithm())

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'ML4QGIS'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('ML4QGIS')

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QgsProcessingProvider.icon(self)

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
