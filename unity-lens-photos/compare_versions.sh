#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=unity-lens-photos-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version unity-lens-photos)"
echo -e "Ubuntu version:   $(get_ubuntu_version unity-lens-photos ${1:-raring})"
