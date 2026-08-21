# Training environment setup

## Where the venv actually lives, and why

**Not** at `training/venv/`, despite that being the natural default and
what earlier docs assumed before this was actually built. It lives at:

```
C:\Users\thisi\.venvs\intent-recovery-v2
```

Reason: `torch`'s CUDA wheel bundles a deeply-nested `licenses/third_party/...`
directory tree (kineto → dynolog → prometheus-cpp → civetweb → duktape,
several levels deep). Combined with this project's own path length under
`OneDrive\Desktop\intent-recovery-model-v2\training\venv\...`, the full
path exceeds Windows' 260-character limit and `pip install` fails with
`OSError: [WinError 206] The filename or extension is too long`. Fixing
this properly means enabling Windows long-path support
(`HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled`),
which needs admin rights and is a machine-wide change, not something to
flip silently for one project. Moving the venv to a short path outside
`OneDrive` sidesteps it entirely — and is arguably better practice anyway,
since a multi-GB ML environment inside a OneDrive-synced folder means
OneDrive tries to sync all of it.

If you ever want the "real" fix instead: enable long paths yourself
(Group Policy or registry, as admin), then the venv can move back under
`training/venv/` if preferred. Until then, use the path above.

## Setup from scratch

```powershell
python -m venv C:\Users\thisi\.venvs\intent-recovery-v2
C:\Users\thisi\.venvs\intent-recovery-v2\Scripts\python.exe -m pip install --upgrade pip

# CUDA build of torch first, from PyTorch's own index -- plain
# `pip install torch` (or installing requirements.txt on its own) gets you
# the CPU-only build instead, silently. Check download.pytorch.org/whl/
# for the current highest cuNNN tag if this project's GPU driver changes;
# this repo's GPU is an RTX 5060, currently matched to cu132.
C:\Users\thisi\.venvs\intent-recovery-v2\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu132

# Everything else, from regular PyPI
C:\Users\thisi\.venvs\intent-recovery-v2\Scripts\python.exe -m pip install transformers sentencepiece accelerate numpy
```

## Running the pipeline

From `training/`, using the venv's own interpreter directly (not `cd` into
the venv, since it isn't inside this directory):

```powershell
C:\Users\thisi\.venvs\intent-recovery-v2\Scripts\python.exe prepare_data.py
C:\Users\thisi\.venvs\intent-recovery-v2\Scripts\python.exe train.py
```

## Verifying CUDA is actually being used

```powershell
C:\Users\thisi\.venvs\intent-recovery-v2\Scripts\python.exe -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

Should print `True NVIDIA GeForce RTX 5060`. If it ever prints `False`,
something reinstalled the CPU-only wheel over the CUDA one — rerun the
`pip install torch --index-url ...` line above.
