import rpy2.robjects as ro

codigo_r = '''
funPrimo <- function(n){
  primos <- c(2,3)
  i <- 4
  k <- 3
  while (i <= n) {
    primos[k]<-i
    for (j in 2:(i%/%2)) {
     if(i%%j == 0){
       primos <- primos[-length(primos)]
       k <- k-1
       break
       }
    }
    i <- i+1
    k <- k+1
  }
  print(primos)
}
'''
ro.r(codigo_r)

primo_py = ro.globalenv['funPrimo']

print("Los numeros primos son")
primo_py(200)