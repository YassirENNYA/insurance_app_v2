import numpy as np
import pandas as pd


def demographic_parity_difference(y_true, y_pred, sensitive_attribute):
    """
    Calcule la différence de parité démographique entre deux groupes.
    Pour des variables continues, on compare les moyennes.
    """
    groups = np.unique(sensitive_attribute)
    means = {}
    for g in groups:
        mask = sensitive_attribute == g
        means[g] = np.mean(y_pred[mask])

    values = list(means.values())
    difference = max(values) - min(values)

    return {
        "groups": means,
        "difference": difference,
        "group_names": list(means.keys()),
    }


def disparate_impact_ratio(
    y_true, y_pred, sensitive_attribute, unprivileged_value, privileged_value
):
    """
    Calcule le ratio d'impact disparate entre groupe privilégié et non-privilégié.
    Ratio < 0.8 indique un biais significatif (règle des 4/5).
    """
    mask_priv = sensitive_attribute == privileged_value
    mask_unpriv = sensitive_attribute == unprivileged_value

    mean_priv = np.mean(y_pred[mask_priv])
    mean_unpriv = np.mean(y_pred[mask_unpriv])

    ratio = mean_unpriv / mean_priv if mean_priv != 0 else 0

    return {
        "privileged_mean": mean_priv,
        "unprivileged_mean": mean_unpriv,
        "ratio": ratio,
        "privileged_value": privileged_value,
        "unprivileged_value": unprivileged_value,
    }


def group_metrics(y_true, y_pred, sensitive_attribute):
    """
    Calcule les métriques par groupe pour un attribut sensible.
    """
    groups = np.unique(sensitive_attribute)
    results = {}
    for g in groups:
        mask = sensitive_attribute == g
        results[g] = {
            "count": int(np.sum(mask)),
            "mean_pred": float(np.mean(y_pred[mask])),
            "mean_true": float(np.mean(y_true[mask])),
            "std": float(np.std(y_pred[mask])),
        }
    return results
