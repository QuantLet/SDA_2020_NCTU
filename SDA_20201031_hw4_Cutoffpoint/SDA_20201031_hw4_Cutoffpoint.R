#Generate random number from normal distribution
set.seed(1357)
n=1000
normal = rnorm(n)

#histogram and its density
h <- hist(normal, breaks=10, col="blue",
     main="Histogram with Normal Curve")
xfit <- seq(min(normal), max(normal), length = 40) 
yfit <- dnorm(xfit, mean = mean(normal), sd = sd(normal)) 
yfit <- yfit * diff(h$mids[1:2]) * length(normal) 

lines(xfit, yfit, col = "black", lwd = 2)


# 25% quantile
q25 <- as.numeric(quantile(normal, probs =0.25))

# 75% quantile
q75 <- as.numeric(quantile(normal, probs =0.75))

#upper cut off point
w = q75 + 1.5 *(q75-q25)
cat("The cut off point is: ", w)

#Boxplot of the data
boxplot(normal, main="Boxplot")

# CDF with x=w
phi<- pnorm(w, mean = 0, sd = 1)

# Calculate the probability of a “normal (distribution)” to be outside the upper cutoff point
p = 2*(1-phi)
cat("The probability of a “normal (distribution)” to be outside the upper cutoff point: ", p)

