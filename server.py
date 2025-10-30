# server.py
import os
import subprocess
from flask import Flask

app = Flask(__name__)

@app.route("/render")
def render_video():
    # Ensure logo exists
    if not os.path.exists("CVPRk7F2_400x400.jpg"):
        return "❌ Logo missing", 400

    # Run Blender in background mode
    cmd = [
        "./blender/blender", "--background",
        "--python", "imback.py",
        "--disable-autoexec"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return "✅ Render complete! Check output folder."
    else:
        return f"❌ Render failed:\n{result.stderr}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
