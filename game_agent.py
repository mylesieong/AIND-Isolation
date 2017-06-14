"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # This heuristic returns the density of player's neigborhood  
    # which is the percentage of legal box-nearby quantity over 
    # the total boxy-nearby quantity
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    neigborhood = # a list of box position
    legal_num = len(n for n in neigborhood if n is legal) # legal box qunaity
    total_num = len(neigborhood)
    
    return float(legal_num/total_num)
    #return float(len(game.get_legal_moves(player)))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # This heuristic returns the delta between 2 player's 
    # density of neigborhood  
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    neigborhood = # a list of box position
    legal_num = len(n for n in neigborhood if n is legal) # legal box qunaity
    total_num = len(neigborhood)
    
    rival_neigborhood = # a list of box position
    rival_legal_num = len(n for n in rival_neigborhood if n is legal) # legal box qunaity
    rival_total_num = len(rival_neigborhood)

    return float(legal_num/total_num) - float(rival_legal_num/rival_total_num)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # This heuristic reutrns the open second move score
    # If box b can be reach by player in 2 steps, then 
    # b is one of the open second move. 
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    open_first_move = game.get_legal_moves(player)
    open_second_move = [game.get_legal_moves(m) for m in open_first_move]
    return float(len(open_second_move))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=2.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)

        try:
            best_move = self.minimax(game, self.search_depth)

        except SearchTimeout:
            best_move = game.get_legal_moves()[0]
            pass  # Handle any actions required after timeout as needed

        return best_move

    def minimax(self, game, depth):
        """
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if legal_moves:
            _, move = max([(self.min_value(game.forecast_move(m), depth - 1), m) for m in legal_moves])
        else:
            move = (-1, -1)

        return move

    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)
        
        legal_moves = game.get_legal_moves()
        v = float("inf")

        for m in legal_moves:
            v =  min(v, self.max_value(game.forecast_move(m), depth -1))
        
        return v

    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0 :
            return self.score(game, self)
        
        legal_moves = game.get_legal_moves()
        v = float("-inf")

        for m in legal_moves:
            v =  max(v, self.min_value(game.forecast_move(m), depth -1))
        
        return v

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)
        iterative_depth = 1

        try:
            while True:
                best_move = self.alphabeta(game, iterative_depth)
                iterative_depth = iterative_depth + 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        
        if legal_moves:
            _, move = max([(self.min_value(game.forecast_move(m), depth - 1, alpha, beta), m) for m in legal_moves])
        else:
            move = (-1, -1)

        return move

    def min_value(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)
        
        legal_moves = game.get_legal_moves()
        v = float("inf")

        for m in legal_moves:
            v =  min(v, self.max_value(game.forecast_move(m), depth -1, alpha, beta))
            if v <= alpha:
                return v
            else:
                beta = min(beta, v)
        
        return v


    def max_value(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0 :
            return self.score(game, self)
        
        legal_moves = game.get_legal_moves()
        v = float("-inf")

        for m in legal_moves:
            v =  max(v, self.min_value(game.forecast_move(m), depth -1, alpha, beta))
            if v >= beta:
                return v
            else:
                alpha = max(alpha, v)
        
        return v
