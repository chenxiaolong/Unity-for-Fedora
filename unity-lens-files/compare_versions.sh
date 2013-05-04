#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=unity-lens-files-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version unity-lens-files)"
echo -e "Ubuntu version:   $(get_ubuntu_version unity-lens-files ${1:-raring})"
