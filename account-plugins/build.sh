#!/usr/bin/env bash

SPECFILE=account-plugins.spec
NO_BASE_PACKAGE=true
MULTILIB=false
DO_NOT_INSTALL=('account-plugins-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
