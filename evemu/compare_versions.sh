#!/usr/bin/env bash

SPECFILE=evemu.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version evemu)"
echo -e "Ubuntu version:    $(get_ubuntu_version evemu ${1:-raring})"
