import json
import os

from src.api.main import app

def main() -> None:
    """
    Generates OpenAPI schema from the running FastAPI app and writes it to interfaces/openapi.json.
    """
    schema = app.openapi()
    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"OpenAPI schema written to {output_path}")

if __name__ == "__main__":
    main()
