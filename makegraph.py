import matplotlib.pyplot as plt
from PIL import Image
def make_graphs(x,y,labelx,labely,pc_user:str):
    try:
        plt.figure()
        plt.plot(x,y)
        plt.xlabel(labelx)
        plt.ylabel(labely)
        #plot the graph and add the labels onto it
        plt.title(str(labelx)+ " vs " +str(labely))#attach title to the top of the graph
        
        plt.savefig("C:/Users/"+pc_user+"/Documents/results/"+str(labelx)+" vs "+str(labely)+".png", bbox_inches='tight')#save the figure under this name
        print("File successfully saved as: "+str(labelx)+" vs "+str(labely)+".png")    
    except FileNotFoundError:
        print("Make a results folder in documents.")
def access_graphs(pc_user:str):
    try:
        guess=input("What is the file name: ")
        im=Image.open(r"C:/Users/"+pc_user+"/Documents/results/"+guess)
        im.show()   
    except FileNotFoundError:
        print("File does not exist")


    
    
    

        
            
        
         
            
             
              


