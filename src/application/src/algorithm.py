# Useful resource https://www.researchgate.net/publication/334986010_Introduction_to_MCDM_Techniques_AHP_as_Example

import numpy as np

# Example data
criteria = np.array([
            [1,   3,   5,   9],
            [1/3, 1,   3,   9],
            [1/5, 1/3, 1,   5],
            [1/9, 1/9, 1/5, 1],
           ])

room_comparisions = {
    "Temperature": np.array([
        [1, 4, 4],
        [1/4, 1, 1],
        [1/4, 1, 1]
    ]),
    "CO2 Levels": np.array([
        [1, 6, 8],
        [1/6, 1, 3],
        [1/8, 1/3, 1]
    ]),
    "Air Quality": np.array([
        [1, 4, 4],
        [1/4, 1, 1],
        [1/4, 1, 1]
    ]),
    "Facilities": np.array([
        [1, 1/7, 1/7],
        [7, 1, 1],
        [7, 1, 1]
    ])
}

class AHP:
    def __init__(self):
        pass

    def normalize_matrix(self, matrix):
        # normalize vector by summing the columns together
        sums = np.sum(matrix, axis=0)
        normalized_matrix = matrix / sums
        return normalized_matrix
    
    def calculate_priority_vector(self, normalized_matrix):
        return np.mean(normalized_matrix, axis=1)
    
    def check_consistency(self, matrix, priority_vector):
        n = matrix.shape[0]
        lambda_max = np.sum(np.dot(matrix, priority_vector) / priority_vector) / n
        ci = (lambda_max - n) / (n - 1)
        # RCI table publicly available
        # https://www.researchgate.net/publication/247759937_The_Analytic_Hierarchy_Process_-_What_It_Is_and_How_It_Is_Used
        random_index = {
            1: 0.0, 2: 0.0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24,
            7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
        }
        ri = random_index.get(n, 1.49)  # Default to 1.49 for n > 10sum
        cr = ci / ri if ri else 0
        return cr
    
    def ahp(self, need_facility, criteria_rates, room_comparisions):
        normalized_matrix = self.normalize_matrix(criteria_rates)
        priority_vector = self.calculate_priority_vector(normalized_matrix)
    
        # check consistency
        cr = self.check_consistency(criteria_rates, priority_vector)
        if cr > 0.1:
            raise ValueError(f"Consistency ratio too high for criteria: {cr}")
    
    
        # Room comparisons
        alternative_weights = {}
        for criterion, alt_matrix in room_comparisions.items():
            normalized_alt_matrix = self.normalize_matrix(alt_matrix)
            alt_weights = self.calculate_priority_vector(normalized_alt_matrix)
    
            cr = self.check_consistency(alt_matrix, alt_weights)
            if cr > 0.1:
                raise ValueError(f"Consistency ratio too high for {criterion}: {cr}")
    
            alternative_weights[criterion] = alt_weights
    
        # final calculations
        final_weights = np.zeros(len(room_comparisions[list(room_comparisions.keys())[0]]))
        for i, criterion in enumerate(alternative_weights):
            final_weights += priority_vector[i] * np.array(alternative_weights[criterion])
    
        return final_weights, np.max(final_weights)

ahp = AHP()

final_weights, optimal = ahp.ahp(True, criteria, room_comparisions)
print(final_weights)
print(optimal)
