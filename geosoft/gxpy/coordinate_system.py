import json
import geosoft
import geosoft.gxapi as gxapi
from . import utility as gxu
from . import dataframe as gxdf

__version__ = geosoft.__version__


def _t(s):
    return geosoft.gxpy.system.translate(s)

#############
# Constants

# 'HCS' and 'hcs' refer to Horizontal Coordinate System
# 'VCS' and 'vcs' refer to Vertical Coordinate System

NAME = None
NAME_HCS = gxapi.IPJ_NAME_PCS
NAME_PROJECTION = gxapi.IPJ_NAME_PROJECTION
NAME_METHOD = gxapi.IPJ_NAME_METHOD
NAME_DATUM = gxapi.IPJ_NAME_DATUM
NAME_ELLIPSOID = gxapi.IPJ_NAME_ELLIPSOID
NAME_LDATUM = gxapi.IPJ_NAME_LDATUM
NAME_UNIT = gxapi.IPJ_NAME_UNIT_ABBR
NAME_UNIT_FULL = gxapi.IPJ_NAME_UNIT_FULL
NAME_TYPE = gxapi.IPJ_NAME_TYPE
NAME_LLDATUM = gxapi.IPJ_NAME_LLDATUM
NAME_METHOD_PARMS = gxapi.IPJ_NAME_METHOD_PARMS
NAME_METHOD_LABEL = gxapi.IPJ_NAME_METHOD_LABEL
NAME_DATUM_PARMS = gxapi.IPJ_NAME_DATUM_PARMS
NAME_LDATUM_PARMS = gxapi.IPJ_NAME_LDATUM_PARMS
NAME_GEOID = gxapi.IPJ_NAME_GEOID
NAME_LDATUMDESCRIPTION = gxapi.IPJ_NAME_LDATUMDESCRIPTION
NAME_METHOD_PARMS_NATIVE = gxapi.IPJ_NAME_METHOD_PARMS_NATIVE
NAME_ORIENTATION = gxapi.IPJ_NAME_ORIENTATION_PARMS
NAME_VCS = -1
NAME_HCS_VCS = -2

LIST_COORDINATESYSTEM = gxapi.IPJ_PARM_LST_COORDINATESYSTEM
LIST_DATUM = gxapi.IPJ_PARM_LST_DATUM
LIST_PROJECTION = gxapi.IPJ_PARM_LST_PROJECTION
LIST_UNITS = gxapi.IPJ_PARM_LST_UNITS
LIST_UNITSDESCRIPTION = gxapi.IPJ_PARM_LST_UNITSDESCRIPTION
LIST_LOCALDATUMDESCRIPTION = gxapi.IPJ_PARM_LST_LOCALDATUMDESCRIPTION
LIST_LOCALDATUMNAME = gxapi.IPJ_PARM_LST_LOCALDATUMNAME

PARM_DATUM = 'datum'
PARM_PROJECTION = 'transform'
PARM_UNITS = 'units'
PARM_LOCAL_DATUM = 'datumtrf'

class CSException(Exception):
    '''
    Exceptions from this module.

    .. versionadded:: 9.2
    '''
    pass

def parameters(what, key):
    """
    Get a dictionary of parameters for a coordinate system item.

    :param what:
            | gxipj.PARM_DATUM
            | gxipj.PARM_PROJECTION
            | gxipj.PARM_UNITS
            | gxipj.LOCAL_DATUM
    :param key:     parameter key to find and return
    :raises CSException: if table or key not found.

    .. versionadded:: 9.2
    """

    try:
        dct = gxdf.table_record(what, key)
    except gxdf.DfException as e:
        raise CSException(str(e))
    return dct

def parameter_exists(what, key):
    """
    Test if a parameter set exists in a coordinate system table.
    :param what:    see parameters()
    :param key:     parameter key
    :return: True if table/key exists
    """
    try:
        parameters(what, key)
    except CSException:
        return False
    else:
        return True

