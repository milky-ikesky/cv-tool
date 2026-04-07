#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# CLIで受け入れ可能なタイプ（画像/動画）
VALID_IMAGE_TYPES = ["image", "i"]
VALID_VIDEO_TYPES = ["video", "v"]

# サポートされる拡張子（先頭にドットを含む）
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".wmv"]

# 動画出力時のデフォルト値
DEFAULT_FPS = 30.0
DEFAULT_CODEC = "mp4v"
DEFAULT_IMAGE_QUALITY = 95
