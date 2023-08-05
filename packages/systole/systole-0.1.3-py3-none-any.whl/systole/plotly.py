# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

from typing import TYPE_CHECKING, Dict, List, Union, overload

import numpy as np
import pandas as pd

from systole.correction import rr_artefacts
from systole.detection import ecg_peaks, oxi_peaks
from systole.hrv import frequency_domain, nonlinear, time_domain
from systole.plotting import plot_psd
from systole.utils import heart_rate

if TYPE_CHECKING:
    from plotly.graph_objs._figure import Figure


def plot_raw(
    signal: Union[pd.DataFrame, List, np.ndarray],
    sfreq: int = 75,
    type: str = "ppg",
    ecg_method: str = "hamilton",
) -> "Figure":
    """Interactive visualization of PPG signal and systolic peaks detection.

    Parameters
    ----------
    signal : :py:class:`pandas.DataFrame`, :py:class:`numpy.ndarray` or list
        Dataframe of PPG or ECG signal in the long format. If a data frame is
        provided, it should contain at least one ``'time'`` and one colum for
        signal(either ``'ppg'`` or ``'ecg'``). If an array is provided, it will
        automatically create a DataFrame using the array as signal and
        ``sfreq`` as sampling frequency.
    sfreq : int
        Signal sampling frequency. Default is set to 75 Hz.
    type : str
        The type of signal provided. Can be ``'ppg'`` (pulse oximeter) or
        ``'ecg'`` (electrocardiography). The peak detection algorithm used
        depend on the type of signal provided.
    ecg_method : str
        Peak detection algorithm used by the
        :py:func:`systole.detection.ecg_peaks` function. Can be one of the
        following: `'hamilton'`, `'christov'`, `'engelse-zeelenberg'`,
        `'pan-tompkins'`, `'wavelet-transform'`, `'moving-average'`. The
        default is `'hamilton'`.

    Returns
    -------
    raw : :py:class:`plotly.graph_objects.Figure`
        Instance of :py:class:`plotly.graph_objects.Figure`.

    See also
    --------
    plot_events, plot_ectopic, plot_shortLong, plot_subspaces, plot_frequency,
    plot_timedomain, plot_nonlinear

    Examples
    --------

    Plotting PPG recording.

    .. jupyter-execute::

       from systole import import_ppg
       from systole.plotly import plot_raw
       # Import PPG recording as pandas data frame
       ppg = import_ppg()
       # Only use the first 60 seconds for demonstration
       ppg = ppg[ppg.time<60]
       plot_raw(ppg)

    Plotting ECG recording.

    .. jupyter-execute::

       from systole import import_dataset1
       from systole.plotly import plot_raw
       # Import PPG recording as pandas data frame
       ecg = import_dataset1(modalities=['ECG'])
       # Only use the first 60 seconds for demonstration
       ecg = ecg[ecg.time<60]
       plot_raw(ecg, type='ecg', sfreq=1000, ecg_method='pan-tompkins')
    """
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots

    if isinstance(signal, pd.DataFrame):
        # Find peaks - Remove learning phase
        if type == "ppg":
            signal, peaks = oxi_peaks(signal.ppg, noise_removal=False)
        elif type == "ecg":
            signal, peaks = ecg_peaks(signal.ecg, method=ecg_method, find_local=True)
    else:
        signal = np.asarray(signal)
        if type == "ppg":
            signal, peaks = oxi_peaks(signal, noise_removal=False, sfreq=sfreq)
        elif type == "ecg":
            signal, peaks = ecg_peaks(
                signal, method=ecg_method, sfreq=sfreq, find_local=True
            )
    time = np.arange(0, len(signal)) / 1000

    # Extract heart rate
    hr, time = heart_rate(peaks, sfreq=1000, unit="rr", kind="linear")

    #############
    # Upper panel
    #############

    # Signal
    ppg_trace = go.Scattergl(
        x=time,
        y=signal,
        mode="lines",
        name="PPG signal",
        hoverinfo="skip",
        showlegend=False,
        line=dict(width=1, color="#c44e52"),
    )
    # Peaks
    peaks_trace = go.Scattergl(
        x=time[peaks],
        y=signal[peaks],
        mode="markers",
        name="Peaks",
        hoverinfo="y",
        showlegend=False,
        marker=dict(size=8, color="white", line=dict(width=2, color="DarkSlateGrey")),
    )

    #############
    # Lower panel
    #############

    # Instantaneous Heart Rate - Lines
    rr_trace = go.Scattergl(
        x=time,
        y=hr,
        mode="lines",
        name="R-R intervals",
        hoverinfo="skip",
        showlegend=False,
        line=dict(width=1, color="#4c72b0"),
    )

    # Instantaneous Heart Rate - Peaks
    rr_peaks = go.Scattergl(
        x=time[peaks],
        y=hr[peaks],
        mode="markers",
        name="R-R intervals",
        showlegend=False,
        marker=dict(size=6, color="white", line=dict(width=2, color="DarkSlateGrey")),
    )

    raw = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_titles=["Recording", "Heart rate"],
    )

    raw.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=5, r=5, b=5, t=5),
        autosize=True,
        xaxis_title="Time (s)",
    )

    raw.add_trace(ppg_trace, 1, 1)
    raw.add_trace(peaks_trace, 1, 1)
    raw.add_trace(rr_trace, 2, 1)
    raw.add_trace(rr_peaks, 2, 1)

    return raw


