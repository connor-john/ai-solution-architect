import pygame
import math
import os


class DiagramVisualiser:
    def __init__(self, data, width=1600, height=900):
        self.data = data
        self.width = width
        self.height = height
        self.padding = 40
        self.group_padding = 20
        self.component_size = 100
        self.font_size = 16
        self.colors = {
            "background": (240, 240, 240),
            "group": (220, 220, 220),
            "component": (200, 200, 200),
            "text": (60, 60, 60),
            "connection": (150, 150, 150),
        }

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tech Diagram Visualizer")
        self.font = pygame.font.Font(None, self.font_size)

        self.load_images()
        self.calculate_layout()

    def load_images(self):
        self.images = {}
        image_files = os.listdir("images")
        for component in self.data["components"]:
            image_found = False
            component_name = component["name"].lower().replace(" ", "-")
            component_type = component["type"].lower().replace(" ", "-")

            # Try to find an exact match first
            if f"{component_name}.png" in image_files:
                self.load_image(component["name"], f"{component_name}.png")
                image_found = True
            elif f"{component_type}.png" in image_files:
                self.load_image(component["name"], f"{component_type}.png")
                image_found = True

            # If no exact match, try partial matching
            if not image_found:
                for image_file in image_files:
                    if (
                        component_name in image_file.lower()
                        or component_type in image_file.lower()
                    ):
                        self.load_image(component["name"], image_file)
                        image_found = True
                        break

            # If still no match, try generic icons
            if not image_found:
                if "aws" in component_name or "aws" in component_type:
                    self.load_image(component["name"], "aws.png")
                elif "database" in component_type or "storage" in component_type:
                    self.load_image(component["name"], "database.png")
                elif "api" in component_type:
                    self.load_image(component["name"], "api.png")
                elif "role" in component_type or "user" in component_type:
                    self.load_image(component["name"], "user.png")
                else:
                    print(f"Could not find image for {component['name']}")

    def load_image(self, component_name, image_file):
        try:
            img = pygame.image.load(os.path.join("images", image_file))
            self.images[component_name] = pygame.transform.scale(
                img, (self.component_size, self.component_size)
            )
        except pygame.error:
            print(f"Error loading image for {component_name}")

    def calculate_layout(self):
        self.group_positions = {}
        self.component_positions = {}

        group_width = (self.width - self.padding * 2) / len(self.data["groups"])
        for i, group in enumerate(self.data["groups"]):
            self.group_positions[group["name"]] = (
                self.padding + i * group_width,
                self.padding,
                group_width - self.group_padding,
                self.height - self.padding * 2,
            )

        for group in self.data["groups"]:
            components = [
                c for c in self.data["components"] if c["group"] == group["name"]
            ]
            rows = math.ceil(math.sqrt(len(components)))
            cols = math.ceil(len(components) / rows)
            cell_width = (group_width - self.group_padding) / cols
            cell_height = (self.height - self.padding * 2 - self.group_padding) / rows

            for i, component in enumerate(components):
                row = i // cols
                col = i % cols
                self.component_positions[component["name"]] = (
                    self.group_positions[group["name"]][0]
                    + col * cell_width
                    + cell_width / 2,
                    self.group_positions[group["name"]][1]
                    + row * cell_height
                    + cell_height / 2
                    + self.group_padding,
                )

    def draw(self):
        self.screen.fill(self.colors["background"])

        # Draw groups
        for group, pos in self.group_positions.items():
            pygame.draw.rect(self.screen, self.colors["group"], pos, border_radius=10)
            text = self.font.render(group, True, self.colors["text"])
            self.screen.blit(text, (pos[0] + 10, pos[1] + 10))

        # Draw connections
        for conn in self.data["connections"]:
            start = self.get_connection_point(conn["from"])
            end = self.get_connection_point(conn["to"])
            if start and end:
                self.draw_connection(start, end, conn["label"])
            else:
                print(
                    f"Warning: Could not draw connection from {conn['from']} to {conn['to']}"
                )

        # Draw components
        for component in self.data["components"]:
            self.draw_component(component)

    def get_connection_point(self, name):
        if name in self.component_positions:
            return self.component_positions[name]
        elif name in self.group_positions:
            group_pos = self.group_positions[name]
            return (group_pos[0] + group_pos[2] / 2, group_pos[1] + group_pos[3] / 2)
        return None

    def draw_connection(self, start, end, label):
        pygame.draw.line(self.screen, self.colors["connection"], start, end, 2)

        # Draw arrow
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        arrow_size = 15
        pygame.draw.polygon(
            self.screen,
            self.colors["connection"],
            [
                (
                    end[0]
                    - arrow_size * math.cos(angle)
                    - arrow_size / 2 * math.sin(angle),
                    end[1]
                    - arrow_size * math.sin(angle)
                    + arrow_size / 2 * math.cos(angle),
                ),
                (
                    end[0]
                    - arrow_size * math.cos(angle)
                    + arrow_size / 2 * math.sin(angle),
                    end[1]
                    - arrow_size * math.sin(angle)
                    - arrow_size / 2 * math.cos(angle),
                ),
                end,
            ],
        )

        # Draw connection label
        mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        label_bg = self.font.render(label, True, self.colors["background"])
        label_fg = self.font.render(label, True, self.colors["text"])
        label_rect = label_bg.get_rect(center=mid)
        pygame.draw.rect(
            self.screen,
            self.colors["background"],
            label_rect.inflate(10, 10),
            border_radius=5,
        )
        self.screen.blit(label_fg, label_rect)

    def draw_component(self, component):
        pos = self.component_positions[component["name"]]
        if component["name"] in self.images:
            img = self.images[component["name"]]
            self.screen.blit(
                img, (pos[0] - img.get_width() / 2, pos[1] - img.get_height() / 2)
            )
        else:
            pygame.draw.rect(
                self.screen,
                self.colors["component"],
                (
                    pos[0] - self.component_size / 2,
                    pos[1] - self.component_size / 2,
                    self.component_size,
                    self.component_size,
                ),
                border_radius=10,
            )

        text = self.font.render(component["name"], True, self.colors["text"])
        text_rect = text.get_rect(
            center=(pos[0], pos[1] + self.component_size / 2 + 15)
        )
        pygame.draw.rect(
            self.screen,
            self.colors["background"],
            text_rect.inflate(10, 10),
            border_radius=5,
        )
        self.screen.blit(text, text_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw()
            pygame.display.flip()

        pygame.quit()

    def save_image(self, filename="tech_diagram.png"):
        self.draw()
        pygame.image.save(self.screen, filename)
        print(f"Diagram saved as {filename}")

    def render(self, filename="tech_diagram.png"):
        self.run()
        self.save_image(filename)
