requirejs(['d3', 'model'], function(d3, Model) { 
function Controler (model, view) {

    this.model = model ; 
    this.view = view ; 

    this.graph = function (){
        
            this.model.reset();
            this.view.draw();
    };

}


/**
 * View class, responsible for visualization.
 * attribut : 
 *  - model 
 *  - root : la scene 
 */
function View (model){
    
    // attribut
    this.model = model;

    // View's variables, useful for transition method 
    var self = this ; 
    var sourceLines = [];               //tableau svg de lines
    var sourceLabels = [];              //tableau svg de Labels
    var srcTag = [];                    //tableau svg de tag
    var isPaused = false;
    //var loop = false; //if flips run continually
    var reverseMode = false; //flag enable when reverse loop (like "loop" but begin at flip i<nbflips and finish to first flip)
    var previousFlip = false;
    var nextFlip = false;
    var transitionDuration = self.model.duration;      
    var lastLineDone = false;

    
    ////////////////// FUNCTION //////////////////

    /**
     * attribute the scene
     * @param {d3.svg} root 
     */
    this.setRoot = function (root){
        this.root = root;
    };

    this.setTextBox = function (textBox) {
        this.textBox = textBox;
    };


    ////////////////////////////
    ////// SCALE FUNCTIONs ///////
 
    this.setScales = function (){ //update scales using x max et y max of the current graph (had to be call before each use of this.scaleYAxis or this.scaleXAxis)

        this.scaleYAxis = d3.scaleLinear()
                    .domain([0, self.model.graphs[self.model.current].Ylimits[1]])
                    .range([500,100]);
        
        this.scaleXAxis = d3.scaleLinear()
                    .domain([0, self.model.graphs[self.model.current].Xlimits[1]])
                    .range([100,500]);
    }
    ////////////////////////////
        //// DRAW FUNCTIONs //// 

    /**
     * draw a label in the container (=root)
     * @param {d3.svg} container root
     * @param {Line} line 
     * @returns put the label at the line 
     */
     this.drawLabel = function(container, line) {
        let result;
        this.setScales();
            result = container.append('text')
            .attr('x', self.scaleXAxis(line.label[0]))
            .attr('y', self.scaleYAxis(line.label[1]))
            .attr('fill', 'black')
            .text(line.tag.toString());

        return result;
    };


    /**
     * draw a half edge in the container (=root)
     * @param {d3.svg} container 
     * @param {Line} line 
     * @param {Boolean} dotted 
     * @returns svg line
     */
    this.drawLine = function(container, line, dotted){
        this.setScales();
        let result = container.append('line')
                    .attr('x1', self.scaleXAxis(line.coords[0][0]))
                    .attr('y1', self.scaleYAxis(line.coords[0][1]))
                    .attr('x2', self.scaleXAxis(line.coords[1][0]))
                    .attr('y2', self.scaleYAxis(line.coords[1][1]))
                    .style('stroke', line.color);
        
        if(dotted){
            result = result.style("stroke-dasharray", ("3, 3"))  ;  
        }
        return result;
    };


    /// TRANSITION FUNCTION /// 

    /**
     * 
     * @param {d3.svg.text} oldLabel 
     * @param {Line} line 
     * @returns place correctly the label at the Line 
     */
     this.moveLabel = function (oldLabel, line){
        this.setScales();
        let result = oldLabel.transition()
                        .duration(transitionDuration) 
                        .attr('x', self.scaleXAxis(line.label[0]))
                        .attr('y', self.scaleYAxis(line.label[1]));
        return result;
    }


    /**
     * update line for the new graphe
     * @param {d3.svg.line} oldline 
     * @param {Line} line 
     * @param {Boolean} dotted 
     * @returns 
     */


    this.moveLine = function(oldline, line) {
        this.setScales();
        oldline.transition()
                        .duration(transitionDuration)
                        .attr('x1', self.scaleXAxis(line.coords[0][0]))
                        .attr('y1', self.scaleYAxis(line.coords[0][1]))
                        .attr('x2', self.scaleXAxis(line.coords[1][0]))
                        .attr('y2', self.scaleYAxis(line.coords[1][1]))
                        .style('stroke', line.color)
                        .on('end', function() { // call transitionLine() when finishing all lines' transitions
                            lastLineDone--;
                        
                            if(self.model.current < self.model.flips.length && self.model.current > 0 ){
                                if(lastLineDone != 0) return;
                                if(isPaused){
                                    if(previousFlip){
                                        self.model.prev();
                                        self.transitionLine();
                                        previousFlip = false;
                                        return;
                                    }
                                    if(nextFlip){
                                        nextFlip = false;
                                        self.model.next();
                                        self.transitionLine();
                                        nextFlip = false;
                                        return;
                                    }
                                }
                                if(!isPaused){
                                    if(reverseMode){
                                        self.model.prev();
                                        if(self.model.current == 0){
                                            isPaused = true;
                                        }
                                    }else{
                                        self.model.next();
                                    }
                                    self.transitionLine();
                                }
                            }else{
                                isPaused = true;
                            }

                        });
    };

    /**
     * move lines and labels to update the graphe
     */
    this.transitionLine = function (){
        if(self.model.current > self.model.flips.length) return;

            lastLineDone = sourceLines.length -1;

            var triang = self.model.graphs[self.model.current];
            var currentFlip = -1;
            if(self.model.current > 0) 
                currentFlip = self.model.flips[self.model.current-1];
            this.textBox.text("Current flip: " + currentFlip);
            for(var element = 0; element< sourceLines.length; element++){ 
                var b = false;
                for(let j = 0; j < triang.nbTriangles && !b; j++){ // trouver l'arête correspondante 
                    for(let edge = 0; edge < 3 && !b ; edge++){
                        let line = triang.triangles[j].lines[edge]; // Objet de type Line 
                        if(srcTag[element] == line.tag){      
                            self.moveLine(sourceLines[element], line) ; 
                            self.moveLabel(sourceLabels[element], line) ;
                            b = true;
                        }
                    }
                }
            }
    }
    
   
    /**
     * recursive function, it stops when all flips have been realized. 
     * draw all graph, 
     */
    
    this.playButton = function (){
        var name = '#' + this.model.playButton;
        d3.select(name)
            .on('click', function(){
                if(self.model.current > self.model.flips.length || !isPaused) return; 
                reverseMode = false;
                isPaused = false;
                self.model.next();
                self.transitionLine();
            });
    }
    this.pauseButton = function (){
        var name = '#' + this.model.pauseButton;
        d3.select(name)
            .on('click', function(){
                if(self.model.current > self.model.flips.length || isPaused) return; 
                console.log("click on Pause");
                isPaused = true;
            });
    }

    this.nextButton = function (){
        var name = '#' + this.model.nextButton;
        d3.select(name)
            .on('click', function(){
                if(self.model.current >= self.model.flips.length) return;
                if(isPaused){       
                    self.model.next();                              
                    self.transitionLine();
                    return;
                }
                if(reverseMode){
                    isPaused = true;
                    nextFlip = true;
                }
            });
    }

    this.prevButton = function (){
        var name = '#' + this.model.prevButton;
        d3.select(name)
            .on('click', function(){
                if(self.model.current == 0) return;
                if(isPaused){       
                    self.model.prev();                              
                    self.transitionLine();
                    return;
                }
                if(!reverseMode){
                    isPaused = true;
                    previousFlip = true;
                }
            });
    }

    this.reverseLoopButton = function (){
        var name = '#' + this.model.reverseButton;
        d3.select(name)
            .on('click', function(){
                if(self.model.current == 0) return; 
                reverseMode = true;
                if(isPaused){
                    self.model.prev();
                    self.transitionLine();
                }
                isPaused = false;
                
            });
    }

    this.resetButton = function (){
        var name = '#' + this.model.resetButton;
        d3.select(name)
            .on('click', function(){
                if(self.model.current == 0) return;    
                isPaused = true;
                self.model.goTo(0);
                self.transitionLine(); 
            });
    }

    this.lastButton = function (){
        var name = '#' + this.model.lastButton;
        d3.select(name)
            .on('click', function(){
                if(self.model.current == self.model.flips.length) return; 
                isPaused = true;
                self.model.goTo(self.model.flips.length);
                self.transitionLine()
    
            });
    }
   
    this.draw = function () {
            var flipCurrent = self.model.current; 
            var halfEdges = self.model.halfEdges;
            var graphC = self.model.graphs[flipCurrent];
            var textBox = d3.select(element.get(0)).append('text')
                            .attr('x', 20)
                            .attr('y', 30)
                            .attr('fill', 'black')
                            .attr("font-size", "40px");
            var viewBox = d3.select(element.get(0)).append("svg") 
                        .style('fill', 'black' )
                        .attr("viewBox", '0 0 650 650');
            
            self.setTextBox(textBox);
            var svg = viewBox.append('svg')
                        .append('g')
            viewBox.call(d3.zoom().scaleExtent([0.7, 1.4])
                        .translateExtent([[50, 50],[630, 630]])
                        .on("zoom", function () {
                            svg.attr("transform", d3.event.transform)}));

            self.setRoot(svg);
            self.playButton();
            self.pauseButton();
            self.nextButton();
            self.prevButton();
            self.reverseLoopButton();
            self.resetButton();
            self.lastButton();

            isPaused = true;
            for(let j = 0; j < graphC.nbTriangles; j++){    // parcours des triangulations du graphes
                for(let edge = 0; edge < 3; edge++){        // parcours des arêtes du graphes

                    let line = graphC.triangles[j].lines[edge];
                    if(!halfEdges.includes(line.tag)){          //verify if this line is a half-edge
                        var sLabel= self.drawLabel (svg,line) ;
                        var sLine = self.drawLine(svg, line, false);
                        sourceLines.push(sLine);                    // Add svg objects in lists
                        sourceLabels.push(sLabel);                  
                        srcTag.push(line.tag);                                    
                    }else{
                        var x = 0 ; 
                        while (line.tag != halfEdges[x] && x < halfEdges.length) x++ ;     
                        if(x%2 ==0 && x < halfEdges.length ){
                            sLabel = self.drawLabel(svg,line);
                            sLine = self.drawLine(svg, line, true);
                            sourceLines.push(sLine);
                            sourceLabels.push(sLabel);
                            srcTag.push(line.tag);
                        }
                    }          
                }       
            }
            lastLineDone = sourceLines.length;
            self.transitionLine();
    };
}


var model = new Model(data);
var ctrl = new Controler(model, new View(model)) ; 

ctrl.graph() ; 

})
