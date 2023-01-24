import pandas as pd
import matplotlib.pyplot as plt


class Plots:
    def __init__(self):
        pass

    def insertion_performance(self, csv_path="data/insertion_performance.csv"):
        df = pd.read_csv(csv_path)

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8))

        ax1.plot(df["seconds"], df["processed_proteins"], "-o")
        ax1.set_title("Number of Processed Proteins")
        ax1.set_xlabel("Time (seconds)")
        ax1.set_ylabel("Number of Proteins")

        ax2.plot(df["seconds"], df["processed_peptides"], "-o")
        ax2.set_title("Number of Processed Peptides")
        ax2.set_xlabel("Time (seconds)")
        ax2.set_ylabel("Number of Peptides")

        ax3.plot(df["seconds"], df["proteins/sec"], "-o")
        ax3.set_title("Throughput of Proteins per Second")
        ax3.set_xlabel("Time (seconds)")
        ax3.set_ylabel("Proteins per Second")

        fig.subplots_adjust(hspace=0.8)

        plt.show()
