class Employee:
    def __init__(self, emp_id, name, age):
        self.emp_id = emp_id
        self.name = name
        self.age = age

    def to_dict(self):
        return {
            'emp_id': self.emp_id,
            'name': self.name,
            'age': self.age,
        }

    @staticmethod
    def from_dict(data):
        try:
            return Employee(emp_id=data['emp_id'], name=data['name'], age=data['age'])
        except KeyError as e:
            raise ValueError(f"Missing required key: {e.args[0]} in data: {data}")