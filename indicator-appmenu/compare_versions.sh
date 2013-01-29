#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=indicator-appmenu-Fedora_17.spec
echo -e "F17 spec version: $(get_spec_version)"
SPECFILE=indicator-appmenu-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version indicator-appmenu)"
echo -e "Ubuntu version:   $(get_ubuntu_version indicator-appmenu ${1:-raring})"
