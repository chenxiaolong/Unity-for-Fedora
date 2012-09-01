#!/usr/bin/env bash

SPECFILE=libunity-webapps.spec
MULTILIB=true
MULTILIB_PACKAGES=('libunity-webapps' 'libunity-webapps-devel')
DO_NOT_INSTALL=('libunity-webapps-debuginfo' 'libunity-webapps-docs')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
