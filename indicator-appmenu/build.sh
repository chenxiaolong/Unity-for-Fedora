#!/usr/bin/env bash

SPECFILE=indicator-appmenu.spec
MULTILIB=false
DO_NOT_INSTALL=('indicator-appmenu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
