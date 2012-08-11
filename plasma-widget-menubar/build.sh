#!/usr/bin/env bash

SPECFILE=plasma-widget-menubar.spec
MULTILIB=false
DO_NOT_INSTALL=('plasma-widget-menubar-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
