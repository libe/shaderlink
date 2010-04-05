##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

import os
import copy
import re

from PyQt4 import QtCore

class Property(QtCore.QObject):    
    Input = 0
    Output = 1
    
    def __init__(self):
        QtCore.QObject.__init__(self)
        
        self.name = ''
        self.category = ''
        self.hint = '' 
        self.value = None
        self.isShaderParameter = False        

    def typeToStr(self):
        assert 0, 'typeToStr needs to be implemented!'
    
    def encodedStr(self):
        assert 0, 'encodedStr needs to be implemented!'

    def valueFromStr(self, str):
        assert 0, 'valueFromStr needs to be implemented!'

    def valueToStr(self):
        assert 0, 'valueToStr needs to be implemented!'
        
    def copy(self):
        assert 0, 'copy needs to be implemented!'
        
    def fireChanged(self):
        self.emit(QtCore.SIGNAL('propertyChanged()'))
        
class ColorProperty(Property):
    @classmethod
    def fromAttributeStrings(cls, name, category, hint, value):
        property = cls()
        property.name = name
        property.category = category
        property.hint = hint
        property.value = property.valueFromStr(value)
        
        return property
    
    def __init__(self):
        Property.__init__(self)

    def __getstate__(self):
        state = {}
        
        # save state
        state['name'] = self.name
        state['category'] = self.category
        state['hint'] = self.hint
        state['value'] = self.value
        state['isShaderParameter'] = self.isShaderParameter
        
        return state

    def __setstate__(self, state):
        self.__init__()
        
        # restore state
        for k, v in state.iteritems():
            setattr(self, k, v)
        
    def typeToStr(self):
        return 'color'
    
    def encodedStr(self):
        return 'C'

    def valueFromStr(self, str):
        if str == '': 
            return [1.0, 1.0, 1.0] # default
        else:
            str = str.replace(' ', '')
            p = re.compile('color\(([+]?([0-9]*\.)?[0-9]+,){2}[+]?([0-9]*\.)?[0-9]+\)')             
            match = p.match(str)
            if match:
                p = re.compile('[+]?[0-9]*\.?[0-9]+')
                f = p.findall(str) 
                f = map(float, f)               
                return [f[0], f[1], f[2]]
            else:
                raise Exception('Cannot parse color property %s values' % (self.name))        

    def valueToStr(self):
        return 'color(' + ''.join('%.3f' % f + ',' for f in self.value[: - 1]) + '%.3f' % self.value[ - 1] + ')'

    def copy(self):
        newColorProperty = ColorProperty()
        
        # copy value
        newColorProperty.name = self.name
        newColorProperty.category = self.category
        newColorProperty.hint = self.hint
        newColorProperty.value = copy.deepcopy(self.value)
        newColorProperty.isShaderParameter = self.isShaderParameter
        
        return newColorProperty

class FloatProperty(Property):
    @classmethod
    def fromAttributeStrings(cls, name, category, hint, value):
        property = cls()
        property.name = name
        property.category = category
        property.hint = hint
        property.value = property.valueFromStr(value)
                
        return property
    
    def __init__(self):
        Property.__init__(self)

    def __getstate__(self):
        state = {}
        
        # save state
        state['name'] = self.name
        state['category'] = self.category
        state['hint'] = self.hint
        state['value'] = self.value
        state['isShaderParameter'] = self.isShaderParameter
        
        return state

    def __setstate__(self, state):
        self.__init__()
        
        # restore state
        for k, v in state.iteritems():
            setattr(self, k, v)

    def typeToStr(self):
        return 'float'
        
    def encodedStr(self):
        return 'F'

    def valueFromStr(self, str):
        if str == '': 
            return 0.0
        else:
            try:
                return float(str)
            except:
                raise Exception('Cannot parse float property %s values' % (self.name))

    def valueToStr(self):
        return '%.3f' % self.value

    def copy(self):
        newFloatProperty = FloatProperty()
                                         
        # copy value
        newFloatProperty.name = self.name
        newFloatProperty.category = self.category
        newFloatProperty.hint = self.hint    
        newFloatProperty.value = copy.deepcopy(self.value)
        newFloatProperty.isShaderParameter = self.isShaderParameter   
        
        return newFloatProperty

