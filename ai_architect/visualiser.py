import os
import difflib
from graphviz import Digraph
import html


class DiagramVisualiser:
    def __init__(self, data, image_directory="images"):
        self.data = data
        self.image_directory = image_directory
        self.components = data["components"]
        self.connections = data["connections"]
        self.groups = data.get("groups", [])
        self.dot = Digraph(comment="Tech Diagram", format="png")
        self.component_dict = {comp["name"]: comp for comp in self.components}
        self.group_names = [group["name"] for group in self.groups]
        self.available_images = os.listdir(self.image_directory)
        self.group_invisible_nodes = {}  # Map group names to their invisible node IDs

        # Set consistent font attributes
        self.fontname = "Arial"
        self.fontsize = "10"
        self.fontcolor = "black"

    def find_image(self, component):
        # [Same as before]
        image_name = component.get("image", "")
        if image_name and image_name in self.available_images:
            return os.path.join(self.image_directory, image_name)
        else:
            possible_names = [
                component.get("image", ""),
                component.get("name", ""),
                component.get("type", ""),
            ]
            names_to_match = set()
            for name in possible_names:
                if not name:
                    continue
                words = name.lower().replace("-", " ").replace("_", " ").split()
                names_to_match.update(words)
            potential_filenames = []
            for name in names_to_match:
                potential_filenames.extend(
                    [f"{name}.png", f"{name}.jpg", f"{name}.svg"]
                )
            for filename in potential_filenames:
                if filename in self.available_images:
                    return os.path.join(self.image_directory, filename)
            image_basenames = [
                os.path.splitext(img)[0].lower() for img in self.available_images
            ]
            for name in names_to_match:
                matches = difflib.get_close_matches(name, image_basenames)
                if matches:
                    matched_index = image_basenames.index(matches[0])
                    matched_image = self.available_images[matched_index]
                    return os.path.join(self.image_directory, matched_image)
            return None

    def create_html_label(self, name, image_path=None):
        # Escape HTML special characters in the name
        name = html.escape(name)
        if image_path:
            # Build HTML-like label with image and text
            label = f"""<
<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">
    <TR><TD FIXEDSIZE="TRUE" WIDTH="80" HEIGHT="80"><IMG SRC="{image_path}" SCALE="TRUE"/></TD></TR>
    <TR><TD ALIGN="CENTER"><FONT POINT-SIZE="{self.fontsize}" FACE="{self.fontname}" COLOR="{self.fontcolor}">{name}</FONT></TD></TR>
</TABLE>
>"""
        else:
            # If no image, just use the name with font styling
            label = f"""<
<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">
    <TR><TD ALIGN="CENTER"><FONT POINT-SIZE="{self.fontsize}" FACE="{self.fontname}" COLOR="{self.fontcolor}">{name}</FONT></TD></TR>
</TABLE>
>"""
        return label

    def render(self, output_filename):
        # Set default graph attributes for consistency and compact layout
        self.dot.attr(
            "graph",
            fontname=self.fontname,
            fontsize=self.fontsize,
            fontcolor=self.fontcolor,
            nodesep="0.3",  # Reduce horizontal spacing between nodes
            ranksep="0.5",  # Reduce vertical spacing between nodes
            splines="ortho",  # Use orthogonal edge routing
        )
        self.dot.attr(
            "node",
            shape="plaintext",
            fontname=self.fontname,
            fontsize=self.fontsize,
            fontcolor=self.fontcolor,
        )
        self.dot.attr(
            "edge",
            fontname=self.fontname,
            fontsize=self.fontsize,
            fontcolor=self.fontcolor,
            penwidth="1.0",
        )

        # Set the layout direction (e.g., left-to-right)
        self.dot.attr(rankdir="LR")

        # Group components by their group
        grouped_components = {}
        for comp in self.components:
            group = comp.get("group")
            if group:
                grouped_components.setdefault(group, []).append(comp)
            else:
                grouped_components.setdefault("Ungrouped", []).append(comp)

        # Create subgraphs (clusters) for groups
        for group_index, (group_name, comps) in enumerate(grouped_components.items()):
            with self.dot.subgraph(name=f"cluster_{group_index}") as sub:
                # Set cluster attributes
                sub.attr(
                    label=group_name if group_name != "Ungrouped" else "",
                    fontsize=self.fontsize,
                    fontname=self.fontname,
                    fontcolor=self.fontcolor,
                    style="rounded",
                    color="gray",
                    penwidth="1",
                )

                # Create an invisible node to represent the group for edges
                if group_name != "Ungrouped":
                    group_node_id = f"group_invisible_{group_name}"
                    sub.node(
                        group_node_id,
                        label="",
                        shape="point",
                        width="0",
                        height="0",
                        style="invis",
                    )
                    self.group_invisible_nodes[group_name] = group_node_id

                for component in comps:
                    name = component["name"]
                    image_path = self.find_image(component)
                    label = self.create_html_label(name, image_path)
                    sub.node(
                        name,
                        label=label,
                    )

        # Add edges
        for conn in self.connections:
            from_node = conn["from"]
            to_node = conn["to"]
            label = conn.get("label", "")

            # Check if 'from_node' or 'to_node' is a group
            if from_node in self.group_names:
                from_node = self.group_invisible_nodes.get(from_node, from_node)
            if to_node in self.group_names:
                to_node = self.group_invisible_nodes.get(to_node, to_node)

            self.dot.edge(from_node, to_node, label=label)

        # Save and render the graph
        self.dot.render(output_filename, view=True)
