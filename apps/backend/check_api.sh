#!/bin/bash
# API Health Check Script for grimOS

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Default API URL
API_URL=${1:-"http://localhost:8000"}

echo -e "${YELLOW}Checking grimOS API Health...${NC}"

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is not installed. Please install it to run this script.${NC}"
    exit 1
fi

# Check API health endpoint
echo -e "\n${YELLOW}Checking API health...${NC}"
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${API_URL}/health)

if [ "$HEALTH_RESPONSE" == "200" ]; then
    echo -e "${GREEN}✓ API health check successful${NC}"
else
    echo -e "${RED}✗ API health check failed with status code: ${HEALTH_RESPONSE}${NC}"
    exit 1
fi

# Check API modules
echo -e "\n${YELLOW}Checking Security Module...${NC}"
SECURITY_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${API_URL}/api/v1/security)
if [ "$SECURITY_RESPONSE" == "200" ] || [ "$SECURITY_RESPONSE" == "404" ]; then
    # 404 is acceptable as the base URL might not have a GET handler
    echo -e "${GREEN}✓ Security module check passed${NC}"
else
    echo -e "${RED}✗ Security module check failed with status code: ${SECURITY_RESPONSE}${NC}"
fi

echo -e "\n${YELLOW}Checking Operations Module...${NC}"
OPERATIONS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${API_URL}/api/v1/operations)
if [ "$OPERATIONS_RESPONSE" == "200" ] || [ "$OPERATIONS_RESPONSE" == "404" ]; then
    echo -e "${GREEN}✓ Operations module check passed${NC}"
else
    echo -e "${RED}✗ Operations module check failed with status code: ${OPERATIONS_RESPONSE}${NC}"
fi

echo -e "\n${YELLOW}Checking Cognitive Module...${NC}"
COGNITIVE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${API_URL}/api/v1/cognitive)
if [ "$COGNITIVE_RESPONSE" == "200" ] || [ "$COGNITIVE_RESPONSE" == "404" ]; then
    echo -e "${GREEN}✓ Cognitive module check passed${NC}"
else
    echo -e "${RED}✗ Cognitive module check failed with status code: ${COGNITIVE_RESPONSE}${NC}"
fi

# Check ScrollWeaver API (this should be more specific to demonstrate the NLP functionality)
echo -e "\n${YELLOW}Testing ScrollWeaver NLP API...${NC}"
SCROLLWEAVER_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
    -d '{"natural_language_input":"Assign document review to John then send notification to manager"}' \
    ${API_URL}/api/v1/cognitive/scrollweaver/generate)

if [[ $SCROLLWEAVER_RESPONSE == *"interpreted_steps"* ]]; then
    echo -e "${GREEN}✓ ScrollWeaver API test successful${NC}"
    echo -e "\n${YELLOW}ScrollWeaver Result:${NC}"
    echo "$SCROLLWEAVER_RESPONSE" | python -m json.tool
else
    echo -e "${RED}✗ ScrollWeaver API test failed${NC}"
    echo "$SCROLLWEAVER_RESPONSE"
fi

echo -e "\n${GREEN}All checks completed!${NC}"
