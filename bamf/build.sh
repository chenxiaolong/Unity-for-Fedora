#!/usr/bin/env bash

SPECFILE=bamf.spec
MULTILIB=true
MULTILIB_PACKAGES=('bamf'  'bamf-devel'
                   'bamf3' 'bamf3-devel')
DO_NOT_INSTALL=('bamf-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
