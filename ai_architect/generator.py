# llm_diagram_generator/diagram_generator.py

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class DiagramGenerator:
    def generate_diagram(self, description):
        prompt = f"""
        Generate a JSON representation of a system architecture based on the following description:

        {description}

        The JSON should strictly adhere to the following structure and guidelines:

        1. Groups: Categorize components into logical groups (e.g., cloud providers, data sources, user types).
        2. Components: List all system components with their details.
        3. Connections: Describe how components are connected or interact.

        Use the following schema:

        {{
            "groups": [
                {{
                    "name": "group_name",
                    "type": "group_type" // e.g., "cloud_provider", "data_source", "user_group", etc.
                }}
            ],
            "components": [
                {{
                    "name": "component_name",
                    "type": "component_type",
                    "group": "group_name",
                    "image": "image_filename.png"
                }}
            ],
            "connections": [
                {{
                    "from": "component_name1",
                    "to": "component_name2",
                    "label": "connection_description"
                }}
            ]
        }}

        Image Naming Guidelines:
        1. For specific cloud services, use "[provider]-[service].png" (e.g., "aws-lambda.png", "azure-sql-database.png").
        2. For generic services, use descriptive names (e.g., "database.png", "api.png", "server.png").
        3. For user roles, use "user.png" or specific roles like "admin.png", "analyst.png".
        4. If unsure, use a generic term related to the component type.

        Example:
        Given the description: "A web application using AWS. It has a React frontend hosted on S3, an API Gateway connecting to Lambda functions, and a DynamoDB database. CloudFront is used as a CDN."

        The JSON output should be:

        {{
            "groups": [
                {{
                    "name": "AWS",
                    "type": "cloud_provider"
                }},
                {{
                    "name": "Frontend",
                    "type": "client_side"
                }}
            ],
            "components": [
                {{
                    "name": "React App",
                    "type": "frontend_framework",
                    "group": "Frontend",
                    "image": "react.png"
                }},
                {{
                    "name": "S3 Bucket",
                    "type": "object_storage",
                    "group": "AWS",
                    "image": "aws-s3.png"
                }},
                {{
                    "name": "CloudFront",
                    "type": "cdn",
                    "group": "AWS",
                    "image": "aws-cloudfront.png"
                }},
                {{
                    "name": "API Gateway",
                    "type": "api_management",
                    "group": "AWS",
                    "image": "aws-api-gateway.png"
                }},
                {{
                    "name": "Lambda",
                    "type": "serverless_function",
                    "group": "AWS",
                    "image": "aws-lambda.png"
                }},
                {{
                    "name": "DynamoDB",
                    "type": "nosql_database",
                    "group": "AWS",
                    "image": "aws-dynamodb.png"
                }}
            ],
            "connections": [
                {{
                    "from": "React App",
                    "to": "CloudFront",
                    "label": "user access"
                }},
                {{
                    "from": "CloudFront",
                    "to": "S3 Bucket",
                    "label": "origin"
                }},
                {{
                    "from": "React App",
                    "to": "API Gateway",
                    "label": "API calls"
                }},
                {{
                    "from": "API Gateway",
                    "to": "Lambda",
                    "label": "triggers"
                }},
                {{
                    "from": "Lambda",
                    "to": "DynamoDB",
                    "label": "read/write"
                }}
            ]
        }}

        Ensure your output is a valid JSON object containing only the requested structure.
        Do not include any explanatory text or markdown formatting.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical diagram generator that outputs only valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content
