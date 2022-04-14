#!/bin/bash
gunicorn kytrade.api.server.app:app
