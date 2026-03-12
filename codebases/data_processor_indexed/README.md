# Data Processor

A robust, multi-module data processing utility for batch operations.

## Overview

This application provides a flexible framework for processing data items in batches. It has been restructured into a modular architecture to support complexity and extensibility.

## Project Structure

- `app/`: Main application package.
  - `main.py`: Core entry point logic.
  - `config.py`: Global configuration and constants.
  - `models/`: Data structures and domain models.
  - `processors/`: Abstract and concrete processing engines.
  - `utils/`: Common utilities like logging and helpers.

## Features

- **Modular Design**: Separates concerns across specialized packages.
- **Batch Processing**: Efficiently handle lists of `DataItem` objects.
- **Hierarchical Logging**: Professional execution tracking using standard `logging`.
- **Extensible Architecture**: Easily add new processors by inheriting from `BaseProcessor`.

## Usage

To run the data processor:

```bash
python main.py
```
