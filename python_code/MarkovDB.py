from numpy import matrix, identity, subtract, matmul, zeros
import pandas as pd

from .MarkovMatrix import MarkovMatrix


class MarkovDB:
    """
    Markov Database

    ...

    Parameters
    ----------
    dataset : list of dict
        Each dictionary has to have the 'conversion', 'value' and
        'path' keys. The value for the 'conversion' key should be
        an integer 1 or 0, denoting if there was a conversion. The
        value
    separator : str
        The path separator for each column (' > ' for example) that
        indicates the customer journey


    Atributes
    ---------
    list_of_paths : list of str
        List of all the different customer paths present in the dataset
    total_conversion : int
        Number of conversions in the dataset
    unique_channels : list of str
        Returns a sorted list with the different channel possibilities of
        the customer journey, including the 'START', 'NULL' and
        'CONVERSION' channels
    transition_states : dict
        Returns a dictionary, with the keys as the different possible
        states, and the values equal to the number of times that
        particular state happened
    transition_probs : dict
        Returns a dictionary, with the keys as the different possible
        states, and the values equal to the probability for that value
        to happen
    transition_matrix : pandas dataframe
        Returns the matrix with the different probabilities for
        each state
    markov_matrix : MarkovMatrix
        Returns a MarkovMatrix object created with the transition matrix
    channel_to_key : dict
        Mapping of the channel name with the integer it represents
    """

    def __init__(self, dataset, var_path, var_conv, var_value, separator):

        self.dataset = dataset
        self.var_path = var_path
        self.var_conv = var_conv
        self.var_value = var_value
        self.separator = separator
        self.total_conversions = 0
        self.total_value = 0
        self.list_of_paths = self.__get_list_of_paths()
        self.unique_channels = self.__get_channels()
        self.channel_to_key = {
            self.unique_channels[i]: i
            for i in range(0, len(self.unique_channels))
        }
        self.transition_matrix = self.__get_transition_matrix()
        self.transition_matrix_df = self.__get_transition_matrix_df()
        self.markov_matrix = self.__get_markov_matrix()

    def __str__(self):
        return (
            """\ndataset:\n{0}\n\nseparator:\n{1}\n\nchannels:\n{2}""".format(
                self.dataset, self.separator, self.unique_channels
            )
        )

    def __get_channels(self):
        """
        Returns a sorted list with the different channel possibilities of the
        customer journey
        """
        channels = set()
        for row in self.dataset:
            rstates = row[self.var_path].split(self.separator)
            for state in rstates:
                if state != "":
                    channels.add(state)
        try:
            channels.remove("NULL")
            return ["START"] + sorted(list(channels)) + ["NULL", "CONVERSION"]
        except:
            return ["START"] + sorted(list(channels)) + ["NULL", "CONVERSION"]

    def __get_list_of_paths(self):
        """
        Returns a list of all the different customer paths present in the dataset
        """
        list_of_paths = []
        for row in self.dataset:
            self.total_conversions += row[self.var_conv]
            self.total_value += row[self.var_value]
            rstates = row[self.var_path].split(self.separator)
            rstates = ["START"] + rstates
            if row[self.var_conv] > 0:
                rstates = rstates + ["CONVERSION"]
            else:
                rstates = rstates + ["NULL"]
            list_of_paths.append(rstates)

        return list_of_paths

    def __get_transition_matrix(self):
        """
        Returns the matrix with the different probabilities for
        each state
        """

        channel_to_key = self.channel_to_key

        size = len(self.unique_channels)

        transition_matrix = zeros((size, size))

        # Absorption states
        i = channel_to_key["CONVERSION"]
        j = channel_to_key["NULL"]
        transition_matrix[i, i] = 1
        transition_matrix[j, j] = 1

        for user_path in self.list_of_paths:
            for index, elem in enumerate(user_path):
                if elem not in ["CONVERSION", "NULL"]:
                    i = channel_to_key[elem]
                    j = channel_to_key[user_path[index + 1]]
                    transition_matrix[i, j] += 1

        return transition_matrix / transition_matrix.sum(axis=1, keepdims=True)

    def __get_markov_matrix(self):
        """
        Returns a MarkovMatrix object created with the
        transition matrix
        """

        return MarkovMatrix(self.transition_matrix)

    def __get_transition_matrix_df(self):

        df = pd.DataFrame(
            self.transition_matrix,
            columns=self.unique_channels,
            index=self.unique_channels,
        )

        return df

    def get_probability(self, trans_state, abs_state):

        if isinstance(trans_state, str) and isinstance(abs_state, str):
            trans_state = self.channel_to_key[trans_state]
            abs_state = self.channel_to_key[abs_state]

        return self.markov_matrix.get_probability(trans_state, abs_state)
