### extends 'class_empty.py'
from . import gxapi_cy

from geosoft.gxapi import GXContext, int_ref, float_ref, str_ref

### block Header
# NOTICE: The code generator will not replace the code in this block
### endblock Header

### block ClassImplementation
# NOTICE: Do not edit anything here, it is generated code
class GXMSTK:
    """
    """

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._wrapper = None

    def __del__(self):
        self._wrapper = None

    def __init__(self, wrapper=None):
        self._wrapper = wrapper if wrapper else gxapi_cy.WrapMSTK(0)

    @classmethod
    def null(cls) -> 'GXMSTK':
        """
        A null (undefined) instance of :class:`GXMSTK`
        
        :returns: A null :class:`GX3DN`
        """
        return cls()

    def is_null(self) -> bool:
        """
        Check if the instance of :class:`GXMSTK` is null (undefined)`
        
        :returns: True if this is a null (undefined) instance of :class:`GXMSTK`, False otherwise.
        """
        return self._wrapper.handle == 0

    def _internal_handle(self):
        return self._wrapper.handle


# Miscellaneous



    def add_stk(self) -> 'GXSTK':
        ret_val = self._wrapper.add_stk()
        return GXSTK(ret_val)




    def chan_list_vv(self, p2: 'GXDB', p3: 'GXVV', p4: 'GXVV', p5: 'GXVV', p6: 'GXVV', p7: 'GXVV') -> None:
        self._wrapper.chan_list_vv(p2, p3, p4, p5, p6, p7)
        



    @classmethod
    def create(cls) -> 'GXMSTK':
        ret_val = gxapi_cy.WrapMSTK.create(GXContext._get_tls_geo())
        return GXMSTK(ret_val)






    def draw_profile(self, p2: 'GXDB', p3: int, p4: 'GXMAP') -> None:
        self._wrapper.draw_profile(p2, p3, p4)
        




    def set_y_axis_direction(self, p2: int) -> None:
        self._wrapper.set_y_axis_direction(p2)
        




    def find_stk2(self, p2: str, p3: int_ref, p4: 'GXVV') -> None:
        p3.value = self._wrapper.find_stk2(p2.encode(), p3.value, p4)
        




    def get_stk(self, p2: int) -> 'GXSTK':
        ret_val = self._wrapper.get_stk(p2)
        return GXSTK(ret_val)




    def delete(self, p2: int) -> None:
        self._wrapper.delete(p2)
        




    def find_stk(self, p2: str, p3: int_ref, p4: str_ref, p6: str_ref, p8: str_ref) -> None:
        p3.value, p4.value, p6.value, p8.value = self._wrapper.find_stk(p2.encode(), p3.value, p4.value.encode(), p6.value.encode(), p8.value.encode())
        




    def get_num_stk(self) -> int:
        ret_val = self._wrapper.get_num_stk()
        return ret_val




    def read_ini(self, p2: 'GXRA') -> None:
        self._wrapper.read_ini(p2)
        




    def save_profile(self, p2: 'GXWA') -> None:
        self._wrapper.save_profile(p2)
        





### endblock ClassImplementation
### block ClassExtend
# NOTICE: The code generator will not replace the code in this block
### endblock ClassExtend


### block Footer
# NOTICE: The code generator will not replace the code in this block
### endblock Footer