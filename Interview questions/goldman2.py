def calculatePossibleCombinations(inputStr):
    # Edge case: empty string
    if not inputStr:
        return 0
   
    # Edge case: string starts with '0'
    if inputStr[0] == '0':
        return 0
   
    n = len(inputStr)
   
    # Initialize dp array
    # dp[i] represents the number of ways to decode inputStr[0...i-1]
    dp = [0] * (n + 1)
    dp[0] = 1  # Empty string has 1 way to decode (base case)
    dp[1] = 1  # Single digit has 1 way to decode (unless it's '0', which we checked above)
   
    for i in range(2, n + 1):
        # Check if the current digit can be decoded by itself
        if inputStr[i-1] != '0':
            dp[i] += dp[i-1]
       
        # Check if the current digit and the previous digit together form a valid letter (10-26)
        two_digit = int(inputStr[i-2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i-2]
   
    return dp[n]

# This can be used with the provided script:
# if __name__ == '__main__':
#     fptr = open(os.environ['OUTPUT_PATH'], 'w')
#     inputStr = input()
#     result = calculatePossibleCombinations(inputStr)
#     fptr.write(str(result) + '\n')
#     fptr.close()
