#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, Any, Optional
import copy
import numbers
import yaml
from loguru import logger
from .constants import DEFAULT_FPS, DEFAULT_CODEC, DEFAULT_IMAGE_QUALITY

# ----------------------------
# Config Loader
# ----------------------------
def load_config(config_file_path: str) -> Dict[str, Any]:
    """
    YAML形式の設定ファイルをロード
    Args:
        config_file_path: 設定ファイルのパス
    Returns:
        Dict[str, Any]: ロードされた設定データ
    """
    config_path = Path(config_file_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

    try:
        with open(config_file_path, 'r', encoding='utf-8') as stream:
            config_data = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        logger.error(f"YAML parse error: {e}")
        raise
    except Exception as e:
        logger.exception("Unexpected error while reading config")
        raise

    if not isinstance(config_data, dict):
        raise ValueError("Config file must contain a YAML dictionary")

    config_data = copy.deepcopy(config_data)

    # 設定値の検証
    validated_config = _validate_and_apply_defaults(config_data)

    logger.info("Configuration loaded: {}", config_file_path)
    logger.debug("Config content: {}", validated_config)

    return validated_config

# ----------------------------
# Default Application + Validation
# ----------------------------
def _validate_and_apply_defaults(config_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if config_data is None:
        config_data = {}

    # 画像設定
    image_config = config_data.get('image_settings') or config_data.get('image') or {}
    image_config.setdefault('quality', DEFAULT_IMAGE_QUALITY)
    config_data['image_settings'] = image_config

    # 動画設定
    video_config = config_data.get('video_settings') or config_data.get('video') or {}
    video_config.setdefault('fps', DEFAULT_FPS)
    video_config.setdefault('codec', DEFAULT_CODEC)
    config_data['video_settings'] = video_config

    # バーリデーション
    _validate_effect(video_config, "crop", "video", _validate_crop)
    _validate_effect(video_config, "resize", "video", _validate_resize)
    _validate_effect(video_config, "brightness", "video", _validate_brightness)
    _validate_effect(video_config, "saturation", "video", _validate_saturation)
    _validate_effect(video_config, "rotate", "video", _validate_rotate)
    _validate_effect(video_config, "flip", "video", _validate_flip)

    _validate_effect(image_config, "crop", "image", _validate_crop)
    _validate_effect(image_config, "resize", "image", _validate_resize)
    _validate_effect(image_config, "brightness", "image", _validate_brightness)
    _validate_effect(image_config, "saturation", "image", _validate_saturation)
    _validate_effect(image_config, "rotate", "image", _validate_rotate)
    _validate_effect(image_config, "flip", "image", _validate_flip)

    return config_data

# ----------------------------
# Common Enabled Checker
# ----------------------------
def _validate_effect(config: Dict[str, Any], key: str, prefix: str = "", validator: callable = None): # type: ignore
    """
    有効化確認
    """
    effect = config.get(key, {})
    if not effect.get('enabled', True):
        return
    if validator:
        validator(effect, prefix)

# ----------------------------
# Individual Validators
# ----------------------------
def _validate_crop(effect: Dict[str, Any], prefix: str):
    coords = effect.get('coordinates')
    if coords is None:
        return
    if not isinstance(coords, list) or len(coords) != 4:
        raise ValueError(f"{prefix}Crop coordinates must be [left, top, right, bottom]")
    left, top, right, bottom = coords
    if not all(isinstance(c, numbers.Integral) and c >= 0 for c in coords): # type: ignore
        raise ValueError(f"{prefix}Crop coordinates must be non-negative integers")
    if left >= right or top >= bottom:
        raise ValueError(f"{prefix}Crop coordinates must satisfy left < right and top < bottom")

def _validate_resize(effect: Dict[str, Any], prefix: str):
    size = effect.get('output_size')
    if size is None:
        return
    if not isinstance(size, list) or len(size) != 2:
        raise ValueError(f"{prefix}Resize output_size must be [width, height]")
    width, height = size
    if not (isinstance(width, numbers.Integral) and isinstance(height, numbers.Integral) and width > 0 and height > 0): # type: ignore
        raise ValueError(f"{prefix}Resize output_size must be positive integers")

def _validate_brightness(effect: Dict[str, Any], prefix: str):
    factor = effect.get('factor')
    if factor is None:
        return
    if not isinstance(factor, (int, float)) or factor <= 0:
        raise ValueError(f"{prefix}Brightness factor must be positive")

def _validate_saturation(effect: Dict[str, Any], prefix: str):
    factor = effect.get('factor')
    if factor is None:
        return
    if not isinstance(factor, (int, float)) or factor <= 0:
        raise ValueError(f"{prefix}Saturation factor must be positive")

def _validate_rotate(effect: Dict[str, Any], prefix: str):
    angle = effect.get('angle')
    if angle is None:
        return
    if not isinstance(angle, int) or not (0 <= angle <= 3):
        raise ValueError(f"{prefix}Rotate angle must be 0~3 (90度単位)")

def _validate_flip(effect: Dict[str, Any], prefix: str):
    option = effect.get('options')
    if option is None:
        return
    if option not in ['vertically', 'horizontally']:
        raise ValueError(f"{prefix}Flip options must be 'vertically' or 'horizontally'")