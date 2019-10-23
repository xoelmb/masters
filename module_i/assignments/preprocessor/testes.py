def add_one_par(pars):
    pars["hey"] = 1
    return True

parameters= {}
add_one_par(parameters)
print(parameters["hey"])