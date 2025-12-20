# memo-sandbox

Sandbox environment for building up memo models alongside reference examples (both in memo and in WebPPL).

## `webppl vs memo/`

| File | Description |
| --- | --- |
| **`index.qmd`** | landing page |
| **`webppl.qmd`** | implementation of two basic models in webppl |
| **`memo.qmd`** | implementations of same two basic models in memo |
| **`xiang2023-exp1-round3.qmd`** | Xiang2023 models for experiment 1, round 3, in WebPPL, _supporting both MCMC (original) and enumeration (new) solution methods_ |
| `xiang2023-exp1-round3_ORIGINAL.wppl` | Xiang2023 models for experiment 1, round 3, in WebPPL (original code recreated in wppl file format, for comparison to `xiang2023-exp1-round3-with-debugging.wppl`). _Only supports MCMC method_ |
| `xiang2023-exp1-round3-with-debugging.wppl` | Xiang2023 models for experiment 1, round 3, in WebPPL with modifications to support debugging (also see `TRACING_GUIDE.md`). _Supports both MCMC and enumeration_ |
| `TRACING_GUIDE.md` | Guide to using the debugging features implemented in `xiang2023-exp1-round3-with-debugging.wppl` and `xiang2023-exp1-round3-memo.qmd` to verify their results equivalence |
| **`xiang2023-exp1-round3-memo.qmd`** | Xiang2023 models for experiment 1, round 3, reimplemented in memo. _Only supports enumeration method_ |
| **`xiang2023-exp1-round3-model_fits_results.csv`** | Predictions from the models defined in `xiang2023-exp1-round3-memo.qmd` |
| `*.png` | Diagrammatic representations of memo models |

> [!INFO]
> See https://github.com/psyc-201/xiang2023 for more information regarding the models for the replication of Xiang2023.
> 
> **`xiang2023-exp1-round3-memo.qmd`** is all that is necessary to reproduce the model fit results, **`xiang2023-exp1-round3-model_fits_results.csv`**. These model fit results are all that is necessary for reproducing the Xiang2023 replication. The remaining files are for reference in comparing WebPPL and memo implementations of probabilistic models, and for tracing the model's intermediate results to verify the equivalence between the WebPPL and memo models of Xiang2023 experiment 1 round 3.

## Usage

- First, set up environment using `pixi install`
- Can preview using `pixi run preview`
- Can render using `pixi run render`
- To deploy rendered documents, render locally then deploy the rendered files

## References

Xiang, Y., Vélez, N., & Gershman, S. J. (2023). Collaborative decision making is grounded in representations of other people’s competence and effort. _J. Exp. Psychol. Gen._, _152_(6), 1565–1579.
