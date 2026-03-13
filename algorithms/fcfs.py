def fcfs_scheduling(processes):
    # Sort processes by arrival time
    processes.sort(key=lambda x: x['arrival_time'])
    
    n = len(processes)
    gantt_chart = []
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    
    for i in range(n):
        p = processes[i]
        
        # IF IDLE: If CPU is free but next process hasn't arrived, jump to its arrival
        if current_time < p['arrival_time']:
            current_time = p['arrival_time']
            
        start_time = current_time
        end_time = start_time + p['burst_time']
        
        # Calculate Metrics
        turnaround_time = end_time - p['arrival_time']
        waiting_time = turnaround_time - p['burst_time']
        
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        
        # Update Gantt
        gantt_chart.append({
            "pid": p['pid'],
            "start": start_time,
            "end": end_time
        })
        
        # Advance clock
        current_time = end_time

    return {
        "algorithm": "FCFS",
        "gantt_chart": gantt_chart,
        "average_waiting_time": total_waiting_time / n if n > 0 else 0,
        "average_turnaround_time": total_turnaround_time / n if n > 0 else 0
    }