#!/usr/bin/env bash

SPECFILE=indicator-printers.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version:  $(get_launchpad_version indicator-printers)"
echo -e "Ubuntu version:    $(get_ubuntu_version indicator-printers ${1:-raring})"
