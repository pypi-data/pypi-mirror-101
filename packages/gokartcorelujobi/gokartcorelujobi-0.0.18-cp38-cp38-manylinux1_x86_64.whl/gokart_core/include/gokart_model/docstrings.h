/*
  This file contains docstrings for use in the Python bindings.
  Do not edit! They were automatically extracted by pybind11_mkdoc.
 */

#define __EXPAND(x)                                      x
#define __COUNT(_1, _2, _3, _4, _5, _6, _7, COUNT, ...)  COUNT
#define __VA_SIZE(...)                                   __EXPAND(__COUNT(__VA_ARGS__, 7, 6, 5, 4, 3, 2, 1))
#define __CAT1(a, b)                                     a ## b
#define __CAT2(a, b)                                     __CAT1(a, b)
#define __DOC1(n1)                                       __doc_##n1
#define __DOC2(n1, n2)                                   __doc_##n1##_##n2
#define __DOC3(n1, n2, n3)                               __doc_##n1##_##n2##_##n3
#define __DOC4(n1, n2, n3, n4)                           __doc_##n1##_##n2##_##n3##_##n4
#define __DOC5(n1, n2, n3, n4, n5)                       __doc_##n1##_##n2##_##n3##_##n4##_##n5
#define __DOC6(n1, n2, n3, n4, n5, n6)                   __doc_##n1##_##n2##_##n3##_##n4##_##n5##_##n6
#define __DOC7(n1, n2, n3, n4, n5, n6, n7)               __doc_##n1##_##n2##_##n3##_##n4##_##n5##_##n6##_##n7
#define DOC(...)                                         __EXPAND(__EXPAND(__CAT2(__DOC, __VA_SIZE(__VA_ARGS__)))(__VA_ARGS__))

#if defined(__GNUG__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-variable"
#endif


static const char *__doc_gokart_model_BrakesInterface = R"doc()doc";

static const char *__doc_gokart_model_BrakesInterfaceStatic = R"doc()doc";

static const char *__doc_gokart_model_BrakesInterfaceStatic_BrakesInterfaceStatic = R"doc()doc";

static const char *__doc_gokart_model_BrakesInterfaceStatic_get_estimated_deceleration =
R"doc(Interface to get the estimated deceleration given by the brakes at
given position travelling at current speed

Parameter ``position:``:
    $Parameter ``speed:``:

Returns:)doc";

static const char *__doc_gokart_model_BrakesInterfaceStatic_get_needed_position =
R"doc(Interface to get the estimated needed brake position to achieve
desired deceleration at current speed

Parameter ``position:``:
    $Parameter ``speed:``:

Returns:)doc";

static const char *__doc_gokart_model_BrakesInterfaceStatic_get_needed_position_2 =
R"doc(Interface to get the estimated needed brake position to achieve
desired deceleration at current speed

Parameter ``dec:``:
    $Parameter ``speed:``:

Returns:)doc";

static const char *__doc_gokart_model_BrakesInterfaceStatic_intervention_tresh = R"doc()doc";

static const char *__doc_gokart_model_BrakesInterfaceStatic_kLinear = R"doc()doc";

static const char *__doc_gokart_model_BrakesInterfaceStatic_kQuadratic = R"doc()doc";

static const char *__doc_gokart_model_BrakesInterfaceStatic_position_threshold = R"doc()doc";

static const char *__doc_gokart_model_BrakesInterface_BrakesInterface = R"doc()doc";

static const char *__doc_gokart_model_BrakesInterface_assert_limits = R"doc()doc";

static const char *__doc_gokart_model_BrakesInterface_dec_limits = R"doc(Considered acceleration bounds in [m/s^2] (negative values))doc";

static const char *__doc_gokart_model_BrakesInterface_get_estimated_deceleration =
R"doc(Interface to get the estimated deceleration (>=0) given by the brakes
at given position travelling at current speed

Parameter ``position:``:
    $Parameter ``speed:``:

Returns:)doc";

static const char *__doc_gokart_model_BrakesInterface_get_needed_position =
R"doc(Interface to get the estimated needed brake position to achieve
desired deceleration (>=0) at current speed

Parameter ``dec:``:
    $Parameter ``speed:``:

Returns:)doc";

static const char *__doc_gokart_model_BrakesInterface_get_needed_position_2 =
R"doc(Interface to get the estimated needed brake position to achieve
desired deceleration (>=0) at current speed

Parameter ``dec:``:
    $Parameter ``speed:``:

