# video2slides

视频转幻灯片工具

## 功能

- 从视频中提取场景
- 生成PPTX幻灯片
- 语音识别，生成字幕
- 自定义场景检测参数

## 安装

确保你已经安装了 [Python](https://www.python.org/) 和 [pip](https://pip.pypa.io/):

```bash
pip install git+https://github.com/m2kar/video2slides.git
```

## 使用方法

```bash
$ video2slides --help
Usage: video2slides [OPTIONS] VIDEO [OUTPUT]

  Convert video to pptx slides

Arguments:
  VIDEO     输入视频文件路径  [required]
  [OUTPUT]  输出pptx文件路径

Options:
  --srt / --no-srt                是否生成字幕  [default: no-srt]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

### 示例

示例视频文件和PPTX输出可查看`./example/example.mp4`和`./example/example.pptx`

将 `example.mp4` 转换为幻灯片：

```bash
video2slides example.mp4
```

如果未指定输出路径，默认生成 `example.pptx`。如果文件已存在，将自动添加时间戳。

也可以指定输出路径：

```bash
video2slides example.mp4 output.pptx
```

添加字幕:

(需正确安装 openai-whisper库)

```bash
# 音轨转换为字幕，放到幻灯片备注:

video2slides example.mp4 --srt
```

## 自定义配置

可以通过修改 `video2slides/main.py` 中的 `Config` 类来调整场景检测参数：


## 依赖

- [scenedetect](https://github.com/Breakthrough/PySceneDetect)
- [typer](https://typer.tiangolo.com/)
- [python-pptx](https://python-pptx.readthedocs.io/)
- [Pillow](https://python-pillow.org/)

- [可选][openai-whisper](https://github.com/openai/whisper)

## TODO
- [ ] 优化有幻灯片过渡的分割准确率
- [ ] 优化包含摄像头的视频的分割准确率
- [ ] 优化PPT内嵌视频的分割准确率

- [ ] scenedetect切换为api调用，非os.system调用
- [ ] 提供GUI界面
- [ ] 提供在线服务
- [ ] 增加多语言支持
- [ ] 增加单元测试和集成测试
- [ ] 开发docker

## 许可证

MIT 许可证。详见 [LICENSE](LICENSE) 文件。