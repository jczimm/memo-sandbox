# TODO

## `webppl vs memo/`

0. extract paper results
1. reproduce using webppl mcmc
2. reproduce using webppl mcmc discrete
3. reproduce using webppl enumerate
    - [x] determine if need to use (1,10) (or another variant) instead of [1,10] for strength prior. I think we should be able to use [1,10] unless we see mismatch with original method
        - [c] not sure why P jumps to 1 so fast after F,F;F,F!
        - [x] figure out how the mcmc mode of my current debugging webppl version diverged from the original mcmc version (reproduced at top)
        - _If want more reliable MCMC results: for MCMC versions, use 10 iterations to recreate paper's method of avging across 10 model runs_
        - **~~seems like we'll need to avoid one of the extremes to prevent startingE from being chosen as 1!~~
        - OR we can see if increasing precision fixes things - Claude thinks that **small error in strength estimates (due to discretization) could be amplified by the equilibrium-finding process**, so we need greater precision.
            - NOTE: if we use memo frames instead of game-theoretic nested optimization, then maybe this isn't a problem anymore
            - -> deciding that [1,10] is sufficient since it's not actually the source of discrepancy; the source is discretization itself... see explanation from Claude below. **choosing to skip now to memo, where I can have very high precision more easily, to see if that matches the original (continuous) MCMC model's startingE_table and final_table**

    > 1. Posterior Mean Mismatch
    >     - Continuous (MCMC): Posterior mean might be 2.347
    >     - Discrete (0.1 steps): Posterior can only represent 2.3 or 2.4, so mean ≈ 2.35
    >     - Small error in mean strength propagates forward
    > 2. Critical Thresholds
    >     - Joint lifting condition: effort_a × strength_a + effort_b × strength_b ≥ 5
    >     - Near threshold boundaries (e.g., strength 2.5-7), small discretization errors  flip lift outcomes from success→fail or vice versa
    >     - This creates discontinuous jumps in expected utility
    > 3. Cascade Through Equilibrium Finding
    >     - jointUtility averages lift2() over all posterior samples: listMean(map2(lift2, strength_a, strength_b))
    >     - Discrete approximation of this average differs from continuous
    >     - The nested best-response iteration (lines 163-210) magnifies this error
    >     - Different expected lift probabilities → different optimal efforts → different  equilibria
    > 4. Amplification
    >     - Small error in posterior mean (0.05 units)
    >     - → Different lift probabilities (5-10% difference)
    >     - → Different equilibrium efforts (0.1-0.2 difference)
    >     - → Large divergence in final joint utility and outcome probability
    >
    > Why it matters most in mid-range (2.5-7): This is where the lift threshold creates maximum sensitivity—agents transition from "can only jointly lift" to "can lift solo," making the utility function most nonlinear.

4.
    - [x] finish memo enumerate, so that it matches webppl enumerate given the same parameters  (xiang2023-exp1-round3-memo.qmd), but higher precision; and log all the stats (see `stats`) -- and investigate discrepancies. e.g. why is Joint utility at optimum so high? why are the agents' utilities different from each other? (~~**compare final P, aU, bU, aE, bE between original version and the memo version**~~)
        - I think the MCMC version is the wrong one, since the outcomes of enumerate webppl exactly match those of the enumerate memo across all scenarios! I'm deciding that not trying to match MCMC but matching the original implementation. I could argue that one issue with MCMC is that it's imprecise or could have systematic error maybe (e.g., due to autocorrelation?) that's amplified during equilibrium finding. next I need to 
        - [x] double-check parity between enumerate versions- compare all the specific stats for the memo enumerate version and the webppl enumerate version, and plot them together like I do with `compare_results`

5.
    - [x] modify memo joint effort model to implement solitary effort and compensatory effort models, and check that the P results match up with the P results from the paper (simple, no need to validate incrementally)
6.
    - [x] try modified joint effort model (as used in supplement)

### Further Ideas

- [ ] modify memo implementation so that the equilibrium-finding process uses memo frames in order to model agent's uncertainty about each other in the equilibrium-finding step (still accelerated by JAX, but now in the language of memo, and considering the uncertainty)
  - _this would be a tweak to the model's implementation_
  - _see related notes at end of xiang2023-exp1-round3-memo.qmd_

- [ ] try refitting alpha, beta, and k(safe model) parameters to our data (to validate the modeling approach; keeping these constant makes sense for the purpose of a replication of the model (to the extent that this makes any sense... since we're not measuring model fit), but refitting the parameters makes sense for replicating the _modeling approach_)

- [ ] try transforming utility with a proper convex utility function (possibly incorporating previously earned rewards as well), per utility/prospect theory
  - _this would be an extension of the model_

## `xiang2023-extension/`

- [-] patch the linting modifications to xiang2023-exp1-round3-memo.qmd onto xiang2023-extension/xiang2023-exp1-round3-memo.qmd (so it matches and is clean) and rename it to xiang2023-extension/add_perceived_effort.qmd
