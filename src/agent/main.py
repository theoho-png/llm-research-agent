import sys
import json
from src.agent.graph import run_pipeline


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.agent.main '<question>'", file=sys.stderr)
        sys.exit(1)
    question = sys.argv[1]
    # Optional: slot-aware mode via env/flag (basic: always false here)
    result = run_pipeline(question)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
