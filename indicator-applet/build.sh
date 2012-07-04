#!/usr/bin/env bash

SPECFILE=indicator-applet.spec
MULTILIB=false
DO_NOT_INSTALL=('indicator-applet-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