def name_list(what, datum_filter=''):
    """
    Get a list of coordinate system names

    :param what:
            | gxipj.LIST_COORDINATESYSTEM
            | gxipj.LIST_DATUM
            | gxipj.LIST_PROJECTION
            | gxipj.LIST_UNITS
            | gxipj.LIST_LOCALDATUMDESCRIPTION
            | gxipj.LIST_LOCALDATUMNAME
            | gxipj.LIST_UNITSDESCRIPTION

    :param datum_filter:
            name of a datum to filter results

    :returns:   sorted list of names

    .. versionadded:: 9.2
    """

    lst = gxapi.GXLST.create(1000)
    gxapi.GXIPJ.get_list(what, datum_filter, lst)
    namelist = list(gxu.dict_from_lst(lst))
    namelist.sort(key=str.lower)
    return namelist


def hcs_orient_vcs_from_name(name):
    """
    Split a full coordinate system name into its components. A name has the form "hcs <orient> [vcs]"
    :param name:
    :return: hcs, orient, vcs

    .. versionadded:: 9.1
    """

    def extract( s, frame):
        c1, c2, *_ = frame
        s = s.strip(' \t"\'')
        end = s.rfind(c2)
        if end > 1:
            start = s.rfind(c1)
            sub = s[start + 1: end]
            s = s[:start] + s[end+1:]
        else:
            sub = ''
        return s.strip(' \t"\''), sub.strip(' \t"\'')

    name, vcs = extract(name, '[]')
    hcs, orient = extract(name, '<>')

    return hcs, orient, vcs


def name_from_hcs_orient_vcs(hcs, orient=None, vcs=None):
    """
    Cpnstruct a coordinate system name from an hcs, orientation and vcs.  If orient or vcs are None or
    empty, the name will not include these parts.

    :param hcs:     horizontal coordinate system string
    :param orient:  orientation string
    :param vcs:     vertical coordinate system string
    :return: "hcs <orient> [vcs]"

    .. versionadded:: 9.2
    """

    if orient:
        orient = ' <' + orient + '>'
    else:
        orient = ''

    if vcs:
        vcs = ' [' + vcs + ']'
    else:
        vcs = ''

    return hcs + orient + vcs

def list_from_wktsrs(wkt):
    """ return a list from a wkt spatial reference string """

    def first_item(wkt):
        n = 0
        i = 0
        for c in wkt:
            if n == 0 and c == ',':
                return wkt[:i].strip(' '), wkt[i + 1:].strip(' ')
            i += 1
            if c == '[':
                n += 1
            elif c == ']':
                n -= 1
        return wkt.strip(' '), ''

    def parse_item(wkt):
        if wkt[0] == '"':
            return wkt[1:-1]

        if '[' in wkt:
            bkt = wkt.find('[')
            items = list_from_wktsrs(wkt[bkt + 1:-1])
            dct = {'key': wkt[:bkt], 'name': items[0]}
            if len(items) > 1:
                dct['items'] = items[1:]
            return dct

        return wkt

    wkt = wkt.strip()
    wktlst = []
    while wkt:
        first, wkt = first_item(wkt)
        wktlst.append(parse_item(first))

    return wktlst

def find_key(wkt, k):
    """ Find a key in the wkt, return it's name and items"""

    for w in wkt:
        if type(w) is dict:
            if w['key'] == k:
                return w['name'], w.get('items', [])

            # try the kids
            name, items = find_key(w.get('items', []), k)
            if name:
                return name, items

    return '', []

def wkt_vcs(vcs):
    """ compose a wkt VERTCS block from a Geosoft vcs string."""
    return 'VERTCS["' + vcs + '"]'

class Wkt:
    """ Helper class to parse WKT-formatted spatial reference strings"""

    def __repr__(self):
        return "{}({})".format(self.__class__, self.__dict__)

    def __str__(self):
        return self.name()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __init__(self, wkt):

        self._wkt = list_from_wktsrs(wkt)

        self.pcs, _ = find_key(self._wkt, 'PROJCS')
        self.gcs, _ = find_key(self._wkt, 'GEOGCS')
        self.vcs, _ = find_key(self._wkt, 'VERTCS')

    def name(self):
        """ return the ESRI name for the coordinate system"""

        if self.pcs:
            name = self.pcs
        else:
            name = self.gcs
        if self.vcs:
            name += ' [{}]'.format(self.vcs)

        return name.strip()

    def find_key(self, k):
        """
        Return the name and list of items for a key
        :param k:   the key to look for in the wkt
        :return:    name ('' if not found), list of parameters, ([] if no items)
        """
        return find_key(self._wkt, k)

