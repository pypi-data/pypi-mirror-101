from collections import defaultdict

import numpy as np
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import f1_score as classification_f1_score



def simple_accuracy(preds, labels):
    """return simple accuracy
    """
    return (preds == labels).mean()


def accuracy(preds, labels):
    """return simple accuracy in expected dict format
    """
    acc = simple_accuracy(preds, labels)
    return {"acc": acc}


def acc_and_f1(preds, labels):
    """return accuracy and f1 score
    """
    acc = simple_accuracy(preds, labels)
    f1 = classification_f1_score(y_true=labels, y_pred=preds)
    return {
        "acc": acc,
        "f1": f1,
        "acc_and_f1": (acc + f1) / 2,
    }


def pearson_and_spearman(preds, labels):
    """get pearson and spearman correlation
    """
    pearson_corr = pearsonr(preds, labels)[0]
    spearman_corr = spearmanr(preds, labels)[0]
    return {
        "pearson": pearson_corr,
        "spearmanr": spearman_corr,
        "corr": (pearson_corr + spearman_corr) / 2,
    }
