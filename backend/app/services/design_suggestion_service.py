from app.models.upload import Upload
from app.models.design_suggestion import DesignSuggestion
from app.schemas.upload import UploadCreate
from app.models.upload import ClothType, Occasion, BudgetRange


class DesignSuggestionEngine:
    """AI/Rule-based design suggestion engine"""
    
    @staticmethod
    def generate_suggestions(upload: Upload) -> dict:
        """Generate design suggestions based on cloth type, occasion, and budget"""
        
        # Base suggestions
        suggestions = {
            "neck_design": DesignSuggestionEngine._suggest_neck(
                upload.cloth_type, upload.occasion, upload.gender
            ),
            "sleeve_style": DesignSuggestionEngine._suggest_sleeve(
                upload.cloth_type, upload.occasion, upload.budget_range
            ),
            "embroidery_pattern": DesignSuggestionEngine._suggest_embroidery(
                upload.occasion, upload.budget_range
            ),
            "color_combination": DesignSuggestionEngine._suggest_color(
                upload.occasion, upload.age_group
            ),
            "border_style": DesignSuggestionEngine._suggest_border(
                upload.cloth_type, upload.budget_range
            ),
            "confidence_score": "High"
        }
        
        # Generate description
        suggestions["description"] = DesignSuggestionEngine._generate_description(
            upload, suggestions
        )
        
        return suggestions
    
    @staticmethod
    def _suggest_neck(cloth_type: ClothType, occasion: Occasion, gender: str) -> str:
        """Suggest neck design"""
        
        suggestions = {
            ClothType.SAREE: {
                Occasion.WEDDING: "Boat neck with heavy embellishment",
                Occasion.CASUAL: "Round neck with minimal design",
                Occasion.FESTIVAL: "V-neck with intricate detailing",
                Occasion.PARTY: "Sweetheart neck with embroidery",
                Occasion.OFFICE: "Round neck with professional cut"
            },
            ClothType.KURTI: {
                Occasion.WEDDING: "Keyhole neck with stone work",
                Occasion.CASUAL: "Round neck simple",
                Occasion.FESTIVAL: "High neck with block print",
                Occasion.PARTY: "Plunge neck with embroidery",
                Occasion.OFFICE: "Collar neck formal"
            },
            ClothType.LEHENGA: {
                Occasion.WEDDING: "Sweetheart neck with zari work",
                Occasion.CASUAL: "Round neck",
                Occasion.FESTIVAL: "High neck with mirror work",
                Occasion.PARTY: "Halter neck with embroidery",
                Occasion.OFFICE: "Crew neck"
            },
            ClothType.SHIRT: {
                Occasion.WEDDING: "Mandarin collar",
                Occasion.CASUAL: "Regular collar",
                Occasion.FESTIVAL: "Spread collar",
                Occasion.PARTY: "Cuban collar",
                Occasion.OFFICE: "Oxford collar"
            },
        }
        
        return suggestions.get(cloth_type, {}).get(
            occasion, "Round neck"
        )
    
    @staticmethod
    def _suggest_sleeve(cloth_type: ClothType, occasion: Occasion, budget: BudgetRange) -> str:
        """Suggest sleeve style"""
        
        suggestions = {
            ClothType.SAREE: "No sleeves (blouse sleeves recommended)",
            ClothType.KURTI: {
                Occasion.WEDDING: "3/4 length with embroidery",
                Occasion.CASUAL: "Half sleeves",
                Occasion.FESTIVAL: "Full sleeves with mirror work",
                Occasion.PARTY: "Puffed sleeves",
                Occasion.OFFICE: "3/4 sleeves"
            },
            ClothType.LEHENGA: "Sleeveless or short sleeves",
            ClothType.SHIRT: {
                Occasion.WEDDING: "Full sleeves",
                Occasion.CASUAL: "Half sleeves",
                Occasion.FESTIVAL: "3/4 sleeves",
                Occasion.PARTY: "Full sleeves",
                Occasion.OFFICE: "Full sleeves"
            },
        }
        
        if cloth_type in [ClothType.KURTI, ClothType.SHIRT]:
            return suggestions.get(cloth_type, {}).get(occasion, "Half sleeves")
        
        return suggestions.get(cloth_type, "Standard sleeves")
    
    @staticmethod
    def _suggest_embroidery(occasion: Occasion, budget: BudgetRange) -> str:
        """Suggest embroidery pattern"""
        
        budget_embroidery = {
            BudgetRange.LOW: {
                Occasion.WEDDING: "Simple block printing",
                Occasion.CASUAL: "Light block print",
                Occasion.FESTIVAL: "Simple geometric print",
                Occasion.PARTY: "Basic embroidery on border",
                Occasion.OFFICE: "Minimal print"
            },
            BudgetRange.MEDIUM: {
                Occasion.WEDDING: "Medium embroidery with mirror work",
                Occasion.CASUAL: "Floral embroidery",
                Occasion.FESTIVAL: "Mixed embroidery and block print",
                Occasion.PARTY: "Medium embroidery all over",
                Occasion.OFFICE: "Subtle embroidery"
            },
            BudgetRange.HIGH: {
                Occasion.WEDDING: "Heavy zari and stone work",
                Occasion.CASUAL: "Premium embroidery",
                Occasion.FESTIVAL: "Intricate threadwork and beads",
                Occasion.PARTY: "Full heavy embroidery",
                Occasion.OFFICE: "Premium subtle embroidery"
            }
        }
        
        return budget_embroidery.get(budget, {}).get(
            occasion, "Floral embroidery"
        )
    
    @staticmethod
    def _suggest_color(occasion: Occasion, age_group: str) -> str:
        """Suggest color combination"""
        
        occasion_colors = {
            Occasion.WEDDING: "Deep maroon with gold, royal blue with zari, red with ivory",
            Occasion.CASUAL: "Pastel shades, earthy tones, soft blues",
            Occasion.FESTIVAL: "Vibrant colors - orange, pink, purple, jewel tones",
            Occasion.PARTY: "Black with gold, deep burgundy, emerald green",
            Occasion.OFFICE: "Neutral tones - white, beige, navy, gray"
        }
        
        return occasion_colors.get(occasion, "Multi-color")
    
    @staticmethod
    def _suggest_border(cloth_type: ClothType, budget: BudgetRange) -> str:
        """Suggest border style"""
        
        budget_border = {
            BudgetRange.LOW: "Simple printed border",
            BudgetRange.MEDIUM: "Embroidered border with contrast",
            BudgetRange.HIGH: "Heavy zari border, intricate lace, stone-studded"
        }
        
        return budget_border.get(budget, "Embroidered border")
    
    @staticmethod
    def _generate_description(upload: Upload, suggestions: dict) -> str:
        """Generate full description"""
        
        fabric_types = {
            ClothType.SAREE: "silk",
            ClothType.KURTI: "cotton or silk blend",
            ClothType.LEHENGA: "silk",
            ClothType.SHIRT: "cotton",
        }
        
        fabric = fabric_types.get(upload.cloth_type, "fabric")
        
        description = (
            f"For this {fabric} {upload.cloth_type.value}, a {suggestions['neck_design']} "
            f"with {suggestions['embroidery_pattern'].lower()}, paired with {suggestions['color_combination'].lower()} "
            f"color combination, is recommended for {upload.occasion.value} wear. "
            f"The {suggestions['sleeve_style'].lower()} complement the look perfectly. "
            f"Accessorize with a {suggestions['border_style'].lower()}."
        )
        
        return description
