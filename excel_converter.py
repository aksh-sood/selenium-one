import pandas as pd

def convert_to_excel(name,date,director,link):
    df=pd.DataFrame(data=name,columns=["Movie names"])
    df["Director"]=director
    df["Release Date"]=date
    df["Link"]=link
    df.to_csv("moviesdata.csv")
