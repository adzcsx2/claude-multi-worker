"""
Multi-Instance Layout Manager for CMS

Handles grid layout calculation for multiple Claude instances.
Supports adaptive layouts: 2x2, 3x2, 4x2, etc.
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class GridLayout:
    """Grid layout specification"""
    rows: int
    cols: int
    positions: List[Tuple[int, int]]  # [(row, col), ...]

    def __str__(self) -> str:
        return f"{self.rows}x{self.cols}"


def calculate_grid_layout(instance_count: int) -> GridLayout:
    """
    Calculate optimal grid layout for given number of instances.

    Strategy:
    - 1 instance: 1x1
    - 2 instances: 1x2 (side by side)
    - 3 instances: 2x2 (top row: 2, bottom row: 1 centered)
    - 4 instances: 2x2
    - 5 instances: 3x2 (top: 3, bottom: 2)
    - 6 instances: 3x2
    - 7 instances: 4x2 (top: 4, bottom: 3)
    - 8 instances: 4x2
    - 9+ instances: 3x3, 4x3, etc.

    Args:
        instance_count: Number of Claude instances to layout

    Returns:
        GridLayout with rows, cols, and positions for each instance
    """
    if instance_count <= 0:
        return GridLayout(1, 1, [(0, 0)])

    if instance_count == 1:
        return GridLayout(1, 1, [(0, 0)])

    if instance_count == 2:
        # Side by side
        return GridLayout(1, 2, [(0, 0), (0, 1)])

    if instance_count <= 4:
        # 2x2 grid
        positions = [(i // 2, i % 2) for i in range(instance_count)]
        return GridLayout(2, 2, positions)

    if instance_count <= 6:
        # 3x2 grid
        positions = [(i // 2, i % 2) for i in range(instance_count)]
        return GridLayout(3, 2, positions)

    if instance_count <= 8:
        # 4x2 grid
        positions = [(i // 2, i % 2) for i in range(instance_count)]
        return GridLayout(4, 2, positions)

    # For 9+ instances, use roughly square grid
    import math
    cols = math.ceil(math.sqrt(instance_count))
    rows = math.ceil(instance_count / cols)
    positions = [(i // cols, i % cols) for i in range(instance_count)]
    return GridLayout(rows, cols, positions)


def get_pane_direction(grid: GridLayout, index: int) -> str:
    """
    Determine the direction to split a new pane based on grid layout.

    Args:
        grid: The grid layout
        index: Current pane index (0-based)

    Returns:
        "right" or "bottom" for splitting direction
    """
    if index == 0:
        return None  # First pane, no split needed

    row, col = grid.positions[index]

    # If we're starting a new row, split from the bottom of the first row
    if col == 0 and row > 0:
        return "bottom"
    else:
        return "right"


def get_pane_percent(grid: GridLayout, index: int, direction: str) -> int:
    """
    Calculate the size percentage for a pane based on grid layout.

    Args:
        grid: The grid layout
        index: Current pane index
        direction: Split direction ("right" or "bottom")

    Returns:
        Percentage (0-100) for pane size
    """
    if direction == "right":
        # Divide space evenly among columns
        return 100 // grid.cols
    else:  # bottom
        # Divide space evenly among rows
        return 100 // grid.rows


def format_layout_summary(grid: GridLayout) -> str:
    """Format a human-readable summary of the layout"""
    return f"{grid.rows}×{grid.cols} grid layout ({grid.rows} rows × {grid.cols} cols)"


# Example usage and testing
if __name__ == "__main__":
    print("Grid Layout Examples:")
    print("=" * 50)

    for count in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        layout = calculate_grid_layout(count)
        print(f"{count} instances: {layout}")
        print(f"  Positions: {layout.positions}")
        print()
