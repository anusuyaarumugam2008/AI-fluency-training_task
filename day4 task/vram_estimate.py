"""
Day 4 Task - Will It Fit, and May I Use It?

Estimates:
- Model weights
- KV cache
- Total memory
- Whether the model fits available memory

It also compares:
- Context lengths
- Quantization levels
"""

# Bytes per parameter for common model precisions
BYTES_PER_PARAM = {
    "FP16": 2.00,
    "Q8_0": 1.00,
    "Q6_K": 0.81,
    "Q5_K_M": 0.68,
    "Q4_K_M": 0.57,
    "Q3_K_M": 0.43,
}

# Approximate KV-cache cost
# 0.02 GB for every 1B parameters per 1K tokens
KV_GB_PER_B_PER_1K = 0.02

# Runtime overhead
OVERHEAD = 1.10


def estimate(params_b, precision="Q4_K_M", context_k=8):
    """
    Estimate memory required by a model.

    Returns:
        weights_gb
        kv_gb
        total_gb
    """

    if precision not in BYTES_PER_PARAM:
        raise ValueError(
            f"Unknown precision: {precision}. "
            f"Choose from {list(BYTES_PER_PARAM.keys())}"
        )

    # Model weights
    weights_gb = params_b * BYTES_PER_PARAM[precision]

    # KV cache
    kv_gb = params_b * context_k * KV_GB_PER_B_PER_1K

    # Total memory including 10% overhead
    total_gb = (weights_gb + kv_gb) * OVERHEAD

    return weights_gb, kv_gb, total_gb


def verdict(total_gb, available_gb):
    """Check whether the model fits available memory."""

    if total_gb <= available_gb * 0.7:
        return "fits comfortably"

    if total_gb <= available_gb:
        return "fits, but tight"

    return "does NOT fit"


def report(name, params_b, precision, context_k, available_gb):
    """Print a formatted memory report."""

    weights, kv, total = estimate(
        params_b,
        precision,
        context_k
    )

    result = verdict(total, available_gb)

    print(
        f"{name:<22} "
        f"{precision:<8} "
        f"{params_b:>5.1f}B "
        f"ctx {context_k:>3}K "
        f"weights {weights:>6.2f} GB "
        f"KV {kv:>5.2f} GB "
        f"total {total:>6.2f} GB "
        f"-> {result}"
    )


def context_experiment(params_b, precision, available_gb):
    """Compare different context lengths."""

    print("\n" + "=" * 75)
    print("CONTEXT LENGTH EXPERIMENT")
    print("=" * 75)

    for context_k in (4, 8, 16, 32, 128):
        report(
            "8B model",
            params_b,
            precision,
            context_k,
            available_gb
        )


def quantization_experiment(params_b, context_k, available_gb):
    """Compare different quantization levels."""

    print("\n" + "=" * 75)
    print("QUANTIZATION EXPERIMENT")
    print("=" * 75)

    for precision in (
        "Q3_K_M",
        "Q4_K_M",
        "Q5_K_M",
        "Q6_K",
        "Q8_0",
        "FP16"
    ):
        report(
            "8B model",
            params_b,
            precision,
            context_k,
            available_gb
        )


if __name__ == "__main__":

    # Change this to your actual available RAM/VRAM.
    AVAILABLE_GB = 8.0

    print("=" * 75)
    print("DAY 4 - VRAM / MEMORY ESTIMATOR")
    print("=" * 75)

    print(f"\nAvailable memory: {AVAILABLE_GB} GB\n")

    # ---------------------------------------------------------
    # MAIN MODEL ESTIMATES
    # ---------------------------------------------------------

    print("=" * 75)
    print("MODEL MEMORY ESTIMATES")
    print("=" * 75)

    report(
        "Small model",
        1.5,
        "Q4_K_M",
        8,
        AVAILABLE_GB
    )

    report(
        "Mid model",
        8.0,
        "Q4_K_M",
        8,
        AVAILABLE_GB
    )

    report(
        "Mid model FP16",
        8.0,
        "FP16",
        8,
        AVAILABLE_GB
    )

    report(
        "Large model",
        30.0,
        "Q4_K_M",
        8,
        AVAILABLE_GB
    )

    report(
        "Server model",
        70.0,
        "Q4_K_M",
        8,
        AVAILABLE_GB
    )

    # ---------------------------------------------------------
    # CONTEXT EXPERIMENT
    # ---------------------------------------------------------

    context_experiment(
        params_b=8.0,
        precision="Q4_K_M",
        available_gb=AVAILABLE_GB
    )

    # ---------------------------------------------------------
    # QUANTIZATION EXPERIMENT
    # ---------------------------------------------------------

    quantization_experiment(
        params_b=8.0,
        context_k=8,
        available_gb=AVAILABLE_GB
    )

    # ---------------------------------------------------------
    # CUSTOM MODELS
    # ---------------------------------------------------------

    print("\n" + "=" * 75)
    print("CUSTOM SCENARIO")
    print("=" * 75)

    report(
        "Recommended model",
        8.0,
        "Q4_K_M",
        8,
        AVAILABLE_GB
    )

    report(
        "Fallback model",
        1.5,
        "Q4_K_M",
        8,
        AVAILABLE_GB
    )