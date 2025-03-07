def minChairs(simulations):
    """
    Calculate the minimum number of chairs required for each simulation.
   
    Args:
        simulations: A list of strings, where each string contains actions 'C', 'U', 'R', or 'L'
       
    Returns:
        A list of integers representing the minimum chairs required for each simulation
    """
    results = []
   
    for simulation in simulations:
        available_chairs = 0  # Chairs not currently in use
        total_chairs = 0      # Total chairs purchased
       
        for action in simulation:
            if action == 'C' or action == 'U':
                # Employee needs a chair
                if available_chairs > 0:
                    # Use an available chair
                    available_chairs -= 1
                else:
                    # No chairs available, buy a new one
                    total_chairs += 1
            elif action == 'R' or action == 'L':
                # Employee leaves, chair becomes available
                available_chairs += 1
       
        results.append(total_chairs)
   
    return results

# The pre-written code will call minChairs and handle the input/output