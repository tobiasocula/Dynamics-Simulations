This article basically describes the exact thing I'm doing here:

https://www.sciencedirect.com/science/article/pii/S2095034919300200

First we note that the parametrisation for the surface in 3D we use is of the form

$F(x,y)=(x,y,f(x,y))$

Then we compute the normal vector:

$N(F(x,y))=(-\frac{df}{dx},-\frac{df}{dy},1) / ||(-\frac{df}{dx},-\frac{df}{dy},1)||$

We will denote this by $n$.

We then define the matrix $P$ as the linear operator which projects onto the tangent plane (perpendicular to $n$):

$P=I-nn^{T}$

This matrix of course depends on the position vector $r$.

We first decompose the acceleration vector $r''$ as:

$r''=g+\lambda n$

such that it has a pure gravitational component and a normal component. We then apply the projection $P$:

$Pr''=Pg+Pn$

but because $Pn=0$ and we want that $r''$ is tangent, we get

$r''=Pg=(I-nn^{T})g=g-(g\cdot n)n$

where $P$ depends on the position $r$ of course.

Another way to see it is: the desired acceleration $r''$ should be the tangent component of gravity.

We can also add friction to this, to make it more realistic:

$r''=Pg+\mu |r'|r'$

If we write this out in coordinates, we get the system of ODEs

\begin{equation}
\begin{aligned}
x''=-g\cdot f_x/D-\mu |v|x'\\
y''=-g\cdot f_y/D-\mu |v|y'\\
z''=-g\cdot g/D-\mu |v|z'
\end{aligned}
\end{equation}

where

\begin{equation}
\begin{aligned}
D=\sqrt{1+f_{x}^2+f_{y}^2}\\
v=r'=\sqrt{(x')^2+(y')^2+(z')^2}
\end{aligned}
\end{equation}

At each step of the iteration, we also (for the sake of numerical stability), project the velocity vector $v=(x',y',z')$ onto the tangent plane, by doing

$v\leftarrow v-(v\cdot n)n$

and normalizing.