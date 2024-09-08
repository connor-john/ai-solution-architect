from ai_architect.visualiser import DiagramVisualiser


def main():
    data = {
        "groups": [
            {"name": "AWS", "type": "cloud_provider"},
            {"name": "Data Sources", "type": "data_source"},
            {"name": "User Groups", "type": "user_group"},
        ],
        "components": [
            {
                "name": "PostgreSQL",
                "type": "database",
                "group": "Data Sources",
                "image": "database.png",
            },
            {
                "name": "Supplier API",
                "type": "api",
                "group": "Data Sources",
                "image": "api.png",
            },
            {
                "name": "S3 Bucket (CSV)",
                "type": "object_storage",
                "group": "Data Sources",
                "image": "aws-s3.png",
            },
            {
                "name": "Step Functions",
                "type": "workflow_service",
                "group": "AWS",
                "image": "aws-step-functions.png",
            },
            {
                "name": "Lambda Functions",
                "type": "serverless_function",
                "group": "AWS",
                "image": "aws-lambda.png",
            },
            {
                "name": "S3 Bucket (Staging)",
                "type": "object_storage",
                "group": "AWS",
                "image": "aws-s3.png",
            },
            {
                "name": "Redshift",
                "type": "data_warehouse",
                "group": "AWS",
                "image": "aws-redshift.png",
            },
            {
                "name": "CloudWatch",
                "type": "monitoring_service",
                "group": "AWS",
                "image": "aws-cloudwatch.png",
            },
            {
                "name": "Data Analyst",
                "type": "role",
                "group": "User Groups",
                "image": "analyst.png",
            },
            {
                "name": "IT Team",
                "type": "role",
                "group": "User Groups",
                "image": "admin.png",
            },
            {
                "name": "Tableau",
                "type": "visualization_tool",
                "group": "User Groups",
                "image": "tableau.png",
            },
        ],
        "connections": [
            {"from": "CloudWatch", "to": "Step Functions", "label": "triggers"},
            {"from": "Step Functions", "to": "Lambda Functions", "label": "invokes"},
            {"from": "Lambda Functions", "to": "PostgreSQL", "label": "extracts data"},
            {
                "from": "Lambda Functions",
                "to": "Supplier API",
                "label": "calls and processes",
            },
            {
                "from": "Lambda Functions",
                "to": "S3 Bucket (CSV)",
                "label": "reads and processes",
            },
            {"from": "Lambda Functions", "to": "Redshift", "label": "loads data"},
            {
                "from": "Lambda Functions",
                "to": "S3 Bucket (Staging)",
                "label": "stores transformed data",
            },
            {
                "from": "Data Analyst",
                "to": "Redshift",
                "label": "queries and generates reports",
            },
            {
                "from": "Tableau",
                "to": "Redshift",
                "label": "connects for visualizations",
            },
            {"from": "IT Team", "to": "AWS", "label": "monitors and manages"},
        ],
    }

    visualizer = DiagramVisualiser(data)
    visualizer.render("test-image")
    print(
        "Visualization complete. The diagram has been saved and should open automatically."
    )


if __name__ == "__main__":
    main()
