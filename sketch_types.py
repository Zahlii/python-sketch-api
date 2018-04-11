import base64
import secrets
from enum import Enum
from typing import NewType, Union, List, Dict

from biplist import readPlistFromString, writePlistToString


class SJRect:
    def __init__(self):
        self._class: str = 'rect'
        self.constrainProportions: bool = False
        self.x: float = None
        self.y: float = None
        self.width: float = None
        self.height: float = None


SJObjectId = NewType('SJObjectId', str)


def get_object_id():
    p = '00CC4CF3-9934-4ED2-9A53-5DD12A47F9B7'.split('-')
    o = []
    for part in p:
        x = int(len(part) / 2)
        o.append(secrets.token_hex(x))

    return '-'.join(o).upper()


class SJIDBase:
    def __init__(self):
        self.do_objectID: SJObjectId = None  # get_object_id()


SJStringRect = NewType('SJStringRect', str)


class SJColor:
    def __init__(self, r=None, g=None, b=None, a=1.0):
        self._class: str = 'color'
        self.red: float = r
        self.green: float = g
        self.blue: float = b
        self.alpha: float = a


class SJColorPalette:
    WHITE = SJColor(r=1.0, g=1.0, b=1.0)
    BLACK = SJColor(r=None, g=None, b=None)


class ResizingType(Enum):
    Stretch = 0
    PinToCorner = 1
    ResizeObject = 2
    FloatInPlace = 3


class LayerListExpandedType(Enum):
    Collapsed = 0
    ExpandedTemp = 1
    Expanded = 2


# https://github.com/turbobabr/sketch-constants/blob/master/src/index.js
class FillTypeEnum(Enum):
    Solid = 0
    Gradient = 1
    Pattern = 4
    Noise = 5


class GradientTypeEnum(Enum):
    Linear = 0
    Radial = 1
    Circular = 2


class PatternFillTypeEnum(Enum):
    Tile = 0
    Fill = 1
    Stretch = 2
    Fit = 3


class NoiseFillTypeEnum(Enum):
    Original = 0
    Black = 1
    White = 2
    Color = 3


class BorderLineCapStyle(Enum):
    Butt = 0
    Round = 1
    Square = 2


class BorderLineJoinStyle(Enum):
    Miter = 0
    Round = 1
    Bevel = 2


class LineDecorationTypeEnum(Enum):
    _None = 0
    OpenedArrow = 1
    ClosedArrow = 2
    Bar = 3


class BlurTypeEnum(Enum):
    GaussianBlur = 0
    MotionBlur = 1
    ZoomBlur = 2
    BackgroundBlur = 3


class BorderPositionEnum(Enum):
    Center = 0
    Inside = 1
    Outside = 2


class MaskModeEnum(Enum):
    Outline = 0
    Alpha = 1


class BooleanOperation(Enum):
    _None: -1
    Union = 0
    Subtract = 1
    Intersect = 2
    Difference = 3


class BlendModeEnum(Enum):
    Normal = 0
    Darken = 1
    Multiply = 2
    ColorBurn = 3
    Lighten = 4
    Screen = 5
    ColorDodge = 6
    Overlay = 7
    SoftLight = 8
    HardLight = 9
    Difference = 10
    Exclusion = 11
    Hue = 12
    Saturation = 13
    Color = 14
    Luminosity = 15


class ExportOptionsFormat(Enum):
    PNG = 'png'
    JPG = 'jpg'
    TIFF = 'tiff'
    PDF = 'pdf'
    EPS = 'eps'
    SVG = 'svg'


class ExportFormat:
    def __init__(self):
        self._class: str = 'exportFormat'
        self.absoluteSize: int = 0
        self.fileFormat: ExportOptionsFormat = 'png'
        self.name: str = ''
        self.namingScheme: int = 0
        self.scale: int = 1
        self.visibleScaleType: int = 0


class TextAlignmentEnum(Enum):
    Left = 0
    Right = 1
    Center = 2
    Justified = 3


class CurveMode(Enum):
    Straight = 1
    Mirrored = 2
    Disconnected = 4
    Asymmetric = 3


class SJBorder:
    def __init__(self):
        self._class: str = 'border'
        self.isEnabled: bool = True
        self.color: SJColor = SJColorPalette.BLACK
        self.fillType: FillTypeEnum = FillTypeEnum.Solid
        self.position: BorderPositionEnum = BorderPositionEnum.Outside
        self.thickness: float = 1.0


FloatList = List[float]


class SJBorderOptions:
    def __init__(self):
        self._class: str = 'borderOptions'
        self.isEnabled: bool = True
        self.dashPattern: FloatList = []
        self.lineCapStyle: BorderLineCapStyle = BorderLineCapStyle.Round
        self.lineJoinStyle: BorderLineJoinStyle = BorderLineJoinStyle.Round


