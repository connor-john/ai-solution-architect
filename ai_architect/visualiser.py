from graphviz import Digraph
import os
import hashlib


class DiagramVisualiser:
    def __init__(self, diagram_data):
        self.diagram_data = diagram_data
        self.dot = Digraph(comment="System Architecture")
        self.dot.attr(rankdir="LR", size="12,8", dpi="300", compound="true")
        self.image_dir = "./images"
        self.available_images = self.get_available_images()
        self.icon_size = 0.8  # in inches

    def get_available_images(self):
        return [f.lower() for f in os.listdir(self.image_dir) if f.endswith(".png")]

    def get_best_matching_image(self, component_name, component_type):
        search_terms = f"{component_name} {component_type}".lower().split()
        best_match = max(
            self.available_images,
            key=lambda img: sum(term in img.lower() for term in search_terms),
            default=None,
        )
        return best_match

    def add_component_node(self, graph, component, group_name):
        node_id = f"{group_name}_{component['name']}".replace(" ", "_")
        image_name = self.get_best_matching_image(component["name"], component["type"])

        if image_name:
            image_path = os.path.join(self.image_dir, image_name)
            graph.node(
                node_id,
                label="",
                image=image_path,
                shape="none",
                imagescale="true",
                width=str(self.icon_size),
                height=str(self.icon_size),
            )
            graph.node(
                f"{node_id}_label", label=component["name"], shape="none", fontsize="10"
            )
            graph.edge(node_id, f"{node_id}_label", style="invis")
        else:
            graph.node(
                node_id,
                label=component["name"],
                shape="box",
                style="filled",
                fillcolor="lightgray",
                fontcolor="black",
            )

        return node_id

    def add_components(self):
        groups = {group["name"]: group for group in self.diagram_data["groups"]}
        node_map = {}

        for group_name, group in groups.items():
            with self.dot.subgraph(name=f"cluster_{group_name}") as c:
                c.attr(label=group["name"], style="dashed", color="gray")
                group_components = [
                    comp
                    for comp in self.diagram_data["components"]
                    if comp["group"] == group_name
                ]
                for component in group_components:
                    node_id = self.add_component_node(c, component, group_name)
                    node_map[component["name"]] = node_id

        ungrouped = [
            comp
            for comp in self.diagram_data["components"]
            if comp["group"] not in groups
        ]
        for component in ungrouped:
            node_id = self.add_component_node(self.dot, component, "ungrouped")
            node_map[component["name"]] = node_id

        return node_map

    def add_connections(self, node_map):
        for connection in self.diagram_data["connections"]:
            from_id = node_map.get(connection["from"])
            to_id = node_map.get(connection["to"])

            if from_id and to_id:
                self.dot.edge(from_id, to_id, label=connection["label"])
            else:
                print(
                    f"Warning: Could not create connection from '{connection['from']}' to '{connection['to']}'"
                )

    def generate(self):
        node_map = self.add_components()
        self.add_connections(node_map)
        return self.dot

    def render(self, filename="system_architecture"):
        self.generate()
        self.dot.render(filename, view=True, format="png", cleanup=True)
