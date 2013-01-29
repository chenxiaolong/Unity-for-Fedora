#!/usr/bin/env bash

SPECFILE=account-plugins.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version online-accounts-account-plugins account-plugins)"
echo -e "Ubuntu version:    $(get_ubuntu_version account-plugins ${1:-raring})"
