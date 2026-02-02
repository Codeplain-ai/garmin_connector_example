#!/usr/bin/env python3
"""🏃‍♂️ CLI entry point for the Garmin Running Analyst."""

import argparse
import sys
import logging
from src.app import GarminChatApp

def main():
    """CLI entry point handling commands for fetching and chatting."""
    parser = argparse.ArgumentParser(
        description="GarminChatApp: Analyze your Garmin running data with AI."
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Fetch Command
    subparsers.add_parser("fetch", help="Retrieve running data from Garmin Connect")
    
    # Chat Command
    subparsers.add_parser("chat", help="Start an interactive chat session about your data")
    
    args = parser.parse_args()
    
    app = GarminChatApp()

    try:
        if args.command == "fetch":
            app.fetch_workflow()
        elif args.command == "chat":
            app.chat_workflow()
        else:
            # Default behavior: run both as per AdditionalFunctionalRequirement
            logging.info("No command specified. Running full workflow (fetch + chat).")
            app.run_all()
            
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ A critical error occurred: {e}", file=sys.stderr)
        logging.error("Application failure details:", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

