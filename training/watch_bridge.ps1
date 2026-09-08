# Live-tails review_bridge/transcript.log with color by section, so a
# review_bridge/ round (training/gemini_bridge.py) is easy to follow in a
# split VS Code terminal: what was sent vs. what came back vs. cost/usage.
#
# Usage (from the repo root):
#   .\training\watch_bridge.ps1
#
# Color persists across a block's continuation lines (e.g. a multi-line
# Gemini reply) until the next recognized header line, since only the first
# line of each block carries a [TAG].

param(
    [string]$Path = "review_bridge\transcript.log"
)

if (-not (Test-Path $Path)) {
    New-Item -ItemType File -Path $Path -Force | Out-Null
}

Write-Host "Watching $Path -- Ctrl+C to stop." -ForegroundColor DarkGray
$color = "Gray"

# Lines now carry an optional leading [HH:MM:SS] stamp before the [TAG],
# e.g. "[14:02:11] [SENDING] ...". Match the tag regardless of the stamp.
$stamp = '(\[\d\d:\d\d:\d\d\] )?'

Get-Content -Wait -Path $Path | ForEach-Object {
    if ($_ -match '^===') { $color = 'Magenta' }
    elseif ($_ -match "^$stamp\[SENDING\]|^$stamp\[PROMPT\]|^$stamp\[STATUS\]") { $color = 'Cyan' }
    elseif ($_ -match "^$stamp\[GEMINI (REPLY|RESPONSE)\]") { $color = 'Green' }
    elseif ($_ -match "^$stamp\[USAGE\]") { $color = 'Yellow' }
    elseif ($_ -match "^$stamp\[ERROR\]|^$stamp\[STDERR\]") { $color = 'Red' }
    elseif ($_ -match "^$stamp\[WRITTEN\]") { $color = 'DarkGray' }
    elseif ($_ -eq '') { $color = 'Gray' }

    Write-Host $_ -ForegroundColor $color
}
