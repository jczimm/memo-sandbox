# Tracing Guide: Comparing WebPPL and Memo Equilibrium Finding

> [!WARNING]
> Disclaimer: Large portions of this section were written in collaboration with Claude Code and verified and edited for accuracy by the author. Of course, author takes responsibility for any inaccuracies and strongly welcomes corrections.

This guide explains how to use the detailed tracing features added to both the WebPPL and memo implementations to validate that they follow identical execution paths.

## Purpose

The tracing capability allows you to see exactly how the recursive equilibrium-finding algorithm executes, step-by-step. This is useful for:

- Validating that WebPPL and memo implementations are equivalent
- Debugging convergence issues
- Understanding the recursive best-response dynamics
- Comparing execution traces between implementations

## How to Enable Tracing

### In WebPPL (`xiang2023-exp1-round3-with-debugging.wppl`)

Set the configuration variable at the top of the file:

```javascript
// Line 6
var ENABLE_TRACE = true  // Change from false to true
```

### In Python/Memo (`xiang2023-exp1-round3-memo.qmd`)

Pass `trace=True` when calling `find_equilibrium`:

```python
effort_a, effort_b, depth = find_equilibrium(
    strength_a, strength_b,
    init_effort=0.0,
    trace=True  # Enable tracing
)
```

## What the Trace Shows

Both implementations produce identical trace output showing:

### 1. Initial Call

```
=== find_equilibrium(init_effort=0.0000) ===
```

### 2. Recursive Function Calls

```
  b(depth=0): Using init_effort = 0.0000
  a(depth=1): B's effort from b(0) = 0.0000
  a(depth=1): A's best response = 0.2500
  b(depth=1): A's effort from a(1) = 0.2500
  b(depth=1): B's best response = 0.2500
```

This shows:

- `b(0)` returns the initial effort
- `a(1)` calls `b(0)`, gets 0.0, computes optimal response 0.25
- `b(1)` calls `a(1)`, gets 0.25, computes optimal response 0.25

### 3. Convergence Check

```
findDepth(1): b(1)=0.2500, b(2)=0.2500, diff=0.0000, converged=True
```

This shows:

- Testing convergence at depth=1
- Comparing `b(1)` vs `b(2)`
- Difference is 0.0, less than threshold 0.06
- Converged!

### 4. Final Efforts (if verbose=True)

```
Converged at depth 1: effort_a=0.2500, effort_b=0.2500
```

## Example: Full Trace for Simple Case

For a case where agents have equal strength and converge immediately:

```
=== find_equilibrium(init_effort=0.0000) ===
  b(depth=0): Using init_effort = 0.0000
  a(depth=1): B's effort from b(0) = 0.0000
  a(depth=1): A's best response = 0.2500
  b(depth=1): A's effort from a(1) = 0.2500
  b(depth=1): B's best response = 0.2500
findDepth(1): b(1)=0.2500, b(2)=0.2500, diff=0.0000, converged=True
Converged at depth 1: effort_a=0.2500, effort_b=0.2500
```

## Comparing WebPPL vs Memo Traces

To verify the implementations are identical:

1. **Enable tracing in both implementations**
2. **Run with same parameters** (same strength values, init_effort, effort discretization)
3. **Compare the traces line-by-line**

The traces should be identical except for:

- Minor formatting differences (Python uses `f"{value:.4f}"`, WebPPL uses `value.toFixed(4)`)
- The memo version may have array/list representations slightly different

### Key Values to Compare:

- ✅ All `a(depth=X)` outputs
- ✅ All `b(depth=X)` outputs
- ✅ Convergence depths
- ✅ Final equilibrium efforts

## Understanding the Recursive Structure

The trace reveals the key recursive pattern:

```
Call Chain for findDepth(1):
  findDepth(1)
    → b(1)
      → a(1)
        → b(0) [returns init_effort]
      ← returns effort_a
    ← returns effort_b
    → b(2)
      → a(2)
        → b(1) [cached or recomputed]
      ← returns effort_a
    ← returns effort_b
    → compare b(1) vs b(2)
```

## Performance Note

Tracing adds significant output overhead. For production runs with many equilibrium computations:

- Keep `ENABLE_TRACE = false` (WebPPL)
- Keep `trace=False` (Python/Memo)

Only enable tracing for debugging or validation purposes.

## Implementation Details

### WebPPL Version

- Uses JavaScript closure to capture `trace` parameter
- Trace flag passed through `ENABLE_TRACE` global variable
- Outputs via `display()` function

### Python/Memo Version

- Uses Python nested functions with closure
- Trace flag passed as function parameter
- Outputs via `print()` function
- Has both recursive (`find_equilibrium`) and iterative (`find_equilibrium_iterative`) versions

The recursive Python version (`find_equilibrium`) exactly mirrors the WebPPL structure for maximum fidelity.
