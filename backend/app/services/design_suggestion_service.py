from app.models.upload import Upload
from app.models.design_suggestion import DesignSuggestion
from app.schemas.upload import UploadCreate
from app.models.upload import ClothType, Occasion, BudgetRange


class DesignSuggestionEngine:
    """AI/Rule-based design suggestion engine with curated fashion designs"""
    
    # Web-inspired design templates based on latest fashion trends - using string keys
    DESIGN_TEMPLATES = {
        "saree": {
            "wedding": [
                {
                    "neck": "Boat neck with heavy embellishment",
                    "sleeve": "No sleeves (blouse sleeves - full with zari work)",
                    "embroidery": "Heavy zari and stone work with beadwork",
                    "color": "Deep maroon with gold, royal blue with zari",
                    "border": "Intricate gold zari border with semi-precious stones"
                },
                {
                    "neck": "V-neck with intricate detailing",
                    "sleeve": "No sleeves (blouse sleeves - 3/4 with embroidery)",
                    "embroidery": "Threadwork with cutwork embroidery",
                    "color": "Red with ivory and gold accents",
                    "border": "Heavy embroidered border with tassel work"
                }
            ],
            "casual": [
                {
                    "neck": "Round neck with minimal design",
                    "sleeve": "No sleeves (blouse sleeves - half sleeves)",
                    "embroidery": "Light block print or simple floral",
                    "color": "Pastel shades - light blue, peach, cream",
                    "border": "Simple printed border"
                }
            ],
            "festival": [
                {
                    "neck": "V-neck with block print",
                    "sleeve": "No sleeves (blouse sleeves - full sleeves with mirror work)",
                    "embroidery": "Geometric block print with mirror work",
                    "color": "Vibrant orange with purple, or pink with green",
                    "border": "Printed border with mirror accents"
                }
            ],
            "party": [
                {
                    "neck": "Sweetheart neck with embroidery",
                    "sleeve": "No sleeves (blouse sleeves - puffed sleeves)",
                    "embroidery": "Medium embroidery with sequin work",
                    "color": "Black with gold, deep burgundy with silver",
                    "border": "Sequined border with lace"
                }
            ],
            "office": [
                {
                    "neck": "Round neck with professional cut",
                    "sleeve": "No sleeves (blouse sleeves - 3/4 sleeves)",
                    "embroidery": "Minimal print",
                    "color": "Neutral tones - white, navy, gray, beige",
                    "border": "Simple solid border"
                }
            ]
        },
        "kurti": {
            "wedding": [
                {
                    "neck": "Keyhole neck with stone work",
                    "sleeve": "Full sleeves with heavy embroidery and stone work",
                    "embroidery": "Heavy embroidery all over with stone and bead work",
                    "color": "Deep maroon with gold, royal blue with silver",
                    "border": "Heavy embroidered hemline"
                }
            ],
            "casual": [
                {
                    "neck": "Round neck simple",
                    "sleeve": "Half sleeves",
                    "embroidery": "Light block print or no print",
                    "color": "Pastel shades - sky blue, peach, mint green",
                    "border": "Simple contrast border"
                }
            ],
            "festival": [
                {
                    "neck": "High neck with block print",
                    "sleeve": "Full sleeves with mirror work",
                    "embroidery": "Mixed embroidery and block print with mirrors",
                    "color": "Vibrant - orange, pink, purple combinations",
                    "border": "Patterned border with mirror embellishments"
                }
            ],
            "party": [
                {
                    "neck": "Plunge neck with embroidery",
                    "sleeve": "Puffed sleeves with embroidery",
                    "embroidery": "Medium embroidery with sequin details",
                    "color": "Black with gold, emerald with silver",
                    "border": "Sequined hemline"
                }
            ],
            "office": [
                {
                    "neck": "Collar neck formal",
                    "sleeve": "Full sleeves",
                    "embroidery": "Minimal or no embroidery",
                    "color": "Professional tones - white, navy, gray, black",
                    "border": "Subtle solid border"
                }
            ]
        },
        "lehenga": {
            "wedding": [
                {
                    "neck": "Sweetheart neck with zari work",
                    "sleeve": "Full sleeves or cap sleeves with heavy embroidery",
                    "embroidery": "Heavy zari work with beads and stones",
                    "color": "Maroon with gold, royal blue with silver",
                    "border": "Heavily embroidered border on lehenga and dupatta"
                }
            ],
            "casual": [
                {
                    "neck": "Round neck",
                    "sleeve": "Half sleeves or sleeveless",
                    "embroidery": "Light print or minimal embroidery",
                    "color": "Pastel or earthy shades",
                    "border": "Simple printed or contrast border"
                }
            ],
            "festival": [
                {
                    "neck": "V-neck with ethnic detailing",
                    "sleeve": "Full sleeves with ethnic embroidery",
                    "embroidery": "Intricate ethnic motifs with beads",
                    "color": "Vibrant colors - orange, pink, purple",
                    "border": "Ornamental border with traditional patterns"
                }
            ],
            "party": [
                {
                    "neck": "Halter neck with embroidery",
                    "sleeve": "Sleeveless with embellished armhole",
                    "embroidery": "Medium embroidery with sequins",
                    "color": "Black with gold, emerald, deep burgundy",
                    "border": "Sequined border"
                }
            ],
            "office": [
                {
                    "neck": "Crew neck",
                    "sleeve": "Full sleeves",
                    "embroidery": "Minimal print",
                    "color": "Neutral professional tones",
                    "border": "Simple solid border"
                }
            ]
        },
        "shirt": {
            "wedding": [
                {
                    "neck": "Mandarin collar with embroidery",
                    "sleeve": "Full sleeves with embroidery",
                    "embroidery": "Embroidered pattern on front and sleeves",
                    "color": "Maroon, navy with gold accents",
                    "border": "Embroidered border on sleeves and hem"
                }
            ],
            "casual": [
                {
                    "neck": "Regular collar",
                    "sleeve": "Half sleeves",
                    "embroidery": "Light print or solid color",
                    "color": "Light shades - white, light blue, pastel",
                    "border": "Simple contrast border"
                }
            ],
            "festival": [
                {
                    "neck": "Spread collar with print",
                    "sleeve": "3/4 sleeves",
                    "embroidery": "Ethnic print or embroidery",
                    "color": "Vibrant colors with contrasts",
                    "border": "Printed border"
                }
            ],
            "party": [
                {
                    "neck": "Cuban collar",
                    "sleeve": "Full sleeves",
                    "embroidery": "Medium embroidery or print",
                    "color": "Dark shades with metallic accents",
                    "border": "Embellished border"
                }
            ],
            "office": [
                {
                    "neck": "Oxford collar",
                    "sleeve": "Full sleeves",
                    "embroidery": "No embroidery",
                    "color": "Professional colors - white, light blue, neutral",
                    "border": "Simple collar band"
                }
            ]
        },
        "dress": {
            "wedding": [
                {
                    "neck": "V-neck or sweetheart with embellishment",
                    "sleeve": "Full sleeves or sleeveless",
                    "embroidery": "Heavy embroidery with beads and stones",
                    "color": "Bridal colors - ivory, gold, light pink",
                    "border": "Ornamental border"
                }
            ],
            "casual": [
                {
                    "neck": "Round neck",
                    "sleeve": "Half or 3/4 sleeves",
                    "embroidery": "No embroidery or minimal print",
                    "color": "Pastels or neutral tones",
                    "border": "Simple hem"
                }
            ],
            "festival": [
                {
                    "neck": "V-neck with print",
                    "sleeve": "3/4 or full sleeves",
                    "embroidery": "Ethnic print or embroidery",
                    "color": "Vibrant festive colors",
                    "border": "Patterned border"
                }
            ],
            "party": [
                {
                    "neck": "Deep V-neck or strapless",
                    "sleeve": "Sleeveless or thin straps",
                    "embroidery": "Sequins and beads",
                    "color": "Dark or metallic shades",
                    "border": "Embellished hemline"
                }
            ]
        },
        "blouse": {
            "wedding": [
                {
                    "neck": "High neck with embroidery",
                    "sleeve": "Full sleeves with embroidery",
                    "embroidery": "Heavy embroidery work",
                    "color": "Rich colors - maroon, burgundy, deep colors",
                    "border": "Embroidered border"
                }
            ],
            "casual": [
                {
                    "neck": "Round neck",
                    "sleeve": "Half or 3/4 sleeves",
                    "embroidery": "Minimal or no embroidery",
                    "color": "Light neutral colors",
                    "border": "Simple border"
                }
            ]
        }
    }
    
    @staticmethod
    def generate_suggestions(upload: Upload) -> dict:
        """Generate design suggestions based on cloth type, occasion, and budget"""
        
        try:
            import random
            
            # Normalize string values (from database)
            cloth_type_str = str(upload.cloth_type).lower().strip()
            occasion_str = str(upload.occasion).lower().strip()
            budget_str = str(upload.budget_range).lower().strip() if upload.budget_range else "3000-8000"
            
            # Try to get template from DESIGN_TEMPLATES using string keys
            template = None
            if cloth_type_str in DesignSuggestionEngine.DESIGN_TEMPLATES:
                cloth_templates = DesignSuggestionEngine.DESIGN_TEMPLATES[cloth_type_str]
                if occasion_str in cloth_templates:
                    template_options = cloth_templates[occasion_str]
                    if template_options and len(template_options) > 0:
                        template = random.choice(template_options)
            
            # Use template if available, otherwise use fallback suggestions
            if template:
                suggestions = {
                    "neck_design": template["neck"],
                    "sleeve_style": template["sleeve"],
                    "embroidery_pattern": template["embroidery"],
                    "color_combination": template["color"],
                    "border_style": template["border"],
                    "confidence_score": "High"
                }
            else:
                # Fallback to algorithm-based suggestions
                suggestions = {
                    "neck_design": DesignSuggestionEngine._suggest_neck(
                        cloth_type_str, occasion_str, upload.gender
                    ),
                    "sleeve_style": DesignSuggestionEngine._suggest_sleeve(
                        cloth_type_str, occasion_str, budget_str
                    ),
                    "embroidery_pattern": DesignSuggestionEngine._suggest_embroidery(
                        occasion_str, budget_str
                    ),
                    "color_combination": DesignSuggestionEngine._suggest_color(
                        occasion_str, upload.age_group
                    ),
                    "border_style": DesignSuggestionEngine._suggest_border(
                        cloth_type_str, budget_str
                    ),
                    "confidence_score": "High"
                }
            
            # Generate description
            suggestions["description"] = DesignSuggestionEngine._generate_description(
                upload, suggestions
            )
            
            return suggestions
        except Exception as e:
            # Fallback: return basic suggestion if anything fails
            return {
                "neck_design": "Round neck",
                "sleeve_style": "Standard sleeves",
                "embroidery_pattern": "Basic embroidery",
                "color_combination": "Multi-color",
                "border_style": "Simple border",
                "description": f"Design suggestion for {upload.cloth_type} for {upload.occasion} wear.",
                "confidence_score": "Medium"
            }
    
    @staticmethod
    def _suggest_neck(cloth_type, occasion, gender) -> str:
        """Suggest neck design"""
        
        suggestions = {
            "saree": {
                "wedding": "Boat neck with heavy embellishment",
                "casual": "Round neck with minimal design",
                "festival": "V-neck with intricate detailing",
                "party": "Sweetheart neck with embroidery",
                "office": "Round neck with professional cut"
            },
            "kurti": {
                "wedding": "Keyhole neck with stone work",
                "casual": "Round neck simple",
                "festival": "High neck with block print",
                "party": "Plunge neck with embroidery",
                "office": "Collar neck formal"
            },
            "lehenga": {
                "wedding": "Sweetheart neck with zari work",
                "casual": "Round neck",
                "festival": "High neck with mirror work",
                "party": "Halter neck with embroidery",
                "office": "Crew neck"
            },
            "shirt": {
                "wedding": "Mandarin collar",
                "casual": "Regular collar",
                "festival": "Spread collar",
                "party": "Cuban collar",
                "office": "Oxford collar"
            },
        }
        
        cloth_type_str = str(cloth_type).lower().strip()
        occasion_str = str(occasion).lower().strip()
        
        if cloth_type_str in suggestions:
            if occasion_str in suggestions[cloth_type_str]:
                return suggestions[cloth_type_str][occasion_str]
        
        return "Round neck"
    
    @staticmethod
    def _suggest_sleeve(cloth_type, occasion, budget) -> str:
        """Suggest sleeve style"""
        
        suggestions = {
            "saree": "No sleeves (blouse sleeves recommended)",
            "kurti": {
                "wedding": "3/4 length with embroidery",
                "casual": "Half sleeves",
                "festival": "Full sleeves with mirror work",
                "party": "Puffed sleeves",
                "office": "3/4 sleeves"
            },
            "lehenga": "Sleeveless or short sleeves",
            "shirt": {
                "wedding": "Full sleeves",
                "casual": "Half sleeves",
                "festival": "3/4 sleeves",
                "party": "Full sleeves",
                "office": "Full sleeves"
            },
        }
        
        cloth_type_str = str(cloth_type).lower().strip()
        occasion_str = str(occasion).lower().strip()
        
        if cloth_type_str in suggestions:
            if isinstance(suggestions[cloth_type_str], dict):
                if occasion_str in suggestions[cloth_type_str]:
                    return suggestions[cloth_type_str][occasion_str]
                return "Standard sleeves"
            else:
                return suggestions[cloth_type_str]
        
        return "Standard sleeves"
    
    @staticmethod
    def _suggest_embroidery(occasion, budget) -> str:
        """Suggest embroidery pattern"""
        
        budget_embroidery = {
            "1000-3000": {
                "wedding": "Simple block printing",
                "casual": "Light block print",
                "festival": "Simple geometric print",
                "party": "Basic embroidery on border",
                "office": "Minimal print"
            },
            "3000-8000": {
                "wedding": "Medium embroidery with mirror work",
                "casual": "Floral embroidery",
                "festival": "Mixed embroidery and block print",
                "party": "Medium embroidery all over",
                "office": "Subtle embroidery"
            },
            "10000+": {
                "wedding": "Heavy zari and stone work",
                "casual": "Premium embroidery",
                "festival": "Intricate threadwork and beads",
                "party": "Full heavy embroidery",
                "office": "Premium subtle embroidery"
            }
        }
        
        budget_str = str(budget).lower().strip()
        occasion_str = str(occasion).lower().strip()
        
        if budget_str in budget_embroidery:
            if occasion_str in budget_embroidery[budget_str]:
                return budget_embroidery[budget_str][occasion_str]
        
        return "Floral embroidery"
    
    @staticmethod
    def _suggest_color(occasion, age_group) -> str:
        """Suggest color combination"""
        
        occasion_colors = {
            "wedding": "Deep maroon with gold, royal blue with zari, red with ivory",
            "casual": "Pastel shades, earthy tones, soft blues",
            "festival": "Vibrant colors - orange, pink, purple, jewel tones",
            "party": "Black with gold, deep burgundy, emerald green",
            "office": "Neutral tones - white, beige, navy, gray"
        }
        
        occasion_str = str(occasion).lower().strip()
        
        if occasion_str in occasion_colors:
            return occasion_colors[occasion_str]
        
        return "Multi-color"
    
    @staticmethod
    def _suggest_border(cloth_type, budget) -> str:
        """Suggest border style"""
        
        budget_border = {
            "1000-3000": "Simple printed border",
            "3000-8000": "Embroidered border with contrast",
            "10000+": "Heavy zari border, intricate lace, stone-studded"
        }
        
        budget_str = str(budget).lower().strip()
        
        if budget_str in budget_border:
            return budget_border[budget_str]
        
        return "Embroidered border"
    
    @staticmethod
    def _generate_description(upload: Upload, suggestions: dict) -> str:
        """Generate full description"""
        
        fabric_types = {
            "saree": "silk or cotton",
            "kurti": "cotton or silk blend",
            "lehenga": "silk with cotton lining",
            "shirt": "premium cotton",
            "dress": "premium fabric",
            "blouse": "silk or cotton blend"
        }
        
        cloth_type_str = str(upload.cloth_type).lower().strip()
        occasion_str = str(upload.occasion).lower().strip()
        
        fabric = "premium fabric"
        if cloth_type_str in fabric_types:
            fabric = fabric_types[cloth_type_str]
        
        description = (
            f"For this {fabric} {upload.cloth_type}, a {suggestions['neck_design'].lower()} "
            f"with {suggestions['embroidery_pattern'].lower()}, paired with {suggestions['color_combination'].lower()} "
            f"color combination, is recommended for {occasion_str} wear. "
            f"The {suggestions['sleeve_style'].lower()} complement the look perfectly. "
            f"Accessorize with a {suggestions['border_style'].lower()}."
        )
        
        return description
