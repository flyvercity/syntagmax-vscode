from server.server import parser

def test_repro():
    with open("reproduce_new_features.stmx", "r") as f:
        content = f.read()

    try:
        parser.parse(content)
        print("Parsing successful!")
    except Exception as e:
        print(f"Parsing failed: {e}")
        exit(1)

if __name__ == "__main__":
    test_repro()
