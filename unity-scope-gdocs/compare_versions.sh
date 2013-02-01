#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=unity-scope-gdocs-Fedora_17.spec
echo -e "F17 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version unity-lens-gdocs unity-scope-gdocs)"
echo -e "Ubuntu version:   $(get_ubuntu_version unity-scope-gdocs ${1:-quantal})"
