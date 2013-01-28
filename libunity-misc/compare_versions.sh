#!/usr/bin/env bash

SPECFILE=libunity-misc.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version:  $(get_launchpad_version libunity-misc)"
echo -e "Ubuntu version:    $(get_ubuntu_version libunity-misc ${1:-raring})"
