import sys
import os
import copy
import traceback

# 1. Setup imports
try:
    from algorithms.fcfs import fcfs_scheduling
    from algorithms.sjf import sjf_scheduling
    from algorithms.srtf import srtf_scheduling
    from algorithms.priority import priority_scheduling
    from algorithms.round_robin import round_robin_scheduling
    print("✅ Imports successful.\n")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you are running this file from the main 'backend' folder.")
    sys.exit(1)

# 2. Define Test Data
# Scenario: Mixed arrival times and priorities
# P1 arrives 0, runs 5 (Priority 2)
# P2 arrives 1, runs 3 (Priority 1 - High)
# P3 arrives 2, runs 1 (Priority 3 - Low)
test_data = [
    {"pid": 1, "arrival_time": 0, "burst_time": 5, "priority": 2},
    {"pid": 2, "arrival_time": 1, "burst_time": 3, "priority": 1},
    {"pid": 3, "arrival_time": 2, "burst_time": 1, "priority": 3}
]

def run_test(name, func, args):
    print(f"🔹 Testing {name}...")
    try:
        # Create a fresh copy of data so previous tests don't mess it up
        data = copy.deepcopy(test_data)
        
        # Run Algorithm
        if name == "Round Robin":
            result = func(data, 2) # Quantum = 2
        else:
            result = func(data)
            
        # Print Success
        print(f"   ✅ SUCCESS!")
        print(f"   Avg Wait: {result['average_waiting_time']:.2f}")
        print(f"   Avg Turn: {result['average_turnaround_time']:.2f}")
        
        # simplified gantt print
        gantt_simple = [f"{b['pid']}({b['start']}-{b['end']})" for b in result['gantt_chart']]
        print(f"   Gantt: {' -> '.join(gantt_simple)}")
        print("-" * 50)
        
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        # Print the exact line number where it crashed
        traceback.print_exc()
        print("-" * 50)

# 3. Execution
if __name__ == "__main__":
    print("-" * 50)
    run_test("FCFS", fcfs_scheduling, None)
    run_test("SJF", sjf_scheduling, None)
    run_test("SRTF", srtf_scheduling, None)
    run_test("Priority", priority_scheduling, None)
    run_test("Round Robin", round_robin_scheduling, None)