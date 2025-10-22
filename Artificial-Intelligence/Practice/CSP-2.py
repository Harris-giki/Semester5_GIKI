# Variables and domains
variables = ['x1', 'x2']
domains = {
    'x1': [1, 2],
    'x2': [2, 3]
}

# Constraint function
def constraint(assignment):
    # Check if all assigned variables satisfy x1 != x2
    if 'x1' in assignment and 'x2' in assignment:
        return assignment['x1'] != assignment['x2']
    return True  # No conflict if not all variables assigned yet

valid_assignments = []

# Recursive backtracking function
def backtrack(assignment={}):
    # If all variables assigned
    if len(assignment) == len(variables):
        if constraint(assignment):
            valid_assignments.append(assignment.copy())  # Store valid ones
        return

    # Select next unassigned variable
    for var in variables:
        if var not in assignment:
            for value in domains[var]:
                assignment[var] = value
                if constraint(assignment):  # Check constraints
                    backtrack(assignment)  # Recur
                del assignment[var]  # Backtrack
            return
