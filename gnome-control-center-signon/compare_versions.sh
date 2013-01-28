#!/usr/bin/env bash

SPECFILE=gnome-control-center-signon.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_launchpad_version online-accounts-gnome-control-center credentials-control-center)"
echo -e "Ubuntu version:    $(get_ubuntu_version gnome-control-center-signon ${1:-raring})"
