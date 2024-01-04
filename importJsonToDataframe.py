from ast import Pass
import requests
import json
#from GraduatesDAO import GraduatesDAO
import pandas as pd


urlBegining = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
urlEnd = "/JSON-stat/2.0/en"

def getAllAsFile(dataset):
    with open("cso.json", "wt") as fp:
        print(json.dumps(getAll(dataset)), file=fp)

def getAll(dataset):   
    urlBegining = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
    urlEnd = "/JSON-stat/2.0/en"
    url = urlBegining + dataset + urlEnd
    response = requests.get(url)
    return response.json()

def getFormattedAsFile(dataset):
    with open("cso-formatted.json", "wt") as fp:
        result, df = getFormatted(dataset)
        print(json.dumps(result), file=fp)
  
# Create the formatted JSON file and the dtaframe.
def getFormatted(dataset):
    data = getAll(dataset)
    ids = data["id"]
    values = data["value"]
    dimensions = data["dimension"]
    sizes = data["size"]
    valuecount = 0
    result = {}

    col1 = dimensions["TLIST(A1)"]["label"]
    col2 = dimensions["C03428V04135"]["label"]
    col3 = dimensions["C03427V04134"]["label"]
    col4 = dimensions["C03685V04428"]["label"]
    col5 = dimensions["STATISTIC"]["category"]["label"]["HEO14C01"]
    df = pd.DataFrame(columns=[col1, col2, col3, col4, col5])
    
    for dim0 in range(0, sizes[0]): # dimension 0 - ["Statistic"]["category"]["label"][index]
        currentId = ids[0] # currentId = STATISTIC
        index = dimensions[currentId]["category"]["index"][dim0] # index = HEO14C01
        label0 = dimensions[currentId]["category"]["label"][index] # label0 = Number of Graduates
        result[label0]={}
        #print(label0)
        
        for dim1 in range(0, sizes[1]): # dimension 1
            currentId = ids[1]
            index = dimensions[currentId]["category"]["index"][dim1]
            label1 = dimensions[currentId]["category"]["label"][index]
            #print("\t",label1)
            result[label0][label1]={}
            
            for dim2 in range(0, sizes[2]): # dimension 2
                currentId = ids[2]
                index = dimensions[currentId]["category"]["index"][dim2]
                label2 = dimensions[currentId]["category"]["label"][index]
                #print("\t\t",label2)
                result[label0][label1][label2]={}

                for dim3 in range(0, sizes[3]): # dimension 3
                    currentId = ids[3]
                    index = dimensions[currentId]["category"]["index"][dim3]
                    label3 = dimensions[currentId]["category"]["label"][index]
                    #print("\t\t\t",label3)
                    result[label0][label1][label2][label3]={}
           
                    for dim4 in range(0, sizes[4]): # dimension 4
                        currentId = ids[4]
                        index = dimensions[currentId]["category"]["index"][dim4]
                        label4 = dimensions[currentId]["category"]["label"][index]
                        #print("\t\t\t",label4, " ", values[valuecount])
                        result[label0][label1][label2][label3][label4]= int(values[valuecount])
                        
                        df.loc[len(df)] = [label1, label2, label3, label4, int(values[valuecount])]

                        valuecount+=1
    return result, df

def cleanData(df):
    # Replace spaces in column names with underscores as it causes problems.
    df.columns = [c.replace(" ", "") for c in df.columns]
    # Replace FieldofStudy with FieldOfStudy to avoid confusion later.
    df.columns = [c.replace("FieldofStudy", "FieldOfStudy") for c in df.columns]

   # Remove duplicate (aggregate) rows and records that have no graduates
    df.drop(df[df['Institutions'] == "All Institutions"].index, inplace = True)
    df.drop(df[df['FieldOfStudy'] == "All fields of education"].index, inplace = True)
    df.drop(df[df['NFQLevel'] == "All NFQ Levels"].index, inplace = True)
    df.drop(df[df['NumberofGraduates'] == 0].index, inplace = True)
    
if __name__ == "__main__":
    #getFormattedAsFile("HEO14")
    #getAllAsFile("HEO14")
    result, df = getFormatted("HEO14")
    cleanData(df)
    print("The Column Headers :", list(df.columns.values))
    df.to_csv('data.csv')
    print("done!!!!")