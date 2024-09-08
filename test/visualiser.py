from ai_architect.visualiser import DiagramVisualiser


def main():
    data = {
        "groups": [
            {"name": "Microsoft Azure", "type": "cloud_provider"},
            {"name": "Data Sources", "type": "data_source"},
            {"name": "User Group", "type": "user_group"},
        ],
        "components": [
            {
                "name": "POS System",
                "type": "csv_data",
                "group": "Data Sources",
                "image": "database.png",
            },
            {
                "name": "Online Store",
                "type": "sql_database",
                "group": "Data Sources",
                "image": "database.png",
            },
            {
                "name": "CRM System",
                "type": "api",
                "group": "Data Sources",
                "image": "api.png",
            },
            {
                "name": "Azure Data Factory",
                "type": "data_extraction_loading",
                "group": "Microsoft Azure",
                "image": "azure-data-factory.png",
            },
            {
                "name": "Azure Blob Storage",
                "type": "raw_data_storage",
                "group": "Microsoft Azure",
                "image": "azure-blob-storage.png",
            },
            {
                "name": "Azure Synapse Analytics",
                "type": "data_warehouse",
                "group": "Microsoft Azure",
                "image": "azure-synapse-analytics.png",
            },
            {
                "name": "Azure Data Lake Analytics",
                "type": "data_processing",
                "group": "Microsoft Azure",
                "image": "azure-data-lake-analytics.png",
            },
            {
                "name": "Power BI",
                "type": "reporting_dashboard",
                "group": "Microsoft Azure",
                "image": "power-bi.png",
            },
            {
                "name": "Azure Active Directory",
                "type": "user_authentication",
                "group": "Microsoft Azure",
                "image": "azure-active-directory.png",
            },
            {
                "name": "Azure Monitor",
                "type": "system_monitoring",
                "group": "Microsoft Azure",
                "image": "azure-monitor.png",
            },
            {
                "name": "Sales Team",
                "type": "user_role",
                "group": "User Group",
                "image": "user.png",
            },
            {
                "name": "Marketing Team",
                "type": "user_role",
                "group": "User Group",
                "image": "user.png",
            },
            {
                "name": "Management",
                "type": "user_role",
                "group": "User Group",
                "image": "admin.png",
            },
        ],
        "connections": [
            {
                "from": "POS System",
                "to": "Azure Data Factory",
                "label": "Data extraction",
            },
            {
                "from": "Online Store",
                "to": "Azure Data Factory",
                "label": "Data extraction",
            },
            {
                "from": "CRM System",
                "to": "Azure Data Factory",
                "label": "Data extraction",
            },
            {
                "from": "Azure Data Factory",
                "to": "Azure Blob Storage",
                "label": "Data loading",
            },
            {
                "from": "Azure Blob Storage",
                "to": "Azure Data Lake Analytics",
                "label": "Data processing",
            },
            {
                "from": "Azure Data Lake Analytics",
                "to": "Azure Synapse Analytics",
                "label": "Data transformation",
            },
            {
                "from": "Azure Synapse Analytics",
                "to": "Power BI",
                "label": "Data source for reporting",
            },
            {
                "from": "Sales Team",
                "to": "Power BI",
                "label": "Report/dashboard access",
            },
            {
                "from": "Marketing Team",
                "to": "Power BI",
                "label": "Report/dashboard access",
            },
            {
                "from": "Management",
                "to": "Power BI",
                "label": "Report/dashboard access",
            },
        ],
    }
    visualizer = DiagramVisualiser(data)
    visualizer.render("test-image")
    print(
        "Visualization complete. The diagram has been saved and should open automatically."
    )


if __name__ == "__main__":
    main()
