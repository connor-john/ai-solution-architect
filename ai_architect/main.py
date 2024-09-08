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
            print("\033[1m\033[94m" + section + "\033[0m\n")
        elif section.startswith("CONNECTIONS:"):
            print("\033[1m\033[92m" + section + "\033[0m")
            connections = section.split("\n")[1:]  # Skip the "CONNECTIONS:" header
            for connection in connections:
                print("  " + connection)
        else:
            components = section.split("COMPONENT")[1:]
            for component in components:
                lines = component.strip().split("\n")
                print("\033[1m" + "COMPONENT" + lines[0] + "\033[0m")
                for line in lines[1:]:
                    print("  " + line)
                print()

    print("\n" + "=" * 50 + "\n")


def main():
    generator = DiagramGenerator()

    description = """
   This is an AWS-based data analytics pipeline for a retail company. The system integrates data from multiple sources, processes it, and stores it in a data warehouse for analysis. Here are the key components and their interactions:

Data Sources:
1. Internal PostgreSQL database containing customer information
2. External API providing real-time inventory data from suppliers
3. Daily sales reports in CSV format stored in an S3 bucket

AWS Components:
1. AWS Step Functions: Orchestrates the entire data pipeline
2. AWS Lambda functions: 
   - Lambda A: Extracts data from the PostgreSQL database
   - Lambda B: Calls the external API and processes the response
   - Lambda C: Processes CSV files from S3
   - Lambda D: Transforms and combines data from all sources
   - Lambda E: Loads processed data into Redshift
3. Amazon S3: Stores raw CSV files and serves as a staging area for processed data
4. Amazon Redshift: Acts as the central data warehouse
5. Amazon CloudWatch: Monitors the pipeline and triggers the Step Functions workflow daily

Data Flow:
1. CloudWatch triggers the Step Functions workflow daily at 1 AM
2. Step Functions invokes Lambda A, B, and C in parallel to extract data from different sources
3. Lambda A connects to the PostgreSQL database and extracts customer data
4. Lambda B calls the external API to fetch inventory data
5. Lambda C reads and parses the CSV files from S3
6. Once all extraction Lambdas complete, Step Functions triggers Lambda D
7. Lambda D combines and transforms the data from all sources
8. Transformed data is stored temporarily in S3
9. Step Functions then triggers Lambda E
10. Lambda E loads the processed data from S3 into Redshift
11. Upon completion, Step Functions sends a notification about the pipeline status

Access and Reporting:
- Data analysts access Redshift to run queries and generate reports
- A Tableau dashboard connects to Redshift for real-time visualizations
- The IT team has full access to monitor and manage all AWS services

This pipeline ensures that the latest data from all sources is available in the Redshift data warehouse every morning for analysis and reporting.
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
        print(f"\033[91mAn error occurred: {e}\033[0m")
        import traceback

        print("Full traceback:")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
