#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=libcolumbus.spec
echo -e "Fedora spec version: $(get_spec_version)"
echo -e "Upstream version:    $(get_launchpad_version libcolumbus)"
echo -e "Ubuntu version:      $(get_ubuntu_version libcolumbus ${1:-raring})"
