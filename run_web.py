#!/usr/bin/env python3
"""
IT Ticket Management System - Web Server Launcher

This script starts the web-based IT ticket management system.

Usage:
    python run_web.py                    # Start on default (0.0.0.0:8000)
    python run_web.py --host 127.0.0.1  # Start on localhost only
    python run_web.py --port 8080       # Start on port 8080

Environment variables:
    WEB_HOST      - Server host (default: 0.0.0.0)
    WEB_PORT      - Server port (default: 8000)
    ENVIRONMENT   - Set to 'development' for auto-reload (default)
    LOG_LEVEL     - Logging level (default: info)
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=False)

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        return True
    except ImportError:
        print("❌ Required dependencies not found!")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Start the IT Ticket Management System web server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--host",
        default=os.getenv("WEB_HOST", "0.0.0.0"),
        help="Server host (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("WEB_PORT", "8000")),
        help="Server port (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=os.getenv("ENVIRONMENT", "development") == "development",
        help="Enable auto-reload on file changes"
    )
    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "info").lower(),
        choices=["critical", "error", "warning", "info", "debug"],
        help="Logging level (default: info)"
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    
    print("\n" + "="*60)
    print("🚀 IT TICKET MANAGEMENT SYSTEM - WEB SERVER")
    print("="*60)
    print(f"\n📍 Server starting on: http://{args.host}:{args.port}")
    print(f"📖 API Documentation: http://{args.host}:{args.port}/api/docs")
    print(f"⚙️  Log level: {args.log_level}")
    print(f"🔄 Auto-reload: {'Enabled' if args.reload else 'Disabled'}")
    print("\n" + "-"*60)
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Change to script directory
        os.chdir(script_dir)
        
        # Build the uvicorn command
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "app:app",
            "--host", args.host,
            "--port", str(args.port),
            "--log-level", args.log_level,
        ]
        
        if args.reload:
            cmd.append("--reload")
        
        # Run the server
        subprocess.run(cmd, check=False)
        
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
