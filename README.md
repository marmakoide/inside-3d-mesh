# inside-3d-mesh

This project demonstrates a short Python function to determine if a set of
points are inside or outside a 3d mesh. The 3d mesh is assumed to be made of
triangles which all have the same orientation. This function manages to be
short yet robust and reasonnably fast. No preprocessing of the mesh is required.

The implementation is using the Generalized Winding Number of a 3d mesh, a
concept introduced in the paper 
[Robust Inside-Outside Segmentation using Generalized Winding Numbers](http://igl.ethz.ch/projects/winding-number/)
by Alec Jacobson, Ladislav Kavan and Olga Sorkine-Hornung.

## Getting Started

### Prerequisites

You will need

* A Unix-ish environment
* Python 2.7 or above
* [Numpy](http://www.numpy.org)
* [Matplotlib](https://matplotlib.org)
* The [xz](https://en.wikipedia.org/wiki/Xz) compression suite


### Running the demos

Both demos 

1. load an ASCII STL file (a file format for 3d triangle mesh) from the
standard input
2. generates an uniform random sampling of the volume enclosed by the mesh
3. displays the samples

Using one the sample STL files provided with the naive implementation demo

```
xzcat meshes/fox.stl.xz | python demo-naive.py
```

Likewise, for the optimized implementation demo

```
xzcat meshes/fox.stl.xz | python demo-turbo.py
```

## Authors

* **Alexandre Devert** - *Initial work* - [marmakoide](https://github.com/marmakoide)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

