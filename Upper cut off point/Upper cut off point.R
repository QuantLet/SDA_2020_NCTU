#generate random normal standard
rand_norm=rnorm(100000)
boxplot(rand_norm)
#calculate uppercut point
uppercut=(quantile(rand_norm,0.75)+(1.5*(quantile(rand_norm,0.75)-quantile(rand_norm,0.25))))
#calculate empirical CDF from random normal
f_upper_cut=ecdf(rand_norm)
#calculate probability of uppercut point
prob=1-f_upper_cut(uppercut)