@overload
def plot_ectopic(
    rr: None,
    artefacts: Dict[str, np.ndarray],
) -> "Figure":
    ...


@overload
def plot_ectopic(
    rr: Union[List[float], np.ndarray],
    artefacts: None,
) -> "Figure":
    ...


@overload
def plot_ectopic(
    rr: Union[List[float], np.ndarray],
    artefacts: Dict[str, np.ndarray],
) -> "Figure":
    ...


def plot_ectopic(rr=None, artefacts=None):
    """Plot interactive ectobeats subspace.

    Parameters
    ----------
    rr : 1d array-like or None
        Interval time-series (R-R, beat-to-beat...), in miliseconds.
    artefacts : dict or None
        The artefacts detected using
        :py:func:`systole.detection.rr_artefacts()`.

    Returns
    -------
    subspacesPlot : :py:class:`plotly.graph_objects.Figure`
        Instance of :py:class:`plotly.graph_objects.Figure`.

    See also
    --------
    plot_events, plot_ectopic, plot_shortLong, plot_subspaces, plot_frequency,
    plot_timedomain, plot_nonlinear

    Notes
    -----
    If both *rr* or *artefacts* are provided, will recompute *artefacts*
    given the current rr time-series.

    Examples
    --------

    Visualizing ectopic subspace from RR time series.

    .. jupyter-execute::

       from systole import import_rr
       from systole.plotly import plot_ectopic
       # Import PPG recording as numpy array
       rr = import_rr().rr.to_numpy()
       plot_ectopic(rr)

    Visualizing ectopic subspace from the `artefact` dictionary.

    .. jupyter-execute::

       from systole import import_rr
       from systole.plotly import plot_ectopic
       from systole.detection import rr_artefacts
       # Import PPG recording as numpy array
       rr = import_rr().rr.to_numpy()
       # Use the rr_artefacts function to find ectopic beats
       artefacts = rr_artefacts(rr)
       plot_ectopic(artefacts=artefacts)
    """
    import plotly.express as px
    import plotly.graph_objs as go

    c1, c2, xlim, ylim = 0.13, 0.17, 10, 5

    if artefacts is None:
        if rr is None:
            raise ValueError("rr or artefacts should be provided")
        artefacts = rr_artefacts(rr)

    outliers = (
        artefacts["ectopic"]
        | artefacts["short"]
        | artefacts["long"]
        | artefacts["extra"]
        | artefacts["missed"]
    )

    # All vlaues fit in the x and y lims
    for this_art in [artefacts["subspace1"], artefacts["subspace2"]]:
        this_art[this_art > xlim] = xlim
        this_art[this_art < -xlim] = -xlim
        this_art[this_art > ylim] = ylim
        this_art[this_art < -ylim] = -ylim

    subspacesPlot = go.Figure()

    # Upper area
    def f1(x):
        return -c1 * x + c2

    subspacesPlot.add_trace(
        go.Scatter(
            x=[-10, -10, -1, -1],
            y=[f1(-10), 10, 10, f1(-1)],
            fill="toself",
            mode="lines",
            opacity=0.2,
            showlegend=False,
            fillcolor="gray",
            hoverinfo="none",
            line_color="gray",
        )
    )

    # Lower area
    def f2(x):
        return -c1 * x - c2

    subspacesPlot.add_trace(
        go.Scatter(
            x=[1, 1, 10, 10],
            y=[f2(1), -10, -10, f2(10)],
            fill="toself",
            mode="lines",
            opacity=0.2,
            showlegend=False,
            fillcolor="gray",
            hoverinfo="none",
            line_color="gray",
            text="Points only",
        )
    )

    # Plot normal intervals
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][~outliers],
            y=artefacts["subspace2"][~outliers],
            mode="markers",
            showlegend=False,
            name="Normal",
            marker=dict(
                size=8,
                color="#4c72b0",
                opacity=0.2,
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )

    # Plot ectopic beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["ectopic"]],
            y=artefacts["subspace2"][artefacts["ectopic"]],
            mode="markers",
            name="Ectopic beats",
            showlegend=False,
            marker=dict(
                size=10, color="#c44e52", line=dict(width=2, color="DarkSlateGrey")
            ),
        )
    )

    # Plot missed beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["missed"]],
            y=artefacts["subspace2"][artefacts["missed"]],
            mode="markers",
            name="Missed beats",
            showlegend=False,
            marker=dict(
                size=10,
                color=px.colors.sequential.Greens[8],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )

    # Plot long beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["long"]],
            y=artefacts["subspace2"][artefacts["long"]],
            mode="markers",
            name="Long beats",
            marker_symbol="square",
            showlegend=False,
            marker=dict(
                size=10,
                color=px.colors.sequential.Greens[6],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )

    # Plot extra beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["extra"]],
            y=artefacts["subspace2"][artefacts["extra"]],
            mode="markers",
            name="Extra beats",
            showlegend=False,
            marker=dict(
                size=10,
                color=px.colors.sequential.Purples[8],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )
    # Plot short beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["short"]],
            y=artefacts["subspace2"][artefacts["short"]],
            mode="markers",
            name="Short beats",
            marker_symbol="square",
            showlegend=False,
            marker=dict(
                size=10,
                color=px.colors.sequential.Purples[6],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )

    subspacesPlot.update_layout(
        width=600,
        height=600,
        xaxis_title=r"Subspace $S_{11}$",
        yaxis_title=r"Subspace $S_{12}$",
        template="simple_white",
        title={
            "text": "Ectopic beats",
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    subspacesPlot.update_xaxes(
        showline=True, linewidth=2, linecolor="black", range=[-xlim, xlim]
    )
    subspacesPlot.update_yaxes(
        showline=True, linewidth=2, linecolor="black", range=[-ylim, ylim]
    )

    return subspacesPlot


@overload
def plot_shortLong(
    rr: None,
    artefacts: Dict[str, np.ndarray],
) -> "Figure":
    ...


@overload
def plot_shortLong(
    rr: Union[List[float], np.ndarray],
    artefacts: None,
) -> "Figure":
    ...


@overload
def plot_shortLong(
    rr: Union[List[float], np.ndarray],
    artefacts: Dict[str, np.ndarray],
) -> "Figure":
    ...


def plot_shortLong(rr=None, artefacts=None) -> "Figure":
    """Plot interactive short/long subspace.

    Parameters
    ----------
    rr : 1d array-like or None
        Interval time-series (R-R, beat-to-beat...), in miliseconds.
    artefacts : dict or None
        The artefacts detected using
        :py:func:`systole.detection.rr_artefacts()`.

    Returns
    -------
    subspacesPlot : :py:class:`plotly.graph_objects.Figure`
        Instance of :py:class:`plotly.graph_objects.Figure`.

    See also
    --------
    plot_events, plot_ectopic, plot_shortLong, plot_subspaces, plot_frequency,
    plot_timedomain, plot_nonlinear

    Notes
    -----
    If both ``rr`` or ``artefacts`` are provided, will recompute ``artefacts``
    given the current rr time-series.

    Examples
    --------

    Visualizing short/long and missed/extra intervals from RR time series.

    .. jupyter-execute::

       from systole import import_rr
       from systole.plotly import plot_shortLong
       # Import PPG recording as numpy array
       rr = import_rr().rr.to_numpy()
       plot_shortLong(rr)

    Visualizing ectopic subspace from the `artefact` dictionary.

    .. jupyter-execute::

       from systole import import_rr
       from systole.plotly import plot_shortLong
       from systole.detection import rr_artefacts
       # Import PPG recording as numpy array
       rr = import_rr().rr.to_numpy()
       # Use the rr_artefacts function to short/long
       # and extra/missed intervals
       artefacts = rr_artefacts(rr)
       plot_shortLong(artefacts=artefacts)
    """
    import plotly.express as px
    import plotly.graph_objs as go

    xlim, ylim = 10, 10

    if artefacts is None:
        if rr is None:
            raise ValueError("rr or artefacts should be provided")
        artefacts = rr_artefacts(rr)

    outliers = (
        artefacts["ectopic"]
        | artefacts["short"]
        | artefacts["long"]
        | artefacts["extra"]
        | artefacts["missed"]
    )

    # All vlaues fit in the x and y lims
    for this_art in [artefacts["subspace1"], artefacts["subspace3"]]:
        this_art[this_art > xlim] = xlim
        this_art[this_art < -xlim] = -xlim
        this_art[this_art > ylim] = ylim
        this_art[this_art < -ylim] = -ylim

    subspacesPlot = go.Figure()

    # Upper area
    subspacesPlot.add_trace(
        go.Scatter(
            x=[-10, -10, -1, -1],
            y=[1, 10, 10, 1],
            fill="toself",
            mode="lines",
            opacity=0.2,
            showlegend=False,
            fillcolor="gray",
            hoverinfo="none",
            line_color="gray",
        )
    )

    # Lower area
    subspacesPlot.add_trace(
        go.Scatter(
            x=[1, 1, 10, 10],
            y=[-1, -10, -10, -1],
            fill="toself",
            mode="lines",
            opacity=0.2,
            showlegend=False,
            fillcolor="gray",
            hoverinfo="none",
            line_color="gray",
            text="Points only",
        )
    )

    # Plot normal intervals
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][~outliers],
            y=artefacts["subspace3"][~outliers],
            mode="markers",
            showlegend=False,
            name="Normal",
            marker=dict(
                size=8,
                color="#4c72b0",
                opacity=0.2,
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )

    # Plot ectopic beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["ectopic"]],
            y=artefacts["subspace3"][artefacts["ectopic"]],
            mode="markers",
            name="Ectopic beats",
            showlegend=False,
            marker=dict(
                size=10, color="#c44e52", line=dict(width=2, color="DarkSlateGrey")
            ),
        )
    )

    # Plot missed beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["missed"]],
            y=artefacts["subspace3"][artefacts["missed"]],
            mode="markers",
            name="Missed beats",
            showlegend=False,
            marker=dict(
                size=10,
                color=px.colors.sequential.Greens[8],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )

    # Plot long beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["long"]],
            y=artefacts["subspace3"][artefacts["long"]],
            mode="markers",
            name="Long beats",
            marker_symbol="square",
            showlegend=False,
            marker=dict(
                size=10,
                color=px.colors.sequential.Greens[6],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )

    # Plot extra beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["extra"]],
            y=artefacts["subspace3"][artefacts["extra"]],
            mode="markers",
            name="Extra beats",
            showlegend=False,
            marker=dict(
                size=10,
                color=px.colors.sequential.Purples[8],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )
    # Plot short beats
    subspacesPlot.add_trace(
        go.Scattergl(
            x=artefacts["subspace1"][artefacts["short"]],
            y=artefacts["subspace3"][artefacts["short"]],
            mode="markers",
            name="Short beats",
            marker_symbol="square",
            showlegend=False,
            marker=dict(
                size=10,
                color=px.colors.sequential.Purples[6],
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )
    )

    subspacesPlot.update_layout(
        width=600,
        height=600,
        xaxis_title=r"Subspace $S_{11}$",
        yaxis_title=r"Subspace $S_{12}$",
        template="simple_white",
        title={
            "text": "Short/longs beats",
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    subspacesPlot.update_xaxes(
        showline=True, linewidth=2, linecolor="black", range=[-xlim, xlim]
    )
    subspacesPlot.update_yaxes(
        showline=True, linewidth=2, linecolor="black", range=[-ylim, ylim]
    )

    return subspacesPlot


def plot_subspaces(rr: Union[List[float], np.ndarray], height: float = 400) -> "Figure":
    """Plot hrv subspace as described by Lipponen & Tarvainen (2019) [#]_.

    Parameters
    ----------
    rr : np.ndarray or list
        Interval time-series (R-R, beat-to-beat...), in miliseconds.
    height : int
        Height of the figure. The width will be set to  `height*2` by default.

    Returns
    -------
    fig : :py:class:`plotly.graph_objects.Figure`
        Instance of :py:class:`plotly.graph_objects.Figure`.

    See also
    --------
    plot_events, plot_ectopic, plot_shortLong, plot_subspaces, plot_frequency,
    plot_timedomain, plot_nonlinear

    References
    ----------
    ..[#] Lipponen, J. A., & Tarvainen, M. P. (2019). A robust algorithm for
        heart rate variability time series artefact correction using novel beat
        classification. Journal of Medical Engineering & Technology, 43(3),
        173–181. https://doi.org/10.1080/03091902.2019.1640306

    Examples
    --------

    Visualizing artefacts from RR time series.

    .. jupyter-execute::

       from systole import import_rr
       from systole.plotly import plot_subspaces
       # Import PPG recording as numpy array
       rr = import_rr().rr.to_numpy()
       plot_subspaces(rr)
    """
    from plotly.subplots import make_subplots

    rr = np.asarray(rr)

    xlim, ylim = 10, 10
    fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.5, 0.5],
        subplot_titles=("Ectopic", "Short/longs beats"),
    )

    ectopic = plot_ectopic(rr=rr)  # type: ignore
    sl = plot_shortLong(rr=rr)  # type: ignore

    for traces in ectopic.data:
        fig.add_traces([traces], rows=[1], cols=[1])
    for traces in sl.data:
        fig.add_traces([traces], rows=[1], cols=[2])

    fig.update_layout(
        width=height * 2,
        height=height,
        xaxis_title=r"Subspace $S_{11}$",
        yaxis_title=r"Subspace $S_{12}$",
        xaxis2_title=r"Subspace $S_{21}$",
        yaxis2_title=r"Subspace $S_{22}$",
        template="simple_white",
    )

    fig.update_xaxes(
        showline=True, linewidth=2, linecolor="black", range=[-xlim, xlim], row=1, col=1
    )
    fig.update_yaxes(
        showline=True, linewidth=2, linecolor="black", range=[-ylim, ylim], row=1, col=1
    )

    fig.update_xaxes(
        showline=True, linewidth=2, linecolor="black", range=[-xlim, xlim], row=1, col=2
    )
    fig.update_yaxes(
        showline=True, linewidth=2, linecolor="black", range=[-ylim, ylim], row=1, col=2
    )

    return fig


def plot_frequency(rr: Union[np.ndarray, list]) -> "Figure":
    """Plot PSD and frequency domain metrics.

    Parameters
    ----------
    rr : 1d array-like
        Interval time-series (R-R, beat-to-beat...), in miliseconds.

    Returns
    -------
    fig : :py:class:`plotly.graph_objects.Figure`
        Instance of :py:class:`plotly.graph_objects.Figure`.

    See also
    --------
    plot_events, plot_ectopic, plot_shortLong, plot_subspaces, plot_frequency,
    plot_timedomain, plot_nonlinear

    Examples
    --------

    Visualizing HRV frequency domain from RR time series.

    .. jupyter-execute::

       from systole import import_rr
       from systole.plotly import plot_frequency
       # Import PPG recording as numpy array
       rr = import_rr().rr.to_numpy()
       plot_frequency(rr)
    """
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots

    df = frequency_domain(rr).round(2)

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        specs=[[{"type": "scatter"}], [{"type": "table"}]],
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=[
                    "<b>Frequency band (HZ)</b>",
                    "<b>Peak (Hz)</b>",
                    "<b>Power (ms<sup>2</sup>)</b>",
                    "<b>Power (%)</b>",
                    "<b>Power (n.u.)</b>",
                ],
                align="center",
            ),
            cells=dict(
                values=[
                    [
                        "VLF \n (0-0.04 Hz)",
                        "LF \n (0.04 - 0.15 Hz)",
                        "HF \n (0.15 - 0.4 Hz)",
                    ],
                    [
                        df[df.Metric == "vlf_peak"].Values,
                        df[df.Metric == "lf_peak"].Values,
                        df[df.Metric == "hf_peak"].Values,
                    ],
                    [
                        df[df.Metric == "vlf_power"].Values,
                        df[df.Metric == "lf_power"].Values,
                        df[df.Metric == "hf_power"].Values,
                    ],
                    [
                        "-",
                        df[df.Metric == "power_lf_nu"].Values,
                        df[df.Metric == "power_hf_nu"].Values,
                    ],
                    [
                        "-",
                        df[df.Metric == "power_lf_per"].Values,
                        df[df.Metric == "power_hf_per"].Values,
                    ],
                ],
                align="center",
            ),
        ),
        row=2,
        col=1,
    )

    freq, psd = plot_psd(rr, show=False)

    fbands = {
        "vlf": ("Very low frequency", (0.003, 0.04), "#4c72b0"),
        "lf": ("Low frequency", (0.04, 0.15), "#55a868"),
        "hf": ("High frequency", (0.15, 0.4), "#c44e52"),
    }

    for f in ["vlf", "lf", "hf"]:
        mask = (freq >= fbands[f][1][0]) & (freq <= fbands[f][1][1])
        fig.add_trace(
            go.Scatter(
                x=freq[mask],
                y=psd[mask],
                fill="tozeroy",
                mode="lines",
                showlegend=False,
                line_color=fbands[f][2],
                line=dict(shape="spline", smoothing=1, width=1, color="#fac1b7"),
            ),
            row=1,
            col=1,
        )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=5, r=5, b=5, t=5),
        autosize=True,
        width=600,
        height=600,
        xaxis_title="Frequencies (Hz)",
        yaxis_title="PSD",
        title={"text": "FFT Spectrum", "x": 0.5, "xanchor": "center", "yanchor": "top"},
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
    fig.update_yaxes(showline=True, linewidth=2, linecolor="black")

    return fig


