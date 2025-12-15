# 1. imports
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# 2. app + db config
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calculations.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 3. model
class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(20), nullable=False)
    operand_a = db.Column(db.Float, nullable=False)
    operand_b = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)

# 4. calculate helper
def calculate(operation, a, b):
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    raise ValueError("Invalid operation")

# 5. ROUTES (ALL ROUTES GO HERE)

# ADD
@app.route("/calculations", methods=["POST"])
def add_calculation():
    data = request.json
    result = calculate(data["operation"], data["operandA"], data["operandB"])

    calc = Calculation(
        operation=data["operation"],
        operand_a=data["operandA"],
        operand_b=data["operandB"],
        result=result
    )

    db.session.add(calc)
    db.session.commit()

    return jsonify({
        "id": calc.id,
        "operation": calc.operation,
        "operandA": calc.operand_a,
        "operandB": calc.operand_b,
        "result": calc.result
    }), 201

# BROWSE
@app.route("/calculations", methods=["GET"])
def get_calculations():
    calculations = Calculation.query.all()
    return jsonify([
        {
            "id": c.id,
            "operation": c.operation,
            "operandA": c.operand_a,
            "operandB": c.operand_b,
            "result": c.result
        }
        for c in calculations
    ])

# ✅ READ (THIS IS WHAT YOU ARE ADDING)
@app.route("/calculations/<int:calc_id>", methods=["GET"])
def get_calculation(calc_id):
    calc = Calculation.query.get(calc_id)
    if not calc:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": calc.id,
        "operation": calc.operation,
        "operandA": calc.operand_a,
        "operandB": calc.operand_b,
        "result": calc.result
    })
# EDIT
@app.route("/calculations/<int:calc_id>", methods=["PUT"])
def update_calculation(calc_id):
    data = request.json

    calc = Calculation.query.get(calc_id)
    if not calc:
        return jsonify({"error": "Calculation not found"}), 404

    try:
        result = calculate(
            data["operation"],
            float(data["operandA"]),
            float(data["operandB"])
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    calc.operation = data["operation"]
    calc.operand_a = data["operandA"]
    calc.operand_b = data["operandB"]
    calc.result = result

    db.session.commit()

    return jsonify({
        "id": calc.id,
        "operation": calc.operation,
        "operandA": calc.operand_a,
        "operandB": calc.operand_b,
        "result": calc.result
    })
#DElETE
@app.route("/calculations/<int:id>", methods=["DELETE"])
def delete_calculation(id):
    calc = Calculation.query.get_or_404(id)

    db.session.delete(calc)
    db.session.commit()

    return "", 204

# HOME
@app.route("/")
def home():
    return "Backend is running"

# 6. app start (ALWAYS LAST)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=3001, debug=True)
