def two_sum(nums, target):
    hash_map = {}
    for idx, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], idx]
        hash_map[num] = idx
