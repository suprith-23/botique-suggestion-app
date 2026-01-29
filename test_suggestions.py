#!/usr/bin/env python3
"""Test design suggestion generation"""

import sys
sys.path.insert(0, '/Users/bpantala/Desktop/suprith/botique-suggestion-app/backend')

from app.models.upload import Upload
from app.services.design_suggestion_service import DesignSuggestionEngine

# Create a test upload object similar to what comes from the database
test_upload = Upload(
    id=1,
    user_id=1,
    file_path="/uploads/test.jpg",
    cloth_type="saree",  # This will be a string from DB
    occasion="wedding",
    gender="female",
    age_group="adult",
    budget_range="3000-8000",
    size_info="Medium"
)

print("Testing suggestion generation...")
print(f"Upload: cloth_type={test_upload.cloth_type}, occasion={test_upload.occasion}")

try:
    suggestions = DesignSuggestionEngine.generate_suggestions(test_upload)
    print("\n✓ Suggestions generated successfully!")
    for key, value in suggestions.items():
        print(f"  {key}: {value}")
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
