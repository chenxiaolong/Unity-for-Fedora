#!/bin/sh

/usr/lib/rpm/find-provides $* | grep -v '\.so'
