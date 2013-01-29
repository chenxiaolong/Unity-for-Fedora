#!/usr/bin/env bash

SPECFILE=frame.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version frame)"
echo -e "Ubuntu version:    $(get_ubuntu_version frame ${1:-raring})"
