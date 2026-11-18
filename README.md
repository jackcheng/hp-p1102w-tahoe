# HP LaserJet Professional P1102w Driver for Modern macOS

## Overview

This repository provides a community-modified driver package for the **HP LaserJet Professional P1102w** printer that installs on current versions of macOS, including **macOS 26 (Tahoe)**, **macOS 27**, and later releases.

HP's official driver package refuses to install on newer macOS releases because its installer checks the macOS version number. This repackage takes the latest official HP driver and replaces only the installer's `Distribution` file with one that has no macOS version check, so the package is no longer tied to a specific macOS version. The driver files themselves are unchanged.

## Features

*   **Not tied to a macOS version:** The installer no longer checks which version of macOS you're running, so a new macOS release won't block it.
*   **Based on Latest Official HP Driver:** Ensures you're getting the most up-to-date core driver components from HP, with only the installer check removed.

## Installation

1.  **Download:** Download `HP_P1102w_macOS_Driver.pkg` from the [latest release](https://github.com/jackcheng/hp-p1102w-tahoe/releases/latest).
2.  **Run Installer:** Double-click the downloaded `.pkg` file to launch the installer and follow the on-screen prompts.
3.  **If macOS blocks the installer:** Because this package isn't signed by HP, macOS may say it "can't be opened" or is from an unidentified developer. To allow it:
    1. Open **System Settings** > **Privacy & Security**.
    2. Scroll down to the **Security** section, where you'll see a message about the blocked installer.
    3. Click **Open Anyway**, then confirm with your password or Touch ID.
    4. The installer will open. Continue with the on-screen prompts.
4.  **Add Printer:** After installation, go to **System Settings** > **Printers & Scanners** and add your HP LaserJet Professional P1102w printer.

**Apple silicon Macs:** HP's driver is built for Intel, so macOS may ask to install Rosetta the first time you run the installer. Allow it.

## How the package is built

*   [`package/Distribution`](package/Distribution) is the installer definition used in the package. Compared with HP's original, it removes the `InstallationCheck()` script that rejected newer macOS versions.
*   [`tools/replace_distribution.py`](tools/replace_distribution.py) swaps that file into the package without touching the HP driver payload.
*   The [release workflow](.github/workflows/release.yml) builds the package and publishes it as a GitHub release. Run it from the **Actions** tab with **Run workflow**.

## Disclaimer

This driver package is a community modification and is **not officially supported by HP Inc.** Use at your own discretion. While care has been taken to ensure functionality, there are no guarantees, and neither the creator nor contributors are liable for any issues that may arise from its use.
