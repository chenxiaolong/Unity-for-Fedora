#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=gnome-control-center-signon-Fedora_18.spec
echo -e "F18 spec version: $(get_spec_version)"
echo -e "Upstream version: $(get_launchpad_version online-accounts-gnome-control-center credentials-control-center)"
echo -e "Ubuntu version:   $(get_ubuntu_version gnome-control-center-signon ${1:-raring})"
