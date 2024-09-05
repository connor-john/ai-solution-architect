from .generator import DiagramGenerator
from .visualiser import DiagramVisualiser

import json


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
   This is a simple data warehouse solution for a retail company using Microsoft Azure services. The system collects data from three main sources:

1. Point of Sale (POS) System: Generates daily sales data in CSV format
2. Online Store: Uses a SQL Server database for order information
3. Customer Relationship Management (CRM) System: Provides customer data via an API

The data warehouse solution uses the following components:

1. Azure Data Factory: Orchestrates the data extraction and loading processes
2. Azure Blob Storage: Acts as a staging area for raw data
3. Azure Synapse Analytics (formerly SQL Data Warehouse): Serves as the main data warehouse
4. Azure Data Lake Analytics: Performs data transformations
5. Power BI: Connects to Synapse Analytics for reporting and dashboards

The data flow is as follows:
1. Azure Data Factory extracts data daily from the POS system, Online Store database, and CRM API
2. Raw data is stored in Azure Blob Storage
3. Azure Data Lake Analytics processes and transforms the raw data
4. Transformed data is loaded into Azure Synapse Analytics
5. Power BI connects to Synapse Analytics to create reports and dashboards

The system also includes:
- Azure Active Directory for user authentication and access control
- Azure Monitor for system monitoring and alerts

End users, including the Sales team, Marketing team, and Management, access reports and dashboards through Power BI.
    """

    print("Starting diagram generation...")
    try:
        diagram_data = generator.generate_diagram(description)
        print("Diagram generation completed.")
        print("Raw diagram data:")
        print(diagram_data)
        print("Type of diagram_data:", type(diagram_data))

        print("\nAttempting to parse as JSON...")
        try:
            parsed_data = json.loads(diagram_data)
            print("Successfully parsed JSON:")
            print(json.dumps(parsed_data, indent=2))
        except json.JSONDecodeError as json_error:
            print(f"Failed to parse JSON: {json_error}")
            print("Attempting to extract JSON from the response...")
            # Try to find and extract a JSON object from the string
            import re

            json_match = re.search(r"\{.*\}", diagram_data, re.DOTALL)
            if json_match:
                try:
                    parsed_data = json.loads(json_match.group())
                    print("Successfully extracted and parsed JSON:")
                    print(json.dumps(parsed_data, indent=2))
                except json.JSONDecodeError:
                    print("Failed to parse extracted JSON")
            else:
                print("No JSON object found in the response")

        print("\nVisualizing...")
        visualizer = DiagramVisualiser(parsed_data)
        visualizer.render("enhanced_system_architecture")
        print(
            "Visualization complete. The diagram has been saved and should open automatically."
        )
    except Exception as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")  # Red error message
        import traceback

        print("Full traceback:")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
