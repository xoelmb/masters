setwd("/home/xoel/github/masters/module_ii/statistical_inference/assignment")
library(dplyr)
library(ggplot2)

# The dataset had to be fixed, since there was blank spaces instead of tabulations at different points across the file.
finches <- read.table("./finches_dataset.txt", header=TRUE, sep="\t")
# Replace the unknown values for Sex with NA.
finches$Sex[finches$Sex == "unknown"] <- NA
finches$Sex <- droplevels(finches$Sex)


# Check which variables are in the dataset
colnames(finches)


# Feature amplification
Age <- finches$Last_Year - finches$First_adult_year + 1
Survival = finches$Last_Year > 1977
finches <-cbind(finches, Age, Survival)


# Remove Band and Species
finches <- finches[,c(3:ncol(finches))]


# Statistics of the variables
for (i in c(1:ncol(finches))){
  print(colnames(finches)[i])
  print(summary(finches[,i]))
  if (colnames(finches)[i] != "Sex" & colnames(finches)[i] != "Survival"){
    print(paste("Var:",var(finches[,i])))
    print(paste("SD:",sd(finches[,i])))
  }
}


# Plot of sex distribution
gendertab <- table(finches$Sex, useNA = "ifany")
names(gendertab)[is.na(names(gendertab))] <- "unknown"
barplot(gendertab, ylim=c(0,50), ylab="Number of specimens", col=c("purple", "gold", "white"), main="Sex")


# Plot of the rest of the variables and normality check
nam_units <- c("Weigth (g)", "Wing (mm)", "Tarsus (mm)", "Beak length (mm)", "Beak depth (mm)", "Beak width (mm)", "Age (years)")
for (i in c(4:10)){
  hist(finches[,i], prob=TRUE, xlab=nam_units[i-3], main="", xlim=c(min(finches[,i]), max(finches[,i]+1)))
  lines(density(finches[,i]))
  norm_result <- shapiro.test(finches[,i])[["p.value"]]
  if (norm_result < 0.05){
    cat(paste(colnames(finches)[i], "is not normally distributed.\n p-value:", norm_result, "\n"))
  }
  else{
    cat(paste(colnames(finches)[i], "is normally distributed.\n p-value:", norm_result, "\n"))
  }
  boxplot(finches[,i], xlab=nam_units[i-3])
}


# Correlation, scatter, density matrix
ggpairs(finches)


# Checking if weight and wing follow normal distributions if divided by sex  
norm_result <- shapiro.test(finches$Weight_.g.[which(finches$Sex == "male")])[["p.value"]]
norm_result # Normal
norm_result <- shapiro.test(finches$Weight_.g.[which(finches$Sex == "female")])[["p.value"]]
norm_result # Not normal

norm_result <- shapiro.test(finches$Wing_.mm.[which(finches$Sex == "male")])[["p.value"]]
norm_result  # Normal
norm_result <- shapiro.test(finches$Wing_.mm.[which(finches$Sex == "female")])[["p.value"]]
norm_result  # Normal

#Checking if weight and wing follow normal distributions if divided by survival  
norm_result <- shapiro.test(finches$Weight_.g.[which(finches$Survival == TRUE)])[["p.value"]]
norm_result # Not normal
norm_result <- shapiro.test(finches$Weight_.g.[which(finches$Survival == FALSE)])[["p.value"]]
norm_result # Normal

norm_result <- shapiro.test(finches$Wing_.mm.[which(finches$Survival == TRUE)])[["p.value"]]
norm_result  # Normal
norm_result <- shapiro.test(finches$Wing_.mm.[which(finches$Survival == FALSE)])[["p.value"]]
norm_result  # Normal


# Testing differences between groups
groups_lab <- c("Sex","Survival")
quant_lab <- c("Wing_.mm.", "Tarsus_.mm.", "Beak_Length_.mm.", "Beak_Depth_.mm.", "Beak_Width_.mm.")

# t-tests for normal data
for (group in groups_lab){
  for (quant in quant_lab){
    cat(paste("\n\nComparing",group,"groups differences in", quant, "\n"))
    homovar <- ifelse(var.test(finches[,quant] ~ finches[,group], data = finches)$p.value > 0.05, TRUE, FALSE)
    if (homovar == TRUE){
      print("Variance is homogeneous.")
    }
    else{
      print("Variance is not homogeneous.")
    }
    t_result <- t.test(finches[,quant] ~ finches[,group], data=finches, var.equal = homovar)
    print(t_result)
  }
}


# Mann-Wihtney U test for weight
for (group in groups_lab){
  cat(paste("\n\nComparing",group,"groups differences in weights\n"))
  homovar <- ifelse(var.test(finches$Weight_.g. ~ finches[,group], data = finches)$p.value > 0.05, TRUE, FALSE)
  if (homovar == TRUE){
    print("Variance is homogeneous.")
  }
  else{
    print("Variance is not homogeneous.")
  }
  mannwhitney_result <- wilcox.test(finches$Weight_.g. ~ finches[,group], data=finches)
  print(mannwhitney_result)
}

