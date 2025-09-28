# PlexArtScaler

A command-line tool for automatically scaling and standardizing artwork for Plex media libraries.

## Overview

PlexArtScaler solves the common problem of inconsistent artwork dimensions in Plex libraries. It:

1. Takes artwork from your Plex media items (movies, TV shows)
2. Scales them to a consistent aspect ratio (default 16:9)
3. For artwork that doesn't match the target ratio, creates a blurred background from the original image
4. Optionally uploads the standardized artwork back to your Plex server

## Features

- Scale artwork for a single item or entire library
- Creates aesthetically pleasing blurred backgrounds for non-standard aspect ratios
- Preserves original artwork in a backup directory
- Configurable image dimensions and blur radius
- Direct integration with the Plex API

## Installation

### Prerequisites

- Python 3.6+
- Plex Media Server with API access

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/PlexArtScaler.git
   cd PlexArtScaler
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application:
   - Copy the `config_template.json` file to `config.json` and update it with your Plex server details:
     ```bash
     cp config_template.json config.json
     # Edit config.json with your preferred editor
     ```

## Usage

PlexArtScaler provides a simple CLI interface:

### Scale a single item

```bash
python cli.py scale "Movie Title" --library "Movies" --upload
```

Options:
- `--upload`: Upload the processed artwork back to Plex (default: False)
- `--library`: Specify which library to search in (optional)
- `--verbose`: Enable verbose output (optional)

### Scale all items in a library

```bash
python cli.py scale-all --library "Movies" --upload
```

Options:
- `--upload`: Upload the processed artwork back to Plex (default: False)
- `--library`: Specify which library to process (optional, defaults to all configured libraries)
- `--verbose`: Enable verbose output (optional)

## How It Works

1. The tool connects to your Plex server using the provided URL and token
2. It retrieves the artwork URL for each media item
3. The original artwork is downloaded and saved to the backup directory
4. If the artwork doesn't match the target aspect ratio:
   - It's resized to fit either width or height (maintaining proportions)
   - A blurred background is created from the original image
   - The original image is centered on top of the background
5. The processed image is saved to the output directory
6. If the `--upload` option is used, the new artwork is uploaded back to Plex

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
