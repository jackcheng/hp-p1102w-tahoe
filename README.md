# HP LaserJet Professional P1102w Driver for macOS Tahoe, Golden Gate and Beyond

## Overview

This repository provides a community-modified driver package for the **HP LaserJet Professional P1102w** printer that installs on current versions of macOS, including **macOS 26 (Tahoe)**, **macOS 27 (Golden Gate)**, and later releases.

HP's official driver package refuses to install on newer macOS releases because its installer checks the macOS version number. This repackage takes the latest official HP driver and replaces only the installer's `Distribution` file with one that has no macOS version check, so the package is no longer tied to a specific macOS version. The driver files themselves are unchanged.

## Supported macOS versions

| macOS version | Supported |
| --- | --- |
| macOS 26 Tahoe | Yes |
| macOS 27 Golden Gate | Yes |
| Later macOS releases | Yes, the installer has no version check |

If you're searching for a **P1102w driver for macOS Tahoe**, a **P1102w driver for macOS Golden Gate**, or a driver for whatever macOS comes next, this is the same package.

## Features

*   **Not tied to a macOS version:** The installer no longer checks which version of macOS you're running, so a new macOS release (Tahoe, Golden Gate, or anything after) won't block it.
*   **Based on Latest Official HP Driver:** Ensures you're getting the most up-to-date core driver components from HP, with only the installer check removed.

## Installation

1.  **Apple silicon Macs: install Rosetta first.** HP's printing filters are Intel-only, so they need Rosetta to run. Upgrading to macOS 27 (Golden Gate) removes Rosetta and doesn't put it back, and macOS won't prompt you to reinstall it for a printer driver. Open Terminal and run:

    ```sh
    sudo softwareupdate --install-rosetta --agree-to-license
    ```

    Intel Macs can skip this step.
2.  **Download:** Download `HP_P1102w_macOS_Driver.pkg` from the [latest release](https://github.com/jackcheng/hp-p1102w-tahoe/releases/latest).
3.  **Run Installer:** Double-click the downloaded `.pkg` file to launch the installer and follow the on-screen prompts.
4.  **If macOS blocks the installer:** This is a modified package, not HP's original, so macOS may say it "can't be opened" or is from an unidentified developer. To allow it:
    1. Open **System Settings** > **Privacy & Security**.
    2. Scroll down to the **Security** section, where you'll see a message about the blocked installer.
    3. Click **Open Anyway**, then confirm with your password or Touch ID.
    4. The installer will open. Continue with the on-screen prompts.
5.  **Add Printer:** After installation, go to **System Settings** > **Printers & Scanners** and add your HP LaserJet Professional P1102w printer.

## Troubleshooting

### Printer shows "Software Incompatible"

If the printer queue says **Software Incompatible** or "The printer software is not compatible with this device", and jobs stop with "Data" failed, Rosetta is missing. This is the usual result of upgrading an Apple silicon Mac to macOS 27, and installing Rosetta fixes it (confirmed on macOS 27.2):

1. Run `sudo softwareupdate --install-rosetta --agree-to-license` in Terminal.
2. In **System Settings** > **Printers & Scanners**, remove the P1102w and add it again.
3. Print a test page.

If you want to confirm the cause first, `/var/log/cups/error_log` will contain `Bad CPU type in executable` for `rastertozjs`.

### Future macOS releases

Apple has said Rosetta will only be generally available through macOS 27. HP's driver is Intel-only and can't be recompiled, so it may stop working on Apple silicon in a later macOS release regardless of how it's packaged.

## How the package is built

*   [`package/Distribution`](package/Distribution) is the installer definition used in the package. Compared with HP's original, it removes the `InstallationCheck()` script that rejected newer macOS versions.
*   [`tools/replace_distribution.py`](tools/replace_distribution.py) swaps that file into the package without touching the HP driver payload.
*   The [release workflow](.github/workflows/release.yml) builds the package, signs it with a Developer ID Installer certificate and notarizes it with Apple when those secrets are configured, and publishes it as a GitHub release. Run it from the **Actions** tab with **Run workflow**.

## Disclaimer

This driver package is a community modification and is **not officially supported by HP Inc.** Use at your own discretion. While care has been taken to ensure functionality, there are no guarantees, and neither the creator nor contributors are liable for any issues that may arise from its use.
