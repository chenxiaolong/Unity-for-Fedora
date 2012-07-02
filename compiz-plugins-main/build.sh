#!/usr/bin/env bash

SPECFILE=compiz-plugins-main.spec
MULTILIB=false
DO_NOT_INSTALL=('compiz-plugins-main-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
