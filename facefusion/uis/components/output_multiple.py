import gradio

from facefusion.uis.core import get_ui_component


def render() -> None:
    global INPUT_FILE_MULTIPLE
    global FILE_MULTIPLE_TEXTBOX
    global FILE_MULTIPLE_SHOW

    INPUT_FILE_MULTIPLE = gradio.FileExplorer(
        glob="**/*.*",
        ignore_glob="**/__init__.py",
        root="/Users/cyan/MEGA/DF/",
        file_count="multiple",
    )
    FILE_MULTIPLE_TEXTBOX = gradio.Textbox(label="Selected Files")
    FILE_MULTIPLE_SHOW = gradio.Button(
        value="Batch Start", variant="primary", size="sm"
    )


def listen() -> None:
    output_path_textbox = get_ui_component("output_path_textbox")
    if output_path_textbox:
        FILE_MULTIPLE_SHOW.click(file_show, INPUT_FILE_MULTIPLE, FILE_MULTIPLE_TEXTBOX)
    INPUT_FILE_MULTIPLE.change(file_show, INPUT_FILE_MULTIPLE, FILE_MULTIPLE_TEXTBOX)


def file_show(files) -> str:
    return "\n".join(files)
