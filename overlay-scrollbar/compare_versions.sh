#!/usr/bin/env bash

SPECFILE=overlay-scrollbar.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version ayatana-scrollbar overlay-scrollbar)"
echo -e "Ubuntu version:    $(get_ubuntu_version overlay-scrollbar ${1:-raring})"
