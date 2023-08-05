# -*- coding: utf-8 -*-
"""Implements the feature tranformers of the VAEP framework."""
from functools import wraps
from typing import Callable, List, Type, Union

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from pandera.typing import DataFrame

import socceraction.spadl.config as spadlconfig
from socceraction.atomic.spadl import AtomicSPADLSchema
from socceraction.spadl.base import SPADLSchema

Actions = Type[Union[DataFrame[SPADLSchema], DataFrame[AtomicSPADLSchema]]]
SPADLActions = Type[DataFrame[SPADLSchema]]
GameStates = List[SPADLActions]
Features = Type[DataFrame]
FeatureTransfomer = Callable[[GameStates], Features]  # type: ignore


def feature_column_names(fs: List[FeatureTransfomer], nb_prev_actions: int = 3) -> List[str]:
    """Return the names of the features generated by a list of transformers.

    Parameters
    ----------
    fs : list(callable)
        A list of feature transformers.
    nb_prev_actions : int (default = 3)
        The number of previous actions included in the game state.

    Returns
    -------
    list(str)
        The name of each generated feature.
    """
    spadlcolumns = [
        'game_id',
        'period_id',
        'time_seconds',
        'timestamp',
        'team_id',
        'player_id',
        'start_x',
        'start_y',
        'end_x',
        'end_y',
        'result_id',
        'result_name',
        'bodypart_id',
        'bodypart_name',
        'type_id',
        'type_name',
    ]
    dummy_actions = pd.DataFrame(np.zeros((10, len(spadlcolumns))), columns=spadlcolumns)
    for c in spadlcolumns:
        if 'name' in c:
            dummy_actions[c] = dummy_actions[c].astype(str)
    gs = gamestates(dummy_actions, nb_prev_actions)
    return list(pd.concat([f(gs) for f in fs], axis=1).columns.values)


def gamestates(actions: Actions, nb_prev_actions: int = 3) -> GameStates:
    r"""Convert a dataframe of actions to gamestates.

    Each gamestate is represented as the <nb_prev_actions> previous actions.

    The list of gamestates is internally represented as a list of actions
    dataframes :math:`[a_0,a_1,\ldots]` where each row in the a_i dataframe contains the
    previous action of the action in the same row in the :math:`a_{i-1}` dataframe.

    Parameters
    ----------
    actions : pd.DataFrame
        A DataFrame with the actions of a game.
    nb_prev_actions : int (default = 3)
        The number of previous actions included in the game state.

    Returns
    -------
    list(pd.DataFrame)
         The <nb_prev_actions> previous actions for each action.
    """
    states = [actions]
    for i in range(1, nb_prev_actions):
        prev_actions = actions.copy().shift(i, fill_value=0)
        prev_actions.loc[: i - 1, :] = pd.concat([actions[:1]] * i, ignore_index=True)
        states.append(prev_actions)
    return states


def play_left_to_right(gamestates: GameStates, home_team_id: int) -> GameStates:
    """Perform all action in the same playing direction.

    This changes the start and end location of each action, such that all actions
    are performed as if the team plays from left to right.

    Parameters
    ----------
    gamestates : list(pd.DataFrame)
        The game states of a game.
    home_team_id : int
        The ID of the home team.

    Returns
    -------
    list(pd.DataFrame)
        The game states with all actions performed left to right.
    """
    a0 = gamestates[0]
    away_idx = a0.team_id != home_team_id
    for actions in gamestates:
        for col in ['start_x', 'end_x']:
            actions.loc[away_idx, col] = spadlconfig.field_length - actions[away_idx][col].values
        for col in ['start_y', 'end_y']:
            actions.loc[away_idx, col] = spadlconfig.field_width - actions[away_idx][col].values
    return gamestates


def simple(actionfn: Callable[[Actions], Features]) -> FeatureTransfomer:
    """Make a function decorator to apply actionfeatures to game states.

    Parameters
    ----------
    actionfn : callable
        A feature transformer that operates on actions.

    Returns
    -------
    callable
        A feature transformer that operates on game states.
    """

    @wraps(actionfn)
    def _wrapper(gamestates: List[pd.DataFrame]) -> pd.DataFrame:
        if not isinstance(gamestates, (list,)):
            gamestates = [gamestates]
        X = []
        for i, a in enumerate(gamestates):
            Xi = actionfn(a)
            Xi.columns = [c + '_a' + str(i) for c in Xi.columns]
            X.append(Xi)
        return pd.concat(X, axis=1)

    return _wrapper


