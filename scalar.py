# ruff: noqa
# adapted from https://github.com/kach/memo/blob/main/demo/Memonomicon.ipynb and made more clear by making variable names unique
# also extended to include another utterance option ("most")

# %%

import jax
import jax.numpy as np
from memo import memo

N = list(range(0,10))  # number of nice people
U = [0, 1, 2, 3]     # utterance: {none, some, most, all} of the people are nice

@jax.jit
def utterance_means_n(u, n):  # (none)  (some)  (most)  (all)
    return np.array([
        n == 0,
        n > 0,
        n > max(N)/2,
        n == max(N)
    ])[u]

# per https://github.com/kach/memo/blob/main/memo/comic.py and figure 4 in https://dl.acm.org/doi/pdf/10.1145/3763078:
# - orange marks choices that are uncertain in the frame
# - blue marks choices that are known in the frame
# - dashed arrow marks conditioning 
@memo(save_comic="scalar")
def scalar[given_n: N, given_u: U](beta):
    # We consider both a speaker and a listener.
    cast: [speaker, listener]

    # The listener thinks that:
    listener: thinks[
        # the speaker, having been given some target n items (with a uniform prior),
        speaker: given(speaker_n in N, wpp=1),

        # has chosen an utterance imagining that,
        speaker: chooses(speaker_u in U, wpp=imagine[
            # the listener--
            # hearing the utterance,
            listener: knows(speaker_u),
            # and estimating n based on what is accurate for the utterance--
            listener: chooses(listener_n in N, wpp=utterance_means_n(speaker_u, listener_n)),
            # will expect the utterance to have been chosen based on[^1] that estimated n (i.e., will expect the speaker to have intended to be informative to some degree).
            exp(beta * E[speaker_n == listener.listener_n])
            # [1]: "based on" = for the listener, the probability of each possible utterance is weighted by beta, so that the relative probability of each utterance (based on the listener's estimated n) is a free parameter. As a result, we could model listeners who are more or less likely to assume that the speaker is intending to be informative, by varying beta. (Here, we're specifically using the softmax function.)
        ])
    ]

    # With this mental model, we establish that the listener now knows that the utterance is the currently specified one
    listener: observes [speaker.speaker_u] is given_u
    # and the listener selects an n for themselves based on the expected value of each n in their representation of the speaker
    listener: chooses(listener_guess_n in N, wpp=E[speaker.speaker_n == listener_guess_n])
    listener: INSPECT()
    return E[listener.listener_guess_n == given_n]


from matplotlib import pyplot as plt
plt.plot(scalar(1), label=['none', 'some', 'most', 'all'])
plt.xlabel('Number of nice people')
plt.ylabel('Posterior probability')
plt.legend()
None
