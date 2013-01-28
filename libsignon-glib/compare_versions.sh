#!/usr/bin/env bash

SPECFILE=libsignon-glib.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version) $(get_spec_release --ubuntu)"
echo -e "Upstream version:  $(get_googlecode_version accounts-sso libsignon-glib)"
echo -e "Ubuntu version:    $(get_ubuntu_version libsignon-glib ${1:-raring})"
