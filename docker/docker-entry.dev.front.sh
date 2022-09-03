#!/bin/sh

echo "Installing Node modules..."
npm install
echo "Node modules installed."

exec "$@"
