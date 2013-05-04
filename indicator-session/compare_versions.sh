#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=indicator-session-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version indicator-session)"
echo -e "Ubuntu version:   $(get_ubuntu_version indicator-session ${1:-raring})"
