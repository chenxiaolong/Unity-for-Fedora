#!/usr/bin/env bash

SPECFILE=indicator-power.spec
MULTILIB=false
DO_NOT_INSTALL=('indicator-power-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
