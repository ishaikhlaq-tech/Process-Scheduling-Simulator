def compare_algorithms(results):
    # Compare based on average waiting time
    best = min(results, key=lambda x: x["average_waiting_time"])
    worst = max(results, key=lambda x: x["average_waiting_time"])

    return {
        "best_algorithm": best["algorithm"],
        "worst_algorithm": worst["algorithm"]
    }
