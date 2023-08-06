/**
 * Model class, where we stock data.
 * In our case Model contains an object type triangulation.
 */
define(['graph'], function (Graph) {
    return function Model(s) {
    
        this.var = JSON.parse(s);
        this.flips = this.var.flips;
        this.current = 0;
    
        this.datax = this.var.dataX;
        this.datay = this.var.dataY;
    
    
        this.playButton = this.var.playButton; 
        this.pauseButton = this.var.pauseButton;
        this.nextButton = this.var.nextButton;
        this.prevButton = this.var.prevButton;
        this.reverseButton = this.var.reverseButton;
        this.resetButton = this.var.resetButton;
        this.lastButton = this.var.lastButton;
        this.duration = this.var.duration;
    
        this.reset = function(){
            this.current = 0;
        };
    
    
        this.next = function(){
            this.current ++;
        };
    
        this.prev = function(){
            this.current --;
        };
    
        this.goTo = function(ind){
            this.current = ind;
        };
    
        this.addGraphs = function(){
            let colors = this.var.edgeColor;
            let faces = this.var.faces;
            let coord = this.var.pos;
            let graphs = [];
            let X = this.datax;
            let Y = this.datay;
    
            for(let i = 0; i <= this.flips.length; i++){
    
                graphs.push(new Graph(coord[i], colors[i], faces[i], X[i], Y[i]));
            }
            return graphs;
        };
    
        this.graphs = this.addGraphs();
    
        this.computeHalfEdges = function(edges){
            var halfEdges = [];
            for(var i = 0; i < edges.length; i++){
                if(edges[i].length>1){
                    if(edges[i][0] < edges[i][1]){
                        halfEdges.push(edges[i][0]);
                        halfEdges.push(edges[i][1]);
                    }
                    else{
                        halfEdges.push(edges[i][1]);
                        halfEdges.push(edges[i][0]);
                    }
                        
                }
            }
            
            return halfEdges;
        };
        this.halfEdges = this.computeHalfEdges(this.var.edges);
        
    };
})