#!/usr/bin/env bash

SPECFILE=python3-distutils-extra.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version python-distutils-extra)"
echo -e "Ubuntu version:    $(get_ubuntu_version python-distutils-extra ${1:-raring})"
