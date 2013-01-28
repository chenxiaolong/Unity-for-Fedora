#!/usr/bin/env bash

SPECFILE=signon-plugin-oauth2.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_googlecode_version accounts-sso signon-oauth2)"
echo -e "Ubuntu version:    $(get_ubuntu_version signon-plugin-oauth2 ${1:-raring})"
