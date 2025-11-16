"""
ComfyUI-PromptLoop
Batch-Verarbeitung von Prompts aus Textdateien
"""

import os
import folder_paths


class PromptLoopFromFile:
    """
    Liest eine Textdatei und gibt jeden Prompt einzeln aus.
    Perfekt für Batch-Generierung: Ein Queue-Auftrag → Viele Bilder
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
        
        return {
            "required": {
                "file": (sorted(files), {"default": "prompts.txt"}),
            },
            "optional": {
                "start_index": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "max_prompts": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "execute"
    CATEGORY = "promptloop"

    def execute(self, file, start_index=0, max_prompts=0):
        """
        Liest die Textdatei und gibt alle Prompts als Liste zurück.
        ComfyUI wird automatisch für jeden Eintrag die nachfolgenden Nodes ausführen.
        """
        input_dir = folder_paths.get_input_directory()
        file_path = os.path.join(input_dir, file)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
        # Datei lesen
        with open(file_path, 'r', encoding='utf-8') as f:
            prompts = [line.strip() for line in f if line.strip()]
        
        # Optionale Filter anwenden
        if start_index > 0:
            prompts = prompts[start_index:]
        
        if max_prompts > 0:
            prompts = prompts[:max_prompts]
        
        if not prompts:
            raise ValueError("Keine Prompts in der Datei gefunden!")
        
        print(f"[PromptLoop] Geladen: {len(prompts)} Prompts aus {file}")
        
        return (prompts,)


class PromptLoopFromText:
    """
    Nimmt einen mehrzeiligen Text und gibt jeden Prompt einzeln aus.
    Alternative zu File-Input für schnelles Testen.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "prompt 1\nprompt 2\nprompt 3"}),
            },
            "optional": {
                "start_index": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "max_prompts": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "execute"
    CATEGORY = "promptloop"

    def execute(self, text, start_index=0, max_prompts=0):
        """
        Teilt den Text in einzelne Zeilen und gibt sie als Liste zurück.
        """
        prompts = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Optionale Filter anwenden
        if start_index > 0:
            prompts = prompts[start_index:]
        
        if max_prompts > 0:
            prompts = prompts[:max_prompts]
        
        if not prompts:
            raise ValueError("Keine Prompts im Text gefunden!")
        
        print(f"[PromptLoop] Verarbeite: {len(prompts)} Prompts")
        
        return (prompts,)


class PromptLoopInfo:
    """
    Zeigt Information über die aktuelle Batch-Verarbeitung.
    Nützlich für Debugging und Dateinamen.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT", "INT",)
    RETURN_NAMES = ("prompt", "current_index", "total_count",)
    FUNCTION = "execute"
    CATEGORY = "promptloop"

    def execute(self, prompt):
        """
        Gibt den Prompt zusammen mit Index-Informationen zurück.
        """
        # In einer Liste gibt ComfyUI uns nur ein Element zur Zeit
        # Wir können den Index aus dem Execution Context holen
        
        return (prompt, 0, 1,)  # Simplified - würde in echter Implementierung erweitert


# Node-Registrierung
NODE_CLASS_MAPPINGS = {
    "PromptLoopFromFile": PromptLoopFromFile,
    "PromptLoopFromText": PromptLoopFromText,
    "PromptLoopInfo": PromptLoopInfo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptLoopFromFile": "🔄 Prompt Loop (File)",
    "PromptLoopFromText": "🔄 Prompt Loop (Text)",
    "PromptLoopInfo": "ℹ️ Prompt Loop Info",
}
