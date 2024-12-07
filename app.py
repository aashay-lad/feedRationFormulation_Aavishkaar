from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.optimize import linprog

app = Flask(__name__)

# Updated feed ingredients for cattle
feed_ingredients = [
    {"name": "Corn", "protein": 7.5, "fiber": 10.0, "cost": 70},
    {"name": "Soybean Meal", "protein": 48.0, "fiber": 6.0, "cost": 180},
    {"name": "Wheat Bran", "protein": 18.0, "fiber": 44.0, "cost": 45},
]

# Updated nutrient requirements
nutrient_requirements = {
    "cattle": {"protein": 700, "fiber": 3000},
    "poultry": {"protein": 170, "fiber": 30},
    "goat": {"protein": 350, "fiber": 400},
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/animal-requirements', methods=['GET', 'POST'])
def animal_requirements():
    if request.method == 'POST':
        animal_type = request.form.get('animal-type')
        weight = float(request.form.get('weight', 0))
        age = float(request.form.get('age', 0))
        activity = request.form.get('activity')

        # Adjust nutrient requirements based on weight, age, and activity
        base_requirements = nutrient_requirements.get(animal_type, {})
        protein = base_requirements.get("protein", 0) * (weight / 500) * (1 + activity_factor(activity))
        fiber = base_requirements.get("fiber", 0) * (weight / 500) * (1 + activity_factor(activity))

        return jsonify({"protein": round(protein, 2), "fiber": round(fiber, 2)})

    return render_template('animal_requirements.html')

def activity_factor(activity_level):
    """Returns a multiplier based on activity level."""
    factors = {"low": 0.1, "medium": 0.2, "high": 0.3}
    return factors.get(activity_level, 0)

@app.route('/feed-options', methods=['GET'])
def feed_options():
    return render_template('feed_options.html', feed_ingredients=feed_ingredients)

@app.route('/cost', methods=['POST'])
def cost_estimation():
    # Get the updated prices and nutrient requirements from the request
    data = request.get_json()

    # Extract nutrient requirements and updated prices from the request
    protein_requirement = float(data['protein'])
    fiber_requirement = float(data['fiber'])
    updated_prices = data['prices']

    # Define the feed ingredients with updated prices
    feed_ingredients = [
        {"name": "Corn", "protein": 7.5, "fiber": 10.0, "cost": float(updated_prices.get("Corn", 70.0))},
        {"name": "Soybean Meal", "protein": 48.0, "fiber": 6.0, "cost": float(updated_prices.get("Soybean Meal", 180.0))},
        {"name": "Wheat Bran", "protein": 18.0, "fiber": 44.0, "cost": float(updated_prices.get("Wheat Bran", 45.0))},
    ]

    # Prepare the cost vector, protein values, and fiber values for the linear programming model
    costs = [ingredient["cost"] for ingredient in feed_ingredients]
    protein_values = [ingredient["protein"] for ingredient in feed_ingredients]
    fiber_values = [ingredient["fiber"] for ingredient in feed_ingredients]

    # Constraints: Protein and fiber must meet or exceed requirements
    A = [
        [-val for val in protein_values],  # Protein constraint (negative for 'greater than or equal to' condition)
        [-val for val in fiber_values],    # Fiber constraint (negative for 'greater than or equal to' condition)
    ]
    b = [-protein_requirement, -fiber_requirement]  # Right-hand side of the constraints

    # Adding minimum constraints for Corn and Soybean Meal
    A.extend([
        [1, 0, 0],  # Corn minimum constraint
        [0, 1, 0],  # Soybean Meal minimum constraint
    ])
    b.extend([10, 5])  # Minimum quantities in kg

    # Bounds: Quantities of each ingredient must be non-negative (no less than 0)
    bounds = [(0, None) for _ in feed_ingredients]

    # Solve the linear programming problem
    result = linprog(c=costs, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    # Debugging output to understand optimization
    print("Optimization result:", result)
    print("Protein requirements:", protein_requirement)
    print("Fiber requirements:", fiber_requirement)
    print("Feed costs:", costs)
    print("Protein values:", protein_values)
    print("Fiber values:", fiber_values)

    # Check if the optimization was successful
    if result.success:
        # Create a dictionary of ingredient quantities
        quantities = {feed_ingredients[i]["name"]: round(qty, 2) for i, qty in enumerate(result.x)}
        total_cost = round(result.fun, 2)  # Total cost of the feed ration
        return jsonify({"success": True, "quantities": quantities, "total_cost": total_cost})

    return jsonify({"success": False, "message": "Unable to calculate cost. Try adjusting requirements."})

if __name__ == '__main__':
    app.run(debug=True)