Parameter ``wheels_speed:``:
    $Returns:)doc";

static const char *__doc_gokart_model_BrakesInterface_position_limits = R"doc(Considered position bounds normalized value in [0, 1])doc";

static const char *__doc_gokart_model_BrakesInterface_speed_limits = R"doc(Considered speed bounds in [m/s])doc";

static const char *__doc_gokart_model_CubicBiPolynomial = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_CubicBiPolynomial = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_evaluate = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p00 = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p01 = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p02 = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p03 = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p10 = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p11 = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p12 = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p20 = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p21 = R"doc()doc";

static const char *__doc_gokart_model_CubicBiPolynomial_p30 = R"doc()doc";

static const char *__doc_gokart_model_GokartGeometry =
R"doc(Geometrical definition of the gokart model containing physical
measurements)doc";

static const char *__doc_gokart_model_GokartGeometry_GokartGeometry =
R"doc(Default constuctor

for parameter explaination look above

Parameter ``l1``:
    l1

Parameter ``l2``:
    l2

Parameter ``w1``:
    w1

Parameter ``w2``:
    w2

Parameter ``back2backaxle``:
    back2backaxle,

Parameter ``frontaxle2front``:
    frontaxle2front

Parameter ``wheel2border``:
    wheel2border)doc";

static const char *__doc_gokart_model_GokartGeometry_back2backaxle = R"doc(Distance from the rear of the gokart to the back axle)doc";

static const char *__doc_gokart_model_GokartGeometry_frontaxle2front = R"doc(Distance from the front axle to the front of the kart)doc";

static const char *__doc_gokart_model_GokartGeometry_get_F2n =
R"doc(Returns the portion of the mass supported by the back wheels

Returns:)doc";

static const char *__doc_gokart_model_GokartGeometry_l1 = R"doc(Distance from cog to front tires)doc";

static const char *__doc_gokart_model_GokartGeometry_l2 = R"doc(Distance from cog to back tires)doc";

static const char *__doc_gokart_model_GokartGeometry_w1 = R"doc(Distance between front Tires)doc";

static const char *__doc_gokart_model_GokartGeometry_w2 = R"doc(Distance between rear Tires)doc";

static const char *__doc_gokart_model_GokartGeometry_wheel2border = R"doc(Side distance between center of the wheel and external frame)doc";

static const char *__doc_gokart_model_GokartModel =
R"doc(Gokart Model, Abstract class defining interfaces to calculate its
dynamics)doc";

static const char *__doc_gokart_model_GokartModel_EF =
R"doc(Integration using Euler forward implemetation

Parameter ``state``:
    State x0 of the gokart at t0

Parameter ``inputs``:
    Input u0 at t0

Parameter ``dt``:
    $Returns:

state of the gokart at time t0+dt)doc";

static const char *__doc_gokart_model_GokartModel_GokartModel =
R"doc(Default constuctor setting base KartGeometry used for simulation of
dynamics

Parameter ``gg``:)doc";

static const char *__doc_gokart_model_GokartModel_RK4 =
R"doc(Integration using 4th order Runge Kutta (RK4) implementation

Parameter ``state``:
    State x0 of the gokart at t0

Parameter ``inputs``:
    Input u0 at t0

Parameter ``dt``:
    $Returns:

state of the gokart at time t0+dt)doc";

static const char *__doc_gokart_model_GokartModel_assertModelInput =
R"doc(Assserts that the given input matches to the used model (used in
inherrited classes)

Parameter ``input``:
    Eigen Matrix to be tested)doc";

static const char *__doc_gokart_model_GokartModel_assertModelState =
R"doc(Assserts that the given state matches to the used model (used in
inherrited classes)

Parameter ``state``:
    Eigen Matrix to be tested)doc";

static const char *__doc_gokart_model_GokartModel_dynamics =
R"doc(calculated the dyamics dx/dt=dynamics(x, u) at t0

Parameter ``state``:
    state x at t0

Parameter ``inputs``:
    input u at t0

Returns:
    derivative of the state at time t0)doc";

static const char *__doc_gokart_model_GokartModel_gk_geometry = R"doc()doc";

static const char *__doc_gokart_model_KittBrakesInterfaceStatic = R"doc()doc";

