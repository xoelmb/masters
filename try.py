

def reverser(text):
    n=0
    while n<=len(text):
        print (text[len(text)-n:len(text)-n-n:-1])
        n+=1
        
reverser("GATAGATAGA")
