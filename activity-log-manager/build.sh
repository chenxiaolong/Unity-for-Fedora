#!/usr/bin/env bash

SPECFILE=activity-log-manager.spec
MULTILIB=false
DO_NOT_INSTALL=('activity-log-manager-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
