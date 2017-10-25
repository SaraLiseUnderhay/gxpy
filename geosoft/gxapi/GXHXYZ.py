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
class GXHXYZ:
    """
    GXHXYZ class.

    High Performance Data Point Storage. This is used
    to put Point data on a DAP server. It is compressed
    and uses a Quad-Tree design to allow very high speed
    data extraction. It is also multi-threaded.
    """

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._wrapper = None

    def __del__(self):
        self._wrapper = None

    def __init__(self, wrapper=None):
        self._wrapper = wrapper if wrapper else gxapi_cy.WrapHXYZ(GXContext._get_tls_geo(), 0)

    @classmethod
    def null(cls):
        """
        A null (undefined) instance of :class:`geosoft.gxapi.GXHXYZ`
        
        :returns: A null :class:`geosoft.gxapi.GXHXYZ`
        """
        return cls()

    def is_null(self):
        """
        Check if the instance of :class:`geosoft.gxapi.GXHXYZ` is null (undefined)`
        
        :returns: True if this is a null (undefined) instance of :class:`geosoft.gxapi.GXHXYZ`, False otherwise.
        """
        return self._wrapper.handle == 0

    def _internal_handle(self):
        return self._wrapper.handle


# Miscellaneous


    @classmethod
    def create(cls, p1):
        """
        Create a handle to an :class:`geosoft.gxapi.GXHXYZ` object
        """
        ret_val = gxapi_cy.WrapHXYZ.create(GXContext._get_tls_geo(), p1.encode())
        return GXHXYZ(ret_val)






    def get_meta(self, p2):
        """
        Get the metadata of a grid.
        """
        self._wrapper.get_meta(p2._wrapper)
        



    @classmethod
    def h_create_db(cls, p1, p2, p3):
        """
        Make an :class:`geosoft.gxapi.GXHXYZ` from GDB
        """
        ret_val = gxapi_cy.WrapHXYZ.h_create_db(GXContext._get_tls_geo(), p1._wrapper, p2._wrapper, p3.encode())
        return GXHXYZ(ret_val)



    @classmethod
    def h_create_sql(cls, p1, p2, p3, p4, p5, p6):
        """
        Make an :class:`geosoft.gxapi.GXHXYZ` from SQL Query
        """
        ret_val = gxapi_cy.WrapHXYZ.h_create_sql(GXContext._get_tls_geo(), p1.encode(), p2.encode(), p3.encode(), p4.encode(), p5._wrapper, p6.encode())
        return GXHXYZ(ret_val)




    def set_meta(self, p2):
        """
        Set the metadata of a grid.
        """
        self._wrapper.set_meta(p2._wrapper)
        





### endblock ClassImplementation
### block ClassExtend
# NOTICE: The code generator will not replace the code in this block
### endblock ClassExtend


### block Footer
# NOTICE: The code generator will not replace the code in this block
### endblock Footer