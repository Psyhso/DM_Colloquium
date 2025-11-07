import pytest
from my_math.natural_module import NaturalModule

@pytest.mark.parametrize("N_1, N_2, expected", [
    (NaturalModule(0, [9]), NaturalModule(1, [2, 1]), NaturalModule(1, [6, 3])),

])

def test_LCM_NN_N(N_1, N_2, expected):
    natural_1 = NaturalModule(N_1.n, N_1.A)
    natural_2 = NaturalModule(N_2.n, N_2.A)

    natural_1.LCM_NN_N(natural_2)
    print(natural_1.n, natural_1.A)
    print(expected.n, expected.A)

    assert natural_1.n == expected.n and natural_1.A == expected.A
