#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import argparse
from typing import Dict

from loguru import logger

from app import __version__
from config.loader import load_config
from utils.log import setup_logging


# ----------------------------
# Argument / Type Helpers
# ----------------------------
def normalize_type(value: str) -> str:
    """
    コマンドライン引数のタイプを正規化（alias対応）
    """
    mapping = {
        "image": "image",
        "i": "image",
        "video": "video",
        "v": "video",
    }

    key = value.lower()
    if key not in mapping:
        raise argparse.ArgumentTypeError(
            f"Invalid type: {value}. Use 'image(i)' or 'video(v)'"
        )

    return mapping[key]


def create_parser() -> argparse.ArgumentParser:
    """
    コマンドライン引数を定義
    """
    parser = argparse.ArgumentParser(
        description="画像・動画前処理ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-t", "--type",
        type=normalize_type,
        default="image",
        help="データタイプ指定: 'image(i)' または 'video(v)' (デフォルト: 'image')"
    )
    parser.add_argument(
        "-p", "--path",
        type=Path,
        default=Path("./assets"),
        help="画像または動画ファイルの入力パス (デフォルト: './assets')"
    )
    parser.add_argument(
        "-c", "--config",
        type=Path,
        default=Path("./config.yaml"),
        help="設定ファイルパス (デフォルト: './config.yaml')"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("./result"),
        help="出力ディレクトリパス (デフォルト: './result')"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="インタラクティブモードを有効化"
    )
    return parser


# ----------------------------
# Core Functions
# ----------------------------
def load_and_validate_config(config_path: Path) -> Dict:
    """
    設定ファイルのロード
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    return load_config(str(config_path))


def run(args: argparse.Namespace) -> None:
    """
    前処理の実行
    """
    data_type = args.type
    input_path = args.path
    output_dir = args.output

    try:
        config = load_and_validate_config(args.config)
    except ValueError as e:
        logger.error(e)
        return
    except FileNotFoundError as e:
        logger.error(e)
        return

    logger.info(f"Running {data_type} preprocessing")
    logger.debug(f"Config: {config}")
    logger.info(f"Input path: {input_path}, Output directory: {output_dir}")


# ----------------------------
# Interactive Mode Helpers
# ----------------------------
def handle_help() -> None:
    print("コマンド:")
    print("  set type <image|video|i|v>")
    print("  set path <path>")
    print("  set config <path>")
    print("  set output <path>")
    print("  run")
    print("  show")
    print("  exit")


def handle_set(parts, current_type, current_path, current_config, current_output):
    if len(parts) < 3:
        print("使用法: set <option> <value>")
        return current_type, current_path, current_config, current_output

    option = parts[1].lower()
    value = " ".join(parts[2:])

    if option == "type":
        try:
            current_type = normalize_type(value)
            print(f"タイプを {current_type} に設定しました")
        except argparse.ArgumentTypeError as e:
            print(e)

    elif option == "path":
        p = Path(value)
        if not p.exists():
            print("パスが存在しません")
        else:
            current_path = p
            print(f"パスを {current_path} に設定しました")

    elif option == "config":
        current_config = Path(value)
        print(f"設定ファイルを {current_config} に設定しました")

    elif option == "output":
        current_output = Path(value)
        print(f"出力ディレクトリを {current_output} に設定しました")

    else:
        print(f"不明なオプション: {option}")

    return current_type, current_path, current_config, current_output


def handle_show(current_type, current_path, current_config, current_output):
    print(f"タイプ: {current_type}")
    print(f"パス: {current_path}")
    print(f"設定ファイル: {current_config}")
    print(f"出力ディレクトリ: {current_output}")


def handle_run(current_type, current_path, current_config, current_output):
    from argparse import Namespace

    args = Namespace(
        type=current_type,
        path=current_path,
        config=current_config,
        output=current_output
    )

    try:
        run(args)
    except Exception as e:
        logger.error(f"実行に失敗しました: {e}")


def interactive_main():
    logger.info("インタラクティブモード開始 ('help' でコマンド一覧)")

    current_type = "image"
    current_path = Path("./assets")
    current_config = Path("./config.yaml")
    current_output = Path("./result")

    while True:
        try:
            command = input(f"cv-tool({current_type})> ").strip()
            if not command:
                continue

            parts = command.split()
            cmd = parts[0].lower()

            if cmd == "exit":
                logger.info("終了します")
                break
            elif cmd == "help":
                handle_help()
            elif cmd == "set":
                current_type, current_path, current_config, current_output = handle_set(
                    parts, current_type, current_path, current_config, current_output
                )
            elif cmd == "show":
                handle_show(current_type, current_path, current_config, current_output)
            elif cmd == "run":
                handle_run(current_type, current_path, current_config, current_output)
            else:
                print(f"不明なコマンド: {cmd}")

        except KeyboardInterrupt:
            logger.info("中断されました")
            break
        except Exception as e:
            logger.error(f"エラー: {e}")


# ----------------------------
# CLI Entrypoint
# ----------------------------
def cli_main():
    try:
        setup_logging(
            log_dir="logs",
            console_level="INFO",
            file_level="DEBUG",
            rotation="10 MB",
            retention="7 days",
        )
    except Exception as exc:
        logger.remove()
        logger.add(sys.stderr, level="INFO")
        logger.warning(f"Failed to configure log files: {exc}")

    logger.info("=" * 40)
    logger.info(f"App version: {__version__}")
    logger.info(f"Python version: {sys.version}")
    logger.info("=" * 40)

    parser = create_parser()
    args = parser.parse_args()

    if args.interactive:
        interactive_main()
    else:
        try:
            run(args)
        except FileNotFoundError as e:
            logger.error(e)
            sys.exit(2)
        except Exception:
            logger.exception("Unexpected error")
            sys.exit(1)
        else:
            logger.info("Processing completed successfully.")


if __name__ == "__main__":
    cli_main()