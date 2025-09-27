
"""
实时语音对话 Demo：录音→ASR→LLM→TTS→ffmpeg 播放
七牛云 AI  https://openai.qiniu.com/v1
"""

import asyncio
import base64
import gzip
import json
import os
import subprocess
import sys
import time
import uuid
import wave
from io import BytesIO

import pyaudio
import requests
import websockets

# ========== 用户必填 ==========
API_KEY = "sk-bd72031991640baf15b152cea288ab787c5adbe8d43171f6b096e594de20e7f3"            # 七牛 AI API Key
FFMPEG_PATH = "D:\\ProgramData\\git\\project\\memory\\online\\mem0\\demo_ffmpeg\\bin"             # 本机 ffmpeg 可执行文件完整路径
# ========== 可选 ==========
MODEL_NAME = "deepseek-v3"                   # 七牛支持的 LLM 模型
VOICE_TYPE = "qiniu_zh_female_xyqxxj"     # 七牛 TTS 音色
BASE_URL = "https://openai.qiniu.com/v1"     # 主接入点
WS_ASR_URL = "wss://openai.qiniu.com/v1/voice/asr"
# ===============================

# ---------- 音频参数 ----------
SAMPLE_RATE = 16_000
CHANNELS = 1
BITS = 16
SEG_DURATION_MS = 300        # 每段音频毫秒
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16





# ---------- LLM 调用 ----------
def chat_with_llm(text: str) -> str:
    """同步调用七牛 LLM（OpenAI-Compatible）"""
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "你是一个简洁的语音助手。"},
            {"role": "user", "content": text}
        ]
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ---------- TTS + ffmpeg 播放 ----------
def tts_and_play(text: str):
    """调用 TTS 得到 MP3(base64) → 保存临时文件 → ffmpeg 播放 → 删文件"""
    url = f"{BASE_URL}/voice/tts"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "audio": {
            "voice_type": VOICE_TYPE,
            "encoding": "mp3",
            "speed_ratio": 1.0
        },
        "request": {"text": text}
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data_b64 = resp.json()["data"]
    mp3_bytes = base64.b64decode(data_b64)

    tmp_mp3 = f"/tmp/qiniu_tts_{uuid.uuid4().hex}.mp3"
    with open(tmp_mp3, "wb") as f:
        f.write(mp3_bytes)

    # 用用户指定 ffmpeg 播放（-nodisp 不弹窗，-autoexit 播完自动退出）
    subprocess.run([
        FFMPEG_PATH, "-loglevel", "quiet", "-nodisp", "-autoexit",
        "-i", tmp_mp3, "-f", "wav", "-"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(tmp_mp3)


# ---------- WebSocket ASR 协议相关 ----------
def gzip_compress(data: bytes) -> bytes:
    return gzip.compress(data)


def gen_header(msg_type=0b0001, flags=0b0001, serial=0b0001, compress=0b0001):
    header = bytearray()
    header_size = 1
    header.append((0b0001 << 4) | header_size)
    header.append((msg_type << 4) | flags)
    header.append((serial << 4) | compress)
    header.append(0)
    return header


def gen_seq_bytes(seq: int) -> bytes:
    return seq.to_bytes(4, "big", signed=True)


# ---------- 麦克风异步流 ----------
async def mic_stream():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE,
                    input=True, frames_per_buffer=CHUNK_SIZE)
    bytes_per_frame = CHUNK_SIZE * (BITS // 8) * CHANNELS
    frames_needed = int(SAMPLE_RATE * SEG_DURATION_MS / 1000)
    bytes_needed = frames_needed * (BITS // 8) * CHANNELS
    buffer = b""
    try:
        while True:
            data = await asyncio.to_thread(stream.read, CHUNK_SIZE, False)
            buffer += data
            while len(buffer) >= bytes_needed:
                segment = buffer[:bytes_needed]
                buffer = buffer[bytes_needed:]
                yield segment
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


# ---------- 主流程 ----------
async def asr_llm_tts_loop():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with websockets.connect(
                      uri=WS_ASR_URL,additional_headers=headers) as ws:
        
    
        # 1. 发送配置包
        reqid = str(uuid.uuid4())
        config = {
            "user": {"uid": reqid},
            "audio": {
                "format": "pcm", "sample_rate": SAMPLE_RATE,
                "bits": BITS, "channel": CHANNELS, "codec": "raw"
            },
            "request": {"model_name": "asr", "enable_punc": True}
        }
        payload = gzip_compress(json.dumps(config).encode())
        full_req = bytearray(gen_header())
        full_req.extend(gen_seq_bytes(1))
        full_req.extend(len(payload).to_bytes(4, "big"))
        full_req.extend(payload)
        await ws.send(full_req)

        seq = 1
        last_text = ""
        async for chunk in mic_stream():
            seq += 1
            # 2. 发送音频包
            audio_req = bytearray(gen_header(msg_type=0b0010, flags=0b0001))
            audio_req.extend(gen_seq_bytes(seq))
            compressed = gzip_compress(chunk)
            audio_req.extend(len(compressed).to_bytes(4, "big"))
            audio_req.extend(compressed)
            await ws.send(audio_req)

            # 3. 收识别结果
            try:
                res = await asyncio.wait_for(ws.recv(), timeout=2)
            except asyncio.TimeoutError:
                continue
            # 简单解析：直接 utf-8 解码看有没有 text 字段
            if isinstance(res, bytes):
                # 偷懒解析，直接转 string 找 text
                try:
                    txt = json.loads(res.split(b'{"text":"')[1].split(b'"}')[0].decode())
                except:
                    txt = ""
            else:
                txt = json.loads(res).get("result", {}).get("text", "")
            if txt and txt != last_text:
                print(f"[ASR] {txt}")
                last_text = txt
                # 4. 调用 LLM
                reply = await asyncio.to_thread(chat_with_llm, txt)
                print(f"[LLM] {reply}")
                # 5. TTS 并播放
                await asyncio.to_thread(tts_and_play, reply)


# ---------- 入口 ----------
if __name__ == "__main__":
    try:
        asyncio.run(asr_llm_tts_loop())
    except KeyboardInterrupt:
        sys.exit(0)