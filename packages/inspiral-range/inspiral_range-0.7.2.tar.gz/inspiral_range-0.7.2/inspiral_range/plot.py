import numpy as np

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from .inspiral_range import sensemon_range


def plot_spectra(freq, psd, H, z, title=None, fig=None):
    dlum = metrics['horizon'][0]

    z = inspiral_range.horizon_redshift(freq, psd, H=H)
    int73 = sensemon_range(freq, psd, integrate=False)
    hfreq, habs = H.z_scale(z)

    label = r"{} {}/{} $\mathrm{{M}}_\odot$ {:0.0f} Mpc".format(
        H.params['approximant'],
        H.params['m1'], H.params['m2'],
        dlum,
    )

    if not fig:
        fig = plt.figure()

    gs = GridSpec(2, 1, height_ratios=(2, 1), hspace=0)
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1])
    ax1.sharex(ax0)
    ax0.loglog(freq, np.sqrt(psd), label="strain noise ASD")
    # put waveform in same units as noise strain
    ax0.loglog(hfreq, habs*2*np.sqrt(hfreq), linestyle='--', label=label)
    ax1.semilogx(freq, int73, color='C2', label="sensemon range ASD")
    ax1.grid()
    ax0.grid()
    ax0.set_ylabel(u"Strain [1/\u221AHz]")
    ax0.tick_params(labelbottom=False)
    ax1.set_ylabel(u"Range [Mpc/\u221AHz]")
    ax1.set_xlabel("Frequency [Hz]")
    ax0.legend()
    ax1.legend()
    # h0, l0 = ax0.get_legend_handles_labels()
    # h1, l1 = ax1.get_legend_handles_labels()
    # ax0.legend(h0+h1, l0+l1)
    if title:
        ax0.set_title(title)

    return fig
