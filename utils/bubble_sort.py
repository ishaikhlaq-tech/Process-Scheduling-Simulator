def bubble_sort(processes, key):
    n = len(processes)
    for i in range(n):
        for j in range(0, n - i - 1):
            if processes[j][key] > processes[j + 1][key]:
                processes[j], processes[j + 1] = processes[j + 1], processes[j]
    return processes
