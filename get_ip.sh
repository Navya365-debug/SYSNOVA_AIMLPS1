#!/bin/bash

# Get Local IP Address for Network Access

echo "🌐 Network Access Information"
echo "=========================================="

# Get local IP address
if command -v hostname >/dev/null 2>&1; then
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
elif command -v ipconfig >/dev/null 2>&1; then
    LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null)
else
    LOCAL_IP="localhost"
fi

echo "📍 Your Local IP Address: $LOCAL_IP"
echo ""
echo "📱 Access URLs from Other Devices:"
echo "   Application:  http://$LOCAL_IP:3000"
echo "   API Docs:     http://$LOCAL_IP:8000/docs"
echo ""
echo "💡 Instructions:"
echo "   1. Make sure all devices are on the same network"
echo "   2. Use the IP address above instead of localhost"
echo "   3. Ensure firewall allows connections on ports 3000 and 8000"
echo ""
echo "🔧 Quick Test:"
echo "   From another device, try: http://$LOCAL_IP:3000"
echo ""
