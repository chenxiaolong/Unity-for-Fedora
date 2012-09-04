#!/usr/bin/env bash

SPECFILE=libsignon-glib.spec
MULTILIB=true
MULTILIB_PACKAGES=('libsignon-glib' 'libsignon-glib-devel')
DO_NOT_INSTALL=('libsignon-glib-debuginfo' 'libsignon-glib-docs')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
