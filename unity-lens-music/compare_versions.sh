#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=unity-lens-music-Fedora_17.spec
echo -e "F17 spec version: $(get_spec_version)"
SPECFILE=unity-lens-music-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version unity-lens-music)"
echo -e "Ubuntu version:   $(get_ubuntu_version unity-lens-music ${1:-raring})"
