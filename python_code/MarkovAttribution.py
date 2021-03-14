from copy import deepcopy
import pandas as pd
from .MarkovDB import MarkovDB


class MarkovAttribution:
    """
    Content Attribution with Markov Chains

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
    db : MarkovDB
        MarkovDB object created from the base dataset
    full_probability : float
        Probability to go from the channel 'START' to 'CONVERSION'
    channels : list of str
        Sorted list with the different channel possibilities of
        the customer journey, including the 'START', 'NULL' and
        'CONVERSION' channels
    transition_matrix : pandas dataframe
        Matrix with the different probabilities for each state
    cprobs : dict
        Returns a dictionary that assess the impact on the conversion if
        a channel is removed
    """

    def __init__(self, dataset, var_path, var_conv, var_value, separator):

        self.dataset = dataset
        self.var_path = var_path
        self.var_conv = var_conv
        self.var_value = var_value
        self.separator = separator
        self.db = MarkovDB(dataset, var_path, var_conv, var_value, separator)
        self.full_probability = self.db.get_probability("START", "CONVERSION")
        self.channels = self.db.unique_channels
        self.df_info = self.__get_df()

    def __rm(self, channel):
        """
        Returns a copy of the original data, with channel equal to NULL
        """
        new_dataset = deepcopy(self.dataset)
        for row in new_dataset:
            try:
                row[self.var_path] = row[self.var_path].replace(
                    channel, "NULL"
                )
            except Exception:
                row[self.var_path] = row[self.var_path]
        return new_dataset

    def __removal_effect(self, channel):
        """
        Returns a dictionary that has information on the effect of removing
        a channel on the dataset
        """

        removal_ds = self.__rm(channel)
        removal_db = MarkovDB(
            removal_ds,
            self.var_path,
            self.var_conv,
            self.var_value,
            self.separator,
        )
        removal_prob = removal_db.get_probability("START", "CONVERSION")
        if self.full_probability == 0:
            removal_eff = 0
        else:
            removal_eff = 1 - (removal_prob / self.full_probability)

        return removal_eff

    def __get_df(self):
        """
        Returns a dictionary that assess the impact on the conversion if
        a channel is removed
        """

        effect = {}
        cumulative = 0
        total_conversions = self.db.total_conversions
        total_value = self.db.total_value

        weighted_effect_list = []
        total_conversion_value_list = []
        total_conversions_list = []

        channels_temp = [
            i
            for i in self.channels
            if i not in ["START", "CONVERSION", "NULL"]
        ]
        for channel in channels_temp:
            effect[channel] = self.__removal_effect(channel)
            cumulative += effect[channel]
        for channel in channels_temp:
            weighted_effect_channel = effect[channel] / cumulative
            total_conversions_channel = (
                weighted_effect_channel * total_conversions
            )
            total_conversion_value_channel = (
                weighted_effect_channel * total_value
            )

            weighted_effect_list.append(weighted_effect_channel)
            total_conversions_list.append(total_conversions_channel)
            total_conversion_value_list.append(total_conversion_value_channel)

        d = {
            "channel_name": channels_temp,
            "total_conversion": total_conversions_list,
            "total_conversion_value": total_conversion_value_list,
        }

        return pd.DataFrame(data=d)
