import random
import pytest
from strategy_scanning import strategy_optimizer_scanning
from strategy import strategy_optimizer
from strategy_brute import strategy_optimizer_brute


def _test_all_three(args, result):
    assert strategy_optimizer(*args) == result
    assert strategy_optimizer_brute(*args) == result
    assert strategy_optimizer_scanning(*args) == result


def _test_all_three_raise_error(args, expected_error):
    with pytest.raises(expected_error):
        strategy_optimizer(*args)
    with pytest.raises(expected_error):
        strategy_optimizer_brute(*args)
    with pytest.raises(expected_error):
        strategy_optimizer_scanning(*args)


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

# Empty rates list should only work with opening and closing currencies being the same
def test_empty_rates():
    _test_all_three(args=[[], 0.05, "C1", "C2", "C1", "C1"], result=[])
    _test_all_three_raise_error(args=[[]], expected_error=ValueError)


# Opening and closing currencies should choosen from currency_1 and currency_2
def test_unknown_currencies():
    _test_all_three_raise_error(args=[[0.9, 1.1, 0.9, 1.1, 0.9], 0.05, "C1", "C2", "C1", "C3"],
                                expected_error=ValueError)
    _test_all_three_raise_error(args=[[0.9, 1.1, 0.9, 1.1, 0.9], 0.05, "C1", "C2", "C6", "C3"],
                                expected_error=ValueError)


# Currency names should differ
def test_indistinguishable_currencies():
    _test_all_three_raise_error(args=[[0.9, 1.1, 0.9, 1.1, 0.9], 0.05, "C1", "C1", "C1", "C1"],
                                expected_error=ValueError)


# Margin should be at least 0
def test_negative_margin():
    _test_all_three_raise_error(args=[[0.9, 1.1, 0.9, 1.1, 0.9], -0.05],
                                expected_error=ValueError)


# Condition-coverage

# Exploratory testing
