import random
from strategy_scanning import strategy_optimizer_scanning
from strategy import strategy_optimizer
from strategy_brute import strategy_optimizer_brute


def _test_all_three(args, result):
    assert strategy_optimizer(*args) == result
    assert strategy_optimizer_brute(*args) == result
    assert strategy_optimizer_scanning(*args) == result


def _test_against_brute(args):
    result_brute = strategy_optimizer_brute(*args)
    assert strategy_optimizer(*args) == result_brute
    assert strategy_optimizer_scanning(*args) == result_brute


# Notice, that most test cases should have at least size of 5 for strategy_optimizer
# Smaller cases should be handled by brute force algorithm

# Boundary values

def test_rates_length_one():
    _test_all_three(args=[[1.1]], result=[0])
    _test_all_three(args=[[0.9]], result=[0])
    _test_all_three(args=[[1.1], 0.9], result=[0])
    _test_all_three(args=[[0.9], 0.9], result=[0])
    _test_all_three(args=[[0.9], 0.01, "C1", "C2", "C1", "C1"], result=[])
    _test_all_three(args=[[1.1], 0.01, "C1", "C2", "C1", "C1"], result=[])


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
def test_big_oracle():
    random.seed(0)
    args = [[float(int(1000 * 2 * random.random()))/1000 for _ in range(16)]]
    _test_against_brute(args + [0.05])
    _test_against_brute(args + [0.75])
    _test_against_brute(args + [0.0001])
    _test_against_brute(args + [0.0])
    _test_against_brute(args + [0.05, "C1", "C2", "C1", "C1"])
    _test_against_brute(args + [0.75, "C1", "C2", "C1", "C1"])
    _test_against_brute(args + [0.0001, "C1", "C2", "C1", "C1"])
    _test_against_brute(args + [0.0, "C1", "C2", "C1", "C1"])

# Equivalence classes

# Condition-coverage
