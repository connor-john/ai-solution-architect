# llm_diagram_generator/visualizer.py

from graphviz import Digraph
import os
from difflib import get_close_matches
import colorsys


class DiagramVisualiser:
    def __init__(self, diagram_data):
        self.diagram_data = diagram_data
        self.dot = Digraph(comment="System Architecture")
        self.dot.attr(rankdir="LR", size="12,8", dpi="300", compound="true")
        self.image_dir = "./images"
        self.available_images = self.get_available_images()
        self.color_map = {}
        self.node_size = 1.5  # in inches, adjust as needed

    def get_available_images(self):
        return [f for f in os.listdir(self.image_dir) if f.endswith(".png")]

    def get_best_matching_image(self, component_name, component_type):
        # List of potential image names to try
        potential_names = [
            f"{component_name.lower().replace(' ', '-')}.png",
            f"{component_type.lower().replace(' ', '-')}.png",
            f"{component_name.split()[0].lower()}.png",
            f"{component_type.split()[0].lower()}.png",
        ]

        # Add cloud provider specific names
        for provider in ["aws", "azure", "gcp"]:
            if provider in component_name.lower() or provider in component_type.lower():
                potential_names.append(f"{provider}.png")
                break

        # Try exact matches first
        for name in potential_names:
            if name in self.available_images:
                return name

        # If no exact match, try fuzzy matching
        close_matches = get_close_matches(
            potential_names[0], self.available_images, n=1, cutoff=0.6
        )
        if close_matches:
            return close_matches[0]

        # Default fallback images
        if "database" in component_type.lower():
            return "database.png"
        elif "api" in component_type.lower():
            return "api.png"
        elif any(
            role in component_type.lower()
            for role in ["user", "team", "analyst", "customer"]
        ):
            return "user.png"

        # Return None for generic case, will be handled with colored nodes
        return None

    def get_color_for_type(self, component_type):
        if component_type not in self.color_map:
            hue = hash(component_type) % 360 / 360.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.95)
            self.color_map[component_type] = (
                f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            )
        return self.color_map[component_type]

    def add_component_node(self, graph, component):
        image_name = self.get_best_matching_image(component["name"], component["type"])
        if image_name:
            image_path = os.path.join(self.image_dir, image_name)
            graph.node(
                component["name"],
                label=component["name"],
                shape="none",
                image=image_path,
                imagescale="true",
                width=str(self.node_size),
                height=str(self.node_size),
            )
        else:
            color = self.get_color_for_type(component["type"])
            graph.node(
                component["name"],
                label=f"{component['name']}\n({component['type']})",
                shape="box",
                style="filled",
                fillcolor=color,
                fontcolor="black",
                width=str(self.node_size),
                height=str(self.node_size),
            )

    def add_components(self):
        groups = {group["name"]: group for group in self.diagram_data["groups"]}

        for group_name, group in groups.items():
            with self.dot.subgraph(name=f"cluster_{group_name}") as c:
                c.attr(label=group["name"], style="dashed", color="gray")

                group_components = [
                    comp
                    for comp in self.diagram_data["components"]
                    if comp["group"] == group_name
                ]
                for component in group_components:
                    self.add_component_node(c, component)

        # Add components not in any group
        ungrouped = [
            comp
            for comp in self.diagram_data["components"]
            if comp["group"] not in groups
        ]
        for component in ungrouped:
            self.add_component_node(self.dot, component)

    def add_connections(self):
        for connection in self.diagram_data["connections"]:
            self.dot.edge(
                connection["from"], connection["to"], label=connection["label"]
            )

    def generate(self):
        self.add_components()
        self.add_connections()
        return self.dot

    def render(self, filename="system_architecture"):
        self.generate()
        self.dot.render(filename, view=True, format="png", cleanup=True)
