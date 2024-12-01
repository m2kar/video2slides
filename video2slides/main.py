# video2slides/main.py
import os
import shutil
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
    skip_frames: int = 5
    num_images:int = 9
    threshold: float = 0.1  # 提高阈值以减少误切
    min_scene_len: float = 0.5  # 最小场景时间长度(s)
    
def make_pptx(output:str,img_list:list,note_list:list=None):
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
    for i,img in enumerate(img_list):
        slide = prs.slides.add_slide(blank_slide_layout)
        left = top = 0
        pic = slide.shapes.add_picture(img, left, top, width=prs.slide_width, height=prs.slide_height)
        
        # add note
        if note_list is not None:
            note = note_list[i]
            slide.notes_slide.notes_text_frame.text = note
        
    prs.save(output)
    
# Scene Number,Start Frame,Start Timecode,Start Time (seconds),End Frame,End Timecode,End Time (seconds),Length (frames),Length (timecode),Length (seconds)
# 1,1,00:00:00.000,0.000,174,00:00:06.960,6.960,174,00:00:06.960,6.960
# 7,16405,00:10:56.160,656.160,18024,00:12:00.960,720.960,1620,00:01:04.800,64.800
def time_info(scene_info_csv:str):
    with open(scene_info_csv) as f:
        f.readline()
        f.readline()
        lines=f.readlines()
    scene_infos=[l.strip().split(",") for l in lines]
    time_notes=[ f"Time Info: scene {scene_details[0]}, {scene_details[2]}-{scene_details[5]} ({scene_details[9]}s)"
                for scene_details in scene_infos]
    return time_notes
 
def seconds_to_timecode(seconds):
    return f"{int(seconds//3600):02d}:{int(seconds%3600//60):02d}:{seconds%60:06.3f}"

def srt_info(scene_info_csv:str,video_path:str):
    print("[*] Converting video to text...")

    import whisper
    model = whisper.load_model("turbo")
    result = model.transcribe(video_path,verbose=True)
    segments=result["segments"]
    print("[*] Convert video to srt Done.")
        
    with open(scene_info_csv) as f:
        f.readline()
        f.readline()
        lines=f.readlines()
    scene_infos=[l.strip().split(",") for l in lines]
    time_notes=[ f"Time Info: scene {scene_details[0]}, {scene_details[2]}-{scene_details[5]} ({scene_details[9]}s)"
                for scene_details in scene_infos]
    
    srt_notes = [""] * len(scene_infos)
    for seg in segments:
        seg_start = seg["start"]
        seg_end = seg["end"]
        seg_text = seg["text"]
        
        max_intersection = 0
        assigned_scene_index = -1
        
        for idx, scene in enumerate(scene_infos):
            scene_start = float(scene[3])  # 假设 start_seconds 在索引3
            scene_end = float(scene[6])    # 假设 end_seconds 在索引6
            
            # 计算交集时间
            overlap_start = max(seg_start, scene_start)
            overlap_end = min(seg_end, scene_end)
            overlap = max(0, overlap_end - overlap_start)
            
            if overlap > max_intersection:
                max_intersection = overlap
                assigned_scene_index = idx
        
        if assigned_scene_index != -1:
            # 添加字幕到对应的场景备注
            if srt_notes[assigned_scene_index]:
                srt_notes[assigned_scene_index] += "\n" + seg_text
            else:
                srt_notes[assigned_scene_index] = seg_text
    
    for i,scene in enumerate(scene_infos):
        srt_notes[i]+="\n\n" + time_notes[i]
    return srt_notes

app = typer.Typer()

@app.command()
def main(
    input: Annotated[str, typer.Argument(..., help="输入视频文件路径")],
    output: Annotated[Optional[str], typer.Argument(...,help="输出pptx文件路径")] =None,
    srt: bool = typer.Option(False, help="是否生成字幕"),
    
    # srt: Annotated[Optional[bool], typer.Option(False, help="是否生成字幕")]=False
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
        f" list-scenes --filename scenes_info.csv "
        f" save-images --num-images {Config.num_images} --filename scene\\$SCENE_NUMBER-img\\$IMAGE_NUMBER "
        f" export-html "
    )
    print(scenedetect_cmd)
    os.system(scenedetect_cmd)

    # 
        
    # get the image list
    imgs_list=os.listdir(tmp_output)
    imgs_list=[f for f in imgs_list if re.match(rf"scene\d+-img0{Config.num_images-1}.jpg",f)]
    imgs_list.sort()
    imgs_list=[os.path.join(tmp_output,f) for f in imgs_list]
    
    # get the note list
    if srt:
        notes_list=srt_info(os.path.join(tmp_output,"scenes_info.csv"),input)
    else:
        time_notes=time_info(os.path.join(tmp_output,"scenes_info.csv"))
        notes_list=time_notes
    
    # convert to pptx
    make_pptx(output,imgs_list,notes_list)
    
    if DEBUG:
        print(f"未删除临时文件夹： {tmp_output}")
    else:
        shutil.rmtree(tmp_output,ignore_errors=True)
        print(f"删除临时文件夹 {tmp_output}")
    print(f"已生成 {output}")
    
if __name__ == "__main__":
    app()