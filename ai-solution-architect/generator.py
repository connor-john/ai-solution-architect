import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class DiagramGenerator:
    def __init__(self):
        self.components = []
        self.connections = []

    def generate_diagram(self, description):
        print("Generating diagram for description:", description)

        example_input = """
        This is a web application that uses a React frontend, a Node.js backend, and a MongoDB database. The frontend communicates with the backend via RESTful APIs. The backend processes requests, interacts with the database, and returns responses to the frontend. The application is hosted on AWS using EC2 instances for the frontend and backend, and uses MongoDB Atlas for the database.
        """

        example_output = {
            "components": [
                {
                    "name": "React Frontend",
                    "type": "Frontend Framework",
                    "logo": "react_logo.png",
                },
                {
                    "name": "Node.js Backend",
                    "type": "Backend Server",
                    "logo": "nodejs_logo.png",
                },
                {"name": "MongoDB", "type": "Database", "logo": "mongodb_logo.png"},
                {
                    "name": "AWS EC2 (Frontend)",
                    "type": "Cloud Instance",
                    "logo": "aws_ec2_logo.png",
                },
                {
                    "name": "AWS EC2 (Backend)",
                    "type": "Cloud Instance",
                    "logo": "aws_ec2_logo.png",
                },
                {
                    "name": "MongoDB Atlas",
                    "type": "Cloud Database Service",
                    "logo": "mongodb_atlas_logo.png",
                },
            ],
            "connections": [
                {
                    "from": "React Frontend",
                    "to": "Node.js Backend",
                    "label": "RESTful API",
                },
                {
                    "from": "Node.js Backend",
                    "to": "MongoDB",
                    "label": "Database Queries",
                },
                {
                    "from": "AWS EC2 (Frontend)",
                    "to": "React Frontend",
                    "label": "Hosts",
                },
                {
                    "from": "AWS EC2 (Backend)",
                    "to": "Node.js Backend",
                    "label": "Hosts",
                },
                {"from": "MongoDB Atlas", "to": "MongoDB", "label": "Hosts"},
            ],
        }

        prompt = f"""
        You are a technical diagram generator. Your task is to interpret a description of a system and generate a JSON representation of the diagram components and connections.

        Here's an example input:
        {example_input}

        And here's the corresponding output:
        {json.dumps(example_output, indent=2)}

        Now, generate a similar JSON representation for the following description:
        {description}

        The JSON should include 'components' (list of objects with 'name', 'type', and 'logo' properties) and 'connections' (list of objects with 'from', 'to', and 'label' properties).
        Be sure to include all relevant components and their connections, and use appropriate logos for well-known services or technologies.
        """

        print("Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a technical diagram generator."},
                {"role": "user", "content": prompt},
            ],
        )
        print("Received response from OpenAI API.")

        print("Raw API response:", response)
        print("Response content:", response.choices[0].message.content)

        try:
            diagram_data = json.loads(response.choices[0].message.content)
            print("Parsed JSON data:", json.dumps(diagram_data, indent=2))
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print("Failed to parse the following content:")
            print(response.choices[0].message.content)
            raise

        self.components = diagram_data["components"]
        self.connections = diagram_data["connections"]

        return self.to_custom_syntax()

    def to_custom_syntax(self):
        syntax = "DIAGRAM:\n"

        for component in self.components:
            syntax += f"COMPONENT {component['name']}:\n"
            syntax += f"  TYPE: {component['type']}\n"
            syntax += f"  LOGO: {component['logo']}\n"

        syntax += "\nCONNECTIONS:\n"
        for connection in self.connections:
            syntax += (
                f"{connection['from']} -> {connection['to']}: {connection['label']}\n"
            )

        return syntax
