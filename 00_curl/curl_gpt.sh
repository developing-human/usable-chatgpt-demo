curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{  
    "model": "gpt-3.5-turbo", 
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."}, 
      {"role": "user", "content": "Recite Dunes litany against fear."}
    ] 
  }'