class SJFill:
    def __init__(self):
        self._class: str = 'fill'
        self.isEnabled: bool = True
        self.color: SJColor = SJColorPalette.WHITE
        self.fillType: FillTypeEnum = FillTypeEnum.Solid
        self.image: SJImageDataReference = None
        self.noiseIndex: float = None
        self.noiseIntensity: float = None
        self.patternFillType: PatternFillTypeEnum = PatternFillTypeEnum.Fill
        self.patternTileScale: float = None


SJShadow__class = Enum('SJShadow__class', {"shadow": "shadow", "innerShadow": "innerShadow"})


class SJShadow_contextSettings:
    def __init__(self):
        self._class: str = 'graphicsContextSettings'
        self.blendMode: BlendModeEnum = BlendModeEnum.Color
        self.opacity: float = 1.0


class SJShadow:
    def __init__(self):
        self._class: SJShadow__class = 'shadow'
        self.isEnabled: bool = False
        self.blurRadius: float = None
        self.color: SJColor = SJColorPalette.BLACK
        self.contextSettings: SJShadow_contextSettings = {}
        self.offsetX: float = None
        self.offsetY: float = None
        self.spread: float = None


SJBorderList = List[SJBorder]
SJShadowList = List[SJBorder]
SJFillList = List[SJFill]


class SJStyle:
    def __init__(self):
        self._class: str = 'style'
        self.sharedObjectID: str = None
        self.borderOptions: SJBorderOptions = None
        self.borders: SJBorderList = None
        self.shadows: SJShadowList = None
        self.innerShadows: SJShadowList = None
        self.fills: SJFillList = None
        self.textStyle: SJTextStyle = None
        self.miterLimit: float = 10.0
        self.startDecorationType: LineDecorationTypeEnum = LineDecorationTypeEnum._None
        self.endDecorationType: LineDecorationTypeEnum = LineDecorationTypeEnum._None


class SJTextStyleAttribute:
    def __init__(self):
        self.MSAttributedStringFontAttribute: KeyValueArchive = None
        self.kerning: int = 0
        self.MSAttributedStringColorAttribute: SJColor = None
        self.paragraphStyle: KeyValueArchive = None


class SJTextStyle:
    def __init__(self):
        self._class: str = 'textStyle'
        self.verticalAlignment: TextAlignmentEnum = 0  # TODO enum?
        self.encodedAttributes: SJTextStyleAttribute = None


class SJSharedStyle(SJIDBase):
    def __init__(self):
        super().__init__()
        self._class: str = 'sharedStyle'
        self.name: str = ''
        self.value: SJStyle = SJStyle()


SJSharedStyleList = List[SJSharedStyle]


class SJSharedTextStyleContainer:
    def __init__(self):
        self._class: str = 'sharedTextStyleContainer'
        self.objects: SJSharedStyleList = []


class SJSharedStyleContainer:
    def __init__(self):
        self._class: str = 'sharedStyleContainer'
        self.objects: SJSharedStyleList = []


class SJSharedSymbolContainer:
    def __init__(self):
        self._class: str = 'sharedStyleContainer'
        self.objects: SJSharedStyleList = []  # TODO not clear


class ExportOptions:
    def __init__(self):
        self._class: str = 'exportOptions'
        self.exportFormats: List[ExportFormat] = []
        self.includedLayerIds: List = []
        self.layerOptions: float = None
        self.shouldTrim: bool = True


class RulerData:
    def __init__(self):
        self._class: str = 'rulerData'
        self.base: float = None
        self.guides: FloatList = []


class SJImageDataReference_data:
    def __init__(self):
        self._data: str = ''


class SJImageDataReference_sha1:
    def __init__(self):
        self._data: str = ''


class SJImageDataReference:
    def __init__(self):
        self._class: str = 'MSJSONOriginalDataReference'
        self._ref: str = ''
        self._ref_class: str = 'MSImageData'
        self.data: SJImageDataReference_data = {}
        self.sha1: SJImageDataReference_sha1 = {}


PointString = NewType('PointString', str)


class SJCurvePoint:
    def __init__(self):
        self._class: str = 'curvePoint'
        self.cornerRadius: float = 1.0
        self.curveFrom: PointString = None
        self.curveMode: CurveMode = CurveMode.Straight
        self.curveTo: PointString = None
        self.hasCurveFrom: bool = False
        self.hasCurveTo: bool = True
        self.point: PointString = None


SJCurvePointList = List[SJCurvePoint]


