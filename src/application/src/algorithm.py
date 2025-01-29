'''Implementation of MCDM algorithms

The file contains the implementation of MCMD algorithms. The file should be
used as python module.
'''

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
    '''AHP algorithm

    Args:
        None
    '''
    def __init__(self):
        pass

    def _normalize_matrix(self, matrix):
        ''' Normalize matrix

        Takes a matrix and does following steps:
        1. Create array with the sums of columns of the given matrix
        2. Divide the items in matrix with their respective sum

        Args:
            matrix: two dimension matrix of the comparisions

        Return:
            normalized_matrix: the normalized two dimensional matrix
        '''
        # normalize vector by summing the columns together
        sums = np.sum(matrix, axis=0)
        normalized_matrix = matrix / sums
        return normalized_matrix
    
    def _calculate_priority_vector(self, normalized_matrix):
        ''' Calculate priority vector (eigenvector)
        
        Args:
            normalized_matrix: A normalized matrix

        Return:
            array: priority vector
        '''
        return np.mean(normalized_matrix, axis=1)
    
    def _check_consistency(self, matrix, priority_vector):
        '''Check consistency
        
        Args:
            matrix: 2 dimensional comparision matrix

        Return:
            float: consistency check result
        '''
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

    def _construct_decision_matrix(self, room_comparisons):
        '''Construct the decision matrix from room comparisons.'''
        criteria = list(room_comparisons.keys())
        alternatives = room_comparisons[criteria[0]].shape[0]
        decision_matrix = np.zeros((alternatives, len(criteria)))

        for j, criterion in enumerate(criteria):
            for i in range(alternatives):
                decision_matrix[i, j] = room_comparisons[criterion][i, i]

        return decision_matrix

    def _normalize_decision_matrix(self, decision_matrix):
        '''Normalize the decision matrix using vector normalization.'''
        norm_matrix = np.zeros_like(decision_matrix)
        for j in range(decision_matrix.shape[1]):
            column = decision_matrix[:, j]
            norm = np.linalg.norm(column)
            norm_matrix[:, j] = column / norm
        return norm_matrix

    def _calculate_ideal_solutions(self, weighted_matrix):
        '''Determine the ideal and negative-ideal solutions.'''
        ideal_solution = np.max(weighted_matrix, axis=0)
        negative_ideal_solution = np.min(weighted_matrix, axis=0)
        return ideal_solution, negative_ideal_solution

    def _calculate_separation_measures(self, weighted_matrix, ideal_solution, negative_ideal_solution):
        '''Calculate the separation measures from the ideal and negative-ideal solutions.'''
        separation_ideal = np.sqrt(np.sum((weighted_matrix - ideal_solution) ** 2, axis=1))
        separation_negative_ideal = np.sqrt(np.sum((weighted_matrix - negative_ideal_solution) ** 2, axis=1))
        return separation_ideal, separation_negative_ideal

    def _calculate_relative_closeness(self, separation_ideal, separation_negative_ideal):
        '''Calculate the relative closeness to the ideal solution.'''
        return separation_negative_ideal / (separation_ideal + separation_negative_ideal)

    def ahp_topsis(self, criteria_matrix, room_comparisons):
        '''Perform the combined AHP-TOPSIS analysis.'''
        # Step 1: AHP to determine criteria weights
        normalized_criteria_matrix = self._normalize_matrix(criteria_matrix)
        criteria_weights = self._calculate_priority_vector(normalized_criteria_matrix)

        # Check consistency of criteria matrix
        cr = self._check_consistency(criteria_matrix, criteria_weights)
        if cr > 0.1:
            raise ValueError(f"Consistency ratio too high for criteria: {cr}")

        # Step 2: Construct the decision matrix
        decision_matrix = self._construct_decision_matrix(room_comparisons)

        # Step 3: Normalize the decision matrix
        normalized_decision_matrix = self._normalize_decision_matrix(decision_matrix)

        # Step 4: Apply criteria weights to the normalized decision matrix
        weighted_matrix = normalized_decision_matrix * criteria_weights

        # Step 5: Determine ideal and negative-ideal solutions
        ideal_solution, negative_ideal_solution = self._calculate_ideal_solutions(weighted_matrix)

        # Step 6: Calculate separation measures
        separation_ideal, separation_negative_ideal = self._calculate_separation_measures(weighted_matrix, ideal_solution, negative_ideal_solution)

        # Step 7: Calculate relative closeness to the ideal solution
        relative_closeness = self._calculate_relative_closeness(separation_ideal, separation_negative_ideal)

        return relative_closeness
    
#    def ahp(self, need_facility, criteria_rates, room_comparisions):
#        '''ahp algorithm
#
#        Args:
#            need_facility: boolean if facility is needed
#            criteria_rates: criteria comparision matrix
#            room_comparisions: room comparision matrix
#
#        Return:
#            final_weigths: final calculated weights
#            preferred_option: preferred option
#        '''
#
#        normalized_matrix = self._normalize_matrix(criteria_rates)
#        priority_vector = self._calculate_priority_vector(normalized_matrix)
#    
#        # check consistency
#        cr = self._check_consistency(criteria_rates, priority_vector)
#        if cr > 0.1:
#            raise ValueError(f"Consistency ratio too high for criteria: {cr}")
#
# # Room comparisons
        # alternative_weights = {}
        # for criterion, alt_matrix in room_comparisions.items():
        #     normalized_alt_matrix = self._normalize_matrix(alt_matrix)
        #     alt_weights = self._calculate_priority_vector(normalized_alt_matrix)
    
        #     cr = self._check_consistency(alt_matrix, alt_weights)
        #     if cr > 0.1:
        #         raise ValueError(f"Consistency ratio too high for {criterion}: {cr}")
    
        #     alternative_weights[criterion] = alt_weights
    
        # # final calculations
        # final_weights = np.zeros(len(room_comparisions[list(room_comparisions.keys())[0]]))
        # for i, criterion in enumerate(alternative_weights):
        #     final_weights += priority_vector[i] * np.array(alternative_weights[criterion])
    
        # return final_weights, np.max(final_weights)

ahp = AHP()

test = ahp.ahp_topsis(criteria, room_comparisions)
print(test)