class MatrixProperty(Property):
    @classmethod
    def fromAttributeStrings(cls, name, category, hint, value):
        property = cls()
        property.name = name
        property.category = category
        property.hint = hint
        property.value = property.valueFromStr(value)
        
        return property
        
    def __init__(self):
        Property.__init__(self)

    def __getstate__(self):
        state = {}
        
        # save state
        state['name'] = self.name
        state['category'] = self.category
        state['hint'] = self.hint
        state['value'] = self.value
        state['isShaderParameter'] = self.isShaderParameter
        
        return state

    def __setstate__(self, state):
        self.__init__()
        
        # restore state
        for k, v in state.iteritems():
            setattr(self, k, v)

    def typeToStr(self):
        return 'matrix'

    def encodedStr(self):
        return 'M'

    def valueFromStr(self, str):
        if str == '':
            # default 
            return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
 
        else:
            str = str.replace(' ', '')
            p = re.compile('matrix\(([-+]?([0-9]*\.)?[0-9]+,){15}[-+]?([0-9]*\.)?[0-9]+\)') 
            match = p.match(str)
            if match:
                p = re.compile('[-+]?[0-9]*\.?[0-9]+')
                f = p.findall(str)                                
                f = map(float, f)
                return [f[0:4], f[4:8], f[8:12], f[12:16]]
            else:
                raise Exception('Cannot parse matrix property %s values' % (self.name))        

    def valueToStr(self):
        return 'matrix(' + ''.join('%.3f' % f + ',' for f in self.value[: - 1]) + '%.3f' % self.value[ - 1] + ')'

    def copy(self):
        newMatrixProperty = MatrixProperty()
        
        # copy value
        newMatrixProperty.name = self.name
        newMatrixProperty.category = self.category
        newMatrixProperty.hint = self.hint
        newMatrixProperty.value = copy.deepcopy(self.value)
        newMatrixProperty.isShaderParameter = self.isShaderParameter
        
        return newMatrixProperty

class PointProperty(Property):
    @classmethod
    def fromAttributeStrings(cls, name, category, hint, value, spaces):
        property = cls()
        property.name = name
        property.category = category
        property.hint = hint
        property.value = property.valueFromStr(value)
        
        if spaces != '':
            property.spaces = spaces.split(',')
        else:
            property.spaces = ['shader']
        
        property.spaceIndex = 0

        return property
    
    def __init__(self):        
        Property.__init__(self)
        
        # spaces
        self.spaces = None
        self.spaceIndex = None

    def __getstate__(self):
        state = {}
        
        # save state
        state['name'] = self.name
        state['category'] = self.category
        state['hint'] = self.hint
        state['spaces'] = self.spaces
        state['spaceIndex'] = self.spaceIndex
        state['value'] = self.value
        state['isShaderParameter'] = self.isShaderParameter
        
        return state

    def __setstate__(self, state):
        self.__init__()
        
        # restore state
        for k, v in state.iteritems():
            setattr(self, k, v)

    def typeToStr(self):
        return 'point'
        
    def encodedStr(self):
        return 'P'
    
    def valueFromStr(self, str):
        if str == '': 
            return [0.0, 0.0, 0.0] # default
        else:
            str = str.replace(' ', '')
            p = re.compile('point\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)') 
            match = p.match(str)
            if match:
                p = re.compile('[-+]?[0-9]*\.?[0-9]+')
                f = p.findall(str)                
                f = map(float, f)                
                return [f[0], f[1], f[2]]
            else:
                raise Exception('Cannot parse point property %s values' % (self.name))    

    def valueToStr(self):
        return 'point(' + ''.join('%.3f' % f + ',' for f in self.value[: - 1]) + '%.3f' % self.value[ - 1] + ')'

    def copy(self): 
        newPointProperty = PointProperty()
        
        # copy value        
        newPointProperty.name = self.name
        newPointProperty.category = self.category
        newPointProperty.hint = self.hint
        newPointProperty.value = copy.deepcopy(self.value)
        newPointProperty.spaceIndex = self.spaceIndex
        newPointProperty.spaces = copy.deepcopy(self.spaces)
        newPointProperty.isShaderParameter = self.isShaderParameter
                
        return newPointProperty
        
class VectorProperty(Property):
    @classmethod
    def fromAttributeStrings(cls, name, category, hint, value, spaces):
        property = cls()
        property.name = name
        property.category = category
        property.hint = hint
        property.value = property.valueFromStr(value)
        
        if spaces != '':
            property.spaces = spaces.split(',')
        else:
            property.spaces = ['shader']
        
        property.spaceIndex = 0

        return property
    
    def __init__(self):
        Property.__init__(self)

    def __getstate__(self):
        state = {}
        
        # save state
        state['name'] = self.name
        state['category'] = self.category
        state['hint'] = self.hint
        state['spaces'] = self.spaces
        state['spaceIndex'] = self.spaceIndex
        state['value'] = self.value
        state['isShaderParameter'] = self.isShaderParameter
        
        return state

    def __setstate__(self, state):
        self.__init__()
        
        # restore state
        for k, v in state.iteritems():
            setattr(self, k, v)

    def typeToStr(self):
        return 'vector'
    
    def encodedStr(self):
        return 'V'

    def valueFromStr(self, str):
        if str == '': 
            return [0.0, 0.0, 0.0] # default
        else:
            str = str.replace(' ', '')
            p = re.compile('vector\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)') 
            match = p.match(str)
            if match:
                p = re.compile('[-+]?[0-9]*\.?[0-9]+')
                f = p.findall(str)                
                f = map(float, f)                
                return [f[0], f[1], f[2]]
            else:
                raise Exception('Cannot parse vector property %s values' % (self.name))   

    def valueToStr(self):
        return 'vector(' + ''.join('%.3f' % f + ',' for f in self.value[: - 1]) + '%.3f' % self.value[ - 1] + ')'

    def copy(self):
        newVectorProperty = VectorProperty()

        # copy value
        newVectorProperty.name = self.name
        newVectorProperty.category = self.category
        newVectorProperty.hint = self.hint        
        newVectorProperty.value = copy.deepcopy(self.value)
        newVectorProperty.spaceIndex = self.spaceIndex
        newVectorProperty.spaces = copy.deepcopy(self.spaces)    
        newVectorProperty.isShaderParameter = self.isShaderParameter        
                
        return newVectorProperty
    