class SJPath:
    def __init__(self):
        self._class: str = 'path'
        self.isClosed: bool = True
        self.points: SJCurvePointList = []


class _SJLayerBase(SJIDBase):
    def __init__(self):
        super().__init__()
        self.name: str = ''
        self.nameIsFixed: bool = False
        self.isVisible: bool = True
        self.isLocked: bool = False
        self.layerListExpandedType: LayerListExpandedType = LayerListExpandedType.Collapsed
        self.hasClickThrough: bool = None
        self.layers: SJLayerList = None
        self.style: SJStyle = None
        self.isFlippedHorizontal: bool = False
        self.isFlippedVertical: bool = False
        self.rotation: float = None
        self.shouldBreakMaskChain: bool = False
        self.resizingType: ResizingType = ResizingType.Stretch
        self.exportOptions: ExportOptions = ExportOptions()
        self.includeInCloudUpload: bool = True
        self.backgroundColor: SJColor = None
        self.hasBackgroundColor: bool = None
        self.horizontalRulerData: RulerData = RulerData()
        self.verticalRulerData: RulerData = RulerData()
        self.includeBackgroundColorInExport: bool = None


class _SJArtboardBase(_SJLayerBase):
    def __init__(self):
        super().__init__()
        self.frame: SJRect = SJRect()




class SJSymbolMaster(_SJArtboardBase):
    def __init__(self):
        super().__init__()
        self._class: str = 'symbolMaster'
        self.includeBackgroundColorInInstance: bool = False
        self.symbolID: SJObjectId = None


class SJNestedSymbolOverride:
    def __init__(self):
        self.symbolID: SJObjectId = None


SJSymbolInstanceLayer_overrides = Dict[SJObjectId, Union[str, SJNestedSymbolOverride, SJImageDataReference]]


class SJSymbolInstanceLayer(_SJLayerBase):
    def __init__(self):
        super().__init__()
        self._class: str = 'symbolInstance'
        self.frame: SJRect = SJRect()
        self.horizontalSpacing: float = None
        self.verticalSpacing: float = None
        self.masterInfluenceEdgeMinXPadding: float = None
        self.masterInfluenceEdgeMaxXPadding: float = None
        self.masterInfluenceEdgeMinYPadding: float = None
        self.masterInfluenceEdgeMaxYPadding: float = None
        self.symbolID: SJObjectId = None
        self.overrides: SJSymbolInstanceLayer_overrides = None


class SJArtboardLayer(_SJArtboardBase):
    def __init__(self):
        super().__init__()
        self._class: str = 'artboard'


class SJTextLayer(_SJLayerBase):
    def __init__(self):
        super().__init__()
        self._class: str = 'text'
        self.attributedString: MSAttributedString = None
        self.glyphBounds: SJStringRect = None


class SJGroupLayer(_SJLayerBase):
    def __init__(self):
        super().__init__()
        self._class: str = 'group'


class SJShapeGroupLayer(_SJLayerBase):
    def __init__(self):
        super().__init__()
        self._class: str = 'shapeGroup'
        self.style: SJStyle = SJStyle()
        self.hasClippingMask: bool = False


SJShapeLayer__class = Enum('SJShapeLayer__class', {"rectangle": "rectangle", "oval": "oval", "shapePath": "shapePath"})


class SJShapeLayer(SJIDBase):
    def __init__(self):
        super().__init__()
        self._class: SJShapeLayer__class = 'rectangle'


EncodedBase64BinaryPlist = NewType('EncodedBase64BinaryPlist', str)


class KeyValueArchive:
    def __init__(self):
        self._archive: EncodedBase64BinaryPlist = EncodedBase64BinaryPlist('')
        self._raw: str = None  # cached copy of dict

    def get_archive(self):
        if self._raw is not None:
            return self._raw

        bstr = base64.b64decode(self._archive)
        a = readPlistFromString(bstr)
        self._raw = a
        return a

    def set_val(self, k: int, v):
        archive = self.get_archive()
        archive['$objects'][k] = v
        dt = writePlistToString(archive)
        bstr = base64.b64encode(dt)
        self._archive = bstr

    def get_val(self, val: int):
        return self.get_archive()['$objects'][val]

NSColorArchive = NewType('NSColorArchive', KeyValueArchive)


