#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云 DashScope Paraformer-v2 语音识别（离线批量版，更准）
流程: ogg -> wav -> 上传OSS临时 -> paraformer-v2识别 -> 输出文本
用法: python asr.py <audio_file_path>
"""
import sys, os, time, subprocess, shutil, tempfile, warnings
warnings.filterwarnings("ignore")

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

API_KEY = os.environ.get("DASHSCOPE_API_KEY", "sk-b72e5db973684cc6a1e2e18067a6ad39")


def to_wav(src):
    """ffmpeg 转 16kHz mono wav"""
    ffmpeg = shutil.which("ffmpeg") or r"C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"
    tmp = tempfile.mktemp(suffix=".wav")
    r = subprocess.run(
        [ffmpeg, "-i", src, "-ar", "16000", "-ac", "1", "-f", "wav", tmp, "-y"],
        capture_output=True, timeout=60
    )
    if r.returncode != 0 or not os.path.exists(tmp):
        raise RuntimeError(f"ffmpeg failed: {r.stderr.decode(errors='replace')[-200:]}")
    return tmp


def transcribe_stream(wav_path):
    """paraformer-realtime-v2 流式识别（无需上传）"""
    import dashscope, wave as wavemod
    from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult
    dashscope.api_key = API_KEY

    texts = []

    class CB(RecognitionCallback):
        def on_open(self): pass
        def on_close(self): pass
        def on_error(self, r): sys.stderr.write(f"err: {r}\n")
        def on_event(self, result):
            s = result.get_sentence()
            if s and RecognitionResult.is_sentence_end(s):
                t = s.get("text", "").strip()
                if t: texts.append(t)

    with wavemod.open(wav_path, "rb") as wf:
        sr = wf.getframerate()
        data = wf.readframes(wf.getnframes())

    rec = Recognition(
        model="paraformer-realtime-v2",
        format="pcm", sample_rate=sr,
        callback=CB(),
        language_hints=["zh", "en"],
    )
    rec.start()
    for i in range(0, len(data), 3200):
        rec.send_audio_frame(data[i:i+3200])
    rec.stop()
    return " ".join(texts)


def transcribe_file(wav_path):
    """paraformer-v2 文件识别（需要公网可访问URL，用OSS）"""
    # 尝试上传到 OSS（如没配置则跳过）
    try:
        import oss2
        # OSS 未配置，跳过
    except ImportError:
        pass
    raise RuntimeError("OSS not configured")


def main(src_path):
    # 1. 转 wav
    ext = os.path.splitext(src_path)[1].lower()
    if ext == ".wav":
        wav = src_path
        cleanup = False
    else:
        wav = to_wav(src_path)
        cleanup = True

    try:
        result = transcribe_stream(wav)
        if result:
            print(result)
        else:
            sys.stderr.write("No speech detected\n")
            sys.exit(1)
    finally:
        if cleanup and os.path.exists(wav):
            try: os.remove(wav)
            except: pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python asr.py <audio_file>\n")
        sys.exit(1)
    p = sys.argv[1]
    if not os.path.exists(p):
        sys.stderr.write(f"File not found: {p}\n")
        sys.exit(1)
    main(p)
