import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path


# ============================================================
# LegalEase - Application Runner
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent
VENV_DIR = ROOT_DIR / ".venv"
REQUIREMENTS_FILE = ROOT_DIR / "requirements.txt"
ENV_FILE = ROOT_DIR / ".env"

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = "8000"
FRONTEND_URL = "http://localhost:8501"


def print_header():
    print("=" * 60)
    print("                 LegalEase")
    print("        AI Legal Document Generator")
    print("=" * 60)
    print()


def get_python_executable():
    """Return the Python executable inside the virtual environment."""
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def create_virtual_environment():
    """Create a virtual environment if it does not exist."""
    if VENV_DIR.exists():
        print("[OK] Virtual environment already exists.")
        return

    print("[INFO] Creating virtual environment...")

    result = subprocess.run(
        [sys.executable, "-m", "venv", str(VENV_DIR)],
        cwd=ROOT_DIR
    )

    if result.returncode != 0:
        print("[ERROR] Failed to create virtual environment.")
        sys.exit(1)

    print("[OK] Virtual environment created.")


def install_dependencies():
    """Install project dependencies."""
    python_exe = get_python_executable()

    if not REQUIREMENTS_FILE.exists():
        print("[ERROR] requirements.txt not found.")
        sys.exit(1)

    print()
    print("[INFO] Upgrading pip...")

    subprocess.run(
        [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
        cwd=ROOT_DIR
    )

    print()
    print("[INFO] Installing project dependencies...")

    result = subprocess.run(
        [
            str(python_exe),
            "-m",
            "pip",
            "install",
            "-r",
            str(REQUIREMENTS_FILE)
        ],
        cwd=ROOT_DIR
    )

    if result.returncode != 0:
        print("[ERROR] Failed to install dependencies.")
        sys.exit(1)

    print("[OK] Dependencies installed.")


def check_env_file():
    """Check whether .env exists."""
    print()

    if not ENV_FILE.exists():
        print("[WARNING] .env file was not found.")
        print()
        print("Create a .env file in the LegalEase root folder.")
        print("You can copy .env.example to .env.")
        print()
        print("Example:")
        print("GEMINI_API_KEY=YOUR_GEMINI_API_KEY")
        print("GEMINI_MODEL=gemini-3.8-flash")
        print()

        answer = input("Continue without .env? (y/n): ").strip().lower()

        if answer != "y":
            print("Application startup cancelled.")
            sys.exit(0)
    else:
        print("[OK] .env file found.")


def start_backend():
    """Start FastAPI backend."""
    python_exe = get_python_executable()

    print()
    print("=" * 60)
    print("Starting FastAPI Backend")
    print("=" * 60)
    print()
    print(f"Backend:  http://{BACKEND_HOST}:{BACKEND_PORT}")
    print(f"API Docs: http://{BACKEND_HOST}:{BACKEND_PORT}/docs")
    print()

    backend_command = [
        str(python_exe),
        "-m",
        "uvicorn",
        "backend.main:app",
        "--reload",
        "--host",
        BACKEND_HOST,
        "--port",
        BACKEND_PORT
    ]

    if os.name == "nt":
        backend_process = subprocess.Popen(
            backend_command,
            cwd=ROOT_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        backend_process = subprocess.Popen(
            backend_command,
            cwd=ROOT_DIR
        )

    return backend_process


def start_frontend():
    """Start Streamlit frontend."""
    python_exe = get_python_executable()
    frontend_file = ROOT_DIR / "frontend" / "app.py"

    if not frontend_file.exists():
        print("[ERROR] frontend/app.py not found.")
        sys.exit(1)

    print()
    print("=" * 60)
    print("Starting Streamlit Frontend")
    print("=" * 60)
    print()
    print(f"Frontend: {FRONTEND_URL}")
    print()

    frontend_command = [
        str(python_exe),
        "-m",
        "streamlit",
        "run",
        str(frontend_file)
    ]

    if os.name == "nt":
        frontend_process = subprocess.Popen(
            frontend_command,
            cwd=ROOT_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        frontend_process = subprocess.Popen(
            frontend_command,
            cwd=ROOT_DIR
        )

    return frontend_process


def main():
    print_header()

    print(f"Project folder: {ROOT_DIR}")
    print()

    # Step 1
    create_virtual_environment()

    # Step 2
    install_dependencies()

    # Step 3
    check_env_file()

    # Step 4
    print()
    print("[INFO] Starting application...")

    backend_process = start_backend()

    # Give FastAPI some time to start
    time.sleep(4)

    frontend_process = start_frontend()

    # Give Streamlit some time to start
    time.sleep(5)

    print()
    print("=" * 60)
    print("             LegalEase is Running!")
    print("=" * 60)
    print()
    print(f"Frontend : {FRONTEND_URL}")
    print(f"Backend  : http://{BACKEND_HOST}:{BACKEND_PORT}")
    print(f"API Docs : http://{BACKEND_HOST}:{BACKEND_PORT}/docs")
    print()
    print("The browser will open automatically.")
    print()
    print("Close the backend/frontend terminal windows to stop")
    print("the LegalEase application.")
    print("=" * 60)

    # Open browser
    time.sleep(2)
    webbrowser.open(FRONTEND_URL)

    try:
        # Keep this runner alive
        while True:
            time.sleep(1)

            # Check whether processes have stopped
            if backend_process.poll() is not None:
                print()
                print("[WARNING] Backend process has stopped.")
                break

            if frontend_process.poll() is not None:
                print()
                print("[WARNING] Frontend process has stopped.")
                break

    except KeyboardInterrupt:
        print()
        print("[INFO] Stopping LegalEase...")

        backend_process.terminate()
        frontend_process.terminate()

        print("[OK] LegalEase stopped.")


if __name__ == "__main__":
    main()
    