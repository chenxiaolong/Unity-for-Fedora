#!/usr/bin/env bash

SPECFILE=grail.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version grail)"
echo -e "Ubuntu version:    $(get_ubuntu_version grail ${1:-raring})"
