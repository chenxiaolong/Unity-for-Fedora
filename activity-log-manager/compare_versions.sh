#!/usr/bin/env bash

SPECFILE=activity-log-manager.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version:  $(get_launchpad_version activity-log-manager)"
echo -e "Ubuntu version:    $(get_ubuntu_version activity-log-manager ${1:-raring})"