# SIMPLE FEATURES


@simple
def actiontype(actions: Actions) -> Features:
    """Get the type of each action.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The 'type_id' of each action.
    """
    return actions[['type_id']]


@simple
def actiontype_onehot(actions: SPADLActions) -> Features:
    """Get the one-hot-encoded type of each action.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        A one-hot encoding of each action's type.
    """
    X = pd.DataFrame()
    for type_name in spadlconfig.actiontypes:
        col = 'type_' + type_name
        X[col] = actions['type_name'] == type_name
    return X


@simple
def result(actions: SPADLActions) -> Features:
    """Get the result of each action.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The 'result_id' of each action.
    """
    return actions[['result_id']]


@simple
def result_onehot(actions: SPADLActions) -> Features:
    """Get the one-hot-encode result of each action.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The one-hot encoding of each action's result.
    """
    X = pd.DataFrame()
    for result_name in spadlconfig.results:
        col = 'result_' + result_name
        X[col] = actions['result_name'] == result_name
    return X


@simple
def actiontype_result_onehot(actions: SPADLActions) -> Features:
    """Get a one-hot encoding of the combination between the type and result of each action.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The one-hot encoding of each action's type and result.
    """
    res = result_onehot.__wrapped__(actions)  # type: ignore
    tys = actiontype_onehot.__wrapped__(actions)  # type: ignore
    df = pd.DataFrame()
    for tyscol in list(tys.columns):
        for rescol in list(res.columns):
            df[tyscol + '_' + rescol] = tys[tyscol] & res[rescol]
    return df


@simple
def bodypart(actions: Actions) -> Features:
    """Get the body part used to perform each action.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The 'bodypart_id' of each action.
    """
    return actions[['bodypart_id']]


@simple
def bodypart_onehot(actions: Actions) -> Features:
    """Get the one-hot-encoded bodypart of each action.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The one-hot encoding of each action's bodypart.
    """
    X = pd.DataFrame()
    for bodypart_name in spadlconfig.bodyparts:
        col = 'bodypart_' + bodypart_name
        X[col] = actions['bodypart_name'] == bodypart_name
    return X


@simple
def time(actions: Actions) -> Features:
    """Get the time when each action was performed.

    This generates the following features:
        :period_id:
            The ID of the period.
        :time_seconds:
            Seconds since the start of the period.
        :time_seconds_overall:
            Seconds since the start of the game. Stoppage time during previous
            periods is ignored.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The 'period_id', 'time_seconds' and 'time_seconds_overall' when each
        action was performed.
    """
    timedf = actions[['period_id', 'time_seconds']].copy()
    timedf['time_seconds_overall'] = ((timedf.period_id - 1) * 45 * 60) + timedf.time_seconds
    return timedf


@simple
def startlocation(actions: SPADLActions) -> Features:
    """Get the location where each action started.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The 'start_x' and 'start_y' location of each action.
    """
    return actions[['start_x', 'start_y']]


@simple
def endlocation(actions: SPADLActions) -> Features:
    """Get the location where each action ended.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The 'end_x' and 'end_y' location of each action.
    """
    return actions[['end_x', 'end_y']]


_goal_x: float = spadlconfig.field_length
_goal_y: float = spadlconfig.field_width / 2


@simple
def startpolar(actions: SPADLActions) -> Features:
    """Get the polar coordinates of each action's start location.

    The center of the opponent's goal is used as the origin.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The 'start_dist_to_goal' and 'start_angle_to_goal' of each action.
    """
    polardf = pd.DataFrame()
    dx = abs(_goal_x - actions['start_x'])
    dy = abs(_goal_y - actions['start_y'])
    polardf['start_dist_to_goal'] = np.sqrt(dx ** 2 + dy ** 2)
    with np.errstate(divide='ignore', invalid='ignore'):
        polardf['start_angle_to_goal'] = np.nan_to_num(np.arctan(dy / dx))
    return polardf


@simple
def endpolar(actions: SPADLActions) -> Features:
    """Get the polar coordinates of each action's end location.

    The center of the opponent's goal is used as the origin.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The 'start_dist_to_goal' and 'start_angle_to_goal' of each action.
    """
    polardf = pd.DataFrame()
    dx = abs(_goal_x - actions['end_x'])
    dy = abs(_goal_y - actions['end_y'])
    polardf['end_dist_to_goal'] = np.sqrt(dx ** 2 + dy ** 2)
    with np.errstate(divide='ignore', invalid='ignore'):
        polardf['end_angle_to_goal'] = np.nan_to_num(np.arctan(dy / dx))
    return polardf


