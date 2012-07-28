#!/usr/bin/env bash

SPECFILE=nux.spec
# Cannot be multilib because gcc46 is not multilib enabled in any way.
MULTILIB=false
DO_NOT_INSTALL=('nux-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
