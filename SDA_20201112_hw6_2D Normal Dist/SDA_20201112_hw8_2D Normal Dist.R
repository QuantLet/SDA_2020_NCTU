#Generate 2D Normal Distribution: Box-Muller

#size
n = 100000

#Uniform
u = runif(n)
v = runif(n)

x=rep(0,n)
y=rep(0,n)

for (i in 1:n){
  x[i] = sqrt(-2*log(u[i]))*cos(2*pi*v[i])
  y[i] = sqrt(-2*log(u[i]))*sin(2*pi*v[i])
}

#Two dimensional Normal Distribution
df <- data.frame(x,y)
print(df)

twonorm <- c(x,y)
hist(twonorm, main="Histogram of 2D Normal", xlab="value")

#Histogram
h <- hist(twonorm, breaks=10, col="grey",
          main="Histogram of 2D Normal", xlab="value", ylim=c(0,80000))
xfit <- seq(min(twonorm), max(twonorm), length = 40) 
yfit <- dnorm(xfit, mean = mean(twonorm), sd = sd(twonorm)) 
yfit <- yfit * diff(h$mids[1:2]) * length(twonorm) 

lines(xfit, yfit, col = "black", lwd = 2)
