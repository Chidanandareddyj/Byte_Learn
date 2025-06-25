#!/usr/bin/env python3
"""
Manim Video Generator
Converts JSON script to animated math videos using Manim
"""

import json
import sys
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any
import argparse

# Ensure MiKTeX is in PATH
miktex_path = os.path.expanduser(r"~\AppData\Local\Programs\MiKTeX\miktex\bin\x64")
if os.path.exists(miktex_path) and miktex_path not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + miktex_path

# Manim imports
from manim import *

# Configure Manim for better LaTeX handling
config.tex_template = TexTemplate()
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")
config.tex_template.add_to_preamble(r"\usepackage{amssymb}")
config.tex_template.add_to_preamble(r"\usepackage{amsfonts}")

class MathVideoScene(Scene):
    def __init__(self, script_data: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.script_data = script_data
        self.title = script_data.get('title', 'MathVideo')
        
        # Handle both old and new JSON structures
        if 'sections' in script_data:
            # New structure
            self.total_duration = script_data.get('totalDuration', 300)
            self.introduction = script_data.get('introduction', {})
            self.sections = script_data.get('sections', [])
            self.conclusion = script_data.get('conclusion', {})
            self.use_new_structure = True
        else:
            # Old structure for backward compatibility
            self.steps = script_data.get('steps', [])
            self.total_duration = script_data.get('duration', 300)
            self.use_new_structure = False
            
        self.current_time = 0
        self.active_mobjects = []  # Track objects to prevent cluttering
        
    def construct(self):
        """Main scene construction with perfect timing synchronization"""
        
        # Create and show title briefly
        title_text = self.title.replace('_', ' ').replace('  ', ' ')
        title = Text(title_text, font_size=44, color=BLUE, weight=BOLD)
        title.move_to(ORIGIN)
        
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)
        self.current_time += 4
        
        if self.use_new_structure:
            # New structure: Introduction → Sections → Conclusion
            if self.introduction:
                self.render_introduction()
            
            for i, section in enumerate(self.sections):
                self.render_section(section, i)
                
            if self.conclusion:
                self.render_conclusion()
        else:
            # Old structure: Steps
            self.render_legacy_steps()
            
        # Final pause to reach exact duration
        remaining_time = max(0, self.total_duration - self.current_time)
        if remaining_time > 0:
            self.wait(remaining_time)
    
    def clear_scene(self):
        """Clear active objects to prevent cluttering"""
        if self.active_mobjects:
            self.play(*[FadeOut(mob) for mob in self.active_mobjects], run_time=0.5)
            self.active_mobjects.clear()
    
    def add_to_scene(self, mobject):
        """Add object to scene and track it"""
        self.active_mobjects.append(mobject)
        return mobject
    
    def render_legacy_steps(self):
        """Render old-style steps for backward compatibility"""
        for i, step in enumerate(self.steps):
            text_content = step.get('text', '')
            math_content = step.get('math', '')
            step_duration = step.get('duration', 20)
            
            # Clear previous content
            if i > 0:
                self.clear_scene()
            
            # Show text
            if text_content:
                text_obj = Text(text_content, font_size=32, color=WHITE)
                text_obj.to_edge(UP, buff=1)
                self.add_to_scene(text_obj)
                self.play(Write(text_obj), run_time=1.5)
            
            # Show math
            if math_content:
                try:
                    cleaned_math = self.clean_latex(math_content)
                    math_obj = MathTex(cleaned_math, font_size=44, color=WHITE)
                    math_obj.move_to(ORIGIN)
                    self.add_to_scene(math_obj)
                    self.play(Write(math_obj), run_time=2)
                    self.play(Indicate(math_obj, color=BLUE), run_time=1)
                except Exception as e:
                    print(f"Math error: {e}")
                    fallback = Text(f"Math: {math_content}", font_size=28, color=BLUE)
                    fallback.move_to(ORIGIN)
                    self.add_to_scene(fallback)
                    self.play(Write(fallback), run_time=1.5)
            
            # Wait for remaining time
            used_time = 4.5 if text_content and math_content else 3 if text_content or math_content else 1
            remaining = max(0.5, step_duration - used_time)
            self.wait(remaining)
            self.current_time += step_duration
        """Render introduction with timing control"""
        intro = self.introduction
        intro_text = intro.get('text', '')
        duration = intro.get('duration', 30)
        
        if intro_text:
            # Create centered introduction text
            intro_obj = Text(intro_text, font_size=36, color=WHITE)
            intro_obj.move_to(ORIGIN)
            
            self.play(Write(intro_obj), run_time=2)
            self.wait(duration - 4)  # Account for write and fade time
            self.play(FadeOut(intro_obj), run_time=2)
            
        self.current_time += duration
    
    def render_section(self, section: Dict[str, Any], section_index: int):
        """Render section with synchronized visuals and timing - NO CLUTTERING"""
        
        section_title = section.get('title', f'Section {section_index + 1}')
        duration = section.get('duration', 45)
        visual_sequence = section.get('visualSequence', [])
        
        print(f"Rendering section: {section_title} (Duration: {duration}s)")
        
        # Clear any previous content at start of section
        if section_index > 0 or self.current_time > 4:  # Don't clear after title
            self.clear_scene()
        
        section_start_time = 0
        
        # Process each visual element with precise timing
        for i, visual in enumerate(visual_sequence):
            # Clear previous visual before showing new one to prevent overlap
            if i > 0:
                self.clear_scene()
            
            self.render_visual_element(visual, section_start_time)
            
        # Final wait to complete section duration
        self.current_time += duration
    
    def render_visual_element(self, visual: Dict[str, Any], section_start: float):
        """Render individual visual element with exact timing - CLEAN DISPLAY"""
        
        visual_type = visual.get('type', '')
        content = visual.get('content', '')
        timing = visual.get('timing', [0, 10])
        start_time, end_time = timing
        
        # Calculate display duration
        display_duration = min(end_time - start_time, 15)  # Cap at 15s to prevent too long displays
        
        if visual_type == "text_display":
            self.show_text_display(content, display_duration)
            
        elif visual_type == "math_equation":
            self.show_math_equation(content, display_duration)
            
        elif visual_type == "graph_plot":
            self.show_graph_plot(content, display_duration)
            
        elif visual_type == "step_by_step":
            self.show_step_by_step(content, display_duration)
            
        elif visual_type == "highlight_parts":
            self.show_highlight_parts(content, display_duration)
            
        elif visual_type == "real_world_example":
            self.show_real_world_example(content, display_duration)
        else:
            # Fallback for unknown types
            self.show_text_display(content, display_duration)
    
    def show_text_display(self, content: str, duration: float):
        """Display text with controlled timing - CLEAN LAYOUT"""
        text_obj = Text(content, font_size=36, color=WHITE)
        text_obj.move_to(ORIGIN)
        self.add_to_scene(text_obj)
        
        animate_time = min(1.5, duration * 0.3)
        hold_time = max(1, duration - animate_time)
        
        self.play(Write(text_obj), run_time=animate_time)
        self.wait(hold_time)
    
    def show_math_equation(self, content: str, duration: float):
        """Display math equation with highlighting - CENTERED"""
        try:
            cleaned_math = self.clean_latex(content)
            math_obj = MathTex(cleaned_math, font_size=48, color=WHITE)
            math_obj.move_to(ORIGIN)
            self.add_to_scene(math_obj)
            
            animate_time = min(2, duration * 0.4)
            hold_time = max(1, duration - animate_time - 1)
            
            self.play(Write(math_obj), run_time=animate_time)
            if hold_time > 0:
                self.wait(hold_time)
            self.play(Indicate(math_obj, color=BLUE), run_time=1)
            
        except Exception as e:
            print(f"Math rendering error: {e}")
            fallback = Text(f"Equation: {content}", font_size=32, color=BLUE)
            fallback.move_to(ORIGIN)
            self.add_to_scene(fallback)
            self.play(Write(fallback), run_time=duration * 0.5)
            self.wait(duration * 0.5)
    
    def show_graph_plot(self, content: str, duration: float):
        """Display coordinate system and function plot - FOCUSED"""
        try:
            # Create clean, centered axes
            axes = Axes(
                x_range=[-4, 4, 1],
                y_range=[-3, 3, 1],
                x_length=8,
                y_length=6,
                axis_config={"color": BLUE, "stroke_width": 2},
            )
            axes.move_to(ORIGIN)
            self.add_to_scene(axes)
            
            # Add minimal labels
            labels = axes.get_axis_labels(x_label="x", y_label="y")
            self.add_to_scene(labels)
            
            # Animate axes creation
            axes_time = min(2, duration * 0.4)
            self.play(Create(axes), Write(labels), run_time=axes_time)
            
            # Add function based on content
            if "quadratic" in content.lower() or "parabola" in content.lower():
                func = axes.plot(lambda x: 0.2 * x**2, color=YELLOW, x_range=[-3, 3])
            elif "linear" in content.lower():
                func = axes.plot(lambda x: 0.5 * x, color=GREEN, x_range=[-3, 3])
            elif "sin" in content.lower():
                func = axes.plot(lambda x: np.sin(x), color=RED, x_range=[-3, 3])
            else:
                func = axes.plot(lambda x: x, color=ORANGE, x_range=[-3, 3])
            
            self.add_to_scene(func)
            func_time = min(2, duration * 0.4)
            remaining_time = max(0.5, duration - axes_time - func_time)
            
            self.play(Create(func), run_time=func_time)
            self.wait(remaining_time)
                
        except Exception as e:
            print(f"Graph error: {e}")
            fallback = Text("Graph visualization", font_size=32, color=YELLOW)
            fallback.move_to(ORIGIN)
            self.add_to_scene(fallback)
            self.play(Write(fallback), run_time=duration)
    
    def show_step_by_step(self, content: str, duration: float):
        """Show step-by-step breakdown - SEQUENTIAL"""
        steps = content.split('|') if '|' in content else [content]
        step_duration = max(2, duration / len(steps))
        
        for i, step in enumerate(steps):
            # Clear previous step
            if i > 0:
                self.clear_scene()
                
            step_text = Text(f"Step {i+1}: {step.strip()}", font_size=28, color=WHITE)
            step_text.move_to(ORIGIN)
            self.add_to_scene(step_text)
            
            self.play(Write(step_text), run_time=min(1.5, step_duration * 0.5))
            self.wait(max(0.5, step_duration - 1.5))
    
    def show_highlight_parts(self, content: str, duration: float):
        """Highlight parts of equations or concepts - SELECTIVE"""
        try:
            # Create the main equation
            main_eq = MathTex(self.clean_latex(content), font_size=44, color=WHITE)
            main_eq.move_to(ORIGIN)
            self.add_to_scene(main_eq)
            
            write_time = min(2, duration * 0.3)
            self.play(Write(main_eq), run_time=write_time)
            
            # Highlight different parts if we have time
            remaining_time = duration - write_time
            if remaining_time > 2 and len(main_eq) > 1:
                highlight_time = min(1, remaining_time / len(main_eq))
                for part in main_eq[:3]:  # Limit to first 3 parts to avoid cluttering
                    self.play(Indicate(part, color=YELLOW), run_time=highlight_time)
            else:
                self.wait(remaining_time)
                    
        except Exception as e:
            print(f"Highlight error: {e}")
            fallback = Text("Concept breakdown", font_size=32, color=YELLOW)
            fallback.move_to(ORIGIN)
            self.add_to_scene(fallback)
            self.play(Write(fallback), run_time=duration)
    
    def show_real_world_example(self, content: str, duration: float):
        """Show real-world application - CLEAR PRESENTATION"""
        title_text = Text("Real-world application:", font_size=32, color=GREEN, weight=BOLD)
        title_text.to_edge(UP, buff=1.5)
        self.add_to_scene(title_text)
        
        content_text = Text(content, font_size=28, color=WHITE)
        content_text.move_to(ORIGIN)
        self.add_to_scene(content_text)
        
        title_time = min(1, duration * 0.3)
        content_time = min(1.5, duration * 0.4)
        wait_time = max(0.5, duration - title_time - content_time)
        
        self.play(Write(title_text), run_time=title_time)
        self.play(Write(content_text), run_time=content_time)
        self.wait(wait_time)
    
    def render_introduction(self):
        """Render introduction section"""
        intro = self.introduction
        intro_text = intro.get('text', '')
        duration = intro.get('duration', 30)
        
        if intro_text:
            # Create centered introduction text
            intro_obj = Text(intro_text, font_size=36, color=WHITE)
            intro_obj.move_to(ORIGIN)
            self.add_to_scene(intro_obj)
            
            self.play(Write(intro_obj), run_time=2)
            self.wait(max(1, duration - 4))  # Account for write and fade time
            
        self.current_time += duration
    
    def render_conclusion(self):
        """Render conclusion section"""
        # Clear previous content
        self.clear_scene()
        
        conclusion = self.conclusion
        conclusion_text = conclusion.get('text', '')
        duration = conclusion.get('duration', 20)
        
        if conclusion_text:
            conclusion_obj = Text(conclusion_text, font_size=32, color=BLUE, weight=BOLD)
            conclusion_obj.move_to(ORIGIN)
            self.add_to_scene(conclusion_obj)
            
            self.play(Write(conclusion_obj), run_time=2)
            self.wait(max(1, duration - 2))
            
        self.current_time += duration
    
    def clean_latex(self, latex_str: str) -> str:
        """Clean LaTeX string for Manim compatibility"""
        # Remove markdown math delimiters
        latex_str = latex_str.replace('$$', '')
        latex_str = latex_str.replace('$', '')
        
        # Remove double backslashes that might cause issues
        latex_str = latex_str.replace('\\\\', '\\')
        
        # Common LaTeX fixes for Manim
        latex_str = latex_str.replace('\\text{', '\\mathrm{')
        latex_str = latex_str.replace('\\pm', '\\pm ')
        
        # Handle common math functions
        latex_str = latex_str.replace('\\sin', '\\sin ')
        latex_str = latex_str.replace('\\cos', '\\cos ')
        latex_str = latex_str.replace('\\tan', '\\tan ')
        latex_str = latex_str.replace('\\log', '\\log ')
        latex_str = latex_str.replace('\\ln', '\\ln ')
        
        # Handle common symbols
        latex_str = latex_str.replace('infinity', '\\infty')
        latex_str = latex_str.replace('∞', '\\infty')
        latex_str = latex_str.replace('±', '\\pm')
        latex_str = latex_str.replace('≤', '\\leq')
        latex_str = latex_str.replace('≥', '\\geq')
        latex_str = latex_str.replace('≠', '\\neq')
        latex_str = latex_str.replace('→', '\\to')
        latex_str = latex_str.replace('∈', '\\in')
        latex_str = latex_str.replace('∀', '\\forall')
        latex_str = latex_str.replace('∃', '\\exists')
        
        # Clean up extra spaces
        import re
        latex_str = re.sub(r'\s+', ' ', latex_str).strip()
        
        return latex_str


