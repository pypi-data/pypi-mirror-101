from deap import tools


def one_point(individual1, individual2):
    """
    One point crossover
    :param individual1: Individual 1
    :param individual2: Individual 2
    :return: A tuple of two individuals
    """
    return tools.cxOnePoint(individual1, individual2)


def two_point(individual1, individual2):
    """
    Two point crossover
    :param individual1: Individual 1
    :param individual2: Individual 2
    :return: A tuple of two individuals
    """
    return tools.cxTwoPoint(individual1, individual2)
