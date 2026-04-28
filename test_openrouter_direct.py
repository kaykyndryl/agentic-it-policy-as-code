#!/usr/bin/env python3
"""
Direct OpenRouter API Test - Shows Raw Model Output
This script demonstrates direct calls to OpenRouter models without agent abstraction.
"""

import os
import json
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment
load_dotenv(override=False)

async def test_openrouter_direct():
    """Test direct OpenRouter API calls with detailed output"""
    
    # Initialize client
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.io/api/v1")
    model = os.getenv("OPENROUTER_MODEL", "nemetron/nemetron-3-super")
    
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not set in .env file")
        print("Please add your OpenRouter API key to continue")
        return
    
    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    
    print("=" * 80)
    print("🧪 DIRECT OPENROUTER API TEST")
    print("=" * 80)
    print(f"\n📡 Configuration:")
    print(f"   API Base URL: {base_url}")
    print(f"   Model: {model}")
    print(f"   API Key: {'*' * 20 + api_key[-8:]}")
    print()
    
    # Test 1: Simple ticket analysis
    print("=" * 80)
    print("TEST 1: Simple Ticket Analysis")
    print("=" * 80)
    
    ticket_1 = """
    Ticket: INC-001
    Title: Password Reset Request
    Description: User forgot their password and cannot access their work account
    Department: Finance
    Severity: Low
    Systems: Active Directory, Email
    """
    
    print(f"\n📝 Input Ticket:\n{ticket_1}")
    print("\n🔄 Sending to OpenRouter model...\n")
    
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an IT support analyst. Analyze the following ticket and provide a risk assessment and recommended actions."
                },
                {
                    "role": "user",
                    "content": f"Analyze this ticket:\n{ticket_1}\n\nProvide: 1) Risk Level, 2) Key Concerns, 3) Recommended Actions"
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        print("✅ Response from OpenRouter:")
        print("-" * 80)
        print(response.choices[0].message.content)
        print("-" * 80)
        print(f"\n📊 API Metadata:")
        print(f"   Model Used: {response.model}")
        print(f"   Tokens Used: {response.usage.total_tokens}")
        print(f"   Input Tokens: {response.usage.prompt_tokens}")
        print(f"   Output Tokens: {response.usage.completion_tokens}")
        
    except Exception as e:
        print(f"❌ Error calling OpenRouter API: {e}")
        print("\nPossible issues:")
        print("   1. API key is invalid or expired")
        print("   2. No internet connection")
        print("   3. OpenRouter service is down")
        print("   4. Rate limit exceeded")
        return
    
    # Test 2: Policy analysis with JSON parsing
    print("\n" + "=" * 80)
    print("TEST 2: Policy Analysis with JSON Output")
    print("=" * 80)
    
    ticket_2 = """
    Ticket: INC-002
    Title: Cannot Access VPN - MFA Issues
    Description: Employee reports repeated MFA failures when connecting to corporate VPN. They are working from home and unable to access necessary resources.
    Department: Engineering
    Severity: Critical
    Systems: VPN, MFA
    """
    
    print(f"\n📝 Input Ticket:\n{ticket_2}")
    print("\n🔄 Sending to OpenRouter model...\n")
    
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an IT security analyst. Analyze IT tickets and respond with JSON containing:
{
    "risk_level": "Low/Medium/High",
    "confidence": 0-1,
    "policies_affected": ["list of policy areas"],
    "reasoning": "detailed explanation",
    "immediate_actions": ["list of actions"],
    "estimated_resolution_time": "time estimate"
}"""
                },
                {
                    "role": "user",
                    "content": f"Analyze this ticket and respond in JSON format:\n{ticket_2}"
                }
            ],
            temperature=0.5,
            max_tokens=600
        )
        
        print("✅ Response from OpenRouter:")
        print("-" * 80)
        response_text = response.choices[0].message.content
        print(response_text)
        print("-" * 80)
        
        # Try to parse as JSON
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                parsed = json.loads(json_str)
                print("\n📊 Parsed Analysis (JSON):")
                print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            print("\n⚠️ Could not parse response as JSON (model may have added explanation text)")
        
        print(f"\n📊 API Metadata:")
        print(f"   Model Used: {response.model}")
        print(f"   Tokens Used: {response.usage.total_tokens}")
        print(f"   Input Tokens: {response.usage.prompt_tokens}")
        print(f"   Output Tokens: {response.usage.completion_tokens}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 3: Multi-turn conversation
    print("\n" + "=" * 80)
    print("TEST 3: Multi-turn Conversation (Agent-like Interaction)")
    print("=" * 80)
    
    messages = [
        {
            "role": "system",
            "content": "You are an IT ticket routing bot. Your job is to classify tickets and recommend routing decisions. Be professional and concise."
        },
        {
            "role": "user",
            "content": "A user reports malware detected on their endpoint. What's the risk level?"
        }
    ]
    
    print("\n💬 Turn 1 - User: A user reports malware detected on their endpoint. What's the risk level?")
    print("\n🔄 Sending to OpenRouter model...\n")
    
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        assistant_response = response.choices[0].message.content
        print("🤖 Assistant Response:")
        print("-" * 80)
        print(assistant_response)
        print("-" * 80)
        
        # Continue conversation
        messages.append({"role": "assistant", "content": assistant_response})
        messages.append({"role": "user", "content": "What actions should we take immediately?"})
        
        print("\n💬 Turn 2 - User: What actions should we take immediately?")
        print("\n🔄 Sending to OpenRouter model...\n")
        
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        assistant_response = response.choices[0].message.content
        print("🤖 Assistant Response:")
        print("-" * 80)
        print(assistant_response)
        print("-" * 80)
        
        print(f"\n📊 API Metadata:")
        print(f"   Model Used: {response.model}")
        print(f"   Tokens Used: {response.usage.total_tokens}")
        print(f"   Input Tokens: {response.usage.prompt_tokens}")
        print(f"   Output Tokens: {response.usage.completion_tokens}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)
    print("\n📌 Summary:")
    print("   - Connected successfully to OpenRouter API")
    print("   - Model provided responses for various ticket types")
    print("   - Token usage tracked for cost monitoring")
    print("   - Multi-turn conversation demonstrated")
    print("\n💡 Next: Check the web interface at http://localhost:8000/")

# Run async test
if __name__ == "__main__":
    asyncio.run(test_openrouter_direct())
