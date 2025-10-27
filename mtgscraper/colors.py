"""
Terminal Gradient & Color Utilities
Beautiful gradient text and shading effects using ANSI escape codes
"""

import re


class Colors:
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Standard foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    @staticmethod
    def rgb(r, g, b):
        """Generate 24-bit RGB foreground color code."""
        return f'\033[38;2;{r};{g};{b}m'
    
    @staticmethod
    def bg_rgb(r, g, b):
        """Generate 24-bit RGB background color code."""
        return f'\033[48;2;{r};{g};{b}m'


def strip_ansi(text):
    """Remove ANSI color codes from text to get actual content."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def visible_length(text):
    """Get the visible length of text (excluding ANSI codes)."""
    return len(strip_ansi(text))


def gradient_text(text, start_color, end_color):
    """
    Apply a smooth gradient effect to text.
    
    Args:
        text: String to apply gradient to
        start_color: Tuple of (R, G, B) for starting color (0-255)
        end_color: Tuple of (R, G, B) for ending color (0-255)
    
    Returns:
        String with ANSI color codes applied
    
    Example:
        gradient_text("HELLO", (0, 255, 255), (200, 0, 255))
        # Cyan to Purple gradient
    """
    if len(text) == 0:
        return text
    
    result = []
    length = len(text)
    
    for i, char in enumerate(text):
        # Calculate interpolated color
        ratio = i / max(length - 1, 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        
        result.append(f'{Colors.rgb(r, g, b)}{char}')
    
    result.append(Colors.RESET)
    return ''.join(result)


def multi_gradient(text, colors):
    """Create gradient through multiple color stops."""
    if len(text) == 0 or len(colors) < 2:
        return text
    
    result = []
    length = len(text)
    num_transitions = len(colors) - 1
    chars_per_transition = length / num_transitions
    
    for i, char in enumerate(text):
        # Determine which color transition we're in
        transition_idx = min(int(i / chars_per_transition), num_transitions - 1)
        start_color = colors[transition_idx]
        end_color = colors[transition_idx + 1]
        
        # Calculate position within this transition
        local_pos = (i - transition_idx * chars_per_transition) / chars_per_transition
        
        r = int(start_color[0] + (end_color[0] - start_color[0]) * local_pos)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * local_pos)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * local_pos)
        
        result.append(f'{Colors.rgb(r, g, b)}{char}')
    
    result.append(Colors.RESET)
    return ''.join(result)


def center_colored_text(colored_text, box_width):
    """Center text accounting for ANSI color codes."""
    visible_len = visible_length(colored_text)
    total_padding = box_width - visible_len
    left_pad = total_padding // 2
    right_pad = total_padding - left_pad
    
    return f"{' ' * left_pad}{colored_text}{' ' * right_pad}"


# Predefined gradient schemes
def cyber_gradient(text):
    """Cyan to Blue gradient (tech/modern)"""
    return gradient_text(text, (0, 255, 255), (0, 100, 255))


def fire_gradient(text):
    """Yellow to Red gradient (fire effect)"""
    return gradient_text(text, (255, 255, 0), (255, 0, 0))


def ocean_gradient(text):
    """Blue to Cyan gradient (ocean)"""
    return gradient_text(text, (0, 119, 190), (0, 180, 216))


def purple_gradient(text):
    """Blue to Purple gradient (premium)"""
    return gradient_text(text, (0, 150, 255), (200, 0, 255))


def green_gradient(text):
    """Green to Cyan gradient (success/growth)"""
    return gradient_text(text, (100, 255, 100), (100, 200, 255))


def sunset_gradient(text):
    """Orange to Red gradient (sunset)"""
    return gradient_text(text, (255, 94, 77), (255, 165, 0))


def magic_gradient(text):
    """Purple to Pink gradient (magical)"""
    return gradient_text(text, (138, 43, 226), (255, 0, 255))


def rainbow_gradient(text):
    """Full rainbow effect"""
    return multi_gradient(text, [
        (255, 0, 0),      # Red
        (255, 127, 0),    # Orange
        (255, 255, 0),    # Yellow
        (0, 255, 0),      # Green
        (0, 0, 255),      # Blue
        (75, 0, 130),     # Indigo
        (148, 0, 211)     # Violet
    ])