class MSAttributedString:
    def __init__(self):
        self._class: str = 'MSAttributedString'
        self.archivedAttributedString: KeyValueArchive = KeyValueArchive()

    def get_text(self):
        return self.archivedAttributedString.get_val(2)

    def set_text(self, string):
        self.archivedAttributedString.set_val(2, string)

    def get_color(self):
        r = self.archivedAttributedString.get_val(25)
        a = self.archivedAttributedString.get_val(26)
        b = self.archivedAttributedString.get_val(27)
        g = self.archivedAttributedString.get_val(28)
        ret = SJColor()
        ret.alpha = a
        ret.red = r
        ret.green = g
        ret.blue = b

        return ret

    def set_color(self, color: SJColor):
        self.archivedAttributedString.set_val(25, color.red)
        self.archivedAttributedString.set_val(26, color.alpha)
        self.archivedAttributedString.set_val(27, color.blue)
        self.archivedAttributedString.set_val(28, color.green)

    def get_font_size(self):
        return self.archivedAttributedString.get_val(16)

    def set_font_size(self, size: float):
        self.archivedAttributedString.set_val(16, size)

    def set_font_family(self, family: str):
        self.archivedAttributedString.set_val(17, family)

    def get_font_family(self):
        return self.archivedAttributedString.get_val(17)


class MSJSONFileReference:
    def __init__(self):
        self._class: str = 'MSJSonFileReference'
        self._ref_class: str = 'MSImmutablePage'
        self._ref: str = ''  # i.e. pages/doObjectID


class SJImageLayer(_SJLayerBase):
    def __init__(self):
        super().__init__()
        self._class: str = 'bitmap'
        self.clippingMask: SJStringRect = SJStringRect('{{0, 0}, {1, 1}}')
        self.fillReplacesImage: bool = False
        self.image: MSJSONFileReference = MSJSONFileReference()


SJLayer = Union[
    SJImageLayer, SJArtboardLayer, SJTextLayer, SJGroupLayer, SJShapeGroupLayer, SJShapeLayer, SJSymbolInstanceLayer]
SJLayerList = List[SJLayer]


class SJImageCollection:
    def __init__(self):
        self._class: str = 'imageCollection'
        self.images: dict = {}  # TODO


SJColorList = List[SJColor]


class SJAssetCollection:
    def __init__(self):
        self._class: str = 'assetCollection'
        self.colors: SJColorList = []
        self.gradients: List = []  # TODO
        self.images: List = []  # TODO
        self.imageCollection: SJImageCollection = SJImageCollection()


MSJSONFileReferenceList = List[MSJSONFileReference]


# document.json
class SketchDocument(SJIDBase):
    def __init__(self):
        super().__init__()
        # TODO document
        self._class: str = 'document'
        self.colorSpace: int = 0
        self.currentPageIndex: int = 0
        self.foreignSymbols = []
        self.assets: SJAssetCollection = {}

        self.layerTextStyles: SJSharedTextStyleContainer = []
        self.layerStyles: SJSharedStyleContainer = []
        self.layerSymbols: SJSharedSymbolContainer = []

        self.pages: MSJSONFileReferenceList = []
        self.userInfo: dict = None  # TODO


# pages/doObjectID.json
class SketchPage(_SJLayerBase):
    def __init__(self):
        super().__init__()
        self._class: str = 'page'
        self.exportOptions: ExportOptions = ExportOptions()
        self.frame: SJRect = SJRect()
        self.resizingConstraint: int = 0  # TODO
        self.horizontalRulerData: RulerData = RulerData()
        self.verticalRulerData: RulerData = RulerData()

    def get_ref(self):
        return 'pages/%s.json' % self.do_objectID


class SketchUserDataEntry:
    def __init__(self):
        self.scrollOrigin: PointString = None
        self.zoomValue: float = None
        self.pageListHeight: int = None


class SJArtboardDescription:
    def __init__(self):
        self.name: str = ''


SJPageArtboardMappingEntryDict = Dict[SJObjectId, SJArtboardDescription]


class SJPageArtboardMappingEntry:
    def __init__(self):
        self.name: str = ''
        self.artboards: SJPageArtboardMappingEntryDict = []


# user.json
SketchUserData = Dict[SJObjectId, SketchUserDataEntry]
SJPageArtboardMapping = Dict[SJObjectId, SJPageArtboardMappingEntry]  # PageID => Artboards


class SketchCreateMeta:
    def __init__(self):
        self.compatibilityVersion: int = 93
        self.build: int = 51160
        self.app: str = 'com.bohemiancoding.sketch3'
        self.autosaved: int = None
        self.variant: str = 'NONAPPSTORE'
        self.commit: str = ''
        self.version: int = 101
        self.appVersion: str = '49'


StrList = List[str]


# meta.json
class SketchMeta(SketchCreateMeta):
    def __init__(self):
        super().__init__()
        self.pagesAndArtboards: SJPageArtboardMapping = {}
        self.fonts: StrList = []

        self.created: SketchCreateMeta = SketchCreateMeta()
        self.saveHistory: StrList = []  # Entries are variant.build
