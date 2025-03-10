import os

def maximumOccuringCharacter(text):
    """
    Returns the most frequent character in the string.
    If multiple characters have the same frequency, returns the one that appears first.
   
    Args:
        text (str): Input string containing characters a-z, A-Z, and 0-9
       
    Returns:
        str: The most frequent character
    """
    if not text:
        return None
   
    # Dictionary to track character counts
    char_count = {}
   
    # List to track character order (first appearance)
    char_order = []
   
    # Count occurrences while preserving first appearance order
    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
            char_order.append(char)
   
    # Find the most frequent character
    max_char = char_order[0]
    max_count = char_count[max_char]
   
    for char in char_order[1:]:
        if char_count[char] > max_count:
            max_char = char
            max_count = char_count[char]
   
    return max_char

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    text = input()
    result = maximumOccuringCharacter(text)
    fptr.write(str(result) + '\n')
    fptr.close()
