# ComfyUI-PromptLoop

Batch processing of prompts from text files - One queue job for many images!

## Features

🔄 **Prompt Loop (File)** - Reads prompts from .txt files  
🔄 **Prompt Loop (Text)** - Processes multi-line text  
ℹ️ **Prompt Loop Info** - Shows index and counter  

## Installation

1. Copy this folder to `ComfyUI/custom_nodes/`
2. Restart ComfyUI
3. Nodes will appear under "promptloop" category

## Usage

1. Create a `prompts.txt` in the `input/` folder (one prompt per line)
2. Add the **Prompt Loop (File)** node
3. Connect the output to **CLIPTextEncode**
4. One queue job → All prompts will be processed!

## Options

- **start_index**: Skip the first X prompts
- **max_prompts**: Limit to X prompts (0 = all)

## Example

```
input/prompts.txt:
a beautiful sunset
a futuristic city
a cute cat

→ Generates 3 images with one queue job!
```

Ideation by max-dingsda, code by Claude-Sonnet
"# ComfyUI-PromptLoop" 
