### extends 'class_empty.py'
from . import gxapi_cy

from geosoft.gxapi import GXContext, int_ref, float_ref, str_ref

### block Header
# NOTICE: The code generator will not replace the code in this block
### endblock Header

### block ClassImplementation
# NOTICE: Do not edit anything here, it is generated code
class GXARCSYS:
    """
    """

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._wrapper = None

    def __del__(self):
        self._wrapper = None

    def __init__(self, wrapper=None):
        self._wrapper = wrapper if wrapper else gxapi_cy.WrapARCSYS(0)

    @classmethod
    def null(cls) -> 'GXARCSYS':
        """
        A null (undefined) instance of :class:`GXARCSYS`
        
        :returns: A null :class:`GX3DN`
        """
        return cls()

    def is_null(self) -> bool:
        """
        Check if the instance of :class:`GXARCSYS` is null (undefined)`
        
        :returns: True if this is a null (undefined) instance of :class:`GXARCSYS`, False otherwise.
        """
        return self._wrapper.handle == 0

    def _internal_handle(self):
        return self._wrapper.handle


# Miscellaneous


    @classmethod
    def get_browse_loc(cls, p1: str_ref) -> None:
        p1.value = gxapi_cy.WrapARCSYS.get_browse_loc(GXContext._get_tls_geo())
        



    @classmethod
    def get_current_doc(cls, p1: str_ref) -> None:
        p1.value = gxapi_cy.WrapARCSYS.get_current_doc(GXContext._get_tls_geo())
        



    @classmethod
    def set_browse_loc(cls, p1: str) -> None:
        gxapi_cy.WrapARCSYS.set_browse_loc(GXContext._get_tls_geo())
        





### endblock ClassImplementation
### block ClassExtend
# NOTICE: The code generator will not replace the code in this block
### endblock ClassExtend


### block Footer
# NOTICE: The code generator will not replace the code in this block
### endblock Footer