#!/usr/bin/env bash

SPECFILE=appmenu-qt.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version appmenu-qt)"
echo -e "Ubuntu version:    $(get_ubuntu_version appmenu-qt ${1:-raring})"
