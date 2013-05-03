#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=bamf-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version bamf)"
echo -e "Fedora version:   $(get_fedora_version bamf 18)"
echo -e "Ubuntu version:   $(get_ubuntu_version bamf ${1:-raring})"
