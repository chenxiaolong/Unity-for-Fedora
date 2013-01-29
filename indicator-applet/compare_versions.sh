#!/usr/bin/env bash

SPECFILE=indicator-applet.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version indicator-applet)"
echo -e "Ubuntu version:    $(get_ubuntu_version indicator-applet ${1:-raring})"
