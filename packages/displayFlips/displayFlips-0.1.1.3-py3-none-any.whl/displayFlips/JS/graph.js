/**
 * graph class contains an array of Trianglutaion class. 
 */

define(['triangle'], function (Triangle) {
    return function Graph (coord, color, faces, X, Y) {
            this.triangles = [];
            this.nbTriangles = coord.length;
            this.Xlimits = X;
            this.Ylimits = Y;
            for(let i = 0; i < this.nbTriangles; i++){
                var tri = new Triangle(coord[i], color, faces[i]) ; 
                this.triangles.push(tri);
            }
    }
}) ; 