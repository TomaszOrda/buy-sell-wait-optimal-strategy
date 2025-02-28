from strategy_scanning import strategy_optimizer_scanning
from strategy import strategy_optimizer
from strategy_brute import strategy_optimizer_brute


def _test_all_three(args, result):
    for optimizer in [strategy_optimizer, strategy_optimizer_brute, strategy_optimizer_scanning]:
        assert optimizer(*args) == result

# Notice, that most test cases should have at least size of 5 for strategy_optimizer
# Smaller cases should be handled by brute force algorithm
# There is no written specification. However we can assume that the list with rates has at least 2 elements

# Boundary values


def test_rates_length_two():
    _test_all_three(args=[[1.1, 0.9]], result=[1])
    _test_all_three(args=[[0.9, 1.1]], result=[0])


def test_rates_empty_result():
    _test_all_three(args=[[1.01, 0.99, 1.01], 0.2, "C1", "C2", "C1", "C1"], result=[])
    _test_all_three(args=[[0.99, 1.01, 0.99], 0.2, "C1", "C2", "C1", "C1"], result=[])
    _test_all_three(args=[[1.01, 0.99, 1.01, 0.99, 1.01], 0.2, "C1", "C2", "C1", "C1"], result=[])
    _test_all_three(args=[[0.99, 1.01, 0.99, 0.99, 1.01], 0.2, "C1", "C2", "C1", "C1"], result=[])


def test_rates_margin():
    _test_all_three(args=[[1.1, 0.9, 1.1], 0.2, "C1", "C2", "C1", "C1"], result=[])
    _test_all_three(args=[[1.1, 0.9, 1.1], 0.0001, "C1", "C2", "C1", "C1"], result=[1, 2])
    _test_all_three(args=[[0.9, 1.1, 0.9], 0.2, "C1", "C2", "C1", "C1"], result=[])
    _test_all_three(args=[[0.9, 1.1, 0.9], 0.0001, "C1", "C2", "C1", "C1"], result=[0, 1])

    _test_all_three(args=[[1.1, 0.9, 1.1, 0.9, 1.1], 0.2, "C1", "C2", "C1", "C1"], result=[])
    _test_all_three(args=[[1.1, 0.9, 1.1, 0.9, 1.1], 0.0001, "C1", "C2", "C1", "C1"], result=[1, 2, 3, 4])
    _test_all_three(args=[[0.9, 1.1, 0.9, 1.1, 0.9], 0.2, "C1", "C2", "C1", "C1"], result=[])
    _test_all_three(args=[[0.9, 1.1, 0.9, 1.1, 0.9], 0.0001, "C1", "C2", "C1", "C1"], result=[0, 1, 2, 3])


def test_rates_margin_zero():
    _test_all_three(args=[[1.1, 0.9, 1.1], 0, "C1", "C2", "C1", "C1"], result=[1, 2])
    _test_all_three(args=[[0.9, 1.1, 0.9], 0, "C1", "C2", "C1", "C1"], result=[0, 1])

    _test_all_three(args=[[1.1, 0.9, 1.1, 0.9, 1.1], 0, "C1", "C2", "C1", "C1"], result=[1, 2, 3, 4])
    _test_all_three(args=[[1.1, 0.9, 1.1, 0.9, 1.1], 0, "C1", "C2", "C1", "C1"], result=[1, 2, 3, 4])
    _test_all_three(args=[[0.9, 1.1, 0.9, 1.1, 0.9], 0, "C1", "C2", "C1", "C1"], result=[0, 1, 2, 3])
    _test_all_three(args=[[0.9, 1.1, 0.9, 1.1, 0.9], 0, "C1", "C2", "C1", "C1"], result=[0, 1, 2, 3])


# Oracle

# Equivalence classes

# Condition-coverage
