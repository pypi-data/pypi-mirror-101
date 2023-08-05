import yaml
from fuzzywuzzy import fuzz
import operator
import numpy as np

def load_yaml(path: str):
    with open(path) as file:
        yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_dict

def similar(a, b):
    """
    Find similarity score between 2 strings
    """
    return fuzz.ratio(a.lower(), b.lower())

def etf_or_fund(sec_name, search_results):
    """
    Predict that the seach string belongs to fund or etf using similarity score
    """
    scores = {'etf':[],'fund':[]}
    for result in search_results:
        scores[result.sec_type].append(result.similarity_score)
    
    if len(scores['etf']) == 0:
        return 'fund'
    elif len(scores['fund']) == 0:
        return 'etf'
    
    score = {'etf':np.mean(scores['etf']),'fund':np.mean(scores['fund'])}
    max_score = max(score.items(), key=operator.itemgetter(1))[0]

    return max_score

def filter_by_currency(search_results):

    currencies = ['usd','eur','gbp','aus']

    results = []
    for currency in currencies:
        for search in search_results:
            if search.symbol.split(':')[-1].lower() == currency:
                results.append(search)
        
        if len(results) > 0:
            break
    
    return results
    
