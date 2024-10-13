import time
import requests
import pandas as pd
import matplotlib.pyplot as plt

def benchmark_litserver(num_requests=10):
    base_url = "http://localhost:5000"

    operations = ["matrix_multiplication", "neural_network_inference", "llama_inference"]
    results = []
    llama_prompt = "Once upon a time, there was a mighty AI called LLAMA. It"

    for op in operations:
        print(f"\nBenchmarking {op} operation...")
        times = []

        for _ in range(num_requests):
            start_time = time.time()
            if op == "llama_inference":
                response = requests.get(f"{base_url}/{op}", params={"prompt": llama_prompt})
            else:
                response = requests.get(f"{base_url}/{op}")
            elapsed_time = time.time() - start_time

            if response.status_code == 200:
                times.append(elapsed_time)
                print(f"Request successful for {op}, time taken: {elapsed_time:.4f} seconds")
            else:
                print(f"Request failed for {op}")

        results.append({"operation": op, "times": times, "avg_time": sum(times) / len(times)})

    # Convert the results into a pandas DataFrame for analysis
    data = []
    for res in results:
        for time_taken in res["times"]:
            data.append({"operation": res["operation"], "time_taken": time_taken})

    df = pd.DataFrame(data)

    # Output the DataFrame to see the results
    print(df)

    # Visualize the benchmark results
    plt.figure(figsize=(10, 6))
    for op in operations:
        subset = df[df["operation"] == op]
        plt.plot(subset.index, subset["time_taken"], marker='o', label=f"{op} (avg: {res['avg_time']:.4f}s)")

    plt.title("Benchmark of GPU Operations (LitServer)")
    plt.xlabel("Request #")
    plt.ylabel("Time taken (seconds)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    benchmark_litserver(num_requests=10)
