"""Chạy localhost, nhập khóa hỏi đáp ẩn và chỉ giữ trong bộ nhớ tiến trình."""

import getpass
import os
from app import app

if __name__ == "__main__":
    if not os.environ.get("CHAT_API_KEY"):
        os.environ["CHAT_API_KEY"] = getpass.getpass("Nhập khóa API hỏi đáp (ẩn): ").strip()
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "8000")), debug=False)
