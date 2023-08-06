class HMETS(Raven):
    identifier = "hmets"

    @dataclass
    class Params:
        GAMMA_SHAPE: float = None
        GAMMA_SCALE: float = None
        GAMMA_SHAPE2: float = None
        GAMMA_SCALE2: float = None
        MIN_MELT_FACTOR: float = None
        MAX_MELT_FACTOR: float = None
        DD_MELT_TEMP: float = None
        DD_AGGRADATION: float = None
        SNOW_SWI_MIN: float = None
        SNOW_SWI_MAX: float = None
        SWI_REDUCT_COEFF: float = None
        DD_REFREEZE_TEMP: float = None
        REFREEZE_FACTOR: float = None
        REFREEZE_EXP: float = None
        PET_CORRECTION: float = None
        HMETS_RUNOFF_COEFF: float = None
        PERC_COEFF: float = None
        BASEFLOW_COEFF_1: float = None
        BASEFLOW_COEFF_2: float = None
        TOPSOIL: float = None
        PHREATIC: float = None

    @dataclass
    class DerivedParams:
        TOPSOIL_m: float = None
        PHREATIC_m: float = None
        SUM_MELT_FACTOR: float = None
        SUM_SNOW_SWI: float = None
        TOPSOIL_hlf: float = None
        PHREATIC_hlf: float = None

    @dataclass
    class ForestHRU(HRU):
        land_use_class: str = "FOREST"
        veg_class: str = "FOREST"
        soil_profile: str = "DEFAULT_P"
        aquifer_profile: str = "[NONE]"
        terrain_class: str = "[NONE]"
        # _hru_type: str = "land"

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self.config = Config(
            hrus=(HMETS.ForestHRU(),),
            subbasins=(
                Sub(
                    subbasin_id=1,
                    name="sub_001",
                    downstream_id=-1,
                    profile="None",
                    gauged=True,
                ),
            ),
            params=HMETS.Params(),
            derived_params=HMETS.DerivedParams(),
        )

        self.config.rvp.tmpl = """
        #-----------------------------------------------------------------
        # Soil Classes
        #-----------------------------------------------------------------
        :SoilClasses
          :Attributes,
          :Units,
          TOPSOIL,
          PHREATIC,
        :EndSoilClasses

        #-----------------------------------------------------------------
        # Land Use Classes
        #-----------------------------------------------------------------
        :LandUseClasses,
          :Attributes,        IMPERM,    FOREST_COV,
               :Units,          frac,          frac,
               FOREST,           0.0,           1.0,
        :EndLandUseClasses

        #-----------------------------------------------------------------
        # Vegetation Classes
        #-----------------------------------------------------------------
        :VegetationClasses,
          :Attributes,        MAX_HT,       MAX_LAI, MAX_LEAF_COND,
               :Units,             m,          none,      mm_per_s,
               FOREST,             4,             5,             5,
        :EndVegetationClasses

        #-----------------------------------------------------------------
        # Soil Profiles
        #-----------------------------------------------------------------
        :SoilProfiles
                 LAKE, 0
                 ROCK, 0
          DEFAULT_P, 2, TOPSOIL,  {derived_params.TOPSOIL_m}, PHREATIC, {derived_params.PHREATIC_m},
        # DEFAULT_P, 2, TOPSOIL,   x(20)/1000, PHREATIC,   x(21)/1000,
        :EndSoilProfiles

        #-----------------------------------------------------------------
        # Global Parameters
        #-----------------------------------------------------------------
        :GlobalParameter         SNOW_SWI_MIN {params.SNOW_SWI_MIN}     # x(9)
        :GlobalParameter         SNOW_SWI_MAX {derived_params.SUM_SNOW_SWI}     # x(9)+x(10)
        :GlobalParameter     SWI_REDUCT_COEFF {params.SWI_REDUCT_COEFF} # x(11)
        :GlobalParameter             SNOW_SWI 0.05         # not sure why/if needed...

        #-----------------------------------------------------------------
        # Soil Parameters
        #-----------------------------------------------------------------
        :SoilParameterList
          :Parameters,        POROSITY,      PERC_COEFF,  PET_CORRECTION,  BASEFLOW_COEFF
               :Units,               -,             1/d,               -,             1/d
              TOPSOIL,             1.0,     {params.PERC_COEFF},{params.PET_CORRECTION},{params.BASEFLOW_COEFF_1}
             PHREATIC,             1.0,             0.0,             0.0, {params.BASEFLOW_COEFF_2}
         #    TOPSOIL,             1.0,           x(17),           x(15),           x(18)
         #   PHREATIC,             1.0,             0.0,             0.0,           x(19)
        :EndSoilParameterList

        #-----------------------------------------------------------------
        # Land Use Parameters
        #-----------------------------------------------------------------
        :LandUseParameterList
          :Parameters, MIN_MELT_FACTOR,  MAX_MELT_FACTOR,    DD_MELT_TEMP,  DD_AGGRADATION,  REFREEZE_FACTOR,    REFREEZE_EXP,  DD_REFREEZE_TEMP,  HMETS_RUNOFF_COEFF,
               :Units,          mm/d/C,          mm/d/C,               C,            1/mm,          mm/d/C,               -,                C,                  -,
            [DEFAULT],{params.MIN_MELT_FACTOR},{derived_params.SUM_MELT_FACTOR},  {params.DD_MELT_TEMP},{params.DD_AGGRADATION},{params.REFREEZE_FACTOR},  {params.REFREEZE_EXP},{params.DD_REFREEZE_TEMP},{params.HMETS_RUNOFF_COEFF},
        #                         x(5),       x(5)+x(6),            x(7),            x(8),           x(13),           x(14),            x(12),              x(16),
        :EndLandUseParameterList
        :LandUseParameterList
          :Parameters,   GAMMA_SHAPE,     GAMMA_SCALE,    GAMMA_SHAPE2,    GAMMA_SCALE2,
               :Units,             -,             1/d,               -,             1/d,
            [DEFAULT],  {params.GAMMA_SHAPE},   {params.GAMMA_SCALE},  {params.GAMMA_SHAPE2},  {params.GAMMA_SCALE2},
            #                   x(1),            x(2),            x(3),            x(4),
        :EndLandUseParameterList
        #-----------------------------------------------------------------
        # Vegetation Parameters
        #-----------------------------------------------------------------
        :VegetationParameterList
          :Parameters,  RAIN_ICEPT_PCT,  SNOW_ICEPT_PCT,
               :Units,               -,               -,
            [DEFAULT],             0.0,             0.0,
        :EndVegetationParameterList
        """

        self.config.rvi.tmpl = """
        :Calendar              {calendar}
        :RunName               {run_name}-{run_index}
        :StartDate             {start_date}
        :EndDate               {end_date}
        :TimeStep              {time_step}
        :Method                ORDERED_SERIES

        :PotentialMeltMethod     POTMELT_HMETS
        :RainSnowFraction        {rain_snow_fraction}
        :Evaporation             {evaporation}  # PET_OUDIN
        :CatchmentRoute          ROUTE_DUMP
        :Routing                 ROUTE_NONE

        :SoilModel               SOIL_TWO_LAYER

        :Alias DELAYED_RUNOFF CONVOLUTION[1]

        :HydrologicProcesses
          :SnowBalance     SNOBAL_HMETS    MULTIPLE     MULTIPLE
          :Precipitation   RAVEN_DEFAULT   ATMOS_PRECIP MULTIPLE
          :Infiltration    INF_HMETS       PONDED_WATER MULTIPLE
            :Overflow      OVERFLOW_RAVEN  SOIL[0]      DELAYED_RUNOFF
          :Baseflow        BASE_LINEAR     SOIL[0]      SURFACE_WATER   # interflow, really
          :Percolation     PERC_LINEAR     SOIL[0]      SOIL[1]         # recharge
            :Overflow      OVERFLOW_RAVEN  SOIL[1]      DELAYED_RUNOFF
          :SoilEvaporation SOILEVAP_ALL    SOIL[0]      ATMOSPHERE      # AET
          :Convolve        CONVOL_GAMMA    CONVOLUTION[0] SURFACE_WATER #'surface runoff'
          :Convolve        CONVOL_GAMMA_2  DELAYED_RUNOFF SURFACE_WATER #'delayed runoff'
          :Baseflow        BASE_LINEAR     SOIL[1]      SURFACE_WATER
        :EndHydrologicProcesses

        #:CreateRVPTemplate

        #---------------------------------------------------------
        # Output Options
        #
        #:WriteForcingFunctions
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

        :NetCDFAttribute model_id hmets

        :NetCDFAttribute time_frequency day
        :NetCDFAttribute time_coverage_start {start_date}
        :NetCDFAttribute time_coverage_end {end_date}
        """

        self.config.rvi.evaporation = "PET_OUDIN"
        self.config.rvi.rain_snow_fraction = "RAINSNOW_DATA"

        self.config.rvc.soil0 = None
        self.config.rvc.soil1 = None

    def derived_parameters(self):
        self.config.rvp.derived_params.TOPSOIL_hlf = (
            self.config.rvp.params.TOPSOIL * 0.5
        )
        self.config.rvp.derived_params.PHREATIC_hlf = (
            self.config.rvp.params.PHREATIC * 0.5
        )
        self.config.rvp.derived_params.TOPSOIL_m = (
            self.config.rvp.params.TOPSOIL / 1000.0
        )
        self.config.rvp.derived_params.PHREATIC_m = (
            self.config.rvp.params.PHREATIC / 1000.0
        )

        self.config.rvp.derived_params.SUM_MELT_FACTOR = (
            self.config.rvp.params.MAX_MELT_FACTOR
        )
        self.config.rvp.derived_params.SUM_SNOW_SWI = (
            self.config.rvp.params.SNOW_SWI_MAX
        )

        # Default initial conditions if none are given
        if not self.config.rvc.hru_states:
            soil0 = (
                self.config.rvp.derived_params.TOPSOIL_hlf
                if self.config.rvc.soil0 is None
                else self.config.rvc.soil0
            )
            soil1 = (
                self.config.rvp.derived_params.PHREATIC_hlf
                if self.config.rvc.soil1 is None
                else self.config.rvc.soil1
            )
            self.config.rvc.hru_states[1] = HRUState(soil0=soil0, soil1=soil1)


class HMETS_OST(Ostrich, HMETS):
    _p = Path(__file__).parent / "ostrich-hmets"
    templates = tuple(_p.glob("model/*.rv?")) + tuple(_p.glob("*.t??"))

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.rvi.suppress_output = True
        self.txt = Ost(
            algorithm="DDS",
            max_iterations=50,
            lowerBounds=HMETS.params(
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ),
            upperBounds=HMETS.params(
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ),
        )

    def derived_parameters(self):
        """Derived parameters are computed by Ostrich."""
        pass

    def ost2raven(self, ops):
        """Return a list of parameter names calibrated by Ostrich that match Raven's parameters.

        Parameters
        ----------
        ops: dict
          Optimal parameter set returned by Ostrich.

        Returns
        -------
        HMETSParams named tuple
          Parameters expected by Raven.
        """
        names = ["par_x{:02}".format(i) for i in range(1, 22)]
        names[5] = "par_sum_x05_x06"
        names[9] = "par_sum_x09_x10"

        out = [ops[n] for n in names]
        out[19] *= 1000
        out[20] *= 1000
        return self.params(*out)