class NormalProperty(Property):
    @classmethod
    def fromAttributeStrings(cls, name, category, hint, value, spaces):
        property = cls()
        property.name = name
        property.category = category
        property.hint = hint
        property.value = property.valueFromStr(value)
        
        if spaces != '':
            property.spaces = spaces.split(',')
        else:
            property.spaces = ['shader']
        
        property.spaceIndex = 0

        return property
    
    def __init__(self):
        Property.__init__(self)

    def __getstate__(self):
        state = {}
        
        # save state
        state['name'] = self.name
        state['category'] = self.category
        state['hint'] = self.hint
        state['spaces'] = self.spaces
        state['spaceIndex'] = self.spaceIndex
        state['value'] = self.value
        state['isShaderParameter'] = self.isShaderParameter
        
        return state

    def __setstate__(self, state):
        self.__init__()
        
        # restore state
        for k, v in state.iteritems():
            setattr(self, k, v)
    
    def typeToStr(self):
        return 'normal'
    
    def encodedStr(self):
        return 'N'
    
    def valueFromStr(self, str):
        if str == '': 
            return [0.0, 0.0, 0.0] # default
        else:
            str = str.replace(' ', '')
            p = re.compile('normal\(([-+]?([0-9]*\.)?[0-9]+,){2}[-+]?([0-9]*\.)?[0-9]+\)') 
            match = p.match(str)
            if match:
                p = re.compile('[-+]?[0-9]*\.?[0-9]+')
                f = p.findall(str)                
                f = map(float, f)                
                return [f[0], f[1], f[2]]
            else:
                raise Exception('Cannot parse normal property %s values' % (self.name))  

    def valueToStr(self):
        return 'normal(' + ''.join('%.3f' % f + ',' for f in self.value[: - 1]) + '%.3f' % self.value[ - 1] + ')'

    def copy(self):
        newNormalProperty = NormalProperty()

        # copy value
        newNormalProperty.name = self.name
        newNormalProperty.category = self.category
        newNormalProperty.hint = self.hint
        newNormalProperty.value = copy.deepcopy(self.value)
        newNormalProperty.spaceIndex = self.spaceIndex
        newNormalProperty.spaces = copy.deepcopy(self.spaces)
        newNormalProperty.isShaderParameter = self.isShaderParameter
                        
        return newNormalProperty

class StringProperty(Property):
    @classmethod
    def fromAttributeStrings(cls, name, category, hint, value):
        property = cls()
        property.name = name
        property.category = category
        property.hint = hint
        property.value = value
        
        return property    
    
    def __init__(self):
        Property.__init__(self)

    def __getstate__(self):
        state = {}
        
        # save state
        state['name'] = self.name
        state['category'] = self.category
        state['hint'] = self.hint
        state['value'] = self.value
        state['isShaderParameter'] = self.isShaderParameter
        
        return state

    def __setstate__(self, state):
        self.__init__()
        
        # restore state
        for k, v in state.iteritems():
            setattr(self, k, v)
            
    def typeToStr(self):
        return 'string'
    
    def encodedStr(self):
        return 'S'

    def valueFromStr(self, str):
        return str

    def valueToStr(self):
        return str(self.value)

    def copy(self):
        newStringProperty = StringProperty()
        
        # copy value
        newStringProperty.name = self.name
        newStringProperty.category = self.category
        newStringProperty.hint = self.hint
        newStringProperty.value = copy.deepcopy(self.value)
        newStringProperty.isShaderParameter = self.isShaderParameter
        
        return newStringProperty

