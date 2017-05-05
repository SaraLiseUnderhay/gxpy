"""
Geosoft aggregates are used to compose georeferenced images on maps and in 3D views.

.. note::

    Regression tests provide usage examples: `Tests <https://github.com/GeosoftInc/gxpy/blob/master/geosoft/gxpy/tests/test_agg.py>`_

"""
import os

import geosoft
import geosoft.gxapi as gxapi
from . import vv as gxvv

__version__ = geosoft.__version__


def _t(s):
    return geosoft.gxpy.system.translate(s)


class AGGException(Exception):
    """
    Exceptions from this module.

    .. versionadded:: 9.2
    """
    pass

ZONE_DEFAULT = 0
ZONE_LINEAR = 1
ZONE_NORMAL = 2
ZONE_EQUALAREA = 3
ZONE_SHADE = 4
ZONE_LOGLINEAR = 5
ZONE_LAST = 6

class Aggregate_image():
    """
    The AGG class supports the creation of aggregate images from one or more grid data sets. Aggergates
    can be placed into a 2D or 3D view for display.

    :param grid_file:   if specified, the ``add_layer()`` method is called with remaining parameters
                        to create a single-image aggregate.  See ``add_layer()``.

    :properties:
    
        :gxagg:         gxapi.GXAGG instance
        :layer_count:   the number of image layers in the aggregate.
        :brightness:    the brightness setting relative to the original colouring.  This ranges from
                        -1.0 (black) to 1.0 (white).
 
    Constructors:

        ======== ================================
        `open()` open an existing aggregate
        `new()`  create a new aggregate
        ======== ================================

    Properties:
    
        :name:          aggregate group name
        :gxagg:         gxapi.GXAGG instance
        :layer_count:   number of layers
        :brightness:    image brightness, -1 (black) to +1 (white). 0 is full colour.

    .. versionadded:: 9.2
    """

    def __repr__(self):
        return "{}({})".format(self.__class__, self.__dict__)

    def __str__(self):
        return self._create_name()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.gxagg = None
        pass

    def __init__(self):
        self.gxagg = None

    @classmethod
    def new(cls, grid_file=None, **kwargs):

        agg = cls()
        agg.gxagg = gxapi.GXAGG.create()
        if grid_file is not None:
            agg.add_layer(grid_file, **kwargs)
        return agg

    @classmethod
    def open(cls, gxagg):

        agg = cls()
        if not isinstance(gxagg, gxapi.GXAGG):
            raise AGGException(_t('A gxapi.GXAGG isstance is required.'))
        agg.gxagg = gxagg
        return agg

    def close(self):
        """Close an agg."""
        self.gxagg = None

    @property
    def layer_count(self):
        return self.gxagg.num_layers()

    @property
    def brightness(self):
        return self.gxagg.get_brightness()

    @brightness.setter
    def brightness(self, adjustment):
        a = max(-1.0, min(adjustment, 1.0))
        self.gxagg.change_brightness(a)

    @property
    def name(self):
        return self._create_name()

    def _create_name(self):
        s = ''
        layernames = self.layer_file_names()
        if not layernames:
            return s
        names = []
        for fn in layernames:
            names.append(os.path.basename(fn).split('.')[0])
        for fn in names:
            # ignore shaded layers if parent is here.
            if fn[-2:] == '_s':
                if fn[:-2] in names:
                    continue
                i = str.rfind(fn[:-2], '_')
                if i > 1 and fn[:i] in names:
                    continue
            s = s + fn + ', '
        return s[:-2]

    def add_layer(self,
                  grid_file,
                  color_map=None,
                  zone=None,
                  shade=False,
                  minimum=None,
                  maximum=None,
                  contour=None):
        """
        Add an image layer to an agg.

        :param grid_file:       The name of a grid file (image or data) to add.
        :param color_map:       gxpy.group.Color_map instance, or the name of a file, which may be 
                                `.tbl`, `.zon`, `.itr`, or `.agg`.
        :param zone:            Colour distribution method:

            ::

                ZONE_DEFAULT        as set by user global default settings
                ZONE_LINEAR         linearly distributed
                ZONE_NORMAL         normal (Gaussian) distribution
                ZONE_EQUALAREA      each colour will occupy an equal area on the image
                ZONE_LOGLINEAR      logarithmic linear distribution
                ZONE_LAST           last used colouring for this grid file
                ZONE_SHADE          Displays the shaded image version of the grid. The shaded image is
                                    a grid file will with '_s' appended to the file name.  If it does not
                                    exist, a shaded image with illumination inclination and declination
                                    both set to 45 degrees is automatically created.
                                    
        :param shade:           True, to add a shading layer
        :param minimum:         Minimum data value. All grid values less than or equal to the
                                minimum will be assigned the first colour in the table.  The default is
                                calculated from the data.
        :param maximum:         Maximum data value.  All grid values greater than or equal to the maximum
                                will be assigned the last colour in the table.  The default is calculated from
                                the data.

        .. versionadded:: 9.2
        """

        if (color_map is None):
            if zone == ZONE_SHADE:
                color_map = 'lgray.tbl'
        if (color_map is None) or (isinstance(color_map, str)):
            color_map = geosoft.gxpy.group.Color_map(color_map)
        color_map = color_map.save_file()

        try:
            if grid_file is not None:
                if zone is None:
                    zone = ZONE_DEFAULT
                if minimum is None:
                    minimum = gxapi.rDUMMY
                if maximum is None:
                    maximum = gxapi.rDUMMY
                if contour is None:
                    contour = gxapi.rDUMMY
                self.gxagg.layer_img_ex(grid_file,
                                        zone,
                                        color_map,
                                        minimum,
                                        maximum,
                                        contour)
                if shade and (zone != ZONE_SHADE):
                    self.gxagg.layer_img(grid_file, ZONE_SHADE, 'lgray.tbl', gxapi.rDUMMY)
        finally:
            if os.path.exists(color_map):
                os.remove(color_map)

    def layer_file_names(self):
        """
        Return list of layer files in the agg.

        .. versionadded:: 9.2
        """

        vv = gxvv.GXvv(dtype='U1024')
        self.gxagg.list_img(vv._vv)
        return list(vv.np)