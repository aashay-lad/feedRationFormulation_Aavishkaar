from pulp import LpProblem, LpMinimize, LpVariable

def calculate_daily_nutrients(animal_type, age, weight, activity_level):
    # Example logic to calculate protein and fiber needs
    if animal_type == 'cattle':
        protein = weight * 1.5
        fiber = weight * 0.16
    elif animal_type == 'poultry':
        protein = weight * 0.9
        fiber = weight * 0.1
    else:
        protein = weight * 1.2
        fiber = weight * 0.14
    
    return {'protein': protein, 'fiber': fiber}

def calculate_minimum_cost(nutrients, feed_ingredients):
    prob = LpProblem("Minimize_Cost", LpMinimize)
    variables = {}
    
    # Create variables for each feed ingredient
    for feed in feed_ingredients:
        variables[feed] = LpVariable(feed, lowBound=0)
    
    # Add objective function based on feed ingredient costs
    prob += sum(feed_ingredients[feed]['cost'] * variables[feed] for feed in feed_ingredients)
    
    # Add nutrient constraints (protein and fiber)
    prob += sum(feed_ingredients[feed]['protein'] * variables[feed] for feed in feed_ingredients) >= nutrients['protein']
    prob += sum(feed_ingredients[feed]['fiber'] * variables[feed] for feed in feed_ingredients) >= nutrients['fiber']
    
    prob.solve()
    return prob.objective.value()


