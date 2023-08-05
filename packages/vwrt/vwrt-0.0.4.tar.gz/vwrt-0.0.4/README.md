# Video Waste Reduction Tool in Python

## Intro

This is a complete python rewrite of [the C++
vwrt](https://github.com/evnb/vwrt).

## Dependencies

-   python3

-   numpy

-   ffmpeg

## Usage

`user$ vwrt [-i INPUT] [-t SPEED] [-s SPEED] [-o OUTDIR]`

## Required Arguments

-   `-i INPUT` or `--input INPUT`: add input
    video<sup>[1](#1)</sup>

-   `-t SPEED` or `--talk-speed SPEED`: set talk speed (aka speed when
    video is above volume threshold)<sup>[1](#1)</sup>

-   `-s SPEED` or `--silence-speed SPEED`: set silence speed (aka speed
    when video is below volume
    threshold)<sup>[1](#1)</sup>

-   `-o OUTDIR` or `--outdir OUTDIR`: set output directory

## Optional Arguments

-   `-h` or `--help`: show this help message and exit

-   `-v` or `--verbose`: set verbose mode

-   `-f` or `--add-frames`: overlay timecode on video before processing

-   `-d` or `--dry-run`: skip video processing

1.  Supports multiple arguments of the same type for batch processing. VWRT will cycle
    through given values until there are no more inputs.
