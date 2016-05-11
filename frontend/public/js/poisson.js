function poisson(lambda) {
  return function(k) {
    return Math.pow(lambda, k) * Math.exp(-lambda) / factorial(k);
  }
}

function factorial(k) {
  var s = 1;
  for (var i=2;i<=k;i++)
    s *= i;
  return s;
}

function getProb(a, b) {
  var f = poisson(a);
  var g = poisson(b);
  var aWin = 0;
  var bWin = 0;
  for (var i=0;i<30;i++) {
    for (var j=0;j<30;j++) {
      if (i < j)
        bWin += f(i) * g(j);
      if (j < i)
        aWin += f(i) * g(j);
    }
  }
  return [aWin, bWin];
}
