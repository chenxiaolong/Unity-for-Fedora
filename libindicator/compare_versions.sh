#!/usr/bin/env bash

SPECFILE=libindicator.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version libindicator)"
echo -e "Fedora version:    $(get_fedora_version libindicator 18)"
echo -e "Ubuntu version:    $(get_ubuntu_version libindicator ${1:-raring})"
