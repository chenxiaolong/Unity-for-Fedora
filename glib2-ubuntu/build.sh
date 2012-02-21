#!/usr/bin/env bash

SPECFILE=glib2-ubuntu.spec

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
