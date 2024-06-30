def two_sum(nums, target):
    complement_map = {}
    for index, number in enumerate(nums):
        complement = target - number
        if complement in complement_map:
            return [complement_map[complement], index]
        complement_map[number] = index
    raise ValueError("No two sum solution")

# Example usage:
nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target))  # Output: [0, 1]