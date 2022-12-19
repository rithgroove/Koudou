import pandas as pd
from .utils import preprocess_linear_data

class ModelOne(object):
    #  activity_history.csv
    _activity_history = pd.NA

    @property
    def activity_history(self):
        return ModelOne._activity_history

    @activity_history.setter
    def activity_history(self, file_df):
        ModelOne._activity_history = file_df

    # agent_position_summary.csv
    _agent_position_summary = pd.NA

    @property
    def agent_position_summary(self):
        return ModelOne._agent_position_summary

    @agent_position_summary.setter
    def agent_position_summary(self, file_df):
        ModelOne._agent_position_summary = file_df

    #  disease_transition.csv
    _disease_transition = pd.NA

    @property
    def disease_transition(self):
        return ModelOne._disease_transition

    @disease_transition.setter
    def disease_transition(self, file_df):
        ModelOne._disease_transition = file_df

    # evacuation.csv
    _evacuation = pd.NA

    @property
    def evacuation(self):
        return ModelOne._evacuation

    @evacuation.setter
    def evacuation(self, file_df):
        ModelOne._evacuation = file_df

    # infection_summary.csv
    _infection_summary = pd.NA

    @property
    def infection_summary(self):
        return ModelOne._infection_summary

    @infection_summary.setter
    def infection_summary(self, file_df):
        file_df = preprocess_linear_data(file_df)
        ModelOne._infection_summary = file_df

    # infection_transition.csv
    _infection_transition = pd.NA

    @property
    def infection_transition(self):
        return ModelOne._infection_transition

    @infection_transition.setter
    def infection_transition(self, file_df):
        ModelOne._infection_transition = file_df

    # new_infection.csv
    _new_infection = pd.NA

    @property
    def new_infection(self):
        return ModelOne._new_infection

    @new_infection.setter
    def new_infection(self, file_df):
        ModelOne._new_infection = file_df

    # log.txt
    _log = []

    @property
    def log(self):
        return ModelOne._log

    @log.setter
    def log(self, file_df):
        ModelOne._log = file_df


class ModelTwo(object):
    #  activity_history.csv
    _activity_history = pd.NA

    @property
    def activity_history(self):
        return ModelTwo._activity_history

    @activity_history.setter
    def activity_history(self, file_df):
        ModelTwo._activity_history = file_df

    # agent_position_summary.csv
    _agent_position_summary = pd.NA

    @property
    def agent_position_summary(self):
        return ModelTwo._agent_position_summary

    @agent_position_summary.setter
    def agent_position_summary(self, file_df):
        ModelTwo._agent_position_summary = file_df

    #  disease_transition.csv
    _disease_transition = pd.NA

    @property
    def disease_transition(self):
        return ModelTwo._disease_transition

    @disease_transition.setter
    def disease_transition(self, file_df):
        ModelTwo._disease_transition = file_df

    # evacuation.csv
    _evacuation = pd.NA

    @property
    def evacuation(self):
        return ModelTwo._evacuation

    @evacuation.setter
    def evacuation(self, file_df):
        ModelTwo._evacuation = file_df

    # infection_summary.csv
    _infection_summary = pd.NA

    @property
    def infection_summary(self):
        return ModelTwo._infection_summary

    @infection_summary.setter
    def infection_summary(self, file_df):
        file_df = preprocess_linear_data(file_df)
        ModelTwo._infection_summary = file_df

    # infection_transition.csv
    _infection_transition = pd.NA

    @property
    def infection_transition(self):
        return ModelTwo._infection_transition

    @infection_transition.setter
    def infection_transition(self, file_df):
        ModelTwo._infection_transition = file_df

    # new_infection.csv
    _new_infection = pd.NA

    @property
    def new_infection(self):
        return ModelTwo._new_infection

    @new_infection.setter
    def new_infection(self, file_df):
        ModelTwo._new_infection = file_df

    # log.txt
    _log = []

    @property
    def log(self):
        return ModelTwo._log

    @log.setter
    def log(self, file_df):
        ModelTwo._log = file_df


class ModelThree(object):
    #  activity_history.csv
    _activity_history = pd.NA

    @property
    def activity_history(self):
        return ModelThree._activity_history

    @activity_history.setter
    def activity_history(self, file_df):
        ModelThree._activity_history = file_df

    # agent_position_summary.csv
    _agent_position_summary = pd.NA

    @property
    def agent_position_summary(self):
        return ModelThree._agent_position_summary

    @agent_position_summary.setter
    def agent_position_summary(self, file_df):
        ModelThree._agent_position_summary = file_df

    #  disease_transition.csv
    _disease_transition = pd.NA

    @property
    def disease_transition(self):
        return ModelThree._disease_transition

    @disease_transition.setter
    def disease_transition(self, file_df):
        ModelThree._disease_transition = file_df

    # evacuation.csv
    _evacuation = pd.NA

    @property
    def evacuation(self):
        return ModelThree._evacuation

    @evacuation.setter
    def evacuation(self, file_df):
        ModelThree._evacuation = file_df

    # infection_summary.csv
    _infection_summary = pd.NA

    @property
    def infection_summary(self):
        return ModelThree._infection_summary

    @infection_summary.setter
    def infection_summary(self, file_df):
        file_df = preprocess_linear_data(file_df)
        ModelThree._infection_summary = file_df

    # infection_transition.csv
    _infection_transition = pd.NA

    @property
    def infection_transition(self):
        return ModelThree._infection_transition

    @infection_transition.setter
    def infection_transition(self, file_df):
        ModelThree._infection_transition = file_df

    # new_infection.csv
    _new_infection = pd.NA

    @property
    def new_infection(self):
        return ModelThree._new_infection

    @new_infection.setter
    def new_infection(self, file_df):
        ModelThree._new_infection = file_df

    # log.txt
    _log = []

    @property
    def log(self):
        return ModelThree._log

    @log.setter
    def log(self, file_df):
        ModelThree._log = file_df
