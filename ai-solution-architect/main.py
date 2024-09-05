from .generator import DiagramGenerator


def print_diagram_syntax(syntax):
    print("\n" + "=" * 50)
    print("Generated Diagram Syntax".center(50))
    print("=" * 50 + "\n")

    sections = syntax.split("\n\n")

    for section in sections:
        if section.startswith("DIAGRAM:"):
            print("\033[1m\033[94m" + section + "\033[0m\n")  # Bold and blue
        elif section.startswith("CONNECTIONS:"):
            print("\033[1m\033[92m" + section + "\033[0m")  # Bold and green
            connections = section.split("\n")[1:]  # Skip the "CONNECTIONS:" header
            for connection in connections:
                print("  " + connection)
        else:
            components = section.split("COMPONENT")[
                1:
            ]  # Split components, remove empty first element
            for component in components:
                lines = component.strip().split("\n")
                print(
                    "\033[1m" + "COMPONENT" + lines[0] + "\033[0m"
                )  # Bold component name
                for line in lines[1:]:
                    print("  " + line)
                print()  # Add a blank line between components

    print("\n" + "=" * 50 + "\n")


def main():
    generator = DiagramGenerator()

    description = """
    This is a data warehouse solution that is on AWS. The solution uses AWS Step Functions to extract from external systems like CSVs in S3 buckets or internal databases or external APIs. The Step Function will then load the data into AWS Redshift. For the transformations, dbt will be used on Redshift to transform the data into the standardized format for analysis to report off.
    """

    print("Starting diagram generation...")
    try:
        diagram_syntax = generator.generate_diagram(description)
        print("Diagram generation completed. Printing syntax...")
        print_diagram_syntax(diagram_syntax)
    except Exception as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")  # Red error message
        import traceback

        print("Full traceback:")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
