#!/usr/bin/env bash

SPECFILE=libindicate.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version libindicate)"
echo -e "Ubuntu version:    $(get_ubuntu_version libindicate ${1:-raring})"
