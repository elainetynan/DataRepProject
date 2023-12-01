from flask import Flask, jsonify, request, abort
from GraduatesDAO import GraduatesDAO

app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)

#@app.route('/')
#def index():
#    return "Hello, World!"

#curl "http://127.0.0.1:5000/grads"
@app.route('/grads')
def getAll():
    #print("in getall")
    results = GraduatesDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/grads/2"
@app.route('/grads/<int:id>')
def findById(id):
    foundData = GraduatesDAO.findByID(id)

    return jsonify(foundData)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Institution\":\"hello\",\"GraduationYear\":\"someone\",\"NumGraduates\":123}" http://127.0.0.1:5000/grads
@app.route('/grads', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    data = {
        "Institution": request.json['Institution'],
        "GraduationYear": request.json['GraduationYear'],
        "FieldOfStudy": request.json['FieldOfStudy'],
        "NFQ_Level": request.json['NFQ_Level'],
        "NumGraduates": request.json['NumGraduates'],
    }
    values =(data['Institution'],data['GraduationYear'],data['FieldOfStudy'],data['NFQ_Level'],data['NumGraduates'])
    newId = GraduatesDAO.create(values)
    data['id'] = newId
    return jsonify(data)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Institution\":\"hello\",\"GraduationYear\":\"someone\",\"NumGraduates\":123}" http://127.0.0.1:5000/grads/1
@app.route('/grads/<int:id>', methods=['PUT'])
def update(id):
    foundData = GraduatesDAO.findByID(id)
    if not foundData:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'NumGraduates' in reqJson and type(reqJson['NumGraduates']) is not int:
        abort(400)
    if 'GraduationYear' in reqJson and type(reqJson['GraduationYear']) is not int:
        abort(400)

    if 'Institution' in reqJson:
        foundData['Institution'] = reqJson['Institution']
    if 'GraduationYear' in reqJson:
        foundData['GraduationYear'] = reqJson['GraduationYear']
    if 'FieldOfStudy' in reqJson:
        foundData['FieldOfStudy'] = reqJson['FieldOfStudy']
    if 'NFQ_Level' in reqJson:
        foundData['NFQ_Level'] = reqJson['NFQ_Level']
    if 'NumGraduates' in reqJson:
        foundData['NumGraduates'] = reqJson['NumGraduates']
    values = (foundData['Institution'],foundData['GraduationYear'],foundData['FieldOfStudy'],foundData['NFQ_Level'],foundData['NumGraduates'],foundData['id'])
    GraduatesDAO.update(values)
    return jsonify(foundData)
        

    

@app.route('/grads/<int:id>' , methods=['DELETE'])
def delete(id):
    GraduatesDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)