class PropertyBuilder(object):
    def buildProperty(self, propAttributes, category):
        type = propAttributes['type']

        if (type == 'color'): return self.buildColorProperty(propAttributes, category)
        if (type == 'float'): return self.buildFloatProperty(propAttributes, category)
        if (type == 'matrix'): return self.buildMatrixProperty(propAttributes, category)
        if (type == 'point'): return self.buildPointProperty(propAttributes, category)
        if (type == 'string'): return self.buildStringProperty(propAttributes, category)
        if (type == 'vector'): return self.buildVectorProperty(propAttributes, category)
        if (type == 'normal'): return self.buildNormalProperty(propAttributes, category)
        
        raise Exception('%s type is not supported!' % (type))

    def getCommonAttributes(self, propAttributes, category):
        try:
            name = propAttributes['name']
        except:
            raise Exception('Property must have a name!') 
    
        default = ''
        hint = ''
        try:
            default = propAttributes['default']
        except:
            pass
        try:
            hint = propAttributes['hint'] 
        except:
            pass
                
        return name, default, hint
    
    def buildColorProperty(self, propAttributes, category):
        name, default, hint = self.getCommonAttributes(propAttributes, category)        
        
        property = ColorProperty.fromAttributeStrings(name,
                                                      category,
                                                      hint,
                                                      default)
        
        return property

    def buildFloatProperty(self, propAttributes, category):
        name, default, hint = self.getCommonAttributes(propAttributes, category)        
                
        property = FloatProperty.fromAttributeStrings(name,
                                                      category,
                                                      hint,
                                                      default)
        
        return property

    def buildMatrixProperty(self, propAttributes, category):
        name, default, hint = self.getCommonAttributes(propAttributes, category)        
        
        property = MatrixProperty.fromAttributeStrings(name,
                                                       category,
                                                       hint,
                                                       default)
        
        return property

    def buildPointProperty(self, propAttributes, category):
        name, default, hint = self.getCommonAttributes(propAttributes, category)
        spaces = 'world'
        try:
            spaces = propAttributes['spaces']
        except:
            pass
        
        property = PointProperty.fromAttributeStrings(name,
                                                      category,
                                                      hint,
                                                      default,
                                                      spaces)
        
        return property

    def buildStringProperty(self, propAttributes, category):
        name, default, hint = self.getCommonAttributes(propAttributes, category)        
        
        property = StringProperty.fromAttributeStrings(name,
                                                       category,
                                                       hint,
                                                       default)
        
        return property

    def buildVectorProperty(self, propAttributes, category):
        name, default, hint = self.getCommonAttributes(propAttributes, category)
        spaces = 'world'
        try:
            spaces = propAttributes['spaces']
        except:
            pass
                
        property = VectorProperty.fromAttributeStrings(name,
                                                       category,
                                                       hint,
                                                       default,
                                                       spaces)
        
        return property

    def buildNormalProperty(self, propAttributes, category):
        name, default, hint = self.getCommonAttributes(propAttributes, category)
        spaces = 'world'
        try:
            spaces = propAttributes['spaces']
        except:
            pass
                
        property = NormalProperty.fromAttributeStrings(name,
                                                       category,
                                                       hint,
                                                       default,
                                                       spaces)
        
        return property
        
