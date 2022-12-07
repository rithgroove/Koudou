import pandas as pd

class Files(object):
    #  activity_history.csv
    _activity_history = pd.NA
    @property
    def activity_history(self):
        return Files._activity_history
    @activity_history.setter
    def activity_history(self, file_df):
        Files._activity_history = file_df

    # agent_position_summary.csv
    _agent_position_summary = pd.NA
    @property
    def agent_position_summary(self):
        return Files._agent_position_summary
    @agent_position_summary.setter
    def agent_position_summary(self, file_df):
        Files._agent_position_summary = file_df

    #  disease_transition.csv
    _disease_transition = pd.NA
    @property
    def disease_transition(self):
        return Files._disease_transition
    @disease_transition.setter
    def disease_transition(self, file_df):
        Files._disease_transition = file_df

    # evacuation.csv
    _evacuation = pd.NA
    @property
    def evacuation(self):
        return Files._evacuation
    @evacuation.setter
    def evacuation(self, file_df):
        Files._evacuation = file_df

    # infection_summary
    _infection_summary = pd.NA
    @property
    def infection_summary(self):
        return Files._infection_summary
    @infection_summary.setter
    def infection_summary(self, file_df):
        Files._infection_summary = file_df

    # infection_transition
    _infection_transition = pd.NA
    @property
    def infection_transition(self):
        return Files._infection_transition
    @infection_transition.setter
    def infection_transition(self, file_df):
        Files._infection_transition = file_df

    # new_infection
    _new_infection = pd.NA
    @property
    def new_infection(self):
        return Files._new_infection
    @new_infection.setter
    def new_infection(self, file_df):
        Files._new_infection = file_df

