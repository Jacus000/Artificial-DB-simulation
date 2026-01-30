import sys
from python.generation_orchestrator import DataGeneratorOrchestrator 

def main():
    try:
        orchestrator = DataGeneratorOrchestrator()
        orchestrator.run_all()
        
        print("Success: Database is populated.")
    except Exception as e:
        print(f"Unexpected error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()