def plot_nonlinear(rr: Union[np.ndarray, List]) -> "Figure":
    """Plot nonlinear domain.

    Parameters
    ----------
    rr : 1d array-like
        Interval time-series (R-R, beat-to-beat...), in miliseconds.

    Returns
    -------
    fig : :py:class:`plotly.graph_objects.Figure`
        Instance of :py:class:`plotly.graph_objects.Figure`.

    See also
    --------
    plot_events, plot_ectopic, plot_shortLong, plot_subspaces, plot_frequency,
    plot_timedomain, plot_nonlinear

    Examples
    --------

    Visualizing HRV non linear domain from RR time series.

    .. jupyter-execute::

       from systole import import_rr
       from systole.plotly import plot_nonlinear
       # Import PPG recording as numpy array
       rr = import_rr().rr.to_numpy()
       plot_nonlinear(rr)
    """
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots

    rr = np.asarray(rr)

    df = nonlinear(rr).round(2)

    fig = make_subplots(
        rows=2,
        cols=1,
        specs=[[{"type": "scatter"}], [{"type": "table"}]],
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["<b>Pointcare Plot</b>", "<b>Value</b>"], align="center"
            ),
            cells=dict(
                values=[
                    ["SD1", "SD2"],
                    [df[df.Metric == "SD1"].Values, df[df.Metric == "SD2"].Values],
                ],
                align="center",
            ),
        ),
        row=2,
        col=1,
    )

    ax_min = rr.min() - (rr.max() - rr.min()) * 0.1
    ax_max = rr.max() + (rr.max() - rr.min()) * 0.1

    fig.add_trace(
        go.Scattergl(
            x=rr[:-1],
            y=rr[1:],
            mode="markers",
            opacity=0.6,
            showlegend=False,
            marker=dict(
                size=8, color="#4c72b0", line=dict(width=2, color="DarkSlateGrey")
            ),
        )
    )

    fig.add_trace(go.Scatter(x=[0, 4000], y=[0, 4000], showlegend=False))

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=5, r=5, b=5, t=5),
        autosize=True,
        width=500,
        height=800,
        xaxis_title="RR<sub>n</sub> (ms)",
        yaxis_title="RR<sub>n+1</sub> (ms)",
        title={
            "text": "Pointcare Plot",
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )
    fig.update_xaxes(
        showline=True, linewidth=2, linecolor="black", range=[ax_min, ax_max]
    )
    fig.update_yaxes(
        showline=True, linewidth=2, linecolor="black", range=[ax_min, ax_max]
    )

    return fig


