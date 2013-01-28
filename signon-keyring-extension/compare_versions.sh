#!/usr/bin/env bash

SPECFILE=signon-keyring-extension.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version online-accounts-keyring-extension keyring)"
echo -e "Ubuntu version:    $(get_ubuntu_version signon-keyring-extension ${1:-raring})"
