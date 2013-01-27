#!/usr/bin/env bash

SPECFILE=libdbusmenu.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version:  $(get_launchpad_version dbusmenu)"
echo -e "Ubuntu version:    $(get_ubuntu_version libdbusmenu ${1:-raring})"
