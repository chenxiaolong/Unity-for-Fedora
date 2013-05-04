#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=unity-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version: $(get_launchpad_version unity)"
echo -e "Ubuntu version:   $(get_ubuntu_version unity ${1:-raring})"
