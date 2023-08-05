from veerer import constants
from veerer import FlatVeeringTriangulation
from IPython.display import *

import json

RIGHT = constants.RIGHT
LEFT = constants.LEFT


class formatage : 
    """
    Class allowing to instantiate objects which can serialize triangulations from a series of flips in a "json" format.
    Its attributes are :
        *_flips         list of edges to flip (in order).
        *_fvt           flat representation of the vereer triangulation.
        *_edges         list of edges.
        *_faces         list of triangles in the triangulation after each flips. Each triangle is dicribe as a triplet of edges.
                        It is therefore a list of triplet of edges.
        *_edgeColor     list of edges colors of the triangulation after each flip (1 = RED and 2 = BLUE).
        *_pos           Coordinates of all the points
        *_xMax
        *_xMin
        *_yMax
        *_y_Min
        *_playButton    Play/Pause button id
        *_nextButton    next button id
        *_prevButton    previous button id
        *_reverseButton    reverse loop button id
        *_sides         List indicating left side or right side to flip for each flip 
        
    So we call "serialize triangulations from a series of flips", the recovery of the following data :
        - _flips.
        - _edges.
        - _faces
        - _edgeColor
        - _pos
        
    """
    def initialize(self, 
                   flatVeeringTriangulation, 
                   flips, 
                   sides, 
                   duration,
                   playButtonName, 
                   pauseButtonName,
                   nextButtonName, 
                   prevButtonName, 
                   reverseButtonName,
                   resetButtonName,
                   lastButtonName
                  ) :
        if len(sides) > 0 and (len(flips) != len(sides)) :
            raise ValueError("'sides' and 'flips' must have the same size")
        self._flips = self.__convertFlips(flips)
        self._fvt = flatVeeringTriangulation
        self._fvtLay = self._fvt.layout()
        self._edges = self._fvtLay._triangulation.edges()
        self._faces = [self._fvtLay._triangulation.faces()]
        self._edgeColor = []
        self._pos = []
        self.__reinitColor()
        self._sides = sides
        self._duration = int(duration)
        
        #define buttons here
        self._playButton = playButtonName
        self._pauseButton = pauseButtonName
        self._nextButton = nextButtonName
        self._prevButton = prevButtonName
        self._reverseButton = reverseButtonName
        self._resetButton = resetButtonName
        self._lastButton = lastButtonName
        
        #Set the max,min tables here
        self._dataX = []
        self._dataY = []
   
        
    def serialization(self) : 
        
        """Serialize a suite of triangulations produced by a series of flips by recovering:
            - _flips.
            - _edges.
            - _faces
            - _edgeColor
            - _pos
        """
        
        self.__computeFlips()
        s = json.dumps({
                "faces" : self._faces, 
                "edges" : self._edges,
                "flips" : self._flips,
                "edgeColor" : self._edgeColor,
                "pos" : self._pos,
                "duration": self._duration,
                "dataX" : self._dataX,
                "dataY" : self._dataY,
                #Add buttons here
                "playButton" :self._playButton,
                "pauseButton" :self._pauseButton,
                "nextButton" :self._nextButton,
                "prevButton" :self._prevButton,
                "reverseButton" :self._reverseButton,
                "resetButton" :self._resetButton,
                "lastButton" :self._lastButton
            }
        )
        self.scriptInJs(s)
        return s  
    
    
    def scriptInJs(self, data):
        """prend un json qui sera les paramètres d'une
        triangulation affichée en JS"""
        idData = str(id(data))
        script = ""
        script +="<div id = '"
        script += idData
        script += "'></div>\n"
        script += "<script>\n"
        script += "var data = '"
        script += data
        script += "';\n"
        script += "document.getElementById('"+idData+"').innerHTML = data;\n"
        script += "document.getElementById('"+idData+"').style.display = 'none';\n"
        script += "</script>\n"
        display(HTML(script))
            
    ##Private Methode  
    def __convertFlips(self, flips) :
        """convert each element in the list into int, for serialization reason
        """
        newFlips = []
        if(flips != None):
            for fl in flips:
                newFlips.append(int(fl))
        return newFlips
        
    def __computeFlips(self) : 
        
        """Compute the series of flips "_flips"  from the initial flat veerer triangulation Layout "_fvtLay"."""
        ind = 0
        self._fvtLay.set_pos() 
        self.__posData(self._fvtLay._pos)
        for e in self._flips : 
            if len(self._sides) != 0:
                self._fvtLay._triangulation.flip(e, self._sides[ind])
                ind += 1
            else:
                self._fvtLay._triangulation.flip(e)
            self._faces.append(self._fvtLay._triangulation.faces())
            self.__reinitColor()
            self._fvtLay.set_pos()
            self.__posData(self._fvtLay._pos)
            
 
    def __reinitColor(self) : 
        
        """Recover the color of each edge of "_fvt" and add them to "_edgeColor" """
        
        color = []
        for edge in range (self._fvtLay._triangulation._n) : 
            color.append(self._fvtLay._triangulation.edge_colour(edge))
        self._edgeColor.append(color)
        
    def __posData(self, pos) : 
        """Compute all points' coordinates """
        graph = []
        fp = self._fvt.face_permutation(copy=False)
        xMax, xMin = 0, 999999
        yMax, yMin = 0, 9999999
        for face in (self._fvtLay._triangulation.faces()):
            edges = []
            for edge in face: 
                (x,y) = (float(pos[edge][0]), float(pos[edge][1]))
                edges.append((x,y))
                if xMax < x:
                    xMax = x
                if xMin > x:
                    xMin = x
                if yMax < y:
                    yMax = y
                if yMin > y:
                    yMin = y
            graph.append(edges)
        self._pos.append(graph)
        self._dataX.append((xMin, xMax))
        self._dataY.append((yMin, yMax))
        
        