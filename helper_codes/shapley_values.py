"""Helper module to compute for the Shapley values of each feature

Authors: Leodegario Lorenzo II, Alva Presbitero
Date: 13 October 2021
"""

from math import factorial


def compute_shapley_value(model_outcomes, feature_name):
    """Return the Shapley value of the feature given model outcomes
    dictionary

    Parameters
    ----------
    model_outcomes : dict of float
        Dictionary contining the model outcomes/prediction for the given
        feature value. Keys of the dictionary are tuples containing the
        feature subset $S$, while the values are the model outcomes.

    feature_name : str
        Name of the feature whose Shapley value is to be computed

    Returns
    -------
    shapley_value : float
        The computed Shapley value of the feature
    """
    # Get number of features
    subsets_list = model_outcomes.keys()
    n = max([len(subset) for subset in subsets_list])

    # Get all subset that contains the feature, this is the domain of set $S$
    S_domain = [subset for subset in subsets_list if feature_name in subset]

    # Initialize results container
    shapley_value = 0

    # Iterate through all possible values of $S$, i.e., those that contain the
    # feature $i$
    for S in S_domain:
        # Compute for the length of set $S$
        s = len(S)

        # Get the subset that don't contain i
        S_without_i = tuple(sorted(set(S) - set((feature_name,))))

        # Compute for the weighted marginal contribution.
        # Note that this has two components:
        # 1. Probability of i joining to form S, P(S)
        P_of_S = factorial(s - 1) * factorial(n - s) / factorial(n)

        # 2. Marginal contribution of i as it joins S, MC_{i, S}
        marginal_contribution = model_outcomes[S] - model_outcomes[S_without_i]

        # We then add the weighted marginal contribution to the feature's
        # Shapley value
        shapley_value += P_of_S * marginal_contribution

    return shapley_value


def get_shapley_values(model_outcomes):
    """Return Shapley values of each feature given model outcomes

    Given the model outcomes for each possible feature subset $S$, this
    function computes for the expected marginal contribution $\phi$ of
    each feature $i$ using the Shapley value definition:

    $$
    \phi_i (v) = \sum_{S \subseteq N} \frac{(s-1)!(n-s)!}{n!}[v(S) - v(S \backslash \{ i \})]
    $$

    where $N$ is the set of all features, $|S|$ and $|N|$ is defined as
    $s$ and $n$ respectively, and $v$ refers to the  corresponding model
    outcome

    Parameters
    ----------
    model_outcomes : dict of float
        Dictionary contining the model outcomes/prediction for the given
        feature value. Keys of the dictionary are tuples containing the
        feature subset $S$, while the values are the model outcomes.

    Returns
    -------
    shapley_values : dict of float
        Dictionary with the feature name as key and value as the
        feature's Shapley value
    """
    # Get superset $N$
    N = sorted(model_outcomes.keys(), key=lambda x: -len(x))[0]

    # Initialize results container
    shapley_values = {}

    # Iterate through all features then compute their Shapley values
    for feature_name in N:
        shapley_values[feature_name] = compute_shapley_value(
            model_outcomes, feature_name)

    return shapley_values
