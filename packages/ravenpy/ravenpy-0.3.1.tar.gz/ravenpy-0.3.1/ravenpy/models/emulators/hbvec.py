class HBVEC(Raven):
    identifier = "hbvec"

    @dataclass
    class Params:
        par_x01: float = None
        par_x02: float = None
        par_x03: float = None
        par_x04: float = None
        par_x05: float = None
        par_x06: float = None
        par_x07: float = None
        par_x08: float = None
        par_x09: float = None
        par_x10: float = None
        par_x11: float = None
        par_x12: float = None
        par_x13: float = None
        par_x14: float = None
        par_x15: float = None
        par_x16: float = None
        par_x17: float = None
        par_x18: float = None
        par_x19: float = None
        par_x20: float = None
        par_x21: float = None

    @dataclass
    class DerivedParams:
        one_plus_par_x15: float = None
        par_x11_half: float = None

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        self.config = Config(
            hrus=(GR4JCN.LandHRU(),),
            subbasins=(
                Sub(
                    subbasin_id=1,
                    name="sub_001",
                    downstream_id=-1,
                    profile="None",
                    gauged=True,
                ),
            ),
            params=HBVEC.Params(),
            derived_params=HBVEC.DerivedParams(),
        )

        self.config.rvp.tmpl = """
        #------------------------------------------------------------------------
        # Global parameters
        #
        #                             HBV_PARA_13=TCALT
        :AdiabaticLapseRate                   {params.par_x13}
        #                                   HBV_PARA_01, CONSTANT,
        :RainSnowTransition                   {params.par_x01},      2.0
        #                                   HBV_PARA_04,
        :IrreducibleSnowSaturation            {params.par_x04}
        #                             HBV_PARA_12=PCALT
        :GlobalParameter PRECIP_LAPSE         {params.par_x12}

        #---------------------------------------------------------
        # Soil classes
        :SoilClasses
         :Attributes,
         :Units,
           TOPSOIL,      1.0,    0.0,       0
           SLOW_RES,     1.0,    0.0,       0
           FAST_RES,     1.0,    0.0,       0
        :EndSoilClasses

        :SoilParameterList
          :Parameters,                POROSITY,FIELD_CAPACITY,    SAT_WILT,    HBV_BETA, MAX_CAP_RISE_RATE,MAX_PERC_RATE,BASEFLOW_COEFF,            BASEFLOW_N
          :Units     ,                    none,          none,        none,        none,              mm/d,         mm/d,           1/d,                  none
          #                        HBV_PARA_05,   HBV_PARA_06, HBV_PARA_14, HBV_PARA_07,       HBV_PARA_16,     CONSTANT,      CONSTANT,              CONSTANT,
            [DEFAULT],               {params.par_x05},     {params.par_x06},   {params.par_x14},    {params.par_x07},        {params.par_x16},          0.0,           0.0,                   0.0
          #                                                       CONSTANT,                                  HBV_PARA_08,   HBV_PARA_09, 1+HBV_PARA_15=1+ALPHA,
             FAST_RES,                _DEFAULT,      _DEFAULT,         0.0,    _DEFAULT,          _DEFAULT,    {params.par_x08},     {params.par_x09},    {derived_params.one_plus_par_x15}
          #                                                       CONSTANT,                                                 HBV_PARA_10,              CONSTANT,
             SLOW_RES,                _DEFAULT,      _DEFAULT,         0.0,    _DEFAULT,          _DEFAULT,     _DEFAULT,     {params.par_x10},                   1.0
        :EndSoilParameterList

        #---------------------------------------------------------
        # Soil profiles
        # name, layers, (soilClass, thickness) x layers
        #
        :SoilProfiles
        #                        HBV_PARA_17,           CONSTANT,           CONSTANT,
           DEFAULT_P, 3, TOPSOIL,  {params.par_x17}, FAST_RES,    100.0, SLOW_RES,    100.0
        :EndSoilProfiles

        #---------------------------------------------------------
        # Vegetation classes
        #
        :VegetationClasses
         :Attributes,   MAX_HT,  MAX_LAI, MAX_LEAF_COND
         :Units,             m,     none,      mm_per_s
           VEG_ALL,         25,      6.0,           5.3
        :EndVegetationClasses

        :VegetationParameterList
          :Parameters,  MAX_CAPACITY, MAX_SNOW_CAPACITY,  TFRAIN,  TFSNOW,
          :Units,                 mm,                mm,    frac,    frac,
          VEG_ALL,             10000,             10000,    0.88,    0.88,
        :EndVegetationParameterList

        #---------------------------------------------------------
        # LandUse classes
        #
        :LandUseClasses
         :Attributes,     IMPERM, FOREST_COV
         :Units,            frac,       frac
              LU_ALL,        0.0,          1
        :EndLandUseClasses

        :LandUseParameterList
          :Parameters,   MELT_FACTOR, MIN_MELT_FACTOR,   HBV_MELT_FOR_CORR, REFREEZE_FACTOR, HBV_MELT_ASP_CORR
          :Units     ,        mm/d/K,          mm/d/K,                none,          mm/d/K,              none
          #              HBV_PARA_02,        CONSTANT,         HBV_PARA_18,     HBV_PARA_03,          CONSTANT
            [DEFAULT],     {params.par_x02},             2.2,           {params.par_x18},       {params.par_x03},              0.48
        :EndLandUseParameterList

        :LandUseParameterList
         :Parameters, HBV_MELT_GLACIER_CORR,   HBV_GLACIER_KMIN, GLAC_STORAGE_COEFF, HBV_GLACIER_AG
         :Units     ,                  none,                1/d,                1/d,           1/mm
           #                       CONSTANT,           CONSTANT,        HBV_PARA_19,       CONSTANT,
           [DEFAULT],                  1.64,               0.05,          {params.par_x19},           0.05
        :EndLandUseParameterList
        """

        self.config.rvi.tmpl = """
        :Calendar              {calendar}
        :RunName               {run_name}-{run_index}
        :StartDate             {start_date}
        :EndDate               {end_date}
        :TimeStep              {time_step}
        :Method                ORDERED_SERIES

        #------------------------------------------------------------------------
        # Model options
        #
        :Method              	    ORDERED_SERIES
        #:Interpolation      	    INTERP_NEAREST_NEIGHBOR

        :Routing             	    ROUTE_NONE
        :CatchmentRoute      	    TRIANGULAR_UH

        :Evaporation         	    {evaporation}  # PET_FROM_MONTHLY
        :OW_Evaporation      	    {ow_evaporation}  # PET_FROM_MONTHLY
        :SWRadiationMethod   	    SW_RAD_DEFAULT
        :SWCloudCorrect      	    SW_CLOUD_CORR_NONE
        :SWCanopyCorrect     	    SW_CANOPY_CORR_NONE
        :LWRadiationMethod   	    LW_RAD_DEFAULT
        :RainSnowFraction    	    {rain_snow_fraction}  # RAINSNOW_HBV
        :PotentialMeltMethod 	    POTMELT_HBV
        :OroTempCorrect      	    OROCORR_HBV
        :OroPrecipCorrect    	    OROCORR_HBV
        :OroPETCorrect       	    OROCORR_HBV
        :CloudCoverMethod    	    CLOUDCOV_NONE
        :PrecipIceptFract    	    PRECIP_ICEPT_USER
        :MonthlyInterpolationMethod MONTHINT_LINEAR_21

        :SoilModel                  SOIL_MULTILAYER 3

        #------------------------------------------------------------------------
        # Soil Layer Alias Definitions
        #
        :Alias       FAST_RESERVOIR SOIL[1]
        :Alias       SLOW_RESERVOIR SOIL[2]
        :LakeStorage SLOW_RESERVOIR

        #------------------------------------------------------------------------
        # Hydrologic process order for HBV-EC Emulation
        #
        :HydrologicProcesses
          :SnowRefreeze      FREEZE_DEGREE_DAY  SNOW_LIQ        SNOW
          :Precipitation     PRECIP_RAVEN       ATMOS_PRECIP    MULTIPLE
          :CanopyEvaporation CANEVP_ALL         CANOPY          ATMOSPHERE
          :CanopySnowEvap    CANEVP_ALL         CANOPY_SNOW     ATMOSPHERE
          :SnowBalance       SNOBAL_SIMPLE_MELT SNOW            SNOW_LIQ
            :-->Overflow     RAVEN_DEFAULT      SNOW_LIQ        PONDED_WATER
          :Flush             RAVEN_DEFAULT      PONDED_WATER    GLACIER
            :-->Conditional HRU_TYPE IS GLACIER
          :GlacierMelt       GMELT_HBV          GLACIER_ICE     GLACIER
          :GlacierRelease    GRELEASE_HBV_EC    GLACIER         SURFACE_WATER
          :Infiltration      INF_HBV            PONDED_WATER    MULTIPLE
          :Flush             RAVEN_DEFAULT      SURFACE_WATER   FAST_RESERVOIR
            :-->Conditional HRU_TYPE IS_NOT GLACIER
          :SoilEvaporation   SOILEVAP_HBV       SOIL[0]         ATMOSPHERE
          :CapillaryRise     RISE_HBV           FAST_RESERVOIR 	SOIL[0]
          :LakeEvaporation   LAKE_EVAP_BASIC    SLOW_RESERVOIR  ATMOSPHERE
          :Percolation       PERC_CONSTANT      FAST_RESERVOIR 	SLOW_RESERVOIR
          :Baseflow          BASE_POWER_LAW     FAST_RESERVOIR  SURFACE_WATER
          :Baseflow          BASE_LINEAR        SLOW_RESERVOIR  SURFACE_WATER
        :EndHydrologicProcesses

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

        :NetCDFAttribute model_id hbvec

        :NetCDFAttribute time_frequency day
        :NetCDFAttribute time_coverage_start {start_date}
        :NetCDFAttribute time_coverage_end {end_date}
        """

        self.config.rvh.tmpl = """
        {subbasins}

        {hrus}

        :SubBasinProperties
        #                       HBV_PARA_11, DERIVED FROM HBV_PARA_11,
        #                            MAXBAS,                 MAXBAS/2,
           :Parameters,           TIME_CONC,             TIME_TO_PEAK
           :Units     ,                   d,                        d,
                     1,            {par_x11},          {par_x11_half},
        :EndSubBasinProperties
        """

        self.config.rvi.evaporation = "PET_FROMMONTHLY"
        self.config.rvi.ow_evaporation = "PET_FROMMONTHLY"
        self.config.rvi.rain_snow_fraction = "RAINSNOW_HBV"

        self.config.rvc.soil2 = 0.50657

    def derived_parameters(self):
        self.config.rvp.derived_params.one_plus_par_x15 = (
            self.config.rvp.params.par_x15 + 1.0
        )
        self.config.rvp.derived_params.par_x11_half = (
            self.config.rvp.params.par_x11 / 2.0
        )

        # These need to be injected in the RVH
        self.config.rvh.par_x11 = self.config.rvp.params.par_x11
        self.config.rvh.par_x11_half = self.config.rvp.derived_params.par_x11_half

        self.config.rvt.rain_correction = self.config.rvp.params.par_x20
        self.config.rvt.snow_correction = self.config.rvp.params.par_x21

        self._monthly_average()

        # Default initial conditions if none are given
        if not self.config.rvc.hru_states:
            self.config.rvc.hru_states[1] = HRUState(soil2=self.config.rvc.soil2)
        if not self.config.rvc.basin_states:
            self.config.rvc.basin_states[1] = BasinIndexCommand()

    # TODO: Support index specification and unit changes.
    def _monthly_average(self):

        if (
            self.config.rvi.evaporation == "PET_FROMMONTHLY"
            or self.config.rvi.ow_evaporation == "PET_FROMMONTHLY"
        ):
            # If this fails, it's likely the input data is missing some necessary variables (e.g. evap).
            tas_cmd = self.config.rvt._var_cmds["tas"]
            tasmin_cmd = self.config.rvt._var_cmds["tasmin"]
            tasmax_cmd = self.config.rvt._var_cmds["tasmax"]
            evspsbl_cmd = self.config.rvt._var_cmds["evspsbl"]

            if tas_cmd:
                tas = xr.open_dataset(tas_cmd.file_name_nc)[tas_cmd.var_name_nc]
            else:
                tasmax = xr.open_dataset(tasmax_cmd.file_name_nc)[
                    tasmax_cmd.var_name_nc
                ]
                tasmin = xr.open_dataset(tasmin_cmd.file_name_nc)[
                    tasmin_cmd.var_name_nc
                ]
                tas = (tasmax + tasmin) / 2.0

            if evspsbl_cmd:
                evap = xr.open_dataset(evspsbl_cmd.file_name_nc)[
                    evspsbl_cmd.var_name_nc
                ]

            mat = tas.groupby("time.month").mean().values
            mae = evap.groupby("time.month").mean().values

            self.config.rvt.monthly_ave_evaporation = tuple(mae)
            self.config.rvt.monthly_ave_temperature = tuple(mat)


class HBVEC_OST(Ostrich, HBVEC):
    _p = Path(__file__).parent / "ostrich-hbv-ec"
    templates = tuple(_p.glob("model/*.rv?")) + tuple(_p.glob("*.t??"))

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.rvi.suppress_output = True
        self.low = HBVEC.params
        self.high = HBVEC.params
        self.txt = Ost(
            algorithm="DDS",
            max_iterations=50,
            lowerBounds=self.low(
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
            upperBounds=self.high(
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

    # TODO: Support index specification and unit changes.
    def derived_parameters(self):
        self.rvt.raincorrection = "par_x20"
        self.rvt.snowcorrection = "par_x21"
        self._monthly_average()
