```markdown
# video2slides

视频转幻灯片工具

## 功能

- 从视频中提取场景
- 生成PPTX幻灯片
- 自定义场景检测参数

## 安装

确保你已经安装了 [Python](https://www.python.org/) 和 [pip](https://pip.pypa.io/):

```bash
pip install video2slides
```

## 使用方法

```bash
video2slides <输入视频路径> [输出PPTX路径]
```

### 示例

将 `example.mp4` 转换为幻灯片：

```bash
video2slides example.mp4
```

如果未指定输出路径，默认生成 `example.pptx`。如果文件已存在，将自动添加时间戳：

```bash
video2slides example.mp4
```

指定输出路径：

```bash
video2slides example.mp4 output.pptx
```

## 配置

可以通过修改 `video2slides/main.py` 中的 `Config` 类来调整场景检测参数：

```python
class Config:
    skip_frames: int = 0
    num_images: int = 7
    threshold: float = 0.1
    min_scene_len: float = 0.5
```

## 依赖

- [scenedetect](https://github.com/Breakthrough/PySceneDetect)
- [typer](https://typer.tiangolo.com/)
- [python-pptx](https://python-pptx.readthedocs.io/)
- [Pillow](https://python-pillow.org/)

## 许可证

MIT 许可证。详见 [LICENSE](LICENSE) 文件。
```