import logging
import pandas as pd
import matplotlib.pyplot as plt


class Plots:
    def __init__(self):
        pass

    def insertion_performance(self, csv_path="data/insertion_performance.csv"):
        df = pd.read_csv(csv_path)
        logging.info(csv_path)

        df["minutes"] = df["seconds"] / 60
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(8, 8))

        ax1.plot(df["minutes"], df["processed_proteins"], "-o")
        ax1.set_title("Number of Processed Proteins")
        ax1.set_xlabel("Time (minutes)")
        ax1.set_ylabel("Number of Proteins")

        ax2.plot(df["minutes"], df["processed_peptides"], "-o")
        ax2.set_title("Number of Processed Peptides")
        ax2.set_xlabel("Time (minutes)")
        ax2.set_ylabel("Number of Peptides")

        ax3.plot(df["minutes"], df["proteins/sec"], "-o")
        ax3.set_title("Throughput of Proteins per Second")
        ax3.set_xlabel("Time (minutes)")
        ax3.set_ylabel("Proteins per Second")

        ax4.plot(df["minutes"], df["peptides/sec"], "-o")
        ax4.set_title("Throughput of Peptides per Second")
        ax4.set_xlabel("Time (minutes)")
        ax4.set_ylabel("Peptides per Second")

        fig.subplots_adjust(hspace=0.8)

        plt.show()
