import os
from typing import Tuple
import gradio

import facefusion.globals
from facefusion import logger
from facefusion.uis.core import get_ui_component
from facefusion.uis.components import output
from facefusion.filesystem import is_image, is_video


def render() -> None:
    global INPUT_FILE_MULTIPLE
    global OUTPUT_FILE_MULTIPLE
    global FILE_MULTIPLE_TEXTBOX
    global FILE_MULTIPLE_SHOW

    root = os.path.dirname(get_ui_component("output_path_textbox").value)
    INPUT_FILE_MULTIPLE = gradio.FileExplorer(
        label='TARGETS',
        glob="**/*.*",
        ignore_glob="**/.*",
        root=root,
        file_count="multiple",
        height=400,
    )
    OUTPUT_FILE_MULTIPLE = gradio.FileExplorer(
        label='OUTPUTS',
        glob="**/*.*",
        ignore_glob="**/.*",
        root=root,
        file_count="single",
        height=400,
        visible=False,
    )
    FILE_MULTIPLE_SHOW = gradio.Button(
        value="Batch Start", variant="primary", size="sm"
    )


def listen() -> None:
    output_path_textbox = get_ui_component("output_path_textbox")
    if output_path_textbox:
        FILE_MULTIPLE_SHOW.click(start_batch, inputs = [output_path_textbox, INPUT_FILE_MULTIPLE], outputs = OUTPUT_FILE_MULTIPLE)
    OUTPUT_FILE_MULTIPLE.change(display_output, inputs = OUTPUT_FILE_MULTIPLE, outputs = [output.OUTPUT_IMAGE, output.OUTPUT_VIDEO])
    
def glob_style(output_paths) -> str:
    return f"{os.path.basename(output_paths)}/*.*" 

def display_output(output_path):
    if is_image(output_path):
        return gradio.Image(value = output_path, visible = True), gradio.Video(value = None, visible = False)
    if is_video(output_path):
        return gradio.Image(value = None, visible = False), gradio.Video(value = output_path, visible = True)
    return gradio.Image(), gradio.Video()
    

def create_output_directory(output_path) -> str:
    source_name, _ = os.path.splitext(os.path.basename(facefusion.globals.source_paths[0]))
    target_dirname = os.path.basename(os.path.dirname(facefusion.globals.target_path))
    if target_dirname in ['img', 'Img']:
       target_dirname = os.path.basename(os.path.dirname(os.path.dirname(facefusion.globals.target_path)))+"-Img"
       
    output_dir = output_path + f"/{source_name}-{target_dirname}"
    try: 
        os.makedirs(output_dir, exist_ok = False) 
        logger.info("Directory '%s' created successfully" % output_dir, __name__.upper()) 
    except FileExistsError as e:
        logger.info("Directory '%s' already exists" % output_dir, __name__.upper())   
    except OSError as error: 
        logger.error("Directory '%s' can not be created" % output_dir, __name__.upper())  
    return output_dir 

def start_batch(output_path : str, file_explorer) -> str:
    for target in file_explorer:
        facefusion.globals.target_path = target
        output_dir = create_output_directory(output_path)
        output_image, output_video = output.start(output_dir)
    # TODO: output_dir could be multiple dir 
    return gradio.update(root=output_path, glob=glob_style(output_dir), visible=True)
