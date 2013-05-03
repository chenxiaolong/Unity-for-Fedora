#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=indicator-messages-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version indicator-messages)"
echo -e "Ubuntu version:   $(get_ubuntu_version indicator-messages ${1:-raring})"
