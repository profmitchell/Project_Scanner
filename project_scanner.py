import tkinter as tk
from tkinter import filedialog, ttk
import os
import json
from datetime import datetime
import markdown
from pathlib import Path
import math

class ProjectScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Friendly Project Scanner")
        self.root.geometry("700x500")
        
        # Supported file extensions
        self.supported_extensions = {
            'js': 'JavaScript',
            'jsx': 'React JavaScript',
            'ts': 'TypeScript',
            'tsx': 'React TypeScript',
            'css': 'CSS',
            'scss': 'SCSS',
            'html': 'HTML',
            'json': 'JSON',
            'md': 'Markdown',
            'py': 'Python',
            'env': 'Environment Variables',
            'gitignore': 'Git Ignore',
            'yml': 'YAML',
            'yaml': 'YAML',
            'package.json': 'Package JSON',
            'next.config.js': 'Next.js Config',
            'tailwind.config.js': 'Tailwind Config',
            'three.js': 'Three.js'
        }
        
        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', padding=10)
        style.configure('TButton', padding=5)
        style.configure('TRadiobutton', padding=2)
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Directory selection
        self.select_button = ttk.Button(
            self.main_frame, 
            text="Select Project Directory",
            command=self.select_directory,
            width=25
        )
        self.select_button.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Selected directory label
        self.dir_label = ttk.Label(self.main_frame, text="No directory selected", wraplength=500)
        self.dir_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Export format frame
        format_frame = ttk.LabelFrame(self.main_frame, text="Export Format", padding=10)
        format_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.format_var = tk.StringVar(value="md")
        formats = [
            ("Markdown (.md) - Best for AI reading", "md"),
            ("Text (.txt) - Simple format", "txt"),
            ("JSON (.json) - Structured data", "json")
        ]
        
        for i, (text, value) in enumerate(formats):
            ttk.Radiobutton(
                format_frame,
                text=text,
                variable=self.format_var,
                value=value
            ).grid(row=i, column=0, pady=2, sticky=tk.W)
        
        # Splitting options frame
        split_frame = ttk.LabelFrame(self.main_frame, text="File Splitting Options", padding=10)
        split_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(split_frame, text="Number of parts:").grid(row=0, column=0, padx=5)
        self.split_var = tk.StringVar(value="1")
        self.split_entry = ttk.Spinbox(
            split_frame,
            from_=1,
            to=10,
            width=5,
            textvariable=self.split_var
        )
        self.split_entry.grid(row=0, column=1, padx=5)
        ttk.Label(split_frame, text="(1 = no splitting, max 10)").grid(row=0, column=2, padx=5)
        
        # Scan button
        self.scan_button = ttk.Button(
            self.main_frame,
            text="Scan and Export",
            command=self.scan_and_export,
            state="disabled",
            width=25
        )
        self.scan_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.main_frame,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="", wraplength=500)
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.selected_directory = None

    def select_directory(self):
        """Handle directory selection"""
        self.selected_directory = filedialog.askdirectory()
        if self.selected_directory:
            self.dir_label.config(text=f"Selected: {self.selected_directory}")
            self.scan_button.config(state="normal")
    
    def read_file_content(self, file_path):
        """Read and return file content with error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            return "[Binary file or encoding not supported]"
        except Exception as e:
            return f"[Error reading file: {str(e)}]"
    
    def scan_directory(self, directory):
        """Scan directory and return structure with file contents"""
        structure = {
            "name": os.path.basename(directory),
            "path": directory,
            "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "directories": [],
            "files": [],
            "ai_summary": "This is a project structure document created for AI analysis. "
                         "The content is organized hierarchically with full file contents included."
        }
        
        for root, dirs, files in os.walk(directory):
            # Skip node_modules and .git directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '.next', 'dist', 'build']]
            
            rel_path = os.path.relpath(root, directory)
            if rel_path == '.':
                current_dir = structure
            else:
                current_dir = self._get_or_create_dir(structure, rel_path)
            
            for file in files:
                file_path = os.path.join(root, file)
                ext = file.split('.')[-1] if '.' in file else ''
                
                if ext in self.supported_extensions or file in self.supported_extensions:
                    content = self.read_file_content(file_path)
                    current_dir["files"].append({
                        "name": file,
                        "type": self.supported_extensions.get(ext, "Unknown"),
                        "content": content,
                        "size": os.path.getsize(file_path)
                    })
        
        return structure
    
    def _get_or_create_dir(self, structure, path):
        """Helper function to get or create nested directory structure"""
        current = structure
        parts = path.split(os.sep)
        
        for part in parts:
            found = False
            for dir_dict in current["directories"]:
                if dir_dict["name"] == part:
                    current = dir_dict
                    found = True
                    break
            
            if not found:
                new_dir = {
                    "name": part,
                    "directories": [],
                    "files": []
                }
                current["directories"].append(new_dir)
                current = new_dir
        
        return current
    
    def split_content(self, content, num_parts):
        """Split content into approximately equal parts"""
        if num_parts <= 1:
            return [content]
            
        # Split by lines to avoid breaking in middle of content
        lines = content.splitlines()
        total_lines = len(lines)
        lines_per_part = math.ceil(total_lines / num_parts)
        
        parts = []
        for i in range(0, total_lines, lines_per_part):
            part = '\n'.join(lines[i:i + lines_per_part])
            if i == 0:  # Add header to first part
                parts.append(f"# Part 1 of {num_parts}\n\n{part}")
            else:
                part_num = (i // lines_per_part) + 1
                parts.append(f"# Part {part_num} of {num_parts}\n\n{part}")
        
        return parts
    
    def generate_markdown(self, structure, level=0):
        """Generate markdown representation of the structure"""
        md = ""
        indent = "  " * level
        
        if level == 0:
            md += f"# Project Structure: {structure['name']}\n\n"
            md += f"Scan Date: {structure['scan_date']}\n\n"
            md += "## Directory Structure\n\n"
            md += "This document contains the complete codebase structure and contents for AI analysis.\n\n"
        
        # Add current directory files
        for file in structure["files"]:
            md += f"{indent}- 📄 **{file['name']}** ({file['type']}, {self.format_size(file['size'])})\n"
            if file['content']:
                md += f"{indent}  ```{file['type'].lower()}\n{file['content']}\n  ```\n\n"
        
        # Recursively add subdirectories
        for directory in structure["directories"]:
            md += f"{indent}- 📁 **{directory['name']}/**\n"
            md += self.generate_markdown(directory, level + 1)
        
        return md
    
    def format_size(self, size):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}GB"
    
    def generate_text(self, structure, level=0):
        """Generate plain text representation of the structure"""
        text = ""
        indent = "  " * level
        
        if level == 0:
            text += f"Project Structure: {structure['name']}\n"
            text += f"Scan Date: {structure['scan_date']}\n\n"
            text += "Directory Structure:\n\n"
        
        for file in structure["files"]:
            text += f"{indent}[FILE] {file['name']} ({file['type']}, {self.format_size(file['size'])})\n"
            if file['content']:
                text += f"{indent}Content:\n{indent}---\n{file['content']}\n{indent}---\n\n"
        
        for directory in structure["directories"]:
            text += f"{indent}[DIR] {directory['name']}/\n"
            text += self.generate_text(directory, level + 1)
        
        return text
    
    def scan_and_export(self):
        """Perform the scan and export operation"""
        if not self.selected_directory:
            return
        
        try:
            num_parts = int(self.split_var.get())
            if num_parts < 1 or num_parts > 10:
                self.status_label.config(text="Please enter a number between 1 and 10 for splitting.")
                return
        except ValueError:
            self.status_label.config(text="Please enter a valid number for splitting.")
            return
        
        self.status_label.config(text="Scanning directory...")
        self.progress["value"] = 0
        self.root.update()
        
        # Scan directory
        structure = self.scan_directory(self.selected_directory)
        self.progress["value"] = 50
        self.root.update()
        
        # Prepare output
        dir_name = os.path.basename(self.selected_directory)
        export_format = self.format_var.get()
        
        try:
            if export_format == "md":
                content = self.generate_markdown(structure)
            elif export_format == "txt":
                content = self.generate_text(structure)
            elif export_format == "json":
                content = json.dumps(structure, indent=2)
            
            # Split content if needed
            contents = self.split_content(content, num_parts)
            
            # Create output directory
            output_dir = os.path.join(self.selected_directory, f"{dir_name}_structure")
            os.makedirs(output_dir, exist_ok=True)
            
            # Save parts
            for i, part_content in enumerate(contents):
                if num_parts > 1:
                    output_file = os.path.join(output_dir, f"{dir_name}_part{i+1}.{export_format}")
                else:
                    output_file = os.path.join(output_dir, f"{dir_name}.{export_format}")
                    
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(part_content)
            
            self.progress["value"] = 100
            if num_parts > 1:
                self.status_label.config(
                    text=f"Export complete! {num_parts} files saved in: {os.path.basename(output_dir)}"
                )
            else:
                self.status_label.config(
                    text=f"Export complete! File saved in: {os.path.basename(output_dir)}"
                )
        except Exception as e:
            self.status_label.config(text=f"Error during export: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectScannerApp(root)
    root.mainloop()