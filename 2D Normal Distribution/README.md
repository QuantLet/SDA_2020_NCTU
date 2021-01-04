[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **2D Normal Distribution** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Published in: 'SDA_2020_NCTU'

Name of Quantlet: '2D Normal Distribution'

Description: 'Generate 2D Normal Distribution with Polar Coordinates'

Submitted:  '4 January 2021'

Keywords: 
- Two Dimension
- Normal
- Uniform
- Exponential
- Box-muller

Input: 'random uniform distribution'

Output:  'Histogram_2dnorm.png'

Author: 'Dwilaksana Abdullah Rasyid'
```

![Picture1](Histogram%202D%20Normal.png)

### R Code
```r

##Generate 2D Normal Distribution: Box-Muller##

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
hist(twonorm, main="Histogram 2D Normal", xlab="value")

#Histogram
h <- hist(twonorm, breaks=10, col="grey",
          main="Histogram of 2D Normal", xlab="value", ylim=c(0,80000))
xfit <- seq(min(twonorm), max(twonorm), length = 40) 
yfit <- dnorm(xfit, mean = mean(twonorm), sd = sd(twonorm)) 
yfit <- yfit * diff(h$mids[1:2]) * length(twonorm) 

lines(xfit, yfit, col = "blue", lwd = 2)
```

automatically created on 2021-01-04