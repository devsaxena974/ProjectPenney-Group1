import heatmap
import simulation

def main():
  
    print("Running simulation.py...")
    simulation.run_simulation()
  
    print("Running heatmap.py...")
    heatmap.create_heatmaps()
  
if __name__ == "__main__":
    main()
