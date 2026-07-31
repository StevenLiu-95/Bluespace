"""
GetPath.py - Unreal Engine Python Script for Windows Path Selection
This script opens a Windows folder/file selection dialog and returns the selected path.
Designed to work with Editor Utility Widget.
"""

import unreal
import tkinter as tk
from tkinter import filedialog
import os


class PathSelector:
    """Handles path selection and communication with Unreal Editor Utility Widget."""
    
    _last_selected_path = None
    
    @staticmethod
    def get_folder_path(title="Select a Folder"):
        """
        Opens a Windows folder selection dialog.
        
        Args:
            title (str): The title of the dialog window
            
        Returns:
            str: The selected folder path, or empty string if cancelled
        """
        try:
            # Create a hidden root window for the file dialog
            root = tk.Tk()
            root.withdraw()  # Hide the window
            root.attributes('-topmost', True)  # Bring dialog to front
            
            # Open folder selection dialog
            folder_path = filedialog.askdirectory(title=title)
            
            root.destroy()
            
            # Store the path for retrieval
            PathSelector._last_selected_path = folder_path
            
            # Log to Unreal Editor Output
            if folder_path:
                unreal.log(f"[GetPath] Selected folder: {folder_path}")
            else:
                unreal.log("[GetPath] Folder selection cancelled")
            
            return folder_path
        
        except Exception as e:
            unreal.log_error(f"[GetPath] Error opening folder dialog: {str(e)}")
            return ""
    
    @staticmethod
    def get_file_path(title="Select a File", file_types="All Files (*.*)|*.*"):
        """
        Opens a Windows file selection dialog.
        
        Args:
            title (str): The title of the dialog window
            file_types (str): File type filter
            
        Returns:
            str: The selected file path, or empty string if cancelled
        """
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            # Open file selection dialog
            file_path = filedialog.askopenfilename(title=title)
            
            root.destroy()
            
            # Store the path for retrieval
            PathSelector._last_selected_path = file_path
            
            # Log to Unreal Editor Output
            if file_path:
                unreal.log(f"[GetPath] Selected file: {file_path}")
            else:
                unreal.log("[GetPath] File selection cancelled")
            
            return file_path
        
        except Exception as e:
            unreal.log_error(f"[GetPath] Error opening file dialog: {str(e)}")
            return ""
    
    @staticmethod
    def get_last_selected_path():
        """
        Returns the last selected path.
        Useful for retrieving the path in Editor Utility Widget.
        
        Returns:
            str: The last selected path
        """
        return PathSelector._last_selected_path if PathSelector._last_selected_path else ""


# Main execution functions for Editor Utility Widget buttons

def select_folder(title="Select a Folder"):
    """
    Main function to select a folder.
    Call this from Editor Utility Widget button event.
    
    Args:
        title (str): Dialog title
        
    Returns:
        str: Selected folder path
    """
    return PathSelector.get_folder_path(title)


def select_file(title="Select a File"):
    """
    Main function to select a file.
    Call this from Editor Utility Widget button event.
    
    Args:
        title (str): Dialog title
        
    Returns:
        str: Selected file path
    """
    return PathSelector.get_file_path(title)


def get_selected_path():
    """
    Get the last selected path.
    Call this to retrieve the path in Editor Utility Widget after selection.
    
    Returns:
        str: The last selected path
    """
    return PathSelector.get_last_selected_path()


# Auto-execution if script is run directly
if __name__ == "__main__":
    # Default: open folder selection dialog
    selected_path = select_folder("Select a Folder")
    print(f"Selected path: {selected_path}")