static const char *__doc_gokart_model_KittBrakesInterfaceStatic_KittBrakesInterfaceStatic = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterface = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpCubic = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpCubic_MotorsInterfaceLookUpCubic = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpCubic_SF_NEG = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpCubic_SF_POS = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpCubic_forwardacc = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpRamp = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpRamp_MotorsInterfaceLookUpRamp = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpRamp_forwardacc = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpRamp_get_max_acc = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpRamp_get_smooth_max_acc = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterfaceLookUpRamp_rampfun = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterface_MotorsInterface = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterface_acc_limits = R"doc(Considered acceleration bounds in [m/s^2])doc";

static const char *__doc_gokart_model_MotorsInterface_assert_limits = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterface_currents_limits = R"doc(Considered current bounds in [ARMS])doc";

static const char *__doc_gokart_model_MotorsInterface_get_estimated_acceleration =
R"doc(Interface to get the estimated acceleration given by the motors at
given speed and current values

Parameter ``speed:``:
    current speed

Parameter ``current:``:
    throttle given to the motors (average of the two)

Returns:)doc";

static const char *__doc_gokart_model_MotorsInterface_get_max_acc = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterface_get_needed_current =
R"doc(Interface to get the estimated needed current by the motors to achieve
desired acceleration at current speed

Parameter ``acc:``:
    the desired acceleration

Parameter ``speed:``:
    the current speed

Returns:)doc";

static const char *__doc_gokart_model_MotorsInterface_get_normalized_needed_current = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterface_normalized_current_scale = R"doc()doc";

static const char *__doc_gokart_model_MotorsInterface_speed_limits = R"doc(Considered speed bounds in [m/s])doc";

static const char *__doc_gokart_model_tricycle_InputIdx = R"doc()doc";

static const char *__doc_gokart_model_tricycle_InputIdx_AB_L = R"doc()doc";

static const char *__doc_gokart_model_tricycle_InputIdx_AB_R = R"doc()doc";

static const char *__doc_gokart_model_tricycle_InputIdx_BETA = R"doc()doc";

static const char *__doc_gokart_model_tricycle_InputIdx_N_INPUT = R"doc()doc";

static const char *__doc_gokart_model_tricycle_KittTricycle = R"doc(Kitt specific parameters for the tricycle model)doc";

static const char *__doc_gokart_model_tricycle_KittTricycle_KITT_GEOMETRY = R"doc(Measured Geometry of KITT)doc";

static const char *__doc_gokart_model_tricycle_KittTricycle_KITT_TRICYCLE_PARAMS = R"doc(Measured Tricycle paramenters of KITT)doc";

static const char *__doc_gokart_model_tricycle_KittTricycle_KittTricycle = R"doc()doc";

static const char *__doc_gokart_model_tricycle_PajieckaParams = R"doc(Parameters of Pajiecka's magic formula)doc";

static const char *__doc_gokart_model_tricycle_PajieckaParams_B = R"doc(B of Pajiecka's magic formula)doc";

static const char *__doc_gokart_model_tricycle_PajieckaParams_C = R"doc(C of Pajiecka's magic formula)doc";

static const char *__doc_gokart_model_tricycle_PajieckaParams_D = R"doc(D of Pajiecka's magic formula)doc";

static const char *__doc_gokart_model_tricycle_PajieckaParams_PajieckaParams =
R"doc(Default Constructor

Parameter ``B``:
    B of Pajiecka's magic formula

Parameter ``C``:
    C of Pajiecka's magic formula

Parameter ``D``:
    D of Pajiecka's magic formula)doc";

static const char *__doc_gokart_model_tricycle_StateIdx = R"doc()doc";

static const char *__doc_gokart_model_tricycle_StateIdx_N_STATE = R"doc()doc";

static const char *__doc_gokart_model_tricycle_StateIdx_THETA = R"doc()doc";

static const char *__doc_gokart_model_tricycle_StateIdx_Vx = R"doc()doc";

static const char *__doc_gokart_model_tricycle_StateIdx_Vy = R"doc()doc";

static const char *__doc_gokart_model_tricycle_StateIdx_X = R"doc()doc";

static const char *__doc_gokart_model_tricycle_StateIdx_Y = R"doc()doc";

static const char *__doc_gokart_model_tricycle_StateIdx_dTHETA = R"doc()doc";

static const char *__doc_gokart_model_tricycle_Tricycle = R"doc(Simplified Model of the gokart, using a three-wheeled approach.)doc";

static const char *__doc_gokart_model_tricycle_TricycleParams =
R"doc(Datatype to contain all further parameters needed to calculate the
system dynamics of a tricycle model)doc";

