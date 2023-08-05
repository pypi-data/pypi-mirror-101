from .fisher_exact import _fisher_exact
import numpy as np
from typing import Literal, NamedTuple, Optional, overload, Union


class FisherExactPvalues(NamedTuple):
    less: float
    greater: float
    two_tail: float


@overload
def fisher_exact(table, alternative: None) -> FisherExactPvalues:
    ...


def fisher_exact(
    table, alternative: Union[Literal["two-sided"], Literal["less"], Literal["greater"]] = "two-sided"
) -> float:

    c = np.asarray(table, dtype=np.int32)
    if not c.shape == (2, 2):
        raise ValueError("The input `table` must be of shape (2, 2).")

    if np.any(c < 0):
        raise ValueError("All values in `table` must be nonnegative.")

    less_pvalue, greater_pvalue, two_tail_pvalue = _fisher_exact(*c.flat)
    if alternative is None:
        return FisherExactPvalues(less_pvalue, greater_pvalue, two_tail_pvalue)
    elif alternative == "two-sided":
        return two_tail_pvalue
    elif alternative == "less":
        return less_pvalue
    elif alternative == "greater":
        return greater_pvalue
    else:
        raise ValueError(f"Unknown alternative = {alternative}. Use one of {{`two-sided`, `less`, `greater`, None}}.")
