"""
Test script for the rock classification API
"""

import requests
import sys

def test_api(image_path, api_url='http://localhost:5000'):
    """Test the rock classification API"""
    
    print(f"🧪 Testing API at {api_url}")
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{api_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test identification endpoint
    print(f"\n2. Testing identification with image: {image_path}")
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{api_url}/identify", files=files)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n   ✅ Rock Identified!")
            print(f"      Name: {result['name']}")
            print(f"      Type: {result['type']}")
            print(f"      Confidence: {result['confidence']}%")
            print(f"      Description: {result['description']}")
            if result.get('minerals'):
                print(f"      Minerals: {', '.join(result['minerals'])}")
            
            if result.get('top_3_predictions'):
                print(f"\n   Top 3 Predictions:")
                for i, pred in enumerate(result['top_3_predictions'], 1):
                    print(f"      {i}. {pred['name']} - {pred['confidence']:.2f}%")
        else:
            print(f"   ❌ Error: {response.json()}")
            
    except FileNotFoundError:
        print(f"   ❌ Error: Image file not found: {image_path}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_api.py <path_to_rock_image.jpg> [api_url]")
        print("Example: python test_api.py test_rock.jpg")
        print("Example: python test_api.py test_rock.jpg http://localhost:5000")
        sys.exit(1)
    
    image_path = sys.argv[1]
    api_url = sys.argv[2] if len(sys.argv) > 2 else 'http://localhost:5000'
    
    test_api(image_path, api_url)
