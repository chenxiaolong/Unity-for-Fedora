#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=compiz-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version: $(get_launchpad_version compiz)"
echo -e "Ubuntu version:   $(get_ubuntu_version compiz ${1:-raring})"
