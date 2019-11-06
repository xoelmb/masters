setwd("/home/xoel/github/masters/module_ii/statistical_inference/assignment")

# The dataset had to be fixed, since there was blank spaces instead of tabulations at different points across the file.
finches <- read.table("./finches_dataset.txt", header=TRUE, sep="\t")

# Feature amplification
Beak_volume <- ((finches$Beak_Width_.mm./2)**2*pi*finches$Beak_Depth_.mm.)/3
Age <- finches$Last_Year - finches$First_adult_year
Survival = as.integer(as.logical(finches$Last_Year > 1977))
finches <-cbind(finches, Beak_volume, Age, Survival)
#Plot
barplot(table(finches$Sex))
quant_col <- c(6:13)
for (i in quant_col){
  print(colnames(finches[i]))
  hist(finches[,i], main=colnames(finches[i]))
}

#Correlations