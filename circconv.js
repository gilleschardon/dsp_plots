
var margins = {
  left: 50,
  right: 200,
  bottom: 10,
  top: 10
};

var L = 12

var t = [...Array(L).keys()]

var x = Array(L).fill(0)
var y = Array(L).fill(0)
var z = Array(L).fill(0)
var r = Array(L).fill(10)

datax = {x: t, y:x, r: r}
datay = {x: t, y:y, r: r}
dataz = {x: t, y:z, r: r}

xrange = [-0.5,L-0.5];
yrange = [-2, 2]
yrange2 = [-5, 5]


ntickx = 20
nticky = 5

axisx = new Axis("#plotx", "x", 700, 150, margins, xrange, yrange, ntickx, nticky)
axisy = new Axis("#ploty", "y", 700, 150, margins, xrange, yrange, ntickx, nticky)
axisz = new Axis("#plotz", "z", 700, 300, margins, xrange, yrange2, ntickx, nticky*2)


function update_data()
{
  dataz.y.fill(0)
  for (var k = 0 ; k < L ; k++)
  {
    for (var l = 0 ; l < L ; l++)
    {
      dataz.y[(k+l)%L] = dataz.y[(k+l)%L] + datax.y[k] * datay.y[l]
    }
  }

}

function update()
{
  update_data()

  stemx.update()
  stemy.update()
  stemz.update()
}

function reset()
{
  datax.y.fill(0)
  datay.y.fill(0)
  dataz.y.fill(0)

  stemx.update()
  stemy.update()
  stemz.update()
}

function updatex(i, x, y)
{
  datax.y[i] = y
  update()
}
function updatey(i, x, y)
{
  datay.y[i] = y
  update()
}
stemx = axisx.stem("dx", "\\( \\mathbf{x} \\)", datax, updatex)
stemy = axisy.stem("dy", "\\( \\mathbf{y} \\)", datay, updatey)
stemz = axisz.stem("dz", "\\( \\mathbf{x} \\circledast \\mathbf{y} \\)", dataz)

d3.select('#reset').on("click", reset)
