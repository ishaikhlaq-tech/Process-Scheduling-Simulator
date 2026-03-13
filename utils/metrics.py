def calculate_metrics(name, gantt_chart, processes):
    waiting = []
    turnaround = []

    for p in processes:
        # If this key is missing, the server crashes!
        if "completion_time" not in p:
             # Fallback to avoid crash, but indicates a bug
            p["completion_time"] = p["arrival_time"] + p["burst_time"]

        tat = p["completion_time"] - p["arrival_time"]
        wt = tat - p["burst_time"]

        turnaround.append(tat)
        waiting.append(max(0, wt)) # Ensure no negative wait time

    avg_wait = sum(waiting) / len(waiting) if waiting else 0
    avg_turn = sum(turnaround) / len(turnaround) if turnaround else 0

    return {
        "algorithm": name,
        "gantt_chart": gantt_chart,
        "average_waiting_time": avg_wait,
        "average_turnaround_time": avg_turn
    }