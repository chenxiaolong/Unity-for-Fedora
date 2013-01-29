#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=indicator-sound-Fedora_17.spec
echo -e "F17 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
SPECFILE=indicator-sound-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version indicator-sound)"
echo -e "Ubuntu version:   $(get_ubuntu_version indicator-sound ${1:-raring})"
