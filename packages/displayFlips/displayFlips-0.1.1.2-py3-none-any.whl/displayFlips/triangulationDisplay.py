from .Formatage import formatage 
from IPython.display import HTML, Javascript
import uuid

class triangulationDisplay : 
    """ This class allows to inject Javascript code to the navigator page. 
    """
    
    def __init__(self):
        self._formatage = formatage()
    
    def displaySerieFlip(self, flatVeeringTriangulation, flips=[], sides=[],duration=2000) : 
        bIDPlay, self._htmlbuttonPlayID = self.__createButton("Play")
        bIDPause, self._htmlbuttonPauseID = self.__createButton("Pause")
        bIDNext, self._htmlbuttonNextID = self.__createButton("Next")
        bIDPrev, self._htmlbuttonPrevID = self.__createButton("Previous")
        bIDReverse, self._htmlbuttonReverseID = self.__createButton("Reverse")
        bIDReset, self._htmlbuttonResetID = self.__createButton("Reset")
        bIDLast, self._htmlbuttonLastID = self.__createButton("Last")
        self._formatage.initialize(flatVeeringTriangulation, 
                                   flips, 
                                   sides, 
                                   duration,
                                   bIDPlay,
                                   bIDPause,
                                   bIDNext, 
                                   bIDPrev, 
                                   bIDReverse, 
                                   bIDReset, 
                                   bIDLast) 
        self._formatage.serialization()
        self.__prepareTools()
        display(Javascript(filename="JS/Main.js"))
        
        
    def __prepareTools(self):
        display(Javascript("require.config({baseUrl : './JS', paths: {d3: 'https://d3js.org/d3.v5.min', config : 'config' }})"))
        strHTML = "<div>\n"
        strHTML += self._htmlbuttonResetID
        strHTML += self._htmlbuttonPrevID                     
        strHTML += self._htmlbuttonPlayID
        strHTML += self._htmlbuttonPauseID
        strHTML += self._htmlbuttonNextID
        strHTML += self._htmlbuttonLastID
        strHTML += self._htmlbuttonReverseID
        strHTML += "</div>"
        display(HTML(strHTML)) 
        
        
    def __createButton(self, name):
        buttonID = "a" + str(uuid.uuid4().hex[:6].upper()) 
        buttonStr = "<input " 
        buttonStr +=  "type=\"button\" " 
        buttonStr += "value=\""
        buttonStr += name
        buttonStr += "\" id=\"" 
        buttonStr += buttonID 
        buttonStr += "\">\n"
        return buttonID, buttonStr

