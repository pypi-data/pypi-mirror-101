"""Maximum entropy distributions

``maxentropy_continuous`` and ``maxentropy_discrete`` are scipy-style random
variable classes with all the associated methods. See
`<https://en.wikipedia.org/wiki/Maximum_entropy_probability_distribution>`_
for mathematical detail.
"""
from typing import Callable, List, Tuple, Union

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.stats import rv_continuous, rv_discrete

Scalar = Union[int, float]
ArrayLike = Union[list, np.ndarray]
MomentCondition = Tuple[Callable, float]


class maxentropy:  # pylint: disable=invalid-name, too-few-public-methods
    """Base for maximum entropy distributions

    Parameters:
        moment_conditions (list[MomentCondition]): List of (function, value)
            tuples. The distribution will be such that the expectation of the
            function will be equal to the value.

        a (Scalar): Lower bound of the support of the distribution.

        b (Scalar): Upper bound of the support of the distribution.

        x0 (np.ndarray): Initial parameter values which will be optimized
            using ``scipy.optimize.minimize``. If ``None``, the initial parameter
            values will be ones. Default is ``None``.

        kwargs (dict): Additional keyword arguments are passed to
            ``scipy.stats.rv_continuous`` for ``maxentropy_continuous`` or
            ``scipy.stats.rv_discrete`` for ``maxentropy_discrete``.
    """

    def __init__(
        self,
        moment_conditions: List[MomentCondition],
        a: Scalar,
        b: Scalar,
        x0=None,
        **kwargs
    ):
        self.a, self.b = a, b
        self.moment_conditions = moment_conditions
        self.moment_conditions.append(
            (lambda x: np.ones(x.shape) if hasattr(x, "shape") else 1, 1)
        )
        if x0 is None:
            x0 = np.ones(len(self.moment_conditions))
        self.functions_, self.alpha_ = zip(*self.moment_conditions)
        self.params_ = minimize(self._loss, x0=x0).x
        super().__init__(a=a, b=b, **kwargs)  # type: ignore

    def _loss(self, params: np.ndarray) -> float:  # pragma: no cover
        """Maximum entropy distribution loss function

        Args:
            params (np.ndarray): Distribution parameters to optimize

        Raises:
            NotImplementedError: Must implement when subclassing

        Returns:
            float: Loss.
        """
        raise NotImplementedError()

    def _cdf(self, x: Union[Scalar, ArrayLike]):  # pragma: no cover
        """CDF of the maximum entropy distribution

        Args:
            x (Union[Scalar, ArrayLike]): Point(s) at which to evaluate the
                CDF.

        Returns:
            Union[Scalar, ArrayLike]: CDF evaluated at ``x``.
        """
        raise NotImplementedError()


class maxentropy_continuous(maxentropy, rv_continuous):  # pylint: disable=invalid-name
    """Continuous maximum entropy distribution"""

    def _loss(self, params: np.ndarray) -> float:
        constraints_loss = lambda x: np.exp(
            params @ np.array([f(x) for f in self.functions_])
        )
        return -(
            params @ np.array(self.alpha_) - quad(constraints_loss, self.a, self.b)[0]
        )

    def _pdf(  # pylint: disable=arguments-differ
        self, x: Union[Scalar, ArrayLike]
    ) -> Union[Scalar, ArrayLike]:
        """Probability density function.

        Args:
            x (Union[Scalar, ArrayLike]): Point(s) at which to evaluate the
                PDF.

        Returns:
            Union[Scalar, ArrayLike]: PDF evaluated at ``x``.
        """
        return np.exp(self.params_ @ np.array([f(x) for f in self.functions_]))

    def _cdf(self, x: Union[Scalar, ArrayLike]) -> Union[Scalar, ArrayLike]:
        try:
            iter(x)  # type: ignore
            return np.array([self._cdf(x) for x in x])  # type: ignore
        except TypeError:
            return quad(self._pdf, self.a, x)[0]


class maxentropy_discrete(maxentropy, rv_discrete):  # pylint: disable=invalid-name
    """Discrete maximum entropy distribution"""

    def __new__(
        cls, moment_conditions, *args, x0=None, **kwargs
    ):  # pylint: disable=unused-argument, invalid-name
        return super().__new__(cls, *args, **kwargs)

    def _loss(self, params):
        constraints_loss = lambda x: np.exp(
            params @ np.array([f(x) for f in self.functions_])
        )
        return -(
            params @ np.array(self.alpha_)
            - np.array(
                [constraints_loss(x) for x in np.arange(self.a, self.b + 1)]
            ).sum()
        )

    def _pmf(  # pylint: disable=arguments-differ
        self, x: Union[Scalar, ArrayLike]
    ) -> Union[Scalar, ArrayLike]:
        """Probability mass function.

        Args:
            x (Union[Scalar, ArrayLike]): Point(s) at which to evaluate to
            PMF.

        Returns:
            Union[Scalar, ArrayLike]: PMF evaluated at ``x``.
        """
        return np.exp(self.params_ @ np.array([f(x) for f in self.functions_]))

    def _cdf(self, x: Union[Scalar, ArrayLike]) -> Union[float, ArrayLike]:
        try:
            iter(x)  # type: ignore
            return np.array([self._cdf(x) for x in x])  # type: ignore
        except TypeError:
            return float(
                np.array([self._pmf(t) for t in np.arange(self.a, x + 1)]).sum()  # type: ignore
            )
