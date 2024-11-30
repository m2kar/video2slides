# video2slides/main.py
import os
import typer
from typing_extensions import Annotated
from typing import Optional

import datetime
import re
from pptx import Presentation
from pptx.util import Inches
from PIL import Image

DEBUG=bool(os.getenv("DEBUG",False))
class Config:
    skip_frames: int = 0
    num_images:int = 7
    threshold: float = 0.1  # 提高阈值以减少误切
    min_scene_len: float = 0.5  # 最小场景时间长度(s)
    
def make_pptx(img_list:list, output:str):
    prs=Presentation()
    
    with open(img_list[0], 'rb') as f:
        im = Image.open(f)
    dpi=im.info.get('dpi',(96,96))
    width_px, height_px = im.size
    width_in = width_px / dpi[0]
    height_in = height_px / dpi[1]
    prs.slide_width = Inches(width_in)
    prs.slide_height = Inches(height_in)
    
    blank_slide_layout = prs.slide_layouts[6]
    for img in img_list:
        slide = prs.slides.add_slide(blank_slide_layout)
        left = top = 0
        pic = slide.shapes.add_picture(img, left, top, width=prs.slide_width, height=prs.slide_height)
        
        # 添加备注信息
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = f"备注信息: {os.path.basename(img)}"
        
    prs.save(output)
    
app = typer.Typer()

@app.command()
def main(
    input: Annotated[str, typer.Argument(..., help="输入视频文件路径")],
    output: Annotated[Optional[str], typer.Argument(...,help="输出pptx文件路径")] =None
    ):
    timestamp=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if output is None:
        output = os.path.splitext(input)[0]+".pptx"
        if os.path.exists(output):
            output = os.path.splitext(input)[0]+f"-{timestamp}.pptx"
    fname=os.path.basename(input)
    tmp_output=f"./tmp-v2s-{timestamp}-{fname}"
    
    # DEBUG，输出统计信息 
    # f" -s stat.csv "

    # 设置 scenedetect 命令
    scenedetect_cmd = (
        f" scenedetect -i '{input}' -o '{tmp_output}' "
        f" -fs {Config.skip_frames} "
        f" detect-hash --size 16  --threshold {Config.threshold}  --lowpass 2 "
        f" --min-scene-len {Config.min_scene_len} "
        f" list-scenes "
        f" save-images --num-images {Config.num_images} --filename scene\\$SCENE_NUMBER-img\\$IMAGE_NUMBER "
        f" export-html "
    )
    print(scenedetect_cmd)
    os.system(scenedetect_cmd)
        
    # get the image list
    img_list=os.listdir(tmp_output)
    img_list=[f for f in img_list if re.match(rf"scene\d+-img0{Config.num_images-1}.jpg",f)]
    img_list.sort()
    img_list=[os.path.join(tmp_output,f) for f in img_list]
    
    # convert to pptx
    make_pptx(img_list,output)
    
    if not DEBUG:
        os.removedirs(tmp_output)
        print(f"未删除临时文件夹 {tmp_output}")
    print(f"已生成 {output}")
    
if __name__ == "__main__":
    app()