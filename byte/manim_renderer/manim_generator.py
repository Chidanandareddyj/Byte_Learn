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
        self.steps = script_data.get('steps', [])
        self.narration = script_data.get('narration', '')
        
    def construct(self):
        """Main scene construction based on JSON script"""
        
        # Create title with better formatting
        title_text = self.title.replace('_', ' ').replace('  ', ' ')
        title = Text(title_text, font_size=40, color=BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        # Animate title
        self.play(Write(title), run_time=2)
        self.wait(1.5)
        
        # Process each step
        for i, step in enumerate(self.steps):
            self.render_step(step, i)
            
        # Final pause with title still visible
        self.wait(3)
    
    def render_step(self, step: Dict[str, Any], step_index: int):
        """Render individual step with text and math"""
        
        # Get step data
        text_content = step.get('text', '')
        math_content = step.get('math', '')
        
        # Create text element if present
        if text_content:
            text_obj = Text(text_content, font_size=32, color=WHITE)
            text_obj.move_to(UP * 1.5)
            self.play(Write(text_obj), run_time=1.5)
            self.wait(1)
        
        # Create math element if present
        if math_content:
            try:
                # Clean LaTeX for Manim
                cleaned_math = self.clean_latex(math_content)
                print(f"Rendering math: {cleaned_math}")  # Debug output
                
                # Create MathTex object with proper LaTeX
                math_obj = MathTex(cleaned_math, font_size=44, color=WHITE)
                math_obj.move_to(DOWN * 1)
                
                # Animate the math appearance
                self.play(Write(math_obj), run_time=2)
                self.wait(1.5)
                
                # Animate transformation if it's an equation
                if '=' in cleaned_math:
                    self.animate_equation(math_obj, cleaned_math)
                else:
                    # Just highlight for non-equations
                    self.play(Indicate(math_obj, color=BLUE), run_time=1)
                    
            except Exception as e:
                print(f"Error rendering math '{math_content}': {e}")
                # Fallback to text with better formatting
                fallback_text = Text(f"Math: {math_content}", font_size=28, color=BLUE)
                fallback_text.move_to(DOWN * 1)
                self.play(Write(fallback_text), run_time=1.5)
                self.wait(1)
        
        # Clear screen for next step (except last step)
        if step_index < len(self.steps) - 1:
            self.play(*[FadeOut(mob) for mob in self.mobjects])
            self.wait(0.5)
    
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
        
        # Handle fractions better
        latex_str = latex_str.replace('\\frac', '\\frac')
        
        # Handle common math functions
        latex_str = latex_str.replace('\\sin', '\\sin ')
        latex_str = latex_str.replace('\\cos', '\\cos ')
        latex_str = latex_str.replace('\\tan', '\\tan ')
        latex_str = latex_str.replace('\\log', '\\log ')
        latex_str = latex_str.replace('\\ln', '\\ln ')
        
        # Ensure proper spacing around operators
        latex_str = latex_str.replace('=', ' = ')
        latex_str = latex_str.replace('+', ' + ')
        latex_str = latex_str.replace('-', ' - ')
        latex_str = latex_str.replace('*', ' \\cdot ')
        
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
    
    def animate_equation(self, math_obj: MathTex, equation: str):
        """Animate equation transformations"""
        try:
            # Simple highlighting animation
            self.play(Indicate(math_obj, color=BLUE))
            self.wait(1)
            
            # If it's a simple equation, try to show step-by-step
            if '=' in equation and '+' in equation:
                # Highlight different parts
                for i in range(len(math_obj)):
                    if i < len(math_obj):
                        self.play(Indicate(math_obj[i], color=BLUE))
                        self.wait(0.5)
                        
        except Exception as e:
            print(f"Animation error: {e}")
            # Just highlight the whole equation
            self.play(Indicate(math_obj, color=GREEN))


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
    """Generate Python code for Manim scene"""
    
    title = json_data.get('title', 'MathVideo')
    steps = json_data.get('steps', [])
    
    # Build scene code
    code = f'''#!/usr/bin/env python3
from manim import *

class MathVideoScene(Scene):
    def construct(self):
        # Title with better formatting
        title_text = "{title.replace('_', ' ').replace('  ', ' ')}"
        title = Text(title_text, font_size=40, color=BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1.5)
        
'''
    
    # Add steps
    for i, step in enumerate(steps):
        text_content = step.get('text', '').replace('"', '\\"')
        math_content = step.get('math', '')
        
        if text_content:
            code += f'''
        # Step {i+1}: Text
        text_{i} = Text("{text_content}", font_size=32, color=WHITE)
        text_{i}.move_to(UP * 1.5)
        self.play(Write(text_{i}), run_time=1.5)
        self.wait(1)
'''
        
        if math_content:
            # Clean and prepare math content for LaTeX
            cleaned_math = math_content.replace('\\\\', '\\\\\\\\').replace('"', '\\"')
            # Remove $ symbols and clean up
            cleaned_math = cleaned_math.replace('$', '').strip()
            
            code += f'''
        # Step {i+1}: Math
        try:
            # Render LaTeX math equation
            math_{i} = MathTex(r"{cleaned_math}", font_size=44, color=WHITE)
            math_{i}.move_to(DOWN * 1)
            self.play(Write(math_{i}), run_time=2)
            self.wait(1.5)
            
            # Highlight the equation
            self.play(Indicate(math_{i}, color=BLUE), run_time=1)
            self.wait(1)
        except Exception as e:
            print(f"Math rendering error: {{e}}")
            # Fallback to text
            fallback_{i} = Text("Math: {cleaned_math}", font_size=28, color=BLUE)
            fallback_{i}.move_to(DOWN * 1)
            self.play(Write(fallback_{i}), run_time=1.5)
            self.wait(1)
'''
        
        # Clear screen for next step
        if i < len(steps) - 1:
            code += f'''
        # Clear for next step
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)
'''
    
    code += '''
        # Final pause with title still visible
        self.wait(3)
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
