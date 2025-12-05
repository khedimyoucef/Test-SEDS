import pandas as pd
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_all_data

def verify_coach_parsing():
    print("Loading data...")
    data = load_all_data()
    athletes_df = data['athletes']
    
    print(f"Total athletes: {len(athletes_df)}")
    
    # Filter for athletes with coach info
    athletes_with_coach = athletes_df[athletes_df['coach'].notna()]
    print(f"Athletes with coach info: {len(athletes_with_coach)}")
    
    if len(athletes_with_coach) == 0:
        print("No coach info found!")
        return

    # Test parsing on a few samples
    print("\n--- Testing Parsing Logic ---")
    samples = athletes_with_coach.sample(5)
    
    for _, athlete in samples.iterrows():
        print(f"\nAthlete: {athlete['name']}")
        coach_info = athlete['coach']
        print(f"Original Coach String: {coach_info}")
        
        # Simulate the logic used in the app
        coaches = str(coach_info).replace('<br>', '\n').split('\n')
        print("Parsed Coaches:")
        for coach in coaches:
            coach = coach.strip()
            if coach:
                print(f"  - {coach}")

if __name__ == "__main__":
    verify_coach_parsing()
