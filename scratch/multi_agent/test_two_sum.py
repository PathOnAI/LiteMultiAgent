import unittest

class TestTwoSum(unittest.TestCase):
    def test_example(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])
    
    def test_another_case(self):
        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2])
    
    def test_negatives(self):
        self.assertEqual(two_sum([-1, -2, -3, -4, -5], -8), [2, 4])
    
    def test_large_numbers(self):
        self.assertEqual(two_sum([2**30, 2**30 + 1], 2 * 2**30 + 1), [0, 1])

if __name__ == '__main__':
    unittest.main()

def two_sum(nums, target):
    complement_map = {}
    for index, number in enumerate(nums):
        complement = target - number
        if complement in complement_map:
            return [complement_map[complement], index]
        complement_map[number] = index
    raise ValueError("No two sum solution")