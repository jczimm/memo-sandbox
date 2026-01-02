# %%
# Reimplement the tug-of-war model from gabegrand/world-models using the memo DSL
import jax
import jax.numpy as np
from memo import memo
import matplotlib.pyplot as plt
from typing import no_type_check

# Discretize strength, effort, and laziness for memo's discrete choices
strength_levels = np.linspace(0, 100, num=4, endpoint=True)  # 0..100
effort_levels = np.concat([
    strength_levels / 2,
    np.max(strength_levels / 2) + strength_levels / 2
])  # 0..100, but with twice the precision, since half-strength can be applied (in cases that lazy1 == 1)
laziness_levels = np.linspace(0, 1, num=4, endpoint=True) # 0..1
lazy_levels = np.array([0, 1])

# %%
# *for optimization, LLM translator should be instructed to use jax.jit functions, e.g. for PDFs
@jax.jit
def strength_pdf(st):
    # return np.exp(-0.5 * ((st - 50)/20)**2)
    return jax.scipy.stats.norm.pdf(st, 50, 20)

@jax.jit
def lazy_pdf(lazy, laziness):
    # return (lazy == 1) * laziness + (lazy == 0) * (1 - laziness)
    # return jax.scipy.stats.bernoulli.pmf(lazy, laziness)
    return np.array([1-laziness, laziness])[lazy]

@jax.jit
def eff_pdf(eff, lazy, st):
    # return (eff == st / 2 if lazy == 1 else eff == st)
    # return (lazy == 1) * (eff == st / 2) + (lazy == 0) * (eff == st)
    # *might need some examples of how to convert from more imperative to more declarative definitions, if needed for performance
    # maybe jax.lax.cond would be more efficient
    return np.array([eff == st, eff == st / 2])[lazy]

@jax.jit
def team_strength(team):
    return np.add.reduce(np.array([player.eff for player in team]))

@jax.jit
def won_against(team1, team2):
    return team_strength(team1) > team_strength(team2)

# ruff: noqa
@no_type_check
@memo
def tug_of_war[S: strength_levels]():
    # cast: [tom, john, mary, sue, obs]
    
    obs: thinks[ # *need to model an observer thinking so we're explicitly querying as an observer
        # *note that we're explicitly setting up the characters, whereas in Church you don't have to, and you just declare character properties using memoized functions which are called by team-strength. there may be a way to do this over an array, but then we're referring to characters by index and it becomes less expressive, which might be harder for the NL-to-PLoT translator
        tom: given(st in strength_levels, wpp=strength_pdf(st)),
        john: given(st in strength_levels, wpp=strength_pdf(st)),
        mary: given(st in strength_levels, wpp=strength_pdf(st)),
        sue: given(st in strength_levels, wpp=strength_pdf(st)),
        
        tom: given(laziness in laziness_levels, wpp=1),
        john: given(laziness in laziness_levels, wpp=1),
        mary: given(laziness in laziness_levels, wpp=1),
        sue: given(laziness in laziness_levels, wpp=1),
        
        tom: given(lazy in lazy_levels, wpp=lazy_pdf(lazy, laziness)),
        # *can't say tom.laziness, must just be laziness!
        john: given(lazy in lazy_levels, wpp=lazy_pdf(lazy, laziness)),
        mary: given(lazy in lazy_levels, wpp=lazy_pdf(lazy, laziness)),
        sue: given(lazy in lazy_levels, wpp=lazy_pdf(lazy, laziness)),

        tom: chooses(eff in effort_levels, wpp=eff_pdf(eff, lazy, st)),
        john: chooses(eff in effort_levels, wpp=eff_pdf(eff, lazy, st)),
        mary: chooses(eff in effort_levels, wpp=eff_pdf(eff, lazy, st)),
        sue: chooses(eff in effort_levels, wpp=eff_pdf(eff, lazy, st))
    ]

    obs: observes_that[tom.eff > john.eff]
    # obs: observes_that [won_against(team(tom), team(john))]
    # *note that at time of writing (25-12-24), we can't pass entire cast members to functions, only choices, limiting the expressivity of our PPL code translation

    obs: observes_that[(john.eff + mary.eff) > (tom.eff + sue.eff)]
    # obs: observes_that [won_against(team(john, mary), team(tom, sue))]

    obs: knows(S) # *push the current support value to the observer
    return obs[Pr[mary.st == S]] # *now query in the observer's frame

# *maybe the llm translation layer should thoroughly learn the DSL parser to know the rules, or maybe do trial and error to learn for itself where the pitfalls are
# also maybe the llm translation layer should learn how to convert from imperative (Church-like) PPL code to declarative (memo) code

@memo
def get_cost():
    return cost @ tug_of_war()

choices = [strength_levels, effort_levels, laziness_levels, lazy_levels]
choices_arithmetic = " * ".join(str(len(c)) for c in choices)
choices_count = np.multiply.reduce(np.array([len(c) for c in choices]))
print(f"total choices = {choices_arithmetic} = {choices_count}")

flops = get_cost()
print(f"FLOPs = {format(flops)}")
print(f"Avg FLOPs per choice = {format(flops/choices_count)}")

# estimate memory needed?

# %%
# Call the memo and plot Mary's posterior over strength_levels
post = tug_of_war()  # array over strength_levels S
s_vals = np.array(list(strength_levels))
plt.figure(figsize=(8,4))
plt.bar(s_vals, np.array(post), width=1.0)
plt.xlabel('Mary strength')
plt.ylabel('Posterior probability')
plt.title("Posterior over Mary's strength (memo conditioned)")
plt.xlim(0,100)
plt.show()

# %%