class GXcs:
    """
    Coordinate system class. A coordinate system defines a horizontal and vertical reference
    system to locate (x, y, z) cartesian coordinates relative to the Earth.

    :param vcs:     The vertical coordinate system as a descriptive name.
    :param hcs:     The horizontal coordinate system as a Geosoft name string (ie. "WGS 84 / UTM zone 32N")
                    an ESRI WKT string (ie. "PROJCS["WGS_1984_UTM_Zone_35N",GEOGCS[..."), a dictionary that
                    contains the coordinate system properties, a JSON string that contains the coordinate
                    system properties, or a list that contains the 5 GXF coordinate system strings.
                    You can also pass a gxapi.GXIPJ.
    :param init:    `True` to initalize immediated, `False` te delay initialization until used.

    Dictionary structure:
    
        :Geosoft: (http://www.geosoft.com/resources/goto/GXF-Grid-eXchange-File)

        .. code::

            {   "type": "Geosoft",
                "name": name
                "datum": datum
                "method": method
                "units": units
                "local_datum": local datum transform
                "orientation": x0, y0, z0, xR, yR, zR
                "vcs": "vertical coordinate system"
            }

        See see http://www.geosoft.com/resources/goto/GXF-Grid-eXchange-File for GXF string reference

        :EPSG: (http://spatialreference.org/)

            .. code::

                {   "type": "EPSG"
                    "code": EPSG_code_number
                    "orientation": x0, y0, z0, xR, yR, zR
                }

        :ESRI: (http://webhelp.esri.com/arcgisserver/9.3/java/index.htm#geodatabases/the_ogc-607957855.htm)

            .. code::

                {   "type": "ESRI",
                    "wkt": wkt format string, starts with "PROJCS[" or "GEOGCS["
                    "orientation": x0, y0, z0, xR, yR, zR
                    "vcs": "vertical coordinate system"
                }

    .. versionadded:: 9.2
        supercedes `ipj` module.
    """

    def __repr__(self):
        return "{}({})".format(self.__class__, self.__dict__)

    def __str__(self):
        if self._gxapi_ipj:
            return self.name(NAME_HCS_VCS)
        else:
            return str(self._init_ipj)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __init__(self, hcs=None, vcs=None, init=False):
        self._init_ipj = hcs
        self._gxapi_ipj = None
        self._dict = None
        self._vcs = vcs
        if init:
            self._setup_ipj()
            self._setup_vcs(vcs)

    def __eq__(self, other):
        return self.same_as(other)

    def _setup_ipj(self):
        """ Setup the horizontal coordinate system. """
        if self._gxapi_ipj is None:
            self._gxapi_ipj = gxapi.GXIPJ.create()
            if type(self._init_ipj) is gxapi.GXIPJ:
                s1 = gxapi.str_ref()
                s2 = gxapi.str_ref()
                s3 = gxapi.str_ref()
                s4 = gxapi.str_ref()
                s5 = gxapi.str_ref()
                self._init_ipj.get_gxf(s1, s2, s3, s4, s5)
                self._from_gxf((s1.value, s2.value, s3.value, s4.value, s5.value))
            else:
                if self._init_ipj is not None:
                    if isinstance(self._init_ipj, str):
                        self._from_str(self._init_ipj)
                    elif isinstance(self._init_ipj, dict):
                        self._from_dict(self._init_ipj)
                    else:
                        self._from_gxf(self._init_ipj)
            self._init_ipj = None

    def _setup_vcs(self, vcs):
        """ setup the vertical coordinate system """
        self._vcs = vcs

    @property
    def gxipj(self):
        """ gxapi.GXIPJ instance"""
        if self._gxapi_ipj is None:
            self._setup_ipj()
        return self._gxapi_ipj

    @property
    def cs(self):
        """ coordinate system name as 'hcs [vcs]' """
        return self.name(NAME_HCS_VCS)

    @property
    def hcs(self):
        """ horizontal coordinate system name"""
        return self.name(NAME_HCS)
                
    @property
    def vcs(self):
        """ vertical coordinate system name"""
        return self.name(NAME_VCS)

    def same_hcs(self, other):
        """ Return true if the HCS are the same."""
        def same_units(a, b):
            a = a.coordinate_dict['units']
            b = b.coordinate_dict['units']
            if not (a and b):
                return True
            else:
                return a == b

        if not same_units(self, other):
            return False
        elif (self.hcs == '*unknown') or (other.hcs == '*unknown'):
            return True
        else:
            return bool(self.gxipj.coordinate_systems_are_the_same(other.gxipj))

    def same_vcs(self, other):
        """ Return true if the VCS are the same."""
        svcs = self.vcs
        ovcs = other.vcs
        if (svcs == '') or (ovcs == ''):
            return True
        else:
            return svcs == ovcs

    def same_as(self, other):
        """ Return true if both coordinate systems (HCS and VCS) are the same. """
        return self.same_hcs(other) and self.same_vcs(other)

    def _from_str(self, cstr):
        """ setup coordinate systems from a string """
        
        # json string
        if cstr[0] == '{':
            try:
                jsondict = json.loads(cstr)
            except ValueError:
                # try replacing single quotes
                jstr = cstr.replace('"', '\\"').replace("'", '"')
                try:
                    jsondict = json.loads(jstr)
                except ValueError:
                    raise ValueError(_t('"Invalid JSON coordinate system string: "{}"').format(cstr))
                
            self._from_dict(jsondict)

        # ESRI WKT
        elif 'GEOGCS[' in cstr:
            self.gxipj.set_esri(cstr)
            self._vcs, _ = Wkt(cstr).find_key('VERTCS')

        else:
            self._from_gxf([cstr, '', '', '', ''])

    def _from_gxf(self, gxfs):

        def raise_gxf_error():
            raise CSException(_t('Unknown coordinate system:' +
                                 '\n       name> {}' +
                                 '\n      datum> {}' +
                                 '\n projection> {}' +
                                 '\n      units> {}' +
                                 '\nlocal datum> {}')
                              .format(gxfs[0], gxfs[1], gxfs[2], gxfs[3], gxfs[4]))

        gxf1, gxf2, gxf3, gxf4, gxf5 = gxfs

        hcs, orient, vcs = hcs_orient_vcs_from_name(gxf1)
        gxf1 = name_from_hcs_orient_vcs(hcs, orient, '')
        
        # if we get a name only, and it has a datum and projection, copy these.
        # The challenge with a name only is that the "datum / projection" must exist as
        # a known coordinate system, otherwise we cannot resolve it.  Users some times
        # combine projections with different datums so copying the values allows for this

        if (gxf2 == '') and (gxf3 == '') and ('/' in gxf1):
            datum, projection, *_ = gxf1.strip('"').split('/')
            gxf2 = datum.strip()
            gxf3, orient, _ = hcs_orient_vcs_from_name(projection)

        # get ipj from gxf, error if unknown
        sref = gxapi.str_ref()

        if not (gxf2 or gxf3 or gxf4 or gxf5) and parameter_exists(PARM_UNITS, gxf1):
            # units only
            self.gxipj.set_gxf('', '', '', gxf1, '')
        else:
            try:
                self.gxipj.set_gxf(gxf1, gxf2, gxf3, gxf4, gxf5)
                self.gxipj.get_display_name(sref)
            except (geosoft.gxapi.GXAPIError, geosoft.gxapi.GXError):
                raise_gxf_error()
            else:
                if gxf1 != "*unknown":
                    if (sref.value == '*unknown') and (gxf2 or gxf3 or gxf5):
                        raise_gxf_error()

        if vcs:
            self._setup_vcs(vcs)


    def _from_dict(self, csdict):
        """
        Create an IPJ from a dictionary.

        .. versionadded:: 9.2
        """

        cstype = csdict.get('type', '').lower()
        if (not cstype) or (cstype == 'geosoft'):
            s1, orient, vcs = hcs_orient_vcs_from_name(csdict.get('name', ''))
            orient = csdict.get('orientation', orient)
            vcs = csdict.get('vcs', vcs)
            s1 = name_from_hcs_orient_vcs(s1, orient, vcs)
            s2 = csdict.get('datum', '')
            s3 = csdict.get('projection', '')
            s4 = csdict.get('units', '')
            s5 = csdict.get('local_datum', '')
            self._from_gxf([s1, s2, s3, s4, s5])

        elif cstype == 'esri':
            wkt = csdict.get('wkt', None)

            if wkt is None:
                raise ValueError("'ESRI missing 'wkt' property.")
            
            # add vertical datum reference from dict if not in the wkt
            vcs = csdict.get('vcs','')
            if vcs and ('VERTCS[' not in wkt):
                wkt += wkt_vcs(vcs)

            # clear any existing coordinate system - bug GX does not clear prior orientation
            self.gxipj.set_gxf('WGS 84 <0,0,0,0,0,0>', '', '', '', '')
            self.gxipj.set_esri(wkt)

            # add orientation and vcs
            orient = csdict.get('orientation', '')
            if orient or vcs:
                gxfs = self.gxf()
                gxfs[0] = name_from_hcs_orient_vcs(gxfs[0], orient, vcs)
                self._from_gxf(gxfs)

        elif cstype == "epsg":
            code = csdict.get('code', None)
            if code is None:
                raise ValueError("'EPSG missing 'code' property.")
            orient = csdict.get('orientation', '')
            self._from_gxf([str(code) + orient, '', '', '', ''])

        elif cstype == 'localgrid':
            # must at least have a latitude and longitude
            lat = csdict.get('latitude', None)
            lon = csdict.get('longitude', None)
            if (lat is None) or (lon is None):
                raise ValueError("'Localgrid must define latitude and longitude properties of the local origin.")
            sf = csdict.get('scalefactor', 0.9996)

            # TODO figure this out with Stephen for 9.2
            
            datum = csdict.get('datum', 'WGS 84')
            proj = '"Oblique Stereographic",' + str(lat) + ',' + str(lon) + ',' + str(sf) + ',0,0'.replace('"', '\\"')
            units = csdict.get('units', 'm')
            ldatum = csdict.get('ldatum', '')
            azimuth = csdict.get('azimuth', 0.0)
            elevation = csdict.get('elevation', 0.0)
            if (azimuth == 0.0) and (elevation == 0.0):
                orient = ''
            else:
                orient = '0,0,' + str(elevation) + ',0,0,' + str(azimuth)

            # construct a name
            name = name_from_hcs_orient_vcs(datum + ' / *Local (' + str(lat) + ',' + str(lon) + ')', orient, '')
            self._from_gxf([name, datum, proj, units, ldatum])

        else:
            raise ValueError("Projection type '{}' not supported.".format(cstype))

    @property
    def coordinate_dict(self):
        """
        Dictionary of coordinate system attributes.

        .. versionadded:: 9.2
        """

        if self._dict is None:

            # initially from GXF values
            gxf1, gxf2, gxf3, gxf4, gxf5 = self.gxf()
            hcs, orient, vcs = hcs_orient_vcs_from_name(gxf1)
            self._dict = {"type": "Geosoft",
                         "name": gxf1,
                         "datum": gxf2,
                         "projection": gxf3,
                         "units": gxf4,
                         "local_datum": gxf5,
                         "orientation": orient,
                         "vcs": vcs
                         }

        return self._dict

    def gxf(self):
        """
        Get GXF string list from ipj.
        Returns list of 5 GXF strings.

        .. versionadded:: 9.2
        """

        s1 = gxapi.str_ref()
        s2 = gxapi.str_ref()
        s3 = gxapi.str_ref()
        s4 = gxapi.str_ref()
        s5 = gxapi.str_ref()
        self.gxipj.get_gxf(s1, s2, s3, s4, s5)
        lst = [s1.value.replace('"', ' ').strip(), s2.value, s3.value, s4.value, s5.value]
        return lst

    def name(self, what=None):
        """
        Return requested name.

        :param what:
                | gxipj.NAME
                | gxipj.NAME_HCS
                | gxapi.NAME_VCS
                | gxapi.NAME_HCS_VCS
                | gxipj.NAME_PROJECTION
                | gxipj.NAME_METHOD
                | gxipj.NAME_DATUM
                | gxipj.NAME_ELLIPSOID
                | gxipj.NAME_LDATUM
                | gxipj.NAME_UNIT
                | gxipj.NAME_UNIT_FULL
                | gxipj.NAME_TYPE
                | gxipj.NAME_LLDATUM
                | gxipj.NAME_METHOD_PARMS
                | gxipj.NAME_METHOD_LABEL
                | gxipj.NAME_DATUM_PARMS
                | gxipj.NAME_LDATUM_PARMS
                | gxipj.NAME_GEOID
                | gxipj.NAME_LDATUMDESCRIPTION
                | gxipj.NAME_METHOD_PARMS_NATIVE
                | gxipj.NAME_ORIENTATION

        If 'what' is not specified, gxipj.NAME assumed, which returns the coordinate system display name.

        :return: The name requested

        .. versionadded:: 9.2
        """

        sref = gxapi.str_ref()
        if what is None:
            self.gxipj.get_display_name(sref)
        else:

            if what == NAME_VCS:
                return str(self._vcs if self._vcs else '')

            elif what == NAME_HCS_VCS:
                # self.gxipj.get_name(NAME_HCS, sref)
                self.gxipj.get_display_name(sref)
                if self._vcs:
                    return "{} [{}]".format(sref.value, str(self._vcs))
                else:
                    return sref.value
            else:
                self.gxipj.get_name(what, sref)

        return sref.value

    def units(self):
        """
        :return: tuple (factor, abbreviation), where factor is multiplier to convert to metres

        .. versionadded:: 9.2
        """

        sref = gxapi.str_ref()
        fref = gxapi.float_ref()
        self.gxipj.get_units(fref, sref)
        return fref.value, sref.value


