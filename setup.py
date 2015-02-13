from cx_Freeze import setup, Executable

setup(
    name = "Barkas",
    version = "0.1",
    description = "Take screenshot and upload to Dropbox",
    executables = [Executable("barkas_uploader.py")]
)
