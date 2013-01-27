#!/usr/bin/env bash

SPECFILE=dee.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version:  $(get_launchpad_version dee)"
echo -e "Ubuntu version:    $(get_ubuntu_version dee ${1:-raring})"
