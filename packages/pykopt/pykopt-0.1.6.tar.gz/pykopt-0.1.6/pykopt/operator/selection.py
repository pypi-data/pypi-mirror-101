from deap import tools


def tournament_selection(individuals, k, tournsize):
    """Tournament selection
    :param individuals: individuals to make selection
    :param k: number of individuals to select
    :param tournsize: number of participants in each tournament
    :return: list of selected indivuduals
    """
    return tools.selTournament(individuals, k, tournsize, fit_attr="fitness")


def roulette_wheel(individuals, k):
    """Roulette wheel selection
    :param individuals: individuals to make selection
    :param k: number of individuals to select
    :return: list of selected indivuduals
    """
    return tools.selRoulette(individuals, k, fit_attr="fitness")


def random_selection(individuals, k):
    """Random selection
    :param individuals:  individuals to make selection
    :param k: number of individuals to select
    :return: list of selected indivuduals
    """
    return tools.selRandom(individuals, k)
