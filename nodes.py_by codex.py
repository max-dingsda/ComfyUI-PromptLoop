"""
ComfyUI-PromptLoop
Batch-Verarbeitung von Prompts aus Textdateien
"""

import os
import folder_paths
import nodes


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
@@ -112,41 +113,87 @@ class PromptLoopFromText:
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


class PromptLoopSaveImage:
    """
    Speichert Bilder wie die Standard-"Save Image"-Node, ergänzt jedoch
    explizit den verwendeten Prompt in den Bild-Metadaten.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "prompt": ("STRING", {"forceInput": True}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "hidden": {"extra_pnginfo": "EXTRA_PNGINFO"},
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ()
    FUNCTION = "save_images"
    CATEGORY = "promptloop"

    def save_images(self, images, prompt, filename_prefix="ComfyUI", extra_pnginfo=None):
        """
        Nutzt die bestehende SaveImage-Implementierung von ComfyUI, fügt
        aber den Prompt zuverlässig in die PNG-Metadaten ein.
        """

        # Ensure the prompt is explicitly present in the metadata even when
        # the upstream nodes provide it as a plain string (instead of the
        # usual prompt object ComfyUI derives from the workflow JSON).
        pnginfo = (extra_pnginfo or {}).copy()
        if prompt is not None:
            pnginfo.setdefault("prompt", prompt)

        saver = nodes.SaveImage()
        return saver.save_images(
            images=images,
            filename_prefix=filename_prefix,
            prompt=prompt,
            extra_pnginfo=pnginfo,
        )


# Node-Registrierung
NODE_CLASS_MAPPINGS = {
    "PromptLoopFromFile": PromptLoopFromFile,
    "PromptLoopFromText": PromptLoopFromText,
    "PromptLoopInfo": PromptLoopInfo,
    "PromptLoopSaveImage": PromptLoopSaveImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptLoopFromFile": "🔄 Prompt Loop (File)",
    "PromptLoopFromText": "🔄 Prompt Loop (Text)",
    "PromptLoopInfo": "ℹ️ Prompt Loop Info",
    "PromptLoopSaveImage": "💾 Prompt Loop Save Image",
}