def plot_timedomain(rr: Union[np.ndarray, list]) -> "Figure":
    """Plot time domain metrics and the histogram of RR intervals.

    Parameters
    ----------
    rr : np.ndarray or list
        Interval time-series (R-R, beat-to-beat...), in miliseconds.

    Returns
    -------
    fig : :py:class:`plotly.graph_objects.Figure`
        Instance of :py:class:`plotly.graph_objects.Figure`.

    See also
    --------
    plot_events, plot_ectopic, plot_shortLong, plot_subspaces, plot_frequency,
    plot_timedomain, plot_nonlinear

    Examples
    --------

    Visualizing HRV time domain metrics from RR time series.

    .. jupyter-execute::

       from systole import import_rr
       from systole.plotly import plot_nonlinear
       # Import PPG recording as numpy array
       rr = import_rr().rr.to_numpy()
       plot_nonlinear(rr)
    """
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots

    df = time_domain(rr).round(2)

    fig = make_subplots(
        rows=2,
        cols=1,
        specs=[[{"type": "scatter"}], [{"type": "table"}]],
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["<b>Variable</b>", "<b>Unit</b>", "<b>Value</b>"],
                align="center",
            ),
            cells=dict(
                values=[
                    ["Mean RR", "Mean BPM", "SDNN", "RMSSD", "pnn50"],
                    ["(ms)", "(1/min)", "(ms)", "(ms)", "(%)"],
                    [
                        df[df.Metric == "MeanRR"].Values,
                        df[df.Metric == "MeanBPM"].Values,
                        df[df.Metric == "SDNN"].Values,
                        df[df.Metric == "RMSSD"].Values,
                        df[df.Metric == "pnn50"].Values,
                    ],
                ],
                align="center",
            ),
        ),
        row=2,
        col=1,
    )

    fig.add_trace(go.Histogram(x=rr, marker={"line": {"width": 2}, "color": "#4c72b0"}))

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=5, r=5, b=5, t=5),
        autosize=True,
        width=500,
        height=800,
        xaxis_title="RR intervals (ms)",
        yaxis_title="Counts",
        title={"text": "Distribution", "x": 0.5, "xanchor": "center", "yanchor": "top"},
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
    fig.update_yaxes(showline=True, linewidth=2, linecolor="black")

    return fig
