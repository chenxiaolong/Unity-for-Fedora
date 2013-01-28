#!/usr/bin/env bash

SPECFILE=signon-ui.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version online-accounts-signon-ui signon-ui)"
echo -e "Ubuntu version:    $(get_ubuntu_version signon-ui ${1:-raring})"
