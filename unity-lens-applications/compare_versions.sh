#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=unity-lens-applications-Fedora_17.spec
echo -e "F17 spec version: $(get_spec_version)"
SPECFILE=unity-lens-applications-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version unity-lens-applications)"
echo -e "Ubuntu version:   $(get_ubuntu_version unity-lens-applications ${1:-raring})"
