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
class GXMAPTEMPLATE:
    """
    GXMAPTEMPLATE class.

    A :class:`geosoft.gxapi.GXMAPTEMPLATE` wraps and provides manipulation and usage for the XML content in map template files.
    See the annotated schema file maptemplate.xsd in the <GEOSOFT>\\maptemplate folder and the accompanying
    documentation in that folder for documentation on the file format.
    """

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._wrapper = None

    def __del__(self):
        self._wrapper = None

    def __init__(self, wrapper=None):
        self._wrapper = wrapper if wrapper else gxapi_cy.WrapMAPTEMPLATE(GXContext._get_tls_geo(), 0)

    @classmethod
    def null(cls):
        """
        A null (undefined) instance of :class:`geosoft.gxapi.GXMAPTEMPLATE`
        
        :returns: A null :class:`geosoft.gxapi.GXMAPTEMPLATE`
        """
        return cls()

    def is_null(self):
        """
        Check if the instance of :class:`geosoft.gxapi.GXMAPTEMPLATE` is null (undefined)`
        
        :returns: True if this is a null (undefined) instance of :class:`geosoft.gxapi.GXMAPTEMPLATE`, False otherwise.
        """
        return self._wrapper.handle == 0

    def _internal_handle(self):
        return self._wrapper.handle


# Content Manipulation Methods



    def get_tmp_copy(self, p2):
        """
        Get a temporary XML file for manipulation of the map template.

        **Note:**

        After manipulating contents the object may be updated by a call to
        the UpdateFromTmpCopy method.
        """
        p2.value = self._wrapper.get_tmp_copy(p2.value.encode())
        




    def update_from_tmp_copy(self, p2):
        """
        Update the object contents from a temporary XML file that may have bee manipulated externally.

        **Note:**

        This method will not modify the original contents of the file until a call to the
        the Commit method is made or the object is destroyed. A call to the Discard method
        will restore the contents to that of the original file. The temporary file is not deleted
        and should be to not leak file resources.
        """
        self._wrapper.update_from_tmp_copy(p2.encode())
        




# File Methods



    def commit(self):
        """
        Commit any changes to the map template to disk
        """
        self._wrapper.commit()
        



    @classmethod
    def create(cls, p1, p2, p3):
        """
        Create a :class:`geosoft.gxapi.GXMAPTEMPLATE` from an existing file.

        **Note:**

        The base template name should be the file name part of a geosoft_maptemplate
        file in the <geosoft>\\maptemplate or <geosoftuser>\\maptemplate folders. A base file
        in the user folder will override any in the Geosoft install dir.
        """
        ret_val = gxapi_cy.WrapMAPTEMPLATE.create(GXContext._get_tls_geo(), p1.encode(), p2.encode(), p3)
        return GXMAPTEMPLATE(ret_val)






    def discard(self):
        """
        Discard all changes made to the map template and reload from disk.
        """
        self._wrapper.discard()
        




    def get_file_name(self, p2):
        """
        Get the file name of the map template.
        """
        p2.value = self._wrapper.get_file_name(p2.value.encode())
        




# Map Making



    def create_map(self, p2, p3):
        """
        Create a map from the map template
        """
        self._wrapper.create_map(p2.encode(), p3.encode())
        




# Render/Preview



    def refresh(self):
        """
        Refresh the map template with any newly saved items
        """
        self._wrapper.refresh()
        




    def render_preview(self, p2, p3, p4, p5, p6):
        """
        Create a preview of the map template onto a
        Windows DC handle
        """
        self._wrapper.render_preview(p2, p3, p4, p5, p6)
        




    def render_preview_map_production(self, p2, p3, p4, p5, p6):
        """
        Render a preview for map sheet production purposes

        **Note:**

        This method can also be used to get the data view pixel location
        by passing a null DC handle. This help to plot the view contents
        preview from another location.
        """
        p3.value, p4.value, p5.value, p6.value = self._wrapper.render_preview_map_production(p2, p3.value, p4.value, p5.value, p6.value)
        





### endblock ClassImplementation
### block ClassExtend
# NOTICE: The code generator will not replace the code in this block
### endblock ClassExtend


### block Footer
# NOTICE: The code generator will not replace the code in this block
### endblock Footer