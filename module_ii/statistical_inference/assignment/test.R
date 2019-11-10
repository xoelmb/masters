setwd("/home/xoel/github/masters/module_ii/statistical_inference/assignment")

# The dataset had to be fixed, since there was blank spaces instead of tabulations at different points across the file.
finches <- read.table("./finches_dataset.txt", header=TRUE, sep="\t")
# Replace the unknown values for Sex with NA.
finches$Sex[finches$Sex == "unknown"] <- NA
finches$Sex <- droplevels(finches$Sex)


# Check which variables are in the dataset
colnames(finches)


# Feature amplification
#Beak_volume <- ((finches$Beak_Width_.mm./2)**2*pi*finches$Beak_Depth_.mm.)/3
Age <- finches$Last_Year - finches$First_adult_year + 1
#Survival = as.integer(as.logical(finches$Last_Year > 1977))
Survival = finches$Last_Year > 1977
finches <-cbind(finches, Age, Survival)


# Statistics of those variables
for (i in c(3:ncol(finches))){
  print(colnames(finches)[i])
  print(summary(finches[,i]))
  if (colnames(finches)[i] != "Sex" & colnames(finches)[i] != "Survival"){
    print(paste("Var:",var(finches[,i])))
    print(paste("SD:",sd(finches[,i])))
  }
}
summary(finches[,c(3:ncol(finches))])
var(finches[,c(4:(ncol(finches)-1))])
sd(finches[,11])


#Plot
barplot(table(finches$Sex), ylim=c(0,50), ylab="Number of specimens", col=c("purple", "gold"))
quant_col <- c(6:12)
for (i in quant_col){
  print(colnames(finches)[i])
  hist(finches[,i], main=colnames(finches[i]), prob=TRUE)
  lines(density(finches[,i]))
  
}

#Correlations
cors <- cor(finches[quant_col])
cors_noNA <- cor(finches[quant_col], use="complete.obs")
summary(finches)

