/**
 * Line class represents a half-edges. He stocked the
 * position of tag (=number of half-edge), label(= position of label),
 * his its and position of points which compose it. 
 */

define (function() {
    function labelPosition (coords){
        var xMean = (coords[0][0] + coords[1][0])/2;
        var yMean = (coords[0][1] + coords[1][1])/2;
        var labelPos = [xMean, yMean];
        return labelPos;
    }
    return function Line(coords, color, id)  {
        this.coords = [];
        this.color = "";
        this.tag = id; 
        for(let i = 0; i < 2; i++){
            this.coords.push(coords[i]);
        }
        this.label = labelPosition(this.coords); 
        if(color == 1)
            this.color = "red";
        else if(color == 2)
            this.color = "steelblue";
        else if(color == 8)
            this.color = "green";
        else
            this.color = "#C71585";

            
        }
}) ; 