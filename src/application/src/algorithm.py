'''Implementation of MCDM algorithms

The file contains the implementation of MCMD algorithms. The file should be
used as python module.
'''

# Useful resource https://www.researchgate.net/publication/334986010_Introduction_to_MCDM_Techniques_AHP_as_Example

import numpy as np

class AHP:
    '''AHP algorithm'''
    def __init__(self, criteria, room_comparisons):
        ''' Constructer of the class
            
        Args:
            criteria_matrix: criteria comaprision matrix
            room_comparision: dictionary of room propreties and their
                              comparisions between every room
        '''

        self.criteria_matrix = criteria
        self.room_comparisons = room_comparisons 


    def _normalize_matrix(self, matrix):
        '''Normalize the comparison matrix.
        
        Args:
            matrix: matrix to normalize

        Returns:
            Calculated new normalized matrix
        '''
        sums = np.sum(matrix, axis=0)
        return matrix / sums
    
    def _calculate_priority_vector(self, normalized_matrix):
        '''Calculate priority vector (eigenvector).

        Args:
            normalized_matrix: a matrix that is already normalized

        Returns:
            Calculates the priority vector.
        '''
        return np.mean(normalized_matrix, axis=1)
    
    def _check_consistency(self, matrix, priority_vector):
        '''Check consistency of the comparison matrix.

        Args:
            matrix: matrix to be checked
            priority_vector

        Returns:
            Result of the check
        '''
        n = matrix.shape[0]
        lambda_max = np.sum(np.dot(matrix, priority_vector) / priority_vector) / n
        ci = (lambda_max - n) / (n - 1)
        random_index = {
            1: 0.0, 2: 0.0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24,
            7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
        }
        ri = random_index.get(n, 1.49)
        cr = ci / ri if ri else 0
        return cr

    def ahp(self):
        '''Perform AHP analysis.

        Retruns:
            A tuple with the final weights and the index of the highest score
        '''
        # Normalize and compute criteria weights
        normalized_criteria_matrix = self._normalize_matrix(self.criteria_matrix)
        criteria_weights = self._calculate_priority_vector(normalized_criteria_matrix)

        # Check consistency
        cr = self._check_consistency(self.criteria_matrix, criteria_weights)
        if cr > 0.1:
            raise ValueError(f"Consistency ratio too high for criteria: {cr}")
        
        # Calculate alternative weights per criterion
        alternative_weights = {}
        for criterion, alt_matrix in self.room_comparisons.items():
            normalized_alt_matrix = self._normalize_matrix(alt_matrix)
            alt_weights = self._calculate_priority_vector(normalized_alt_matrix)
            
            cr = self._check_consistency(alt_matrix, alt_weights)
            if cr > 0.1:
                raise ValueError(f"Consistency ratio too high for {criterion}: {cr}")
            
            alternative_weights[criterion] = alt_weights
        
        # Compute final scores
        final_weights = np.zeros(len(list(self.room_comparisons.values())[0]))
        for i, criterion in enumerate(alternative_weights):
            final_weights += criteria_weights[i] * np.array(alternative_weights[criterion])
        
        return final_weights, np.argmax(final_weights)

# Example data
criteria = np.array([
    [1,   3,   5,   9],
    [1/3, 1,   3,   9],
    [1/5, 1/3, 1,   5],
    [1/9, 1/9, 1/5, 1],
])

room_comparisons = {
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

ahp = AHP(criteria, room_comparisons)
final_weights, best_option = ahp.ahp()
print("Final Weights:", final_weights)
print("Best Option:", best_option)
