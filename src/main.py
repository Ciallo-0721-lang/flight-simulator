#!/usr/bin/env python3
"""
Flight Simulator - Main Entry Point

This is the main application entry point for the flight simulator game.
It initializes all systems and runs the main game loop.
"""

import sys
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.game import GameEngine
from core.config import Config


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('flight_simulator.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def main():
    """Main application entry point."""
    logger = setup_logging()
    logger.info("Starting Flight Simulator...")
    
    try:
        # Load configuration
        config = Config()
        logger.info(f"Configuration loaded: {config.screen_width}x{config.screen_height}")
        
        # Initialize and run game engine
        engine = GameEngine(config)
        logger.info("Game engine initialized")
        
        engine.run()
        logger.info("Game closed normally")
        
    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
