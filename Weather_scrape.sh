# Remove pre-exisiting location file
rm location_codes.txt
# Create location_codes.txt
echo $'twc\npsr\nfgz\nabq' >location_codes.txt
# Check if location_codes.txt exists (very unlikely error given script creates the .txt)
if [ ! -f "location_codes.txt" ]; then
    echo "Error: location codes unparsed."
    exit 1
fi

# Realize  each location code from location_codes.txt and execute Python script
while read -r areacode; do
    echo "Fetching weather data for $areacode..."
    python3 Weather_data.py "$areacode"
done < location_codes.txt

echo "Check directory for csv files."