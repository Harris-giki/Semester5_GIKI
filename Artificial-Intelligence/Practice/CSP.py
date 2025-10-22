regions = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'Q', 'SA'],
    'Q': ['NT', 'NSW', 'SA'],
    'NSW': ['Q', 'SA', 'V'],
    'V': ['SA', 'NSW'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'T': ['SA']
}
colors = ['red', 'green', 'blue']
assignment = {}  # Empty dictionary to store which color each region gets
def is_valid_assignment(region,color):
    for neighbour in regions[region]:
        if neighbour in assignment and assignment[neighbour] == color:
            return False
        return True
    
# pick a region to color next

def select_unassigned_region():
    for region in regions:
        if region not in assignment:
            return region
    return None
# backtracking search algorithm
def backtrack():
    if len(assignment) == len(regions):
        return assignment  # All regions are assigned a color
    region = select_unassigned_region()
    for color in colors:
        if is_valid_assignment(region, color):
            assignment[region] = color  # Assign color
            result = backtrack()
            if result:
                return result
            del assignment[region]  # Remove assignment (backtrack)
    return None  # Trigger backtracking