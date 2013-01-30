#!/usr/bin/env bash

SPECFILE=geis.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version geis)"
echo -e "Ubuntu version:    $(get_ubuntu_version geis ${1:-raring})"
