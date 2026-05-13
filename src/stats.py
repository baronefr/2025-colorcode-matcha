
from statsmodels.stats.proportion import proportion_confint

def get_pfail(shots, fails, alpha=0.01, confint_method='binom_test'):
    pfail_low, pfail_high = proportion_confint(
        fails,
        shots,
        alpha=alpha,
        method=confint_method
    )
    pfail = (pfail_low + pfail_high) / 2
    delta_pfail = pfail_high - pfail

    return pfail, delta_pfail
