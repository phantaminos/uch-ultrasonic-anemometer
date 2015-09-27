# Introduction #

This page describe how the firmware that controls the signals on the excitation board works.


# General Description #

The microcontroller must wait for a conversion to be started and then send a 40 kHz in one transducer and then wait for an echo on the corresponding transducer pair. In this process the output of the excitation board is selected using an analog multiplexer. When the pulse is generated the output is the pulse itself, then the output is selected to the paired transducer to listen to the echo.

The firmware makes uses of two counters in the ATmega328 to generate the timing necessary. These counters can generate interruptions that call certain routines to take action at a certain time. One of this timers is used to generate the specific frequency of the pulses while the other runs a state machine that activate the

# main.cpp #

This file mainly contains the code of the state machine that controls the global timing of the measurement of one frame. The state machine is executed on each call of `ISR(TIMER0_COMPA_vect)`. This function is called when the timer associated with counter 0 goes off. This timer is set up on function `setup_timer(uint8_t ticks, state_t next_state)` here `next_state` is one of those defined on `state_t`. and `ticks` defines on how many slices of time that event will be executed. The time corresponding to a `tick` depends of the definition of `setup_timer`.

The other responsibility of this file is initiate the state machine when a conversion is started. This condition is indicated by a falling edge of the signal `chip_select`. To detect this condition an external interruption is enabled in the `main` function. Every time this condition is met the interrupt vector `ISR (INT0_vect)` will be called. This will start the measuring sequence by calling `setup_timer` with the state `DRIVE_NORTH`.

When the microcontroller is not working it is put into sleep mode by calling `sleep_mode`.

# pulse\_generation.cpp #

This file purpose is to create a pulse of a specific frequency. The timer 1 is used for this. The function `start_pulses` set ups the timer and the interruptions. Every half period the interrupt vector `ISR(TIMER1_COMPA_vect)` goes off and change the level of the pulse. And decrements the counter indicating how many more times this action has to be taken. When there are no more remaining pulses the timer is disabled and the drivers are set to high impedance. The calculation of the enabling or disabling of the transducers is done offline on the interrupt vector `ISR(TIMER1_COMPB_vect)`. This is done to keep a very specific timing on the first routine.

These timers are set on the function `start_pulses(uint8_t pulses, uint8_t enable_mask)`. `pulses` indicates how many pulses need to be send. The user must keep this value low (~100 at a maximum) so the counter of the timer does not overflow. The enable mask correspond to the enable signal send to the H-bridges and specify which ones are driving and which ones are on high impedance state.