#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
Simple training script to demonstrate custom Docker image usage
This would be copied into your Docker image
"""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from loguru import logger


def _args():
    """Parse command line arguments"""
    import argparse

    parser = argparse.ArgumentParser(description="Simple ML Training Script")

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output',
    )

    return parser.parse_args()


def train():
    """Main training function"""
    args = _args()

    if args.verbose:
        logger.info("Verbose mode enabled")

        logger.info("=" * 60)
        logger.info("ML Training Script")
        logger.info("=" * 60)
    
    # Load data
    if args.verbose:
        logger.info("\n1. Loading Iris dataset...")
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    if args.verbose:
        logger.info(f"   Training samples: {len(X_train)}")
        logger.info(f"   Test samples: {len(X_test)}")
    
    # Train model
    if args.verbose:
        logger.info("\n2. Training Random Forest model...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    if args.verbose:
        logger.info("\n3. Evaluating model...")
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    if args.verbose:
        logger.info(f"   Accuracy: {accuracy:.4f}")
    logger.info("\n" + "=" * 60)
    logger.info("Training complete!")
    logger.info("=" * 60)

if __name__ == '__main__':
    train()
