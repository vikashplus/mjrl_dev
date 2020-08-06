#!/bin/bash
RULE_FILE="/etc/udev/rules.d/99-dynamixel-usb.rules"
DCLAW_FILTERS="SUBSYSTEM==\"tty\", ENV{ID_MODEL_ID}==\"6014\", ENV{ID_VENDOR_ID}==\"0403\""
add_dclaw_rule() {
rule="ACTION==\"add\", ${DCLAW_FILTERS}, ENV{ID_SERIAL_SHORT}==\"${1}\", SYMLINK+=\"${2}\""
echo "Adding rule: $rule"
echo $rule >> $RULE_FILE
}
# Empty the rule file.
truncate -s 0 ${RULE_FILE}
add_dclaw_rule FT3R4CCT dk
add_dclaw_rule FT2H2MX4 dl
# Reload rules.
udevadm control -R