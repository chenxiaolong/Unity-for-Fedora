#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=libunity-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version libunity)"
echo -e "Ubuntu version:   $(get_ubuntu_version libunity ${1:-raring})"
