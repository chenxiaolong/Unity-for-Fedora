#!/usr/bin/env bash

SPECFILE=python-oauthlib.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version:  $(get_pypi_version oauthlib)"
echo -e "Ubuntu version:    $(get_ubuntu_version python-oauthlib ${1:-raring})"
