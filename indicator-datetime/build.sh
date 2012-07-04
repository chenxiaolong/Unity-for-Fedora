#!/usr/bin/env bash

SPECFILE=indicator-datetime.spec
MULTILIB=false
DO_NOT_INSTALL=('indicator-datetime-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
