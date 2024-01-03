from flask import Flask, jsonify, request
from flask_cors import CORS
from client import start_client
from models import Employee

app = Flask(__name__)
cors = CORS(app)

client = start_client()
db = client['employee_details']
collection = db['collection']


@app.route("/get_data")
def get_data():
    data = list(collection.find({}))
    json_data = [employee.to_dict() for employee in map(Employee.from_dict, data)]
    return jsonify(json_data)

@app.route('/post_data', methods=['POST'])
def insert_data():
    data = request.json
    employee_id = data["emp_id"]

    existing_document = collection.find_one({'emp_id': employee_id})

    if existing_document:
        response = {'error': 'Document already exists'}
        return jsonify(response), 409
    else:
        employee = Employee.from_dict(data)
        inserted_data = collection.insert_one(employee.to_dict())
        inserted_id = str(inserted_data.inserted_id)
        response = {'id': inserted_id , "employee_data" : data}
        return jsonify(response)

@app.route("/delete_data/<emp_id>", methods=["DELETE"])
def delete_record(emp_id):
    
    result = collection.delete_one({"emp_id": int(emp_id)})
    
    if result.deleted_count == 1:
        return {"message": "Record deleted successfully"}
    else:
        print(f"Record not found or already deleted for emp_id: {emp_id}")
        return {"message": "Record not found or already deleted"}, 404




@app.route("/update_data/<emp_id>", methods=["PUT"])
def update_record(emp_id):
    data = request.get_json()
    result = collection.update_one({"emp_id": int(emp_id)}, {"$set": data})
    if result.modified_count == 1:
        return {"message": "Record updated successfully"}
    else:
        return {"message": "Record not found or update failed"}, 404


if __name__ == '__main__':
    app.run()
