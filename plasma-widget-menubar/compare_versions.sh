#!/usr/bin/env bash

SPECFILE=plasma-widget-menubar.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version plasma-widget-menubar)"
echo -e "Ubuntu version:    $(get_ubuntu_version plasma-widget-menubar ${1:-raring})"
