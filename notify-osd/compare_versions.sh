#!/usr/bin/env bash

SPECFILE=notify-osd.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version notify-osd)"
echo -e "Ubuntu version:    $(get_ubuntu_version notify-osd ${1:-raring})"
