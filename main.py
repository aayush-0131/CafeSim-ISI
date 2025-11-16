# main.py
# CORRECTED LOGIC: Measures total time in system.
import simpy
import random
import statistics

# --- 1. PARAMETERS ---
# WARNING: THESE PARAMETERS CREATE AN UNSTABLE SYSTEM
# Arrival rate (1/17.14) > Food Service Rate (1/120)
SIM_TIME = 3600
MEAN_IAT = 17.14
MEAN_FOOD_TIME = 120
MEAN_PAY_TIME = 30
FOOD_COUNTERS = 20
CASHIERS = 29

wait_times = [] # This now stores TOTAL TIME, not wait time

# --- 2. STUDENT PROCESS ---
def student(env, name, food_counter, cashier):
    """
    Correctly models a student's journey and records
    their TOTAL time spent in the system.
    """
    arrival_time = env.now
    
    # 1. Food counter queue and service
    with food_counter.request() as req:
        yield req # Wait for the counter
        # Now, get food (service time)
        yield env.timeout(random.expovariate(1.0 / MEAN_FOOD_TIME))
        
    # 2. Cashier queue and service
    with cashier.request() as req:
        yield req # Wait for the cashier
        # Now, pay (service time)
        yield env.timeout(random.expovariate(1.0 / MEAN_PAY_TIME))
    
    # 3. Record total time in system
    total_time_in_system = env.now - arrival_time
    wait_times.append(total_time_in_system)

# --- 3. SETUP PROCESS ---
def setup(env, food_counters, cashiers):
    food_counter = simpy.Resource(env, capacity=food_counters)
    cashier = simpy.Resource(env, capacity=cashiers)
    
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / MEAN_IAT))
        i += 1
        env.process(student(env, f'Student {i}', food_counter, cashier))

# --- 4. EXECUTION ---
if __name__ == "__main__":
    
    print(f"--- CafeSim-ISI: Simulation ({FOOD_COUNTERS} Food Counter(s), {CASHIERS} Cashier(s)) ---")
    
    random.seed(42)
    env = simpy.Environment()
    wait_times.clear()
    
    env.process(setup(env, FOOD_COUNTERS, CASHIERS))
    env.run(until=SIM_TIME)
    
    print("\n--- Simulation Results ---")
    print(f"Simulation ran for {SIM_TIME / 60:.0f} minutes.")
    print(f"Total students served: {len(wait_times)}")
    
    if wait_times:
        avg_time_min = (statistics.mean(wait_times) / 60)
        max_time_min = (max(wait_times) / 60)
        
        # Renamed print statement for accuracy
        print(f"Average TOTAL time in system: {avg_time_min:.2f} minutes")
        print(f"Maximum TOTAL time in system: {max_time_min:.2f} minutes")
    else:
        print("No students were served.")
