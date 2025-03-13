def calculate_score(text, prefix_string, suffix_string):
    """
    Returns the longest substring of text that begins with an ending substring of prefix_string
    and ends with a beginning substring of suffix_string.
   
    Args:
        text (str): The text to search in
        prefix_string (str): The string whose ending should match the beginning of the result
        suffix_string (str): The string whose beginning should match the ending of the result
       
    Returns:
        str: The longest matching substring, or empty string if no match found
    """
    best_substring = ""
   
    # For each possible starting position in text
    for start in range(len(text)):
        # Find the longest ending substring of prefix_string that matches
        # the text starting at this position
        max_prefix_match = 0
        for i in range(1, min(len(prefix_string) + 1, len(text) - start + 1)):
            if text[start:start+i] == prefix_string[-i:]:
                max_prefix_match = i
       
        # For each possible ending position after our start
        for end in range(start + max_prefix_match, len(text) + 1):
            # Find the longest beginning substring of suffix_string that matches
            # the text ending at this position
            max_suffix_match = 0
            for i in range(1, min(len(suffix_string) + 1, end - start + 1)):
                if text[end-i:end] == suffix_string[:i]:
                    max_suffix_match = i
           
            # If we have both a valid prefix and suffix match
            if max_prefix_match > 0 and max_suffix_match > 0:
                current = text[start:end]
                if len(current) > len(best_substring):
                    best_substring = current
   
    return best_substring