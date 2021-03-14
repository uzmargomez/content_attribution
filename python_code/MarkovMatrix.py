import numpy as np
import warnings


class MarkovMatrix:
    """
    Markov Matrix

    ...

    Parameters
    ----------
    matrix_arr : list of lists
        Each list representing a single row. This will create a matrix


    Attributes
    ----------
    matrix_obj : numpy matrix
        Markov matrix
    epsilon : float
        Variable that defines an upper and a lower limit
    size : int
        Size of the matrix
    status : bool
        Checks if the matrix is right stochastic, i.e. if it is a real
        square matrix with each row summing to 1, and all entries are
        nonnegative.
    absorption_states : list
        Absorption states given by the index position in the matrix
    transient_states : list
        Transition states given by the index position in the matrix
    num_absorption_states : int
        Number of absorption states
    standard_matrix : numpy matrix
        The same matrix_obj, expressed in the canonical form (see more
        information below)
    q,r,n,m : numpy matrix
        Matrices obtained from the standard matrix (see more information
        below)


    Methods
    -------
    get_probability(absorbing_state, transient_state)
        Returns the probability that an absorbing chain will be
        absorbed in the absorbing state s_j if it starts in the transient
        state s_i
    """

    def __init__(self, matrix_arr):
        self.matrix_obj = matrix_arr
        self.epsilon = 0.02
        self.size = self.matrix_obj.shape[0]
        self.num_absorption_states = 2

        states = [i for i in range(self.size)]
        self.transient_states = states[: self.size - 2]
        self.absorption_states = states[self.size - 2 :]
        self.q = self.__get_q()
        self.r = self.__get_r()
        self.n = self.__get_n()
        self.m = self.__get_m()

    def __get_q(self):
        maximum = self.size - self.num_absorption_states
        Q = self.matrix_obj[0:maximum, 0:maximum]

        return Q

    def __get_r(self):
        maximum = self.size - self.num_absorption_states
        R = self.matrix_obj[0:maximum, maximum:]

        return R

    def __get_n(self):
        """
        Fundamental matrix

        N = (I - Q)^{-1} = I + Q + Q^2 + ...

        The ij-entry of the matrix N is the expected number of times the chain
        is in state s_j given that it starts in state s_i.
        """
        pre_n = self.q.copy()

        np.fill_diagonal(pre_n, [i - 1 for i in self.q.diagonal()])

        return np.linalg.inv(-pre_n)

    def __get_m(self):
        """
        Absorption matrix

        Let m_{ij} be the probability that an absorbing chain will be
        absorbed in the absorbing state s_j if it starts in the transient
        state s_i. Let M be the matrix with entries m_{ij}, then

        M = NR
        """
        return np.matmul(self.n, self.r)

    def get_probability(self, transient_state, absorbing_state):
        """
        Returns the probability that an absorbing chain will be
        absorbed in the absorbing state s_j if it starts in the transient
        state s_i

        Parameters
        ----------
        absorbing_state : int
        transient_state : int
        """

        transient_states = self.transient_states
        absorption_states = self.absorption_states

        if (transient_state in transient_states) and (
            absorbing_state in absorption_states
        ):

            elements = [
                (i, j)
                for i in self.transient_states
                for j in self.absorption_states
            ]
            
            prob = dict(zip(elements, self.m.flatten().tolist()))

            return prob[(transient_state, absorbing_state)]
        else:

            print(
                "\nValid transient states   :{}".format(self.transient_states)
            )
            print(
                "\nValid absorption states  :{}\n".format(
                    self.absorption_states
                )
            )

            warnings.warn(
                "Invalid combination of absorption and transient states"
            )

            return None

    '''
    CODE THAT MAY BE USEFUL IN THE FUTURE, BUT IT'S NOT NECESSARY FOR THIS
    APPLICATION

    def __is_stochastic(self):
        """
        **************** CODE NOT USED ****************

        Checks if the matrix is right stochastic, i.e. if it is a real square
         matrix with each row summing to 1, and all entries are
        nonnegative.
        """
        for row in self.matrix_obj:
            row_sum = np.sum(row)
            if row_sum >= 1 + self.epsilon or row_sum <= 1 - self.epsilon:
                sum_to_one = False
                break
            else:
                sum_to_one = True

        result = (
            self.matrix_obj.shape[0] == self.matrix_obj.shape[1]
            and np.all(self.matrix_obj >= 0)
            and sum_to_one
        )
        if not result:
            raise Exception(
                "This is not a stochastic matrix. It should be a real square \
                matrix with each row summing to 1."
            )
        return result

    def __get_absorption_states(self):
        """
        **************** CODE NOT USED ****************
        Absorption states in the Markov Matrix. Such states
        are those that, when reached, is impossible to leave. This
        accounts for the amount of entries equal to 1 on the diagonal
        of the matrix
        """
        diagonal = np.diag(self.matrix_obj)
        epsilon = self.epsilon
        absorption_states = []

        for counter, element in enumerate(diagonal):
            if (1 - epsilon <= element) and (element <= 1 + epsilon):
                absorption_states.append(counter)

        return absorption_states

    def __get_non_absorption_states(self):
        """
        **************** CODE NOT USED ****************
        Non absorption states or transient states in the Markov Matrix.
        """
        transient_states = [
            i for i in range(self.size) if i not in self.absorption_states
        ]
        return transient_states

    def __get_standard_matrix(self):
        """
        **************** CODE NOT USED ****************
        Get Markov matrix in standard form. Given a Markov matrix P, it can
        be expressed in the following way

        P = | Q R |
            | 0 I |

        Where Q is a t x t matrix, R is a t x r matrix, 0 is a r x t zero
        matrix, and I is a r x r identity matrix, where r is the number
        of absorption states.

        Below are two funtions that return the Q and R matrices
        """

        standard_matrix = self.matrix_obj.copy()

        reordered_states = self.transient_states + self.absorption_states

        initial_list = [
            (i, j) for i in range(self.size) for j in range(self.size)
        ]

        swap_list = [
            (i, j) for i in reordered_states for j in reordered_states
        ]

        for i, s in zip(initial_list, swap_list):
            if i != s:
                standard_matrix.itemset(i, self.matrix_obj.item(s))

        return standard_matrix
    '''
