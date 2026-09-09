"""
Shared model-execution configuration for the Qwen3.5-4B causal-LM pipeline
-- the one place BitsAndBytesConfig's exact shape is defined, reused by
train.py, evaluate_real.py, and probe_adversarial.py rather than typed
three times where the copies could drift. See docs/decisions/PDR-012.md
for why this project moved off flan-t5-base onto 4-bit QLoRA in the first
place, and training/SETUP.md for the confirmed-working bitsandbytes/peft
versions this config depends on.

Deliberately separate from prepare_data.py: that module's own concerns are
dataset iteration, schema validation, and tokenization -- it only ever
needs a tokenizer, never torch/bitsandbytes directly. This module is the
opposite: nothing here touches datasets or tokenization, only how the
model itself gets loaded for training or inference. Split out this way
per review_bridge/ round 5 (2026-09-09) -- Gemini's objection to putting
`build_bnb_config()` in prepare_data.py instead, upheld.
"""
import torch
from transformers import BitsAndBytesConfig


def build_bnb_config() -> BitsAndBytesConfig:
    """The exact 4-bit quantization shape Stage 0 confirmed working on the
    product owner's actual RTX 5060 (see PDR-012: Qwen3.5-4B, 4.66GB/7.93GB
    peak) -- one function so train.py's real training load and
    evaluate_real.py/probe_adversarial.py's inference-time reload can
    never drift apart from each other."""
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
