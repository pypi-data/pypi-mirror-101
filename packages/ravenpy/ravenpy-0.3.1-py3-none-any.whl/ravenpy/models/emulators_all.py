from collections import defaultdict, namedtuple
from dataclasses import dataclass
from pathlib import Path

import xarray as xr

from ravenpy.config.commands import BasinIndexCommand
from ravenpy.config.rvs import Config

from .base import Ostrich, Raven
from .rv import HRU, LU, RV, HRUState, Sub

__all__ = [
    "GR4JCN",
    "MOHYSE",
    "HMETS",
    "HBVEC",
    "BLENDED",
    "GR4JCN_OST",
    "MOHYSE_OST",
    "HMETS_OST",
    "HBVEC_OST",
    "BLENDED_OST",
    "get_model",
    "Routing",
]


class Routing(Raven):
    """Routing model - no hydrological modeling"""

    identifier = "routing"

    # params = namedtuple("RoutingParams", ())

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        # Declare the parameters that can be user-modified.

        self.config = Config()
        self.config.rvp.tmpl = """
        {soil_classes}

        {soil_profiles}

        {vegetation_classes}

        {land_use_classes}

        {avg_annual_runoff}

        {channel_profiles}
        """

        self.config.rvi.tmpl = """
        :Calendar              {calendar}
        :RunName               {run_name}-{run_index}
        :StartDate             {start_date}
        :EndDate               {end_date}
        :TimeStep              {time_step}
        :Method                ORDERED_SERIES                # Numerical method used for simulation

        :CatchmentRoute        ROUTE_DUMP                    # Catchment routing method, used to convey water from the catchment tributaries and rivulets to the subbasin outlets. DEFAULT ROUTE_DUMP, which instantly ‘dumps’ all water in the subbasin stream reach.
        :Routing               ROUTE_DIFFUSIVE_WAVE          # Channel routing method which is used to transport water from upstream to downstream within the main subbasin channels. DEFAULT ROUTE_DIFFUSIVE_WAVE, which analytically solves the diffusive wave equation along the reach using a constant reference celerity.
        :PrecipIceptFract      PRECIP_ICEPT_NONE             # Estimation of the precipitation interception fraction. In this routing model, stream input(s) are "pretending" to be precipitation going into Raven, thus using DEFAULT PRECIP_ICEPT_NONE to indicate no interception processes are adopted.
        :PotentialMeltMethod   POTMELT_NONE                  # Estimation of the potential snow melt. In this routing model, snow melt processes are not relevant, thus using DEFAULT POTMELT_NONE method.
        :SoilModel             SOIL_ONE_LAYER                # In this routing model, use DEFAULT SOIL_ONE_LAYER to define single soil layer structure.

        :HydrologicProcesses
          :Precipitation     PRECIP_RAVEN             ATMOS_PRECIP     PONDED_WATER          # Moves stream input(s) from ATMOS_PRECIP to PONDED_WATER storage (waiting for runoff). Use DEFAULT PRECIP_RAVEN method.
          :Flush             RAVEN_DEFAULT            PONDED_WATER     SURFACE_WATER         # Moves water from PONDED_WATER to SURFACE_WATER (routed to outlet). Use DEFAULT RAVEN_DEFAULT method.
        :EndHydrologicProcesses


        # Output Options
        #
        #:WriteForcingFunctions
        # Defines the hydrograph performance metrics output by Raven. Either one or multiple is acceptable.
        :EvaluationMetrics {evaluation_metrics}
        :WriteNetcdfFormat  yes
        #:NoisyMode
        :SilentMode
        :PavicsMode
        {suppress_output}

        :NetCDFAttribute title Simulated river discharge
        :NetCDFAttribute history Created on {now} by Raven
        :NetCDFAttribute references  Craig, J.R., and the Raven Development Team, Raven user's and developer's manual (Version 2.8), URL: http://raven.uwaterloo.ca/ (2018).
        :NetCDFAttribute comment Raven Hydrological Framework version {raven_version}

        :NetCDFAttribute model_id routing

        :NetCDFAttribute time_frequency day
        :NetCDFAttribute time_coverage_start {start_date}
        :NetCDFAttribute time_coverage_end {end_date}
        """

    def derived_parameters(self):
        pass


def get_model(name):
    """Return the corresponding Raven emulated model instance.

    Parameters
    ----------
    name : str
      Model class name or model identifier.

    Returns
    -------
    Raven model instance
    """
    from ravenpy.models import emulators

    model_cls = getattr(emulators, name, None)

    if model_cls is None:
        for m in [GR4JCN, MOHYSE, HMETS, HBVEC, BLENDED]:
            if m.identifier == name:
                model_cls = m

    if model_cls is None:
        raise ValueError("Model {} is not recognized.".format(name))

    return model_cls


def used_storage_variables(fn):
    """Identify variables that are used by the model."""
    import xarray as xr

    ds = xr.open_dataset(fn)
    return [
        (key, da.isel(time=-1).values.tolist(), da.units)
        for key, da in ds.data_vars.items()
        if any(ds[key] != 0)
    ]
