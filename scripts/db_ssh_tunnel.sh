#!/usr/bin/env bash

username=$1

ssh -vN -L 5432:120.0.0.1:5432 $1@hackfsu.com