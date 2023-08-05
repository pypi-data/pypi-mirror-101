/**
 * Triangle class contains data of a triangulation : 
 *  - lines -> table of Line class
 * Class needs an array of coordonate, colors and faces.   
 */

define(['line'], function(Line){
    return function Triangle (coords, colors, faces) {
            this.lines = [];
            for(let i = 0; i < 3; i++){
                let linePoints = [coords[i%3], coords[(i+1)%3] ];
                let nl = new Line(linePoints, colors[faces[i]], faces[i]);
                this.lines.push( nl );
            }
    }
}) ; 