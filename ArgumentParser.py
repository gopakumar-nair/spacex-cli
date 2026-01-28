"""
Argument parser configuration for SpaceX CLI.
"""
import argparse


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description='Fetch and analyze SpaceX launch data'
    )
    parser.add_argument(
        '--cache',
        type=str,
        default='./cache/launches.json',
        help='Path to cache file (default: ./cache/launches.json)'
    )
    parser.add_argument(
        '--refresh',
        action='store_true',
        help='Force refresh from API, bypass cache'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--action',
        type=str,
        required=True,
        choices=['report', 'payloads', 'launchpads'],
        help='Action to perform on the data'
    )
    return parser


def parse_args():
    return create_parser().parse_args()
