#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=indicator-datetime-Fedora_17.spec
echo -e "F17 spec version: $(get_spec_version)"
SPECFILE=indicator-datetime-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version indicator-datetime)"
echo -e "Ubuntu version:   $(get_ubuntu_version indicator-datetime ${1:-raring})"