class NodeReader(object):
    def __init__(self, file):
        self.file = file
                
    def getXMLData(self, node, what):
        # "safe" XML data getter
        data = node.getElementsByTagName(what)
        if len(data) > 0:
            if len(data[0].childNodes) > 0:
                return data[0].childNodes[0].data
            
        return ''
    
    def getXMLAttribute(self, node, what):
        # "safe" XML attribute getter
        data = node.attributes.get(what)
        if data != None:
            return data.value.strip()
        else:
            return ''
                    
    def readNodeFromFile(self):
        import xml.dom.minidom as mdom
        parsed = mdom.parse(self.file)   
        
        nodeElem = parsed.getElementsByTagName('node')[0]        
        
        # node name        
        nodeName = self.getXMLAttribute(nodeElem, 'name')        
        
        # author        
        author = self.getXMLAttribute(nodeElem, 'author')
        
        # help
        help = self.getXMLData(nodeElem, 'help')        

        # type
        type = self.getXMLAttribute(nodeElem, 'type')        
        
        # includes
        includes = []
        includeElems = nodeElem.getElementsByTagName('include')
        if len(includeElems) > 0:
            fileElems = includeElems[0].getElementsByTagName('file')
            for fileElem in fileElems:
                includes.append(self.getXMLAttribute(fileElem, 'name'))
        
        # property builder
        propertyBuilder = PropertyBuilder()
                        
        # input properties
        inputProps = []
        inputElems = nodeElem.getElementsByTagName('input')
        if len(inputElems) > 0:
            propElems = inputElems[0].getElementsByTagName('property')
            for propElem in propElems:
                propAttributes = {}
                for k, v in zip(propElem.attributes.keys(), propElem.attributes.values()):
                    propAttributes[k] = v.value
                try:
                    inputProperty = propertyBuilder.buildProperty(propAttributes, Property.Input)
                    inputProps.append(inputProperty)
                except Exception, e:
                    print 'Couldn\'t input property parse %s. %s' % (self.file, e.args)
        
        # output properties
        outputProps = []                                
        outputElems = nodeElem.getElementsByTagName('output')
        if len(outputElems) > 0:
            propElems = outputElems[0].getElementsByTagName('property')
            for propElem in propElems:
                propAttributes = {}
                for k, v in zip(propElem.attributes.keys(), propElem.attributes.values()):
                    propAttributes[k] = v.value
                    
                propAttributes['code'] = self.getXMLData(propElem, 'code')
                
                try:
                    outputProperty = propertyBuilder.buildProperty(propAttributes, Property.Output)
                    outputProps.append(outputProperty)
                except Exception, e:
                    print 'Couldn\'t parse output property %s. %s' % (self.file, e.args)

        # internal variables (only names: type is defined into shader code template)
        internals = []
        internalElems = nodeElem.getElementsByTagName('internal')
        if len(internalElems) > 0:
            variableElems = internalElems[0].getElementsByTagName('variable')
            for variableElem in variableElems:                    
                internals.append(self.getXMLAttribute(variableElem, 'name'))
                
        # code
        code = self.getXMLData(nodeElem, 'code')

        # preview codes
        previewCodes = {}
        previewElems = nodeElem.getElementsByTagName('preview')
        if len(previewElems) > 0:
            shaderElems = previewElems[0].getElementsByTagName('shader')
            if len(shaderElems) > 0:
                for shaderElem in shaderElems:
                    codeElems = shaderElem.getElementsByTagName('code')
                    if len(codeElems) > 0:
                        previewCode = self.getXMLData(shaderElem, 'code')
                        shaderType = self.getXMLAttribute(shaderElem, 'type')
                        previewCodes[shaderType] = previewCode
        
        return Node.buildFrom(type,
                              nodeName,
                              nodeName,
                              author,
                              help,
                              inputProps, outputProps,
                              internals,
                              code,
                              includes,
                              previewCodes)
                    
