// AI Service for Rock Identification
// Supports multiple AI providers

import { readAsStringAsync } from 'expo-file-system/legacy';

export type RockIdentification = {
  name: string;
  type: string; // igneous, sedimentary, metamorphic
  confidence: number;
  description: string;
  minerals?: string[];
};

// Option 1: OpenAI GPT-4 Vision
export async function identifyRockWithOpenAI(imageUri: string): Promise<RockIdentification> {
  const base64 = await readAsStringAsync(imageUri, { encoding: 'base64' });
  
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.EXPO_PUBLIC_OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'gpt-4o',
      messages: [{
        role: 'user',
        content: [
          {
            type: 'text',
            text: 'Identify this rock. Provide: name, type (igneous/sedimentary/metamorphic), confidence (0-100), brief description, and main minerals. Respond in JSON format: {"name": "", "type": "", "confidence": 0, "description": "", "minerals": []}'
          },
          {
            type: 'image_url',
            image_url: { url: `data:image/jpeg;base64,${base64}` }
          }
        ]
      }],
      max_tokens: 500
    })
  });

  const data = await response.json();
  const result = JSON.parse(data.choices[0].message.content);
  return result;
}

// Option 2: Google Gemini Vision
export async function identifyRockWithGemini(imageUri: string): Promise<RockIdentification> {
  const base64 = await readAsStringAsync(imageUri, { encoding: 'base64' });
  
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${process.env.EXPO_PUBLIC_GEMINI_API_KEY}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{
          parts: [
            { text: 'Identify this rock. Provide: name, type (igneous/sedimentary/metamorphic), confidence (0-100), brief description, and main minerals. Respond in JSON format: {"name": "", "type": "", "confidence": 0, "description": "", "minerals": []}' },
            {
              inline_data: {
                mime_type: 'image/jpeg',
                data: base64
              }
            }
          ]
        }]
      })
    }
  );

  const data = await response.json();
  const result = JSON.parse(data.candidates[0].content.parts[0].text);
  return result;
}

// Option 3: Your Custom Model API
export async function identifyRockWithCustomModel(imageUri: string): Promise<RockIdentification> {
  const formData = new FormData();
  formData.append('image', {
    uri: imageUri,
    type: 'image/jpeg',
    name: 'rock.jpg',
  } as any);

  const apiUrl = process.env.EXPO_PUBLIC_CUSTOM_MODEL_URL;
  if (!apiUrl) {
    throw new Error('EXPO_PUBLIC_CUSTOM_MODEL_URL not configured');
  }

  const response = await fetch(`${apiUrl}/identify`, {
    method: 'POST',
    body: formData,
  });

  const result = await response.json();
  return result;
}

// Main function - choose your provider
export async function identifyRock(imageUri: string): Promise<RockIdentification> {
  // Change this to switch providers
  const provider = process.env.EXPO_PUBLIC_AI_PROVIDER || 'gemini'; // 'openai' | 'gemini' | 'custom'
  
  try {
    switch (provider) {
      case 'openai':
        return await identifyRockWithOpenAI(imageUri);
      case 'gemini':
        return await identifyRockWithGemini(imageUri);
      case 'custom':
        return await identifyRockWithCustomModel(imageUri);
      default:
        throw new Error('Invalid AI provider');
    }
  } catch (error) {
    console.error('Rock identification failed:', error);
    throw error;
  }
}
