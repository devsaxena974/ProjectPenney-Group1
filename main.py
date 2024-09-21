import heat_map
import simulation

def main():
  
    print("Running simulation.py...")
    simulation.run_simulation()
  
    print("Running heatmap.py...")
    heat_map.create_heatmaps()
  
if __name__ == "__main__":
    main()
