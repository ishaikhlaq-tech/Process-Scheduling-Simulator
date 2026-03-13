from utils.metrics import calculate_metrics

def priority_scheduling(processes):
    n = len(processes)
    completed = 0
    current_time = 0
    visited = [False] * n
    gantt_chart = []
    
    processes.sort(key=lambda x: x["arrival_time"])

    while completed < n:
        ready_queue = []
        for i in range(n):
            if not visited[i] and processes[i]["arrival_time"] <= current_time:
                ready_queue.append((processes[i], i))

        if not ready_queue:
            next_arrival = float('inf')
            for i in range(n):
                if not visited[i]:
                    next_arrival = min(next_arrival, processes[i]["arrival_time"])
            if next_arrival == float('inf'): break
            current_time = next_arrival
            continue

        # Lower number = Higher priority
        best_process, idx = min(ready_queue, key=lambda x: (x[0]["priority"], x[0]["arrival_time"]))

        start = current_time
        end = start + best_process["burst_time"]
        
        gantt_chart.append({
            "pid": best_process["pid"],
            "start": start,
            "end": end
        })
        
        # --- FIX: SAVE COMPLETION TIME ---
        best_process["completion_time"] = end
        # ---------------------------------
        
        current_time = end
        visited[idx] = True
        completed += 1

    return calculate_metrics("Priority", gantt_chart, processes)