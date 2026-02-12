import os
import importlib.util
from pathlib import Path

class SkillLoader:
    def __init__(self, skills_dir="safe_zone/skills"):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)

    def run_skill(self, prompt):
        """
        Scans for python files in skills_dir and attempts to execute them if they match the prompt.
        For simplicity, each skill script should have a list of 'KEYWORDS' and a 'run(prompt)' function.
        """
        for skill_file in self.skills_dir.glob("*.py"):
            skill_name = skill_file.stem
            spec = importlib.util.spec_from_file_location(skill_name, skill_file)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)

                # Check if the skill matches the prompt
                keywords = getattr(module, "KEYWORDS", [])
                if any(keyword.lower() in prompt.lower() for keyword in keywords):
                    if hasattr(module, "run"):
                        return module.run(prompt)
            except Exception as e:
                return f"Error executing skill '{skill_name}': {e}"

        return None # No skill matched