class GXpj:
    """
    Class to reproject coordinates.

    :params cs_from:  GXcs from coordinate system
    :params cs_to:    GXcs to coordinate system

    .. versionadded:: 9.2
    """

    def __repr__(self):
        return "{}({})".format(self.__class__, self.__dict__)

    def __str__(self):
        return "PJ from \'{}\' to \'{}\'".format(str(self._cs_from), str(self._cs_to))

    _cs_from = None
    _cs_to = None
    _sr = gxapi.str_ref()

    def __init__(self, cs_from, cs_to):
        self._cs_from = cs_from
        self._cs_to = cs_to
        self._pj = gxapi.GXPJ.create_ipj(cs_from.gxipj, cs_to.gxipj)

    def convert(self, xyz):
        """
        Project data in array in which first columns are x,y or x,y,z.

        Coordinates are reprojected in-place.

        :param xyz:
                | numpy array shape (,3+) for (x,y,z) conversion
                | numpy array shape (,2) for x,y conversion

        :example:
            Given an array shape (500,6), which represents 500 data records with 6 columns
            in which the first 3 columns are coordinates X, Y and Z.

            .. code::

                data = np.zeros((10,5), dtype='float') #then fill the array with some data

                pj.convert(data[:,2])       #transform x,y
                pj.convert(data[:,3])       #transform x,y and z
                pj.convert(data)            #transform x,y and z (same as previous line)

        .. versionadded:: 9.2
        """

        npoints = xyz.shape[0]
        if npoints == 0:
            return

        nd = xyz.shape[1]
        if nd < 2:
            raise CSException(_t('Data must have minimum dimension 2 (x,y) or 3 for (x,y,z).'))

        vvx = gxapi.GXVV.create_ext(gxapi.GS_DOUBLE, npoints)
        vvy = gxapi.GXVV.create_ext(gxapi.GS_DOUBLE, npoints)
        vvx.set_data_np(0, xyz[:, 0])
        vvy.set_data_np(0, xyz[:, 1])

        if nd >= 3:
            vvz = gxapi.GXVV.create_ext(gxapi.GS_DOUBLE, npoints)
            vvz.set_data_np(0, xyz[:, 2])
            self._pj.convert_vv3(vvx, vvy, vvz)
            xyz[:, 2] = vvz.get_data_np(0, npoints, 'f8')
        else:
            self._pj.convert_vv(vvx, vvy)

        xyz[:, 0] = vvx.get_data_np(0, npoints, 'f8')
        xyz[:, 1] = vvy.get_data_np(0, npoints, 'f8')