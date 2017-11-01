### extends 'class_empty.py'
### block ClassImports
# NOTICE: Do not edit anything here, it is generated code
from . import gxapi_cy
from geosoft.gxapi import GXContext, float_ref, int_ref, str_ref


### endblock ClassImports

### block Header
# NOTICE: The code generator will not replace the code in this block
### endblock Header

### block ClassImplementation
# NOTICE: Do not edit anything here, it is generated code
class GXGMSYS:
    """
    GXGMSYS class.

    The `GXGMSYS <geosoft.gxapi.GXGMSYS>` Methods
    """

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._wrapper = None

    def __del__(self):
        self._wrapper = None

    def __init__(self, wrapper=None):
        self._wrapper = wrapper if wrapper else gxapi_cy.WrapGMSYS(GXContext._get_tls_geo(), 0)

    @classmethod
    def null(cls):
        """
        A null (undefined) instance of `GXGMSYS`
        
        :returns: A null `GXGMSYS`
        """
        return cls()

    def is_null(self):
        """
        Check if the instance of `GXGMSYS` is null (undefined)`
        
        :returns: True if this is a null (undefined) instance of `GXGMSYS`, False otherwise.
        """
        return self._wrapper.handle == 0

    def _internal_handle(self):
        return self._wrapper.handle


# Miscellaneous


    @classmethod
    def launch(cls, model):
        """
        Launch `GXGMSYS <geosoft.gxapi.GXGMSYS>` with extension
        
        :param model:  Model name
        :type  model:  str

        .. versionadded:: 5.0.1
        """
        gxapi_cy.WrapGMSYS.launch(GXContext._get_tls_geo(), model.encode())
        





### endblock ClassImplementation
### block ClassExtend
# NOTICE: The code generator will not replace the code in this block
### endblock ClassExtend


### block Footer
# NOTICE: The code generator will not replace the code in this block
### endblock Footer