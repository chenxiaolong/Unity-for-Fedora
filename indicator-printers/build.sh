#!/usr/bin/env bash

SPECFILE=indicator-printers.spec
MULTILIB=false
DO_NOT_INSTALL=('indicator-printers-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
