[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **Crypto Currency Index (CRIX)** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Published in: 'SDA_2020_NCTU'

Name of Quantlet: 'Crypto Currency Index (CRIX)'

Description: 'Calculating index for Crypto Currency'

Output: 'Time series plot from yahoo finance dataset'

Keywords:
- Crypto Currency
- Yahoo finance
- Time Series
- Crypto Currency index
- Laspeyres price index

Author: Dwilaksana
```

![Picture1](time%20series%20plot%20from%20yahoo%20finance%20dataset.png)

### R Code
```r

index_comp = function(index_const, order_derive, current_lines_func, 
                      begin_line_func, comp1){
  
  index             = list()
  index_members_m   = list()
  index_members_t   = list()
  order_market_list = list()
  
  if (per == 1){
    index_value = base_value
  } else if (comp1 == T) {
    index_value = tail(crix[, 1], n = 1)
  } else if (comp1 == F){
    index_value = base_value
  }
  ##########################################################
  ############## for loop for index computation ############
  ##########################################################
  for (i in 1:(index_periods)){
    if (i == 1){
      last_index_period_time   = price[current_lines_func[1]:(
        current_lines_func[2] - 1), ]
      last_index_period_market = market[current_lines_func[1]:(
        current_lines_func[2] - 1), ]
      if (chosen_index == "CRIX") {
        last_index_period_vol = vol[current_lines_func[1]:(
          current_lines_func[2] - 1), ]}
      if (chosen_index == "CRIX") {
        omit_last = Reduce(intersect, list(which(apply(is.na(
          last_index_period_time), 2, any)
          == F), which(apply(is.na(last_index_period_market), 2, any) == F), 
          which(apply(is.na(last_index_period_vol), 2, any) == F)))
      } else {
        omit_last = Reduce(intersect, list(which(apply(is.na(
          last_index_period_time), 2, any)
          == F), which(apply(is.na(last_index_period_market), 2, any) == F)))
      }
      last_index_period_time   = last_index_period_time[, omit_last]
      last_index_period_market = last_index_period_market[, omit_last]
      if (chosen_index == "CRIX") {
        last_index_period_vol = last_index_period_vol[, omit_last]
      }
      omit_last_zero           = Reduce(intersect, list(which(apply(
        last_index_period_time == 0, 2, any) == F), which(apply(
          last_index_period_market == 0, 2, any) == F)))
      last_index_period_time   = last_index_period_time[, omit_last_zero]
      last_index_period_market = last_index_period_market[, omit_last_zero]
      if (chosen_index == "CRIX") {
        last_index_period_vol = last_index_period_vol[, omit_last_zero]
      }
    } else {
      if (chosen_index == "CRIX") {
        omit_now = Reduce(intersect, list(which(apply(is.na(
          index_period_time), 2, any) == F), which(apply(
            is.na(index_period_market), 2, any) == F), which(apply(
              is.na(index_period_vol), 2, any) == F)))
      } else {
        omit_now = Reduce(intersect, list(which(apply(is.na(
          index_period_time), 2, any)
          == F), which(apply(is.na(index_period_market), 2, any) == F)))
      }
      last_index_period_time    = index_period_time[, omit_now]
      last_index_period_market  = index_period_market[, omit_now]
      if (chosen_index == "CRIX") {
        last_index_period_vol = index_period_vol[, omit_now]
      }
      omit_now_zero            = Reduce(intersect, list(which(apply(
        index_period_time == 0, 2, any) == F), which(apply(
          index_period_market == 0, 2, any) == F)))
      last_index_period_time   = index_period_time[, omit_now_zero]
      last_index_period_market = index_period_market[, omit_now_zero]
      if (chosen_index == "CRIX") {
        last_index_period_vol = index_period_vol[, omit_now_zero]
      }
    }
    
    if (dim(last_index_period_market)[2] <= index_const){
      return(NULL)
    }
    
    last_line = if (i == 1){
      begin_line_func
    } else {
      next_line
    } 
    break_loop = FALSE
    if (per == numb_aic & is.na(current_lines_func[i + (2)]) == T) {
      next_line = length(all_days) + 1
      break_loop = TRUE
    } else {
      next_line = current_lines_func[i + 2]
    }
    last_index_time   = price[(last_line - 1), ]
    last_index_market = market[(last_line - 1), ]
    if (chosen_index == "CRIX") {
      last_index_vol = vol[(last_line - 1), ]  
    }
    if (chosen_index == "CRIX") {
      ### Liquidity rule 1: 
      adtv_cryptos = apply(last_index_period_vol, 2, mean)
      adtv_perc    = quantile(adtv_cryptos, 0.25)
      adtv_which   = which(adtv_cryptos >= adtv_perc)
      ### Liquidity rule 2: 
      adtc_cryptos = apply((last_index_period_vol / last_index_period_time), 
                           2, mean)
      adtc_perc    = quantile(adtc_cryptos, 0.25)
      adtc_which   = which(adtc_cryptos >= adtc_perc)
      w_take       = unique(adtv_which, adtc_which)
      if (length(w_take) != 0){
        last_index_period_time   = last_index_period_time[, w_take]
        last_index_period_market = last_index_period_market[, w_take]
        last_index_period_vol    = last_index_period_vol[, w_take]
      }
    }
    
    order_market = order(last_index_market[colnames(last_index_period_market)], 
                         decreasing = T)
    if (order_derive == T){
      order_market_list = append(order_market_list, list(colnames(
        last_index_period_time[, order_market])))
    }
    
    if (chosen_index == "CRIX") {
      if (length(w_take) >= index_const){
        order_market = order_market[1:index_const]
      } else {
        order_market = order_market[1:length(w_take)]
      }
    } else if (chosen_index == "ECRIX" || chosen_index == "EFCRIX" || 
               chosen_index == "DAX" || chosen_index == "IPC") {
      if (length(order_market) >= index_const){
        order_market = order_market[1:index_const]
      }
    }
    
    index_members_m[[i]]     = colnames(last_index_period_market)[order_market]
    index_members_t[[i]]     = colnames(last_index_period_time)[order_market]
    last_index_period_time   = last_index_period_time[, order_market]
    last_index_period_market = last_index_period_market[, order_market]
    if (chosen_index == "CRIX") {
      last_index_period_vol = last_index_period_vol[, order_market]
    }
    
    if (is.null(dim(last_index_period_market)) == T) {
      if (i == 1){
        divisor = sum(tail(last_index_period_market, n = 1)) / index_value
      } else if (i > 1){
        divisor = sum(last_index_market[index_members_m[[i]]]) / 
          index[[i - 1]][length(index[[i - 1]])]
      }
    } else {
      if (i == 1){
        divisor = sum(tail(last_index_period_market[, index_members_m[[i]]], 
                           n = 1)) / index_value
      } else if (i > 1){
        divisor = sum(last_index_market[index_members_m[[i]]]) / 
          index[[i - 1]][length(index[[i - 1]])]
      }
    }
    
    index_period_time   = price[last_line:(next_line - 1),]
    index_period_market = market[last_line:(next_line - 1),]
    if (chosen_index == "CRIX") {
      index_period_vol = vol[last_line:(next_line - 1),]
    }
    
    index_period_time1   = na.locf(price)[last_line:(next_line - 1),]
    index_period_market1 = na.locf(market)[last_line:(next_line - 1),]
    if (chosen_index == "CRIX") {
      index_period_vol1 = na.locf(vol)[last_line:(next_line - 1),]
    }
    
    index_old_amount = (last_index_market)[index_members_m[[i]]] / 
      (last_index_time)[index_members_t[[i]]]
    if (is.null(dim(index_period_time1))) {
      index_comp1 = t(index_old_amount * t(index_period_time1[
        index_members_t[[i]]]))
      index[[i]] = sum(index_comp1)
    } else {
      index_comp1 = t(index_old_amount * t(index_period_time1[, 
                                                              index_members_t[[i]]]))
      index[[i]] = apply(index_comp1, 1, sum)
    }
    index[[i]] = index[[i]] / divisor
    
    if (break_loop == T){
      break
    }
  } # end for loop
  
  ################### Index derivation done
  # building whole index time series
  plot_index = c()
  for (i in 1:length(index)){
    plot_index = c(plot_index, index[[i]])
  }
  
  list(plot_index, order_market_list)
}

# end function

##### begin function all ####

index_comp_all = function(index_const, current_lines_func, begin_line_func, 
                          comp, comp1){
  
  index           = list()
  index_members_m = list()
  index_members_t = list()
  full_coin_numb  = c()
  
  if (per == 1){
    index_value = base_value
  } else if (comp1 == T){
    if (comp == T){
      index_value = tail(crix[, 1], n = 1)[[1]]
    } else {
      index_value = tail(crix_all[, 1], n = 1)[[1]]
    }
  } else if (comp1 == F){
    index_value = base_value
  }
  
  ##########################################################
  ############## for loop for index computation ############
  ##########################################################
  for ( i in 1:(index_periods)){
    if (i == 1){
      last_index_period_time   = price[current_lines_func[1]:(
        current_lines_func[2] - 1),]
      last_index_period_market = market[current_lines_func[1]:(
        current_lines_func[2] - 1),]
      omit_last                = Reduce(intersect, list(which(apply(is.na(
        last_index_period_time), 2, any) == F), which(apply(is.na(
          last_index_period_market), 2, any) == F)))
      last_index_period_time   = last_index_period_time[, omit_last]
      last_index_period_market = last_index_period_market[, omit_last]
      omit_last_zero           = Reduce(intersect, list(which(apply(
        last_index_period_time == 0, 2, any) == F), which(apply(
          last_index_period_market == 0, 2, any) == F)))
      last_index_period_time   = last_index_period_time[, omit_last_zero]
      last_index_period_market = last_index_period_market[, omit_last_zero]
    } else {
      omit_now                 = Reduce(intersect, list(which(apply(is.na(
        index_period_time), 2, any) == F), which(apply(is.na(
          index_period_market), 2, any) == F)))
      last_index_period_time   = index_period_time[, omit_now]
      last_index_period_market = index_period_market[, omit_now]
      omit_now_zero            = Reduce(intersect, list(which(apply(
        index_period_time == 0, 2, any) == F), which(apply(
          index_period_market == 0, 2, any) == F)))
      last_index_period_time   = index_period_time[, omit_now_zero]
      last_index_period_market = index_period_market[, omit_now_zero]
    }
    
    last_line = if (i == 1){
      begin_line_func
    } else {
      next_line
    }
    break_loop = FALSE
    if (per == numb_aic & is.na(current_lines_func[i + 2]) == T) {
      next_line  = length(all_days) + 1
      break_loop = TRUE
    } else {
      next_line = current_lines_func[i + 2]
    }
    
    last_index_time          = price[(last_line - 1),]
    last_index_market        = market[(last_line - 1),]
    order_market             = order(last_index_market[colnames(
      last_index_period_market)], decreasing = T)
    last_index_period_time   = last_index_period_time[, order_market]
    last_index_period_market = last_index_period_market[, order_market]
    full_coin_numb           = c(full_coin_numb, dim(last_index_period_time)[2])
    index_members_m[[i]]     = colnames(last_index_period_market)
    index_members_t[[i]]     = colnames(last_index_period_time)
    if (i == 1){
      divisor = sum(tail(last_index_period_market[, index_members_m[[i]]], 
                         n = 1)) / index_value
    } else if (i > 1){
      divisor = sum(last_index_market[index_members_m[[i]]]) / 
        index[[i - 1]][length(index[[i - 1]])]
    }
    
    index_period_time    = price[last_line:(next_line - 1),]
    index_period_market  = market[last_line:(next_line - 1),]
    index_period_time1   = na.locf(price)[last_line:(next_line - 1),]
    index_period_market1 = na.locf(market)[last_line:(next_line - 1),]
    index_old_amount     = (last_index_market)[index_members_m[[i]]] / 
      (last_index_time)[index_members_t[[i]]]
    if (is.null(dim(index_period_time1))) {
      index_comp1 = t(index_old_amount * t(index_period_time1[
        index_members_t[[i]]]))
      index[[i]]  = sum(index_comp1)
    } else {
      index_comp1 = t(index_old_amount * t(index_period_time1[, 
                                                              index_members_t[[i]]]))
      index[[i]]  = apply(index_comp1, 1, sum)
    }
    index[[i]] = index[[i]] / divisor
    if (break_loop == T){
      break
    }
  } # end for loop
  
  ################### Index derivation done
  ########## checking of the index ###################
  # building whole index time series
  plot_index = c()
  for (i in 1:length(index)){
    plot_index = c(plot_index, index[[i]])
  }
  
  list(plot_index, full_coin_numb)
}

# end function

#=======================================================================
# please change your working directory
#setwd("C:/...")

# Specify index to compute, should be either CRIX, ECRIX, EFCRIX, 
# DAX or IPC. Default CRIX
chosen_index = "CRIX"

#load("CryptoData.RData")
#source("CRIXcodehelper.R")

# install and load packages
libraries = c("lubridate", "fBasics", "dgof", "ks", "KernSmooth", "zoo")
lapply(libraries, function(x) if (!(x %in% installed.packages())) {
    install.packages(x)
})
lapply(libraries, library, quietly = TRUE, character.only = TRUE)

library("readxl")


#ifelse(is

coins_price2=read.csv("D:/S2/NCTU/smart data analytics 1/crix analysis/-crypto-price-new.csv",header=T,sep=';',row.names="date")
coins_vol2=read.csv('D:/S2/NCTU/smart data analytics 1/crix analysis/-crypto-volume-new.csv',header=T,sep=';',row.names="date")
coins_market2=read.csv('D:/S2/NCTU/smart data analytics 1/crix analysis/-crypto-market.csv',header=T,sep=';',row.names="date")
index = rownames(coins_price2)
coins_price2.m <- as.matrix(coins_price2) ; coins_vol2.m <- as.matrix(coins_vol2) ; coins_market2.m <- as.matrix(coins_market2)
matrix_coins <- matrix(coins_price2.m, nrow = 2235, ncol = 12, dimnames=list(c(index),c(names(coins_price2))))
matrix_vol <- matrix(coins_vol2.m, nrow = 2235, ncol = 12, dimnames=list(c(index),c(names(coins_vol2))))
matrix_market <- matrix(coins_market2.m, nrow = 2235, ncol = 12, dimnames=list(c(index),c(names(coins_price2))))

coins_price2=as.data.frame(sapply(coins_price2, as.character))
coins_vol2=as.data.frame(sapply(coins_vol2, as.character))
coins_market2 = as.data.frame(sapply(coins_market2, as.character))
coins_price = matrix_coins;coins_vol = matrix_vol;coins_market=matrix_market


base_value            = 1000
begin_date            = "01"
derivation_period     = 1
derivation_period_aic = 3
if (chosen_index == "DAX" || chosen_index == "IPC") {
    derivation_period     = 3
    derivation_period_aic = 3
}

switch(chosen_index,
    "CRIX"   = {market = coins_market
                   price  = coins_price
                   vol    = coins_vol},
    "ECRIX"  = {market = coins_market
                   price  = coins_price
                   vol    = coins_vol},
    "EFCRIX" = {market = coins_market
                   price  = coins_price
                   vol    = coins_vol},
    "DAX"    = {market = Germany_market
                   price  = Germany_price},
    "IPC"    = {market = Mexico_market
                   price  = Mexico_price}
)
  

if (chosen_index == "CRIX" || chosen_index == "ECRIX" || 
    chosen_index == "EFCRIX") {
    all_days  = sub('.*(?=.{2}$)', '', rownames(price), perl=T)
    days_line = which(begin_date == all_days)
} else if (chosen_index == "DAX") {
    all_days      = sub('.*(?=.{2}$)', '', rownames(price), perl=T)
    find_friday1  = which(diff(as.numeric(all_days)) < 0) + 1 
    find_friday2  = which(weekdays(as.Date(rownames(price))) == "Friday")
    find_friday3  = find_friday2[find_friday2 > 44]
    find_friday4  = find_friday1[-c(1, 2)]
    third_fridays = c() 
for (i in 2:length(find_friday4)) {
    third_fridays[i - 1] = find_friday3[find_friday3 >= find_friday4[i - 1] & 
    find_friday3 < find_friday4[i]][3]
}
    days_line = third_fridays + 1
} else if (chosen_index == "IPC") {
    all_days  = sub('.*(?=.{2}$)', '', rownames(price), perl = T)
    days_line = (which(diff(as.numeric(all_days)) < 0) + 1)[-c(1:5)]
}
index_periods = max(floor(derivation_period_aic / derivation_period), 1)
numb_aic1     = (length(days_line) - (derivation_period + 1)) / 
    derivation_period_aic
if ((numb_aic1%%1 == 0) == TRUE){
    numb_aic = numb_aic1 - 1
} else {
    numb_aic = floor(numb_aic1)
}

index_comp_numb = switch(chosen_index,
    "CRIX"   = {seq(5,dim(price)[[2]], 5)},
    "ECRIX"  = {seq(1,dim(price)[[2]], 1)},
    "EFCRIX" = {seq(1,dim(price)[[2]], 1)},
    "DAX"    = {seq(30,dim(price)[[2]], 5)},
    "IPC"    = {seq(35,dim(price)[[2]], 5)}
)

aic_matrix    = matrix(NA, nrow = numb_aic, ncol = length(index_comp_numb))
max_coin_numb = matrix(NA, nrow = 1, ncol = numb_aic)
for (per in 1:numb_aic){
    print(paste(per, " / ", numb_aic, sep = ""))
    current_lines         = days_line[seq((1 + derivation_period_aic * 
        (per - 1)), (derivation_period_aic * per + (derivation_period + 1)), 
    derivation_period)]
    begin_line            = current_lines[2]
    index_t_v_all         = index_comp_all("dummy", current_lines, begin_line, 
        TRUE, FALSE)
    max_coin_numb[1, per] = max(index_t_v_all[[2]])
for (per1 in 1:length(index_comp_numb)){
    index_t_v_numb = index_comp(index_comp_numb[per1], FALSE, current_lines, 
        begin_line, FALSE)
    plot_diff      = index_t_v_all[[1]] - index_t_v_numb[[1]]
    logLik1        = c()
for (cv1 in 1:length(plot_diff)){
    eva = try(with(density(plot_diff[-cv1], bw = dpik(plot_diff[-cv1], 
        kernel = "epanech", gridsize = 1601L), kernel = "epanechnikov"), 
        approxfun(x, y, yleft = 0.00000000000000000001, 
        yright = 0.00000000000000000001)), silent = T)
if (class(eva) == "try-error"){
    break
}
    eva1         = eva(plot_diff[cv1])
    logLik1[cv1] = log(eva1)
}
if (class(eva) == "try-error"){
    break
}
    logLik                = sum(logLik1)
    aic_matrix[per, per1] = 2 * index_comp_numb[per1] - 2 * logLik
if (chosen_index == "CRIX" || chosen_index == "ECRIX" || 
    chosen_index == "DAX" || chosen_index == "IPC") {
if (per1 >= 2){
if (aic_matrix[per, per1] > aic_matrix[per, per1 - 1]){
    break
}
}
}
}
if (chosen_index == "CRIX" || chosen_index == "ECRIX" || 
    chosen_index == "DAX" || chosen_index == "IPC") {
if (per1 > 1) {
    index_members = index_comp_numb[per1 - 1]
} else if (per1 == 1) {
    index_members = index_comp_numb[per1]
}
} else if (chosen_index == "EFCRIX") {
    index_members = which.min(aic_matrix[per,])
}
    current_lines1 = days_line[seq((1 + derivation_period_aic * (per)), 
        (derivation_period_aic * (per + 1) + (derivation_period + 1)), 
        derivation_period)]
    begin_line1    = current_lines1[2]
    crix1          = index_comp(index_members, TRUE, current_lines1, 
        begin_line1, TRUE)
while (is.null(crix1)){
    index_members = index_members - 1
    crix1         = index_comp(index_members, TRUE, current_lines1, begin_line1, 
        TRUE)
}
    crix2     = crix1[[1]]
    crix_all2 = index_comp_all("dummy", current_lines1, begin_line1, 
        FALSE, TRUE)
    crix_all1 = crix_all2[[1]]
    crix_all4 = index_comp_all("dummy", current_lines1, begin_line1, TRUE, TRUE)
    crix_all3 = crix_all4[[1]]
if (per == 1){
    crix          = do.call(cbind,list(crix2))
    crix_all      = do.call(cbind,list(crix_all1))
    crix_all_comp = do.call(cbind,list(crix_all3))
} else {
    crix          = rbind(crix, do.call(cbind, list(crix2)))
    crix_all      = rbind(crix_all, do.call(cbind, list(crix_all1)))
    crix_all_comp = rbind(crix_all_comp, do.call(cbind, list(crix_all3)))
}
}

#compare the crix origin and crix 12 crypto
plot(as.ts(crix_all_comp))
crix=read.csv("D:/S2/NCTU/smart data analytics 1/crix analysis/_crix.csv",header=T,sep=',')
plot(as.ts(crix['price']),add=T)

#summary(is.na(coins_market))
#quantile()
```

automatically created on 2020-11-19