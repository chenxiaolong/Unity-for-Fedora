#!/usr/bin/env bash

SPECFILE=signon-ui.spec
MULTILIB=false
DO_NOT_INSTALL=('signon-ui-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
