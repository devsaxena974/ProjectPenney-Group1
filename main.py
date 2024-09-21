import heat_map
import simulation

def main():
  
    print("Running simulation.py...")
    simulation.run_simulation()
  
    print("Running heat_map.py...")
    heat_map.generate_heat_map()
  
if __name__ == "__main__":
    main()