static const char *__doc_gokart_model_tricycle_TricycleParams_Ic = R"doc(Moment of inertia)doc";

static const char *__doc_gokart_model_tricycle_TricycleParams_TricycleParams =
R"doc(Default Constructor

Parameter ``FB``:
    B of Pajiecka's magic formula for the front wheel

Parameter ``FC``:
    C of Pajiecka's magic formula for the front wheel

Parameter ``FD``:
    D of Pajiecka's magic formula for the front wheel

Parameter ``RB``:
    B of Pajiecka's magic formula for the rear wheel

Parameter ``RC``:
    C of Pajiecka's magic formula for the rear wheel

Parameter ``RD``:
    D of Pajiecka's magic formula for the rear wheel

Parameter ``Ic``:
    Moment of inertia)doc";

static const char *__doc_gokart_model_tricycle_TricycleParams_front_paj = R"doc(Parameters of Pajiecka's magic formula for the front wheel)doc";

static const char *__doc_gokart_model_tricycle_TricycleParams_rear_paj = R"doc(Parameters of Pajiecka's magic formula for the back wheel)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_REG = R"doc()doc";

static const char *__doc_gokart_model_tricycle_Tricycle_Tricycle = R"doc()doc";

static const char *__doc_gokart_model_tricycle_Tricycle_ackermann_map =
R"doc(Steering map from angle at the rack to the front wheel (only one in
tricycle model)

Parameter ``beta``:
    wheel command

Returns:
    steering angle)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_assertModelInput = R"doc()doc";

static const char *__doc_gokart_model_tricycle_Tricycle_assertModelState = R"doc()doc";

static const char *__doc_gokart_model_tricycle_Tricycle_capfactor =
R"doc(function representing capacity for sidewards grip (Marc Heim, (2.76)),

Parameter ``taccx``:
    longitudinal tire force, f^*_x from (2.75)

Parameter ``D``:
    from magic formula used in kappa function

Returns:
    slip coefficient)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_cn =
R"doc(Slice of the MotorsInterface Lookup at max current (for negative
velocities)

Parameter ``v``:
    velocity

Returns:
    max acceleration at that speed)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_cp =
R"doc(Slice of the MotorsInterface Lookup at max current (for positive
velocities)

Parameter ``v``:
    velocity

Returns:
    max acceleration at that speed)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_dynamics =
R"doc(dynamics of the tricycle model maps current state and input to its
current derivative: dx/dt = dyn(x, u).

Parameter ``state:``:
    current state

Parameter ``inputs:``:
    current input

Returns:
    : derivative of state at current time)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_get_front_acc_y =
R"doc(Returns the lateral acceleration of the front wheel acc. to. Marc Heim
(2.80)

Parameter ``v_y``:
    longitudinal ground velocity in wheel frame.

Parameter ``v_x``:
    lateral ground velocity in wheel frame.

Returns:)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_get_rear_acc_y =
R"doc(Returns the lateral acceleration of the rear axle acc. to. Marc Heim
(2.75)

Parameter ``v_y``:
    longitudinal ground velocity in wheel frame.

Parameter ``v_x``:
    lateral ground velocity in wheel frame.

Parameter ``taccx``:
    longitudinal tire force, f^*_x from (2.75)

Returns:)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_magic =
R"doc(Pajiecka's magic formula mapping the slipping coefficient to the
coefficient of friction between the tire and the road.

Parameter ``s``:
    slipping coefficient

Parameter ``paj_params``:
    Struct containing B, C, D of the magic Formula

Returns:
    Coefficient offriction)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_model_params = R"doc()doc";

static const char *__doc_gokart_model_tricycle_Tricycle_satfun =
R"doc(Saturation function for the remaining capacity of the sidewards grip
ν(x) (Marc Heim, (Figure 2.14.))

Parameter ``x:``:
    value > 0

Returns:
    saturation function)doc";

static const char *__doc_gokart_model_tricycle_Tricycle_simpleslip =
R"doc(Simplified Slip function, (part of Marc Heim, (2.75))

Parameter ``v_y``:
    longitudinal ground velocity in wheel frame.

Parameter ``v_x``:
    lateral ground velocity in wheel frame.

Parameter ``taccx``:
    longitudinal tire force, f^*_x from (2.75)

Parameter ``D``:
    from magic formula used in kappa function

Returns:)doc";

#if defined(__GNUG__)
#pragma GCC diagnostic pop
#endif

