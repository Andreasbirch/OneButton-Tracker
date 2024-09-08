# Test Project for configuration with both Tilt-switch sensor and BNO module
This test aims to compare readouts of tilt-switch with BNO to see if it can reliably measure movement.

The code for the switch tests if the state has been switched from on to off or vice versa.

The test will poll both the BNO and the switch with a set interval, and compare the two.