class Node(object):
    id = 0

    def __init__(self):
        self.id = None
        self.type = None
        self.name = None
        self.childs = set()
        self.nodeName = None
        self.author = None
        self.help = None
        self.code = None
        self.internals = None
        self.includes = None
        self.inputProps = None
        self.outputProps = None
        self.inputLinks = None
        self.outputLinks = None        
        self.gfxNode = None
        self.previewCodes = None
    
    @classmethod
    def buildFrom(cls, type, name, nodeName, author, help,
                  inputProps, outputProps, internals, code, includes, previewCodes):
        node = cls()
        
        # id to identify a single instance
        Node.id += 1
        node.id = Node.id
        
        # node stuff
        node.type = type
        node.name = name
        node.nodeName = nodeName
        node.author = author
        node.help = help
        node.code = code
        node.includes = includes
        node.previewCodes = previewCodes
        
        node.childs = set()
        
        # internals
        node.internals = internals
        
        # input properties
        node.inputProps = inputProps
        
        # output properties
        node.outputProps = outputProps
        
        # input links
        node.inputLinks = {}

        # output links
        node.outputLinks = {}
        for outputProp in node.outputProps:
            node.outputLinks[outputProp] = []
                    
        # create gfxNode
        from gfx.view import GfxNode
        node.gfxNode = GfxNode(node)
                
        return node

    def __getstate__(self):
        state = {}
        
        # save state
        state['id'] = self.id
        state['type'] = self.type
        state['name'] = self.name
        state['nodeName'] = self.nodeName
        state['author'] = self.author
        state['help'] = self.help
        state['internals'] = self.internals
        state['code'] = self.code        
        state['includes'] = self.includes
        state['previewCodes'] = self.previewCodes
        state['inputProps'] = self.inputProps
        state['outputProps'] = self.outputProps        
        state['gfxNodePos'] = (self.gfxNode.pos().x(), self.gfxNode.pos().y())
        
        return state

    def __setstate__(self, state):
        self.__init__()
        
        self.id = state['id']
        self.type = state['type']
        self.name = state['name'] 
        self.nodeName = state['nodeName']
        self.author = state['author'] 
        self.help = state['help'] 
        self.internals = state['internals']
        self.code = state['code']         
        self.includes = state['includes']
        self.previewCodes = state['previewCodes']
        self.inputProps = state['inputProps'] 
        self.outputProps = state['outputProps']         
        
        # childs
        self.childs = set()
        
        # input links
        self.inputLinks = {}

        # output links
        self.outputLinks = {}
        for outputProp in self.outputProps:
            self.outputLinks[outputProp] = []
        
        # create new gfxNode
        from gfx.view import GfxNode
        self.gfxNode = GfxNode(self)
        
        # set position
        pos = state['gfxNodePos']
        self.gfxNode.setPos(QtCore.QPointF(pos[0], pos[1]))
            
    def copy(self):
        # copy input props
        inputProps = []
        for inputProp in self.inputProps:
            inputProps.append(inputProp.copy())    
        
        # copy output props
        outputProps = []
        for outputProp in self.outputProps:
            outputProps.append(outputProp.copy())
                    
        # create a new node, skipping links
        newNode = Node.buildFrom(self.type,
                                 self.name,
                                 self.nodeName,
                                 self.author,
                                 self.help,
                                 inputProps, outputProps,
                                 self.internals,
                                 self.code,
                                 self.includes,
                                 self.previewCodes)

        return newNode
            
    def attachOutputPropToLink(self, prop, link):
        self.outputLinks[prop].append(link)
        
    def detachOutputPropFromLink(self, prop, link):
        outputLinks = self.outputLinks[prop]
        outputLinks.remove(link)

    def attachInputPropToLink(self, prop, link):
        self.inputLinks[prop] = link
        
    def detachInputPropFromLink(self, prop):
        self.inputLinks.pop(prop)      
        
    def isInputPropertyLinked(self, property):
        return property in self.inputLinks.keys()   
    
    def getIncludes(self, includes, alreadyVisitedNodes = None):
        if alreadyVisitedNodes is None: alreadyVisitedNodes = set()
        
        # recurse down the tree
        for child in self.childs:
            if child not in alreadyVisitedNodes:
                child.getIncludes(includes, alreadyVisitedNodes)
        
        # append node includes
        includes += self.includes
        
        # update visited nodes
        alreadyVisitedNodes.add(self)  
    
    def getAvailableShaderParameters(self, params, alreadyVisitedNodes = None):
        if alreadyVisitedNodes is None: alreadyVisitedNodes = set()

        # recurse down the tree
        for child in self.childs:
            if child not in alreadyVisitedNodes:
                child.getAvailableShaderParameters(params, alreadyVisitedNodes)
        
        # append properties that are shader parameters
        for inputProp in self.inputProps:
            if not self.isInputPropertyLinked(inputProp):
                params.append({'property' : inputProp, 'node' : self})
        
        # update visited nodes
        alreadyVisitedNodes.add(self)                

    def getShaderParameters(self, params, alreadyVisitedNodes = None):
        if alreadyVisitedNodes is None: alreadyVisitedNodes = set()
        
        # recurse down the tree
        for child in self.childs:
            if child not in alreadyVisitedNodes:
                child.getShaderParameters(params, alreadyVisitedNodes)
        
        # append properties that are shader parameters
        for inputProp in self.inputProps:
            if not self.isInputPropertyLinked(inputProp) and inputProp.isShaderParameter:
                params.append('%s %s_%s = %s' % (inputProp.typeToStr(),
                                                 self.name, inputProp.name,
                                                 inputProp.valueToStr()))

        # update visited nodes
        alreadyVisitedNodes.add(self)                

    def getCode(self, shaderCode, alreadyGeneratedNodes = None):
        if alreadyGeneratedNodes is None: alreadyGeneratedNodes = set()

        print 'In node: %s' % self.name
        # recurse down the tree
        for child in self.childs:
            if child not in alreadyGeneratedNodes:
                shaderCode = child.getCode(shaderCode, alreadyGeneratedNodes)
                    
        # define start node comment
        nodeCode = '''// START NODE %s \n''' % self.name
        
        # declare and define input properties
        for inputProp in self.inputProps:
            if not self.isInputPropertyLinked(inputProp) and not inputProp.isShaderParameter:
                nodeCode += '''%s %s_%s = %s;\n''' % (inputProp.typeToStr(),
                                                      self.name, inputProp.name,
                                                      inputProp.valueToStr())
        
        import copy
        code = copy.deepcopy(self.code)

        # replace input properties
        for inputProp in self.inputProps:
            if self.isInputPropertyLinked(inputProp):
                inputLink = self.inputLinks[inputProp]                
                name = '%s_%s' % (inputLink.sourceNode.name, inputLink.sourceProp.name)
                code = code.replace('$(%s)' % inputProp.name, name)                
            else:
                name = '%s_%s' % (self.name, inputProp.name)
                code = code.replace('$(%s)' % inputProp.name, name)
                                        

        # replace output properties
        for outputProp in self.outputProps:                
            name = '%s_%s' % (self.name, outputProp.name)
            code = code.replace('$(%s)' % outputProp.name, name)            

        # replace internals
        for internal in self.internals:
            name = '%s_%s' % (self.name, internal)
            code = code.replace('$(%s)' % internal, name)     
        
        # append to node code
        nodeCode += '''\n%s\n''' % code        
               
        # define end node comment
        nodeCode += '''// END NODE %s \n\n''' % self.name
        
        # append to shader code
        shaderCode += nodeCode
        
        # update generated nodes
        alreadyGeneratedNodes.add(self)
        
        return shaderCode

    def getPreviewCode(self, shaderType):
        import copy
        previewCode = copy.deepcopy(self.previewCodes[shaderType])
        
        # replace output properties
        for outputProp in self.outputProps:                
            name = '%s_%s' % (self.name, outputProp.name)
            previewCode = previewCode.replace('$(%s)' % outputProp.name, name)        
            
        return previewCode    
    
    def __str__( object ):
        return self.name;

    def __repr__( object ):
        return object.name;
                                            
class Link(object):
    id = 0
    
    def __init__(self):
        self.id = None
        self.sourceNode = None
        self.destNode = None
        
        self.sourceProp = None
        self.destProp = None

    @classmethod
    def buildFrom(cls, sourceNode, destNode, sourceProp, destProp):
        link = cls()
        
        # id to identify a single instance
        Link.id += 1
        link.id = Link.id
                
        link.sourceNode = sourceNode
        link.destNode = destNode
        
        link.sourceProp = sourceProp
        link.destProp = destProp
        
        # create gfxLink
        from gfx.view import GfxLink
        link.gfxLink = GfxLink.createFromLink(link)     
        
        return link  
                
class ShaderLink(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        
        # node library
        self.nodeLibrary = {}

        # nodes
        self.nodes = {}
        
        # links
        self.links = {}
        
        # name cache to avoid redefinitions
        self.nodeNamesInUse = {}
                
        # rendering settings
        self.renderingSettings = {}
        
        # renderers
        self.renderers = []
        self.currentRendererIndex = 0;
        
        # paths
        self.paths = {}
        
        # dirtyState
        self.dirtyState = False
        
    def initialize(self):
        # load paths
        self.loadPaths()
        
        # load node library
        self.loadNodeLibrary()
        
        # load rendering settings
        self.loadRenderingDefaultSettings()

    def loadPaths(self):
        import os, sys
        if len(sys.argv) == 2:
            root = sys.argv[1]
        else:                        
            root = os.path.realpath(sys.path[0])

        nodes = os.path.join(root, 'data', 'node')
        ribs = os.path.join(root, 'data', 'rib')
        include = os.path.join(root, 'data', 'include')
        temp = os.path.join(root, 'data', 'temp')
        shader = os.path.join(root, 'data', 'shader')
        archive = os.path.join(root, 'data', 'archive')

        self.paths['root'] = root
        self.paths['node'] = nodes
        self.paths['rib'] = ribs
        self.paths['include'] = include
        self.paths['temp'] = temp
        self.paths['shader'] = shader
        self.paths['archive'] = archive
        
    def loadNodeLibrary(self):
        # node library path
        pathNodeLibrary = self.paths['node']
        
        # node library is a dictionary like this: self.nodeLibrary[dir][nodeName] = node
        for (thisDir, subsHere, filesHere) in os.walk(pathNodeLibrary):
            for subHere in subsHere:
                self.nodeLibrary[os.path.basename(subHere)] = {}
        
        for (thisDir, subsHere, filesHere) in os.walk(pathNodeLibrary):
            for filename in filesHere:
                if filename.endswith('.xml'):
                    fullname = os.path.join(thisDir, filename)
                    print 'Loading node: ' + fullname
                    nodeReader = NodeReader(fullname)               
                    node = nodeReader.readNodeFromFile()
                    self.nodeLibrary[os.path.basename(thisDir)][node.name] = node
                    # notify guys interest in this stuff
                    self.emit(QtCore.SIGNAL('nodeLoaded'), node)
                    
        
        # notify guys interest in this stuff
        self.emit(QtCore.SIGNAL('nodeLibraryLoaded'), self.nodeLibrary)
    
    def loadRenderingDefaultSettings(self):
        # rendering options
        self.renderingSettings['Rib'] = 'sphere.rib'
        self.renderingSettings['Format'] = (640, 480)
        self.renderingSettings['AspectRatio'] = 1.0
        self.renderingSettings['Samples'] = (3, 3)
        self.renderingSettings['Filter'] = 'catmull-rom'
        self.renderingSettings['FilterWidth'] = (3, 3)
        self.renderingSettings['ShadingRate'] = 2.0
        self.renderingSettings['Preview'] = True
        
        # shaders in use (list of shaders and current in use)
        self.renderingSettings['Surface'] = [['None'], 0]
        self.renderingSettings['Displacement'] = [['None'], 0]
        self.renderingSettings['Atmosphere'] = [['None'], 0]
        self.renderingSettings['Interior'] = [['None'], 0]
        self.renderingSettings['Exterior'] = [['None'], 0]
        self.renderingSettings['Imager'] = [['None'], 0]
        
        # renderers
        self.renderers = self.parseRendererSettings()        
        
        # notify guys interest in this stuff
        self.fireRenderingSettingsLoaded()
        
    def parseRendererSettings(self):
        from xml.dom import minidom
        renderers = []
        dom = minidom.parse(os.path.join(self.paths['root'], 'settings.xml'))
        xmlRenderers = dom.getElementsByTagName('renderer')
        for xmlRenderer in xmlRenderers:
            name = xmlRenderer.attributes['name'].nodeValue
            compileTool = xmlRenderer.getElementsByTagName('compileTool')[0].firstChild.data
            renderTool = xmlRenderer.getElementsByTagName('renderTool')[0].firstChild.data
            renderers.append({'name' : name, 'compileTool' : compileTool, 'renderTool' : renderTool})
                            
        return renderers

    def fireRenderingSettingsLoaded(self):
        self.emit(QtCore.SIGNAL('renderingSettingsLoaded'), self.renderingSettings)
        
    def fixNodeNameRedefinitions(self, node):
        # update name cache
        nextId = 0
        if node.nodeName in self.nodeNamesInUse.keys():
            nextId = self.nodeNamesInUse[node.nodeName] + 1
            
        self.nodeNamesInUse[node.nodeName] = nextId
        
        # build new name
        node.name = node.nodeName + str(nextId)
        

    def addNodeFromLibrary(self, dirName, nodeName, dropPos):
        # get node from node library
        libraryNode = self.nodeLibrary[dirName][nodeName]
        
        # make a new copy
        node = libraryNode.copy()
        
        # fix name redefinitions
        self.fixNodeNameRedefinitions(node)
                
        # set new drop position
        node.gfxNode.setPos(dropPos)    
        
        # update node id
	if self.nodes.keys():    
		node.id = max(self.nodes.keys()) + 1
        
        # add node
        self.addNode(node)                
        
        return node
            
    def addLinkFromNodes(self, sourceNode, destNode, sourceProp, destProp):
        # create new link
        link = Link.buildFrom(sourceNode, destNode, sourceProp, destProp)
        
        # add link
        self.addLink(link)
                
        return link

    def addNode(self, node):
        # add node to model nodes
        self.nodes[node.id] = node
        
        print 'adding to model ' + node.name
        
        # notify guys interested?
        self.emit(QtCore.SIGNAL('nodeAdded'), node)
        
    def addLink(self, link):
        # add to model links
        self.links[link.id] = link
        
        # attach link to nodes
        link.sourceNode.attachOutputPropToLink(link.sourceProp, link)
        link.destNode.attachInputPropToLink(link.destProp, link)
        
        # add child (since it is a set no duplicates allowed)
        link.destNode.childs.add(link.sourceNode)
        
        # notify guys interested?
        self.emit(QtCore.SIGNAL('linkAdded'), link)
                        
    def removeNode(self, node):
        # remove from model nodes
        nodePopped = self.nodes.pop(node.id)        
        
        # notify guys interested?
        print 'removing from model ' + node.name
        self.emit(QtCore.SIGNAL('nodeRemoved'), node)

    def removeLink(self, link):
        # remove from model links
        linkPopped = self.links.pop(link.id)
        
        # detach node from links
        linkPopped.sourceNode.detachOutputPropFromLink(linkPopped.sourceProp, linkPopped)
        linkPopped.destNode.detachInputPropFromLink(linkPopped.destProp)
        
        # check if we can remove a child from destination node
        destNode = linkPopped.destNode
        sourceNode = linkPopped.sourceNode
        
        sourceNodeReferenceCount = 0
        for inputLink in destNode.inputLinks.values():
            if inputLink.sourceNode == sourceNode:
                sourceNodeReferenceCount += 1
        if sourceNodeReferenceCount == 0:
            destNode.childs.remove(sourceNode)                
        
        # notify guys interested?
        self.emit(QtCore.SIGNAL('linkRemoved'), link)
        
    def clear(self):
        print 'model nodes ' + str(self.nodes)
        
        # remove links
        for link in self.links.values():
            self.removeLink(link)
        
        # remove nodes    
        for node in self.nodes.values():
            self.removeNode(node)
            
        # nodes
        self.nodes = {}
        
        # links
        self.links = {}
        
        # name cache
        self.nodeNamesInUse = {}

        # rendering settings
        self.renderingSettings = {}
        
    def getNodeFromName(self, nodeName):
        for node in self.nodes.values():
            if node.name == nodeName:
                return node
            
        return None
                
