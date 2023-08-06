import os
import logging
import argparse
import numpy as np

from . import __version__
from . import logger
from . import inspiral_range

logger.setLevel(os.getenv('LOG_LEVEL', 'WARNING').upper())
formatter = logging.Formatter(
    '%(asctime)s.%(msecs)d %(message)s',
    datefmt='%H:%M:%S',
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

##################################################

description = """Calculate GW detector inspiral range from ASD/PSD

Strain spectra data should be two-column ASCII, (freq, strain), and
may be given in amplitude or power (ASD or PSD).  The --divisor option
can be used to specify a scalar converstion for e.g. meters to strain.

Inspiral waveform parameters are specified as PARAM=VALUE pairs.  Mass
('m1'/'m2') parameters are assumed to be in solar masses (Msolar)
Default: m1 = m2 = 1.4 Msolar.

"""

def parse_params(clparams):
    params = {}
    for param in clparams:
        try:
            k, v = param.split('=')
        except ValueError:
            raise ValueError("Could not parse parameter: {}".format(param))
        try:
            params[k] = float(v)
        except ValueError:
            params[k] = v
    return params


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
)


class FileAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'file', values)
        setattr(namespace, 'stype', self.dest)
        delattr(namespace, 'asd')
        delattr(namespace, 'psd')


class ParamsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            params = parse_params(values)
        except ValueError as e:
            parser.error(e)
        setattr(namespace, self.dest, params)


igroup = parser.add_mutually_exclusive_group(required=True)
igroup.add_argument(
    '-a', '--asd', action=FileAction,
    help="assume noise spectrum is ASD")
igroup.add_argument(
    '-p', '--psd', action=FileAction,
    help="assume noise spectrum is PSD")
parser.add_argument(
    '-d', '--divisor', default=1, type=float,
    help="factor to divide PSD (e.g. convert displacement to strain)")
ogroup = parser.add_mutually_exclusive_group()
ogroup.add_argument(
    '-f', '--format', dest='fmt', choices=['txt', 'json', 'yaml'], default='txt',
    help="output format (default: txt)")
ogroup.add_argument(
    '-s', '--single', metavar='FUNC',
    help="print output from single function only")
parser.add_argument(
    '--plot', action='store_true',
    help="plot the spectrum and the waveform")
parser.add_argument(
    '-v', '--version', action='version', version=__version__,
    help="output value of specific calculation only (from available inspiral_range functions)")
parser.add_argument(
    'params', metavar='PARAM=VALUE', nargs='*', action=ParamsAction,
    help="waveform parameters")


def main():
    args = parser.parse_args()

    data = np.loadtxt(args.file)
    freq = data[1:, 0]
    psd = data[1:, 1]
    psd /= args.divisor
    if args.stype == 'asd':
        psd **= 2

    metrics, H = inspiral_range.all_ranges(freq, psd, **args.params)

    if args.single:
        print(metrics[args.single][0])
    elif args.fmt == 'txt':
        print('metrics:')
        fmt = '  {:18} {:.3f} {}'
        for r, v in metrics.items():
            print(fmt.format(r+':', v[0], v[1] or ''))
        print('waveform:')
        fmt = '  {:18} {}'
        for p, v in H.params.items():
            print(fmt.format(p+':', v))
    else:
        out = {'metrics': dict(metrics), 'waveform': dict(H.params)}
        if args.fmt == 'json':
            import json
            print(json.dumps(out))
        elif args.fmt == 'yaml':
            import yaml
            print(yaml.safe_dump(out, default_flow_style=False))
        else:
            parser.error("Unknown output format: {}".format(args.fmt))

    if args.plot:
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec
        import signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        asd = np.sqrt(psd)
        # calc waveform strain
        dlum = metrics['range'][0]
        z = inspiral_range.horizon_redshift(freq, psd, H=H)
        hfreq, habs = H.z_scale(z)
        # put waveform in same units as noise strain
        habs *= 2*np.sqrt(hfreq)
        # limit the waveform plot range
        hmin = min(asd) / 100
        hind = np.where(habs > hmin)[0]
        hfreq = hfreq[hind]
        habs = habs[hind]
        find = np.where((hfreq >= freq[0]) & (hfreq <= freq[-1]))[0]
        hfreq = hfreq[find]
        habs = habs[find]
        # sensemon range integrand
        int73 = inspiral_range.sensemon_range(
            freq, psd, m1=H.params['m1'], m2=H.params['m2'], integrate=False,
        )
        # plot
        label = r"{} {}/{} $\mathrm{{M}}_\odot$ @ {:0.0f} Mpc".format(
            H.params['approximant'],
            H.params['m1'], H.params['m2'],
            dlum,
        )
        fig = plt.figure()
        gs = GridSpec(2, 1, height_ratios=(2, 1), hspace=0)
        ax0 = fig.add_subplot(gs[0])
        ax1 = fig.add_subplot(gs[1])
        ax1.sharex(ax0)
        ax0.loglog(freq, asd, label="strain noise ASD")
        ax0.loglog(hfreq, habs, linestyle='--', label=label)
        ax1.semilogx(freq, int73, label="sensemon range ASD")
        ax0.autoscale(enable=True, axis='x', tight=True)
        ax0.grid()
        ax1.grid()
        ax0.set_title(f"{args.file}")
        ax0.set_ylabel(u"Strain [1/\u221AHz]")
        ax0.tick_params(labelbottom=False)
        ax1.set_ylabel(u"Range [Mpc/\u221AHz]")
        ax1.set_xlabel("Frequency [Hz]")
        ax0.legend()
        ax1.text(
            0.985, 0.94, "SenseMon range integrand",
            transform=ax1.transAxes, ha="right", va="top", size=10,
            bbox=dict(boxstyle="round", fc="w", ec="0.7", alpha=0.7),
        )
        plt.show()

##################################################

if __name__ == '__main__':
    main()
