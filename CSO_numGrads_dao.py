from ast import Pass
import requests
import json


urlBegining = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
urlEnd = "/JSON-stat/2.0/en"

def getAllAsFile(dataset):
    with open("cso.json", "wt") as fp:
        print(json.dumps(getAll(dataset)), file=fp)

def getAll(dataset):   
    url = urlBegining + dataset + urlEnd
    response = requests.get(url)
    return response.json()

def getFormattedAsFile(dataset):
    with open("cso-formatted.json", "wt") as fp:
        print(json.dumps(getFormatted(dataset)), file=fp)
  

def getFormatted(dataset):
    data = getAll(dataset)
    ids = data["id"]
    values = data["value"]
    dimensions = data["dimension"]
    sizes = data["size"]
    valuecount = 0
    result = {}
    
    for dim0 in range(0, sizes[0]): # dimension 0 - ["Statistic"]["category"]["label"][index]
        currentId = ids[0]
        index = dimensions[currentId]["category"]["index"][dim0]
        label0 = dimensions[currentId]["category"]["label"][index]
        result[label0]={}
        #print(label0)
        
        for dim1 in range(0, sizes[1]): # dimension 1 - ["TList(A1)"]["category"]["label"][index]
            currentId = ids[1]
            index = dimensions[currentId]["category"]["index"][dim1]
            label1 = dimensions[currentId]["category"]["label"][index]
            #print("\t",label1)
            result[label0][label1]={}
            
            for dim2 in range(0, sizes[2]): # dimension 2 - ["C02199V02655"]["category"]["label"][index]
                currentId = ids[2]
                index = dimensions[currentId]["category"]["index"][dim2]
                label2 = dimensions[currentId]["category"]["label"][index]
                #print("\t\t",label2)
                result[label0][label1][label2]={}
           
                for dim3 in range(0, sizes[3]): # dimension 3 - ["C03685V04428"]["category"]["label"][index]
                    currentId = ids[3]
                    index = dimensions[currentId]["category"]["index"][dim3]
                    label3 = dimensions[currentId]["category"]["label"][index]
                    #print("\t\t\t",label3, " ", values[valuecount])
                    result[label0][label1][label2][label3]= values[valuecount]
                    valuecount+=1
                    
    #print(result)    
    return result
    
if __name__ == "__main__":
    # HEO14
    # EDA99
  #  getAllAsFile("HEO14")
    getFormattedAsFile("HEO14")

  #  data = getAll("HEO14")
    data = getFormatted("HEO14")
 #   for key, value in data.items():
 #       print("Key-> "+key + " ~VAL~ ")
 #       for x in value:
 #           print("Next: "+x+"~~")
 #           for y in x:
 #               print(y)
 #               input()

    #print("~~~~~~~~~")

    print("~~~~~~~~~")

    print(data)
    print("~~~~~~~~~")
    #print(list(data.values())[0])
    #print("~~~~~~~~~")

  #  for entry in data:
     #   valuationReports = entry["Number of Graduates"]
     #   statReport = entry["2010"]
     #   print(entry)
     #   input()
     #   for valuationReport in valuationReports:
            #print(valuationReport)
      #      if valuationReport["FloorUse"] == "HAIR SALON":
          #      print (valuationReport["Area"],"+", totalArea,"=", end="")
                #totalArea += valuationReport["Area"]
                #print(totalArea)

    #print (totalArea)