from rapidfuzz import fuzz, process

def best_match(query: str, candidates: list, key: str = "description", score_cutoff: int = 60):
    """
    candidates: list of dicts; by default compare candidate[key]
    returns (best_candidate, score) or (None, 0)
    """
    choices = {i: c.get(key, "") for i, c in enumerate(candidates)}
    result = process.extractOne(query, choices, scorer=fuzz.WRatio, score_cutoff=score_cutoff)
    if result:
        index, score = result[2], result[1]  # (choice, score, key) depending on API
        return candidates[index], score
    return None, 0
