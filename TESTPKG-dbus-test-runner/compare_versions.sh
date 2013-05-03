#!/usr/bin/env bash

source "$(dirname ${0})/../version_checker.sh"

SPECFILE=dbus-test-runner.spec
echo -e "Fedora spec version: $(get_spec_version)"
echo -e "Upstream version:    $(get_launchpad_version dbus-test-runner)"
echo -e "Ubuntu version:      $(get_ubuntu_version dbus-test-runner ${1:-raring})"
