


var margins = {
  left: 50,
  right: 200,
  bottom: 10,
  top: 10
};

var L = 8

const FFT = new FFTNayuki(L)

var t = [...Array(L).keys()]

var sigreal = Array(L).fill(0)
var sigimag = Array(L).fill(0)
var dftreal = Array(L).fill(0)
var dftimag = Array(L).fill(0)

var r = Array(t.length).fill(15)


datasigreal = {x: t, y:sigreal, r: r}
datasigimag = {x: t, y:sigimag, r: r}
datadftreal = {x: t, y:dftreal, r: r}
datadftimag = {x: t, y:dftimag, r: r}

xrange = [-0.5,L + 0.5];
yrangesig = [-5, 5]
yrangedft = [-2.5 * L, 2.5 * L]


ntickx = L
nticky = 5

axissig = new Axis("#plotsig",  "sig", 1000, 200, margins, xrange, yrangesig, ntickx, nticky)
axisdft = new Axis("#plotdft", "dft", 1000, 200, margins, xrange, yrangedft, ntickx, nticky)




function updatesig(i, x, y, data)
{
  data.y[i] = y

  let real = Float32Array.from(datasigreal.y)
  let imag = Float32Array.from(datasigimag.y)
  FFT.forward(real, imag)

  datadftreal.y = real
  datadftimag.y = imag

  update()
}


function updatefreq(i, x, y, data)
{
  data.y[i] = y

  let real = Float32Array.from(datadftreal.y)
  let imag = Float32Array.from(datadftimag.y)
  FFT.inverse(real, imag)

  datasigreal.y = real.map(t => t/L)
  datasigimag.y = imag.map(t => t/L)

  update()
}

function reset()
{
  datasigreal.y.fill(0)
  datasigimag.y.fill(0)
  datadftreal.y.fill(0)
  datadftimag.y.fill(0)

  update()
}

function update()
{
  stemsigreal.update()
  stemsigimag.update()
  stemdftreal.update()
  stemdftimag.update()

}

symbolreal = "M 0 1 L -1 0 L 0 -1 Z"
symbolimag = "M 0 1 L 1 0 L 0 -1 Z"

stemsigreal = axissig.stem("sigreal", "\\(\\Re x_n\\)", datasigreal, (i, x, y) => updatesig(i, x, y, datasigreal), symbolreal)
stemsigimag = axissig.stem("sigimag", "\\(\\Im x_n\\)", datasigimag, (i, x, y) => updatesig(i, x, y, datasigimag), symbolimag)
stemdftreal = axisdft.stem("dftreal", "\\(\\Re X_k\\)", datadftreal, (i, x, y) => updatefreq(i, x, y, datadftreal), symbolreal)
stemdftimag = axisdft.stem("dftimag", "\\(\\Im X_k\\)", datadftimag, (i, x, y) => updatefreq(i, x, y, datadftimag), symbolimag)

d3.select('#reset').on("click", reset)
