import matplotlib.pyplot as plt
import networkx as nx


def draw_binary_tree():
    G = nx.DiGraph()

    # Initial nodes for the horizontal line series before the root
    initial_nodes = ["FF1", "FF2", "FF3",  "FF4"]
    for idx, node in enumerate(initial_nodes[:-1]):
        G.add_edge(node, initial_nodes[idx + 1])

    pos = {node: (idx * 0.06, 0) for idx, node in enumerate(initial_nodes)}
    labels = {node: node for node in initial_nodes}

    horizontal_edge_values = ["PF1", "PF2", "PF3"]
    edge_labels = {(initial_nodes[idx], initial_nodes[idx + 1]): val for idx, val in enumerate(horizontal_edge_values)}

    queue = [("FF4", 0, 0, '')]
    node_count = len(initial_nodes)

    s_counter = 1
    path_labels = {}

    while queue:
        current, depth, vpos, path = queue.pop(0)

        if depth < 6:
            top = node_count
            bottom = node_count + 1

            G.add_edge(current, top)
            G.add_edge(current, bottom)

            top_path = path + '0'
            bottom_path = path + '1'

            if depth == 5:
                labels[top] = 'S' + str(s_counter)
                path_labels[top] = top_path
                s_counter += 1
                labels[bottom] = 'S' + str(s_counter)
                edge_labels[(current, top)] = 'PF19'
                edge_labels[(current, bottom)] = 'PF20, PF21'
                path_labels[bottom] = bottom_path
                s_counter += 1
            else:
                labels[top] = 'FF' + str(4 + depth + 1)
                labels[bottom] = 'FF' + str(4 + depth + 1)

                edge_label_mapping = {
                    'FF5': (('PF4', 'PF5, PF6')),
                    'FF6': (('PF7', 'PF8, PF9')),
                    'FF7': (('PF10', 'PF11, PF12')),
                    'FF8': (('PF13', 'PF14, PF15')),
                    'FF9': (('PF16', 'PF17, PF18'))
                }

                label_bottom = labels[bottom]
                if label_bottom in edge_label_mapping:
                    edge_labels[(current, top)], edge_labels[(current, bottom)] = edge_label_mapping[label_bottom]

            v_spacing = 5 * (0.5 / (2 ** (depth + 1)))

            if depth == 0:
                next_depth_x = 0.15 + (1 / 20)
            else:
                next_depth_x = 0.15 + (depth * (1 / 10))

            pos[top] = (next_depth_x, vpos - v_spacing)
            pos[bottom] = (next_depth_x, vpos + v_spacing)

            queue.append((top, depth + 1, vpos - v_spacing, top_path))
            queue.append((bottom, depth + 1, vpos + v_spacing, bottom_path))

            node_count += 2

    plt.figure(figsize=(90, 150))
    nx.draw(G, pos, labels=labels, font_size=80, font_weight='bold', with_labels=True, arrows=True, node_size=14000,
            node_color='skyblue', width=7.5, edge_color='black', arrowstyle='-', arrowsize=30)

    for (src, dest), label in edge_labels.items():
        x_src, y_src = pos[src]
        x_dest, y_dest = pos[dest]

        # Calculate the midpoint.
        x_label = 0.6 * x_src + 0.42 * x_dest

        # Determine the direction of the arrow (upwards or downwards).
        if y_dest > y_src:
            # Arrow is pointing upwards.
            y_label = 0.6 * y_src + 0.4 * y_dest + 0.02  # adjust the vertical offset value as needed
        else:
            # Arrow is pointing downwards.
            y_label = 0.6 * y_src + 0.4 * y_dest - 0.05  # adjust the vertical offset value as needed

        plt.annotate(label, (x_label, y_label), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=80,
                    )

    plt.title('Binary Decision Tree for Variables PF6 to PF12 with Initial Nodes')
    plt.savefig("binary_tree_family_1.png")


draw_binary_tree()
