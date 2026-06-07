import matplotlib.pyplot as plt
from typing import List
from mathematical_structure import SyntacticObject, LexicalItem, Workspace

def draw_tree(so: SyntacticObject, ax, x=0, y=0, dx=1, dy=1):
    """Draws a binary tree on a 2D plane."""
    if isinstance(so, LexicalItem):
        ax.text(x, y, str(so), bbox=dict(boxstyle="circle", fc="white", ec="black"), ha='center')
        return

    # internal ndoe
    ax.plot(x, y, 'ko', markersize=4)
    
    # children
    left, right = so.elements
    
    # left branch
    ax.plot([x, x - dx], [y, y - dy], 'k-')
    draw_tree(left, ax, x - dx, y - dy, dx/2, dy)
    
    # right branch
    ax.plot([x, x + dx], [y, y - dy], 'k-')
    draw_tree(right, ax, x + dx, y - dy, dx/2, dy)

def visualize(ws_list: List[Workspace]):
    """Display the WS forest structure at each step of the derivation."""
    fig, axes = plt.subplots(1, len(ws_list), figsize=(5 * len(ws_list), 5))
    if len(ws_list) == 1: axes = [axes]
    
    for i, (ws, ax) in enumerate(zip(ws_list, axes)):
        ax.set_title(f"Step {i}: $\sigma$={ws.sigma}")
        ax.set_xlim(-4, 4)
        ax.set_ylim(-3, 1)
        ax.axis('off')
        
        # seperate SOs in WS
        spacing = 8 / (len(ws.items) + 1)
        for j, item in enumerate(ws.items):
            draw_tree(item, ax, x=-4 + (j + 1) * spacing, y=0)
    plt.tight_layout()
    plt.show()