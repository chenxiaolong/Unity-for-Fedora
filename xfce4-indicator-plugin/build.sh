#!/usr/bin/env bash

SPECFILE=xfce4-indicator-plugin.spec
MULTILIB=false
DO_NOT_INSTALL=('xfce4-indicator-plugin-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
