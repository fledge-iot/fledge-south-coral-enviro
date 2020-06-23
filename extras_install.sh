#!/usr/bin/env bash

##--------------------------------------------------------------------
## Copyright (c) 2020 Dianomic Systems Inc.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##--------------------------------------------------------------------

##
## Author: Ashish Jabble, Ashwin Gopalakrishnan
##

ID=$(cat /etc/os-release | grep -w ID | cut -f2 -d"=")
if [[ ${ID} == "raspbian" ]]; then
    echo "The sensor board includes an EEPROM that allows the Raspberry Pi to automatically apply the device tree that configures all the header pins. Done"
else
    echo "Applying device tree"
    curl "https://coral.googlesource.com/coral-cloud/+/refs/heads/master/coral-enviro-devicetree/coral-enviro-board.dtbo?format=TEXT" \
| base64 --decode | tee /boot/coral-enviro-board.dtbo > /dev/null
    sed -i '$ s/$/ coral-enviro-board/' /boot/overlays.txt
fi

echo "Please reboot"


