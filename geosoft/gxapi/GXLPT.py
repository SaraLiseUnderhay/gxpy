### extends 'class_empty.py'
### block ClassImports
# NOTICE: Do not edit anything here, it is generated code
from typing import NewType
from . import gxapi_cy
from geosoft.gxapi import GXContext, float_ref, int_ref, str_ref


### endblock ClassImports

### block Header
# NOTICE: The code generator will not replace the code in this block
### endblock Header

### block ClassImplementation
# NOTICE: Do not edit anything here, it is generated code
class GXLPT:
    """
    GXLPT class.

    This class allows access to the current default line patterns.
    It does not allow the definition of individual patterns. It is
    is used primarily with :class:`geosoft.gxapi.GXMAP` class functions.
    """

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._wrapper = None

    def __del__(self):
        self._wrapper = None

    def __init__(self, wrapper=None):
        self._wrapper = wrapper if wrapper else gxapi_cy.WrapLPT(GXContext._get_tls_geo(), 0)

    @classmethod
    def null(cls):
        """
        A null (undefined) instance of :class:`geosoft.gxapi.GXLPT`
        
        :returns: A null :class:`geosoft.gxapi.GXLPT`
        """
        return cls()

    def is_null(self):
        """
        Check if the instance of :class:`geosoft.gxapi.GXLPT` is null (undefined)`
        
        :returns: True if this is a null (undefined) instance of :class:`geosoft.gxapi.GXLPT`, False otherwise.
        """
        return self._wrapper.handle == 0

    def _internal_handle(self):
        return self._wrapper.handle


# Miscellaneous


    @classmethod
    def create(cls):
        """
        Creates a line pattern object with current default patterns.
        """
        ret_val = gxapi_cy.WrapLPT.create(GXContext._get_tls_geo())
        return GXLPT(ret_val)






    def get_lst(self, p2):
        """
        Copies all pattern names into a :class:`geosoft.gxapi.GXLST` object.
        """
        self._wrapper.get_lst(p2._wrapper)
        




    def get_standard_lst(self, p2):
        """
        Copies the six standard line types into a :class:`geosoft.gxapi.GXLST` object.

        **Note:**

        The six standard line types are "solid", "long dash", "dotted", "short dash", "long, short dash" and "dash dot".
        """
        self._wrapper.get_standard_lst(p2._wrapper)
        





### endblock ClassImplementation
### block ClassExtend
# NOTICE: The code generator will not replace the code in this block
### endblock ClassExtend


### block Footer
# NOTICE: The code generator will not replace the code in this block
### endblock Footer