"""Điểm vào Flask dành cho Vercel."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "server"))
# Vercel chỉ cho phép ghi dữ liệu tạm trong /tmp.
os.environ.setdefault("MEDIAKIT_OUT", "/tmp/mediakit-out")

from app import app