def setup_manim_environment():
    """Setup proper environment for Manim with LaTeX"""
    # Ensure MiKTeX is in PATH
    miktex_path = os.path.expanduser(r"~\AppData\Local\Programs\MiKTeX\miktex\bin\x64")
    if os.path.exists(miktex_path) and miktex_path not in os.environ['PATH']:
        os.environ['PATH'] += os.pathsep + miktex_path
        print(f"Added MiKTeX to PATH: {miktex_path}")
    
    # Create media directory if it doesn't exist
    media_dir = Path("./media")
    media_dir.mkdir(exist_ok=True)
    
    return True


def generate_video_from_json(json_data: Dict[str, Any], output_path: str, audio_path: str = None) -> bool:
    """
    Generate video from JSON script data
    
    Args:
        json_data: Script data dictionary
        output_path: Where to save the video
        audio_path: Optional audio file path
        
    Returns:
        bool: Success status
    """
    try:
        # Setup environment
        setup_manim_environment()
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create scene file
            scene_file = temp_path / "generated_scene.py"
            
            # Generate Python scene code
            scene_code = generate_scene_code(json_data)
            
            with open(scene_file, 'w', encoding='utf-8') as f:
                f.write(scene_code)
            
            # Run Manim to generate video
            cmd = [
                "manim",
                "-ql",  # Low quality for faster rendering (removed -p to prevent auto-opening)
                "--disable_caching",  # Disable caching to prevent file locks
                str(scene_file),
                "MathVideoScene"
            ]
            
            print(f"Running Manim command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_dir)
            
            if result.returncode != 0:
                print(f"Manim error: {result.stderr}")
                return False
            
            print("Manim rendering completed successfully")
            
            # Find generated video
            media_dir = temp_path / "media" / "videos" / "generated_scene" / "480p15"
            video_files = list(media_dir.glob("*.mp4"))
            
            if not video_files:
                print("No video file generated")
                return False
            
            generated_video = video_files[0]
            print(f"Found generated video: {generated_video}")
            
            # Wait a moment to ensure file is released
            import time
            time.sleep(2)
            
            # If audio is provided, combine audio and video
            if audio_path and os.path.exists(audio_path):
                print("Combining video with audio...")
                final_output = combine_audio_video(str(generated_video), audio_path, output_path)
                return final_output
            else:
                # Just copy the video
                print("Copying video without audio...")
                import shutil
                shutil.copy2(generated_video, output_path)
                return True
                
    except Exception as e:
        print(f"Error generating video: {e}")
        return False


def generate_scene_code(json_data: Dict[str, Any]) -> str:
    """Generate Python code for Manim scene - SIMPLIFIED APPROACH"""
    
    # Use the new structure approach - delegate to class-based scene
    code = f'''#!/usr/bin/env python3
import json
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from manim import *
import numpy as np

# Configure Manim for better LaTeX handling
config.tex_template = TexTemplate()
config.tex_template.add_to_preamble(r"\\usepackage{{amsmath}}")
config.tex_template.add_to_preamble(r"\\usepackage{{amssymb}}")
config.tex_template.add_to_preamble(r"\\usepackage{{amsfonts}}")

# Script data
script_data = {json.dumps(json_data, indent=2)}

class MathVideoScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.script_data = script_data
        self.title = script_data.get('title', 'MathVideo')
        
        # Handle both old and new JSON structures
        if 'sections' in script_data:
            # New structure
            self.total_duration = script_data.get('totalDuration', 300)
            self.introduction = script_data.get('introduction', {{}})
            self.sections = script_data.get('sections', [])
            self.conclusion = script_data.get('conclusion', {{}})
            self.use_new_structure = True
        else:
            # Old structure for backward compatibility
            self.steps = script_data.get('steps', [])
            self.total_duration = script_data.get('duration', 300)
            self.use_new_structure = False
            
        self.current_time = 0
        self.active_mobjects = []  # Track objects to prevent cluttering
    
    def construct(self):
        """Main scene construction with perfect timing synchronization"""
        
        # Create and show title briefly
        title_text = self.title.replace('_', ' ').replace('  ', ' ')
        title = Text(title_text, font_size=44, color=BLUE, weight=BOLD)
        title.move_to(ORIGIN)
        
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)
        self.current_time += 4
        
        if self.use_new_structure:
            # New structure: Introduction → Sections → Conclusion
            if self.introduction:
                self.render_introduction()
            
            for i, section in enumerate(self.sections):
                self.render_section(section, i)
                
            if self.conclusion:
                self.render_conclusion()
        else:
            # Old structure: Steps
            self.render_legacy_steps()
            
        # Final pause to reach exact duration
        remaining_time = max(0, self.total_duration - self.current_time)
        if remaining_time > 0:
            self.wait(remaining_time)
    
    def clear_scene(self):
        """Clear active objects to prevent cluttering"""
        if self.active_mobjects:
            self.play(*[FadeOut(mob) for mob in self.active_mobjects], run_time=0.5)
            self.active_mobjects.clear()
    
    def add_to_scene(self, mobject):
        """Add object to scene and track it"""
        self.active_mobjects.append(mobject)
        return mobject
    
    def render_introduction(self):
        """Render introduction section"""
        intro = self.introduction
        intro_text = intro.get('text', '')
        duration = intro.get('duration', 30)
        
        if intro_text:
            intro_obj = Text(intro_text, font_size=36, color=WHITE)
            intro_obj.move_to(ORIGIN)
            self.add_to_scene(intro_obj)
            
            self.play(Write(intro_obj), run_time=2)
            self.wait(max(1, duration - 4))
            
        self.current_time += duration
    
    def render_section(self, section, section_index):
        """Render section with synchronized visuals"""
        
        section_title = section.get('title', f'Section {{section_index + 1}}')
        duration = section.get('duration', 45)
        visual_sequence = section.get('visualSequence', [])
        
        print(f"Rendering section: {{section_title}} (Duration: {{duration}}s)")
        
        # Clear any previous content at start of section
        if section_index > 0 or self.current_time > 4:
            self.clear_scene()
        
        # Process each visual element
        for i, visual in enumerate(visual_sequence):
            # Clear previous visual before showing new one
            if i > 0:
                self.clear_scene()
            
            self.render_visual_element(visual)
            
        self.current_time += duration
    
    def render_visual_element(self, visual):
        """Render individual visual element"""
        
        visual_type = visual.get('type', '')
        content = visual.get('content', '')
        timing = visual.get('timing', [0, 10])
        start_time, end_time = timing
        
        display_duration = min(end_time - start_time, 15)
        
        if visual_type == "text_display":
            self.show_text_display(content, display_duration)
            
        elif visual_type == "math_equation":
            self.show_math_equation(content, display_duration)
            
        elif visual_type == "graph_plot":
            self.show_graph_plot(content, display_duration)
            
        elif visual_type == "step_by_step":
            self.show_step_by_step(content, display_duration)
            
        elif visual_type == "highlight_parts":
            self.show_highlight_parts(content, display_duration)
            
        elif visual_type == "real_world_example":
            self.show_real_world_example(content, display_duration)
        else:
            self.show_text_display(content, display_duration)
    
    def show_text_display(self, content, duration):
        """Display text cleanly"""
        text_obj = Text(content, font_size=36, color=WHITE)
        text_obj.move_to(ORIGIN)
        self.add_to_scene(text_obj)
        
        animate_time = min(1.5, duration * 0.3)
        hold_time = max(1, duration - animate_time)
        
        self.play(Write(text_obj), run_time=animate_time)
        self.wait(hold_time)
    
    def show_math_equation(self, content, duration):
        """Display math equation"""
        try:
            cleaned_math = self.clean_latex(content)
            math_obj = MathTex(cleaned_math, font_size=48, color=WHITE)
            math_obj.move_to(ORIGIN)
            self.add_to_scene(math_obj)
            
            animate_time = min(2, duration * 0.4)
            hold_time = max(1, duration - animate_time - 1)
            
            self.play(Write(math_obj), run_time=animate_time)
            if hold_time > 0:
                self.wait(hold_time)
            self.play(Indicate(math_obj, color=BLUE), run_time=1)
            
        except Exception as e:
            print(f"Math rendering error: {{e}}")
            fallback = Text(f"Equation: {{content}}", font_size=32, color=BLUE)
            fallback.move_to(ORIGIN)
            self.add_to_scene(fallback)
            self.play(Write(fallback), run_time=duration * 0.5)
            self.wait(duration * 0.5)
    
    def show_graph_plot(self, content, duration):
        """Display graph"""
        try:
            axes = Axes(
                x_range=[-4, 4, 1],
                y_range=[-3, 3, 1],
                x_length=8,
                y_length=6,
                axis_config={{"color": BLUE, "stroke_width": 2}},
            )
            axes.move_to(ORIGIN)
            self.add_to_scene(axes)
            
            labels = axes.get_axis_labels(x_label="x", y_label="y")
            self.add_to_scene(labels)
            
            axes_time = min(2, duration * 0.4)
            self.play(Create(axes), Write(labels), run_time=axes_time)
            
            # Add function based on content
            if "quadratic" in content.lower() or "parabola" in content.lower():
                func = axes.plot(lambda x: 0.2 * x**2, color=YELLOW, x_range=[-3, 3])
            elif "linear" in content.lower():
                func = axes.plot(lambda x: 0.5 * x, color=GREEN, x_range=[-3, 3])
            elif "sin" in content.lower():
                func = axes.plot(lambda x: np.sin(x), color=RED, x_range=[-3, 3])
            else:
                func = axes.plot(lambda x: x, color=ORANGE, x_range=[-3, 3])
            
            self.add_to_scene(func)
            func_time = min(2, duration * 0.4)
            remaining_time = max(0.5, duration - axes_time - func_time)
            
            self.play(Create(func), run_time=func_time)
            self.wait(remaining_time)
                
        except Exception as e:
            print(f"Graph error: {{e}}")
            fallback = Text("Graph visualization", font_size=32, color=YELLOW)
            fallback.move_to(ORIGIN)
            self.add_to_scene(fallback)
            self.play(Write(fallback), run_time=duration)
    
    def show_step_by_step(self, content, duration):
        """Show steps sequentially"""
        steps = content.split('|') if '|' in content else [content]
        step_duration = max(2, duration / len(steps))
        
        for i, step in enumerate(steps):
            if i > 0:
                self.clear_scene()
                
            step_text = Text(f"Step {{i+1}}: {{step.strip()}}", font_size=28, color=WHITE)
            step_text.move_to(ORIGIN)
            self.add_to_scene(step_text)
            
            self.play(Write(step_text), run_time=min(1.5, step_duration * 0.5))
            self.wait(max(0.5, step_duration - 1.5))
    
    def show_highlight_parts(self, content, duration):
        """Highlight equation parts"""
        try:
            main_eq = MathTex(self.clean_latex(content), font_size=44, color=WHITE)
            main_eq.move_to(ORIGIN)
            self.add_to_scene(main_eq)
            
            write_time = min(2, duration * 0.3)
            self.play(Write(main_eq), run_time=write_time)
            
            remaining_time = duration - write_time
            if remaining_time > 2 and len(main_eq) > 1:
                highlight_time = min(1, remaining_time / len(main_eq))
                for part in main_eq[:3]:
                    self.play(Indicate(part, color=YELLOW), run_time=highlight_time)
            else:
                self.wait(remaining_time)
                    
        except Exception as e:
            print(f"Highlight error: {{e}}")
            fallback = Text("Concept breakdown", font_size=32, color=YELLOW)
            fallback.move_to(ORIGIN)
            self.add_to_scene(fallback)
            self.play(Write(fallback), run_time=duration)
    
    def show_real_world_example(self, content, duration):
        """Show real-world application"""
        title_text = Text("Real-world application:", font_size=32, color=GREEN, weight=BOLD)
        title_text.to_edge(UP, buff=1.5)
        self.add_to_scene(title_text)
        
        content_text = Text(content, font_size=28, color=WHITE)
        content_text.move_to(ORIGIN)
        self.add_to_scene(content_text)
        
        title_time = min(1, duration * 0.3)
        content_time = min(1.5, duration * 0.4)
        wait_time = max(0.5, duration - title_time - content_time)
        
        self.play(Write(title_text), run_time=title_time)
        self.play(Write(content_text), run_time=content_time)
        self.wait(wait_time)
    
    def render_conclusion(self):
        """Render conclusion"""
        self.clear_scene()
        
        conclusion = self.conclusion
        conclusion_text = conclusion.get('text', '')
        duration = conclusion.get('duration', 20)
        
        if conclusion_text:
            conclusion_obj = Text(conclusion_text, font_size=32, color=BLUE, weight=BOLD)
            conclusion_obj.move_to(ORIGIN)
            self.add_to_scene(conclusion_obj)
            
            self.play(Write(conclusion_obj), run_time=2)
            self.wait(max(1, duration - 2))
            
        self.current_time += duration
    
    def render_legacy_steps(self):
        """Render old-style steps"""
        for i, step in enumerate(self.steps):
            text_content = step.get('text', '')
            math_content = step.get('math', '')
            step_duration = step.get('duration', 20)
            
            if i > 0:
                self.clear_scene()
            
            if text_content:
                text_obj = Text(text_content, font_size=32, color=WHITE)
                text_obj.to_edge(UP, buff=1)
                self.add_to_scene(text_obj)
                self.play(Write(text_obj), run_time=1.5)
            
            if math_content:
                try:
                    cleaned_math = self.clean_latex(math_content)
                    math_obj = MathTex(cleaned_math, font_size=44, color=WHITE)
                    math_obj.move_to(ORIGIN)
                    self.add_to_scene(math_obj)
                    self.play(Write(math_obj), run_time=2)
                    self.play(Indicate(math_obj, color=BLUE), run_time=1)
                except Exception as e:
                    print(f"Math error: {{e}}")
                    fallback = Text(f"Math: {{math_content}}", font_size=28, color=BLUE)
                    fallback.move_to(ORIGIN)
                    self.add_to_scene(fallback)
                    self.play(Write(fallback), run_time=1.5)
            
            used_time = 4.5 if text_content and math_content else 3 if text_content or math_content else 1
            remaining = max(0.5, step_duration - used_time)
            self.wait(remaining)
            self.current_time += step_duration
    
    def clean_latex(self, latex_str):
        """Clean LaTeX for Manim"""
        latex_str = latex_str.replace('$$', '').replace('$', '')
        latex_str = latex_str.replace('\\\\\\\\', '\\\\')
        latex_str = latex_str.replace('\\\\text{{', '\\\\mathrm{{')
        latex_str = latex_str.replace('\\\\pm', '\\\\pm ')
        return latex_str.strip()
'''
    
    return code


def combine_audio_video(video_path: str, audio_path: str, output_path: str) -> bool:
    """
    Combine video and audio using FFmpeg
    
    Args:
        video_path: Path to video file
        audio_path: Path to audio file
        output_path: Path for combined output
        
    Returns:
        bool: Success status
    """
    try:
        # Wait to ensure video file is completely written
        import time
        time.sleep(1)
        
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            "-y",  # Overwrite output file
            output_path
        ]
        
        print(f"Combining audio and video: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            # Try without audio mapping if it fails
            print("Trying without audio mapping...")
            simple_cmd = [
                "ffmpeg",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                "-y",
                output_path
            ]
            result = subprocess.run(simple_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"FFmpeg simple command also failed: {result.stderr}")
                return False
            
        print("Audio and video combined successfully")
        return True
        
    except Exception as e:
        print(f"Error combining audio and video: {e}")
        return False


def test_latex_rendering():
    """Test function to check if LaTeX is rendering properly"""
    try:
        # Test basic LaTeX expressions
        test_expressions = [
            "x^2 + y^2 = z^2",
            "\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            "\\sum_{i=1}^{n} x_i",
            "\\int_{0}^{\\infty} e^{-x} dx"
        ]
        
        for expr in test_expressions:
            try:
                math_obj = MathTex(expr)
                print(f"✅ LaTeX '{expr}' rendered successfully")
            except Exception as e:
                print(f"❌ LaTeX '{expr}' failed: {e}")
                
        return True
    except Exception as e:
        print(f"❌ Error testing LaTeX: {e}")
        return False


def main():
    """Main function for command line usage"""
    # Setup environment first
    setup_manim_environment()
    
    parser = argparse.ArgumentParser(description='Generate Manim video from JSON script')
    parser.add_argument('--json', required=True, help='Path to JSON script file')
    parser.add_argument('--output', required=True, help='Output video path')
    parser.add_argument('--audio', help='Optional audio file path')
    
    args = parser.parse_args()
    
    # Load JSON data
    with open(args.json, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Generate video
    success = generate_video_from_json(json_data, args.output, args.audio)
    
    if success:
        print("Video generated successfully: " + args.output)
        sys.exit(0)
    else:
        print("Failed to generate video")
        sys.exit(1)


if __name__ == "__main__":
    main()
