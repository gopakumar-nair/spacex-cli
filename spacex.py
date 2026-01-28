#!/usr/bin/env python3
"""
SpaceX Launch Data CLI - Fetches and analyzes SpaceX launch data.
"""
from ArgumentParser import parse_args
from Pipeline import Pipeline
from LoggerConfig import setup_logging


def main():
    """Main CLI entry point."""
    args = parse_args()
    
    # Setup logging before creating pipeline
    setup_logging(verbose=args.verbose)
    
    # Create pipeline and process data with fluent interface
    pipeline = Pipeline(cache_path=args.cache)
    pipeline.fetch_data(args.refresh) \
            .filter_data('by_year', year=2022) \
            .perform_action(args.action) \
            .print_result()


if __name__ == '__main__':
    main()