@simple
def movement(actions: SPADLActions) -> Features:
    """Get the distance covered by each action.

    Parameters
    ----------
    actions : pd.DataFrame
        The actions of a game.

    Returns
    -------
    pd.DataFrame
        The horizontal ('dx'), vertical ('dy') and total ('movement') distance
        covered by each action.
    """
    mov = pd.DataFrame()
    mov['dx'] = actions.end_x - actions.start_x
    mov['dy'] = actions.end_y - actions.start_y
    mov['movement'] = np.sqrt(mov.dx ** 2 + mov.dy ** 2)
    return mov


# STATE FEATURES


def team(gamestates: GameStates) -> Features:
    """Check whether the possession changed during the game state.

    For each action in the game state, True if the team that performed the
    action is the same team that performed the last action of the game state;
    otherwise False.

    Parameters
    ----------
    gamestates : pd.DataFrame
        The game states of a game.

    Returns
    -------
    pd.DataFrame
        A dataframe with a column 'team_ai' for each <nb_prev_actions> indicating
        whether the team that performed action a0 is in possession.
    """
    a0 = gamestates[0]
    teamdf = pd.DataFrame()
    for i, a in enumerate(gamestates[1:]):
        teamdf['team_' + (str(i + 1))] = a.team_id == a0.team_id
    return teamdf


def time_delta(gamestates: GameStates) -> pd.DataFrame:
    """Get the number of seconds between the last and previous actions.

    Parameters
    ----------
    gamestates : pd.DataFrame
        The game states of a game.

    Returns
    -------
    pd.DataFrame
        A dataframe with a column 'time_delta_i' for each <nb_prev_actions>
        containing the number of seconds between action ai and action a0.
    """
    a0 = gamestates[0]
    dt = pd.DataFrame()
    for i, a in enumerate(gamestates[1:]):
        dt['time_delta_' + (str(i + 1))] = a0.time_seconds - a.time_seconds
    return dt


def space_delta(gamestates: GameStates) -> Features:
    """Get the distance covered between the last and previous actions.

    Parameters
    ----------
    gamestates : pd.DataFrame
        The gamestates of a game.

    Returns
    -------
    pd.DataFrame
        A dataframe with a column for the horizontal ('dx_a0i'), vertical
        ('dy_a0i') and total ('mov_a0i') distance covered between each
        <nb_prev_actions> action ai and action a0.
    """
    a0 = gamestates[0]
    spaced = pd.DataFrame()
    for i, a in enumerate(gamestates[1:]):
        dx = a.end_x - a0.start_x
        spaced['dx_a0' + (str(i + 1))] = dx
        dy = a.end_y - a0.start_y
        spaced['dy_a0' + (str(i + 1))] = dy
        spaced['mov_a0' + (str(i + 1))] = np.sqrt(dx ** 2 + dy ** 2)
    return spaced


# CONTEXT FEATURES


def goalscore(gamestates: GameStates) -> Features:
    """Get the number of goals scored by each team after the action.

    Parameters
    ----------
    gamestates : pd.DataFrame
        The gamestates of a game.

    Returns
    -------
    pd.DataFrame
        The number of goals scored by the team performing the last action of the
        game state ('goalscore_team'), by the opponent ('goalscore_opponent'),
        and the goal difference between both teams ('goalscore_diff').
    """
    actions = gamestates[0]
    teamA = actions['team_id'].values[0]
    goals = actions['type_name'].str.contains('shot') & (
        actions['result_id'] == spadlconfig.results.index('success')
    )
    owngoals = actions['type_name'].str.contains('shot') & (
        actions['result_id'] == spadlconfig.results.index('owngoal')
    )
    teamisA = actions['team_id'] == teamA
    teamisB = ~teamisA
    goalsteamA = (goals & teamisA) | (owngoals & teamisB)
    goalsteamB = (goals & teamisB) | (owngoals & teamisA)
    goalscoreteamA = goalsteamA.cumsum() - goalsteamA
    goalscoreteamB = goalsteamB.cumsum() - goalsteamB

    scoredf = pd.DataFrame()
    scoredf['goalscore_team'] = (goalscoreteamA * teamisA) + (goalscoreteamB * teamisB)
    scoredf['goalscore_opponent'] = (goalscoreteamB * teamisA) + (goalscoreteamA * teamisB)
    scoredf['goalscore_diff'] = scoredf['goalscore_team'] - scoredf['goalscore_opponent']
    return scoredf
