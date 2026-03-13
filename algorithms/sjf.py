def sjf_scheduling(processes):
    n = len(processes)
    # 1. Sort by arrival time initially to handle the first process
    processes.sort(key=lambda x: x['arrival_time'])
    
    completed = 0
    current_time = 0
    visited = [False] * n
    gantt_chart = []
    
    total_waiting_time = 0
    total_turnaround_time = 0

    while completed < n:
        # 2. Find all processes that have arrived and haven't been processed
        ready_queue = []
        for i in range(n):
            if not visited[i] and processes[i]['arrival_time'] <= current_time:
                ready_queue.append(i)

        if not ready_queue:
            # CPU is IDLE: Jump to the arrival time of the next available process
            next_arrival = min([p['arrival_time'] for i, p in enumerate(processes) if not visited[i]])
            current_time = next_arrival
            continue

        # 3. Pick the process with the shortest burst time among those ready
        best_idx = min(ready_queue, key=lambda i: processes[i]['burst_time'])
        p = processes[best_idx]

        # 4. Execute the process
        start_time = current_time
        end_time = start_time + p['burst_time']
        
        # 5. Calculate Metrics (The FCFS style)
        turnaround_time = end_time - p['arrival_time']
        waiting_time = turnaround_time - p['burst_time']
        
        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time
        
        # 6. Record to Gantt Chart
        gantt_chart.append({
            "pid": p['pid'],
            "start": start_time,
            "end": end_time
        })

        # 7. Update state
        current_time = end_time
        visited[best_idx] = True
        completed += 1

    return {
        "algorithm": "SJF",
        "gantt_chart": gantt_chart,
        "average_waiting_time": total_waiting_time / n if n > 0 else 0,
        "average_turnaround_time": total_turnaround_time / n if n > 0 else 0
    }