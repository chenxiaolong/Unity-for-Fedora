#!/usr/bin/env bash

SPECFILE=sni-qt.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version sni-qt)"
echo -e "Ubuntu version:    $(get_ubuntu_version sni-qt ${1:-raring})"
