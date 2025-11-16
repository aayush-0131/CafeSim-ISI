# CafeSim-ISI: A Digital Twin of the ISI Cafeteria

This is a "Pi-shaped" project that builds a Digital Twin of the ISI Kolkata cafeteria to find and fix system bottlenecks. It combines **Operations Research** (Queueing Theory) with **Discrete-Event Simulation (DES)** using the `SimPy` library.

The project demonstrates a key insight: "common sense" assumptions about a system are often wrong, and a computational model is the only way to find the true, non-obvious bottlenecks.

## 1. The Initial Model (The "Ground Truth")

The system was modeled based on real-world observations during a 1-hour peak period:
* **Arrival Rate:** 1 student every 17.14s ($\lambda \approx 3.5/\text{min}$)
* **Food Service Time:** 120s per student ($\mu_1 = 0.5/\text{min}$)
* **Payment Time:** 30s per student ($\mu_2 = 2/\text{min}$)

## 2. Baseline Run (Proving the System is Broken)

A simulation with **1 Food Counter** and **1 Cashier** was run.

* **Result:**
    * **Total Students Served:** 31
    * **Average Time in System:** 19.09 minutes
    * **Total Arrivals (Expected):** ~210

**Analysis:** The model proved the system was catastrophically unstable. It could only serve **31** of the **~210** students who arrived. The queue would, in theory, grow to infinity.

## 3. Finding the *Real* Bottleneck

The "common sense" assumption was that the cashier was the bottleneck. The model proved this wrong.

**The Math:**
* **Arrival Rate ($\lambda$):** 1 person / 17.14s
* **Food Service Rate ($\mu_1$):** 1 person / 120s

The system was unstable because the **arrival rate was 7x faster than the food service rate**.

## 4. Iterative Hypothesis Testing

The model was then used to find a stable and optimal solution.

### Hypothesis 1: Fix the Food Counter
* **Test:** `FOOD_COUNTERS = 8` (to beat the arrival rate), `CASHIERS = 1`
* **Result:**
    * **Total Students Served:** 110
    * **Average Time in System:** 15.31 minutes
* **Analysis:** The system got *worse*. We fixed the food bottleneck, which created a new, massive pile-up at the single cashier. This proves a system must be balanced.

### Hypothesis 2: Balance the System
* **Test:** `FOOD_COUNTERS = 8`, `CASHIERS = 5`
* **Result:**
    * **Total Students Served:** 194 (serving ~92% of all arrivals)
    * **Average Time in System:** 3.41 minutes
* **Analysis:** This is a stable, optimal solution. The system is now flowing, and the total time is reasonable.

## 5. Finding the Point of Diminishing Returns

Can we make it faster?

* **Test:** `FOOD_COUNTERS = 20`, `CASHIERS = 29` (massively over-provisioned)
* **Result:**
    * **Total Students Served:** 193
    * **Average Time in System:** 2.63 minutes
* **Analysis:** The average time has hit a "floor." This 2.63-minute average is the **physical service time** (120s food + 30s payment = 150s or 2.5 min, plus random variance). Adding more resources is a waste of money; the system cannot go any faster.

## Conclusion

This project successfully demonstrates the use of DES to:
1.  Model a real-world system.
2.  Disprove initial, "common sense" assumptions.
3.  Identify the true, non-obvious bottleneck.
4.  Run iterative tests to find an optimal, balanced solution.
5.  Identify the physical limits and point of diminishing returns.

## How to Run

1.  Clone the repository.
2.  Activate the virtual environment: `source venv/bin/activate`
3.  Install dependencies: `pip install -r requirements.txt`
4.  Modify parameters (e.g., `FOOD_COUNTERS`) in `main.py`.
5.  Run the simulation: `python main.py`