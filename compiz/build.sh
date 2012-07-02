#!/usr/bin/env bash

SPECFILE=compiz.spec
MULTILIB=false
DO_NOT_INSTALL=('compiz-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
