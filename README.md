# inside-3d-mesh

This project demonstrates a short Python function to determine if a set of
points are inside or outside a 3d mesh. The 3d mesh is assumed to be made of
triangles which all have the same orientation. This function manages to be
short yet robust and reasonnably fast.

The implementation is using the Generalized Winding Number of a 3d mesh, a
concept introduced in the paper 
[Robust Inside-Outside Segmentation using Generalized Winding Numbers](http://igl.ethz.ch/projects/winding-number/)
by Alec Jacobson, Ladislav Kavan and Olga Sorkine-Hornung.
