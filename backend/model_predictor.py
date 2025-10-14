import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import timm
import os
import json

class LocalModelPredictor:
    def __init__(self, confidence_threshold=0.7):
        """
        Initialize the local model predictor with pre-trained models
        confidence_threshold: minimum confidence to trust local models (default 0.7)
        """
        self.confidence_threshold = confidence_threshold
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.models = {}
        self.model_names = {
            'convnext': 'best_model_ConvNeXt-B.pth',
            'efficientnet': 'best_model_EfficientNetV2-M.pth',
            'vit': 'best_model_ViT-B-16.pth'
        }
        
        # Define image transforms
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Load class names (you'll need to provide these based on your training)
        self.load_class_names()
        
        print(f"Local Model Predictor initialized on device: {self.device}")
    
    def load_class_names(self):
        """Load food class names - modify this based on your actual classes"""
        # Default food-101 classes - replace with your actual trained classes
        self.class_names = [
            "apple_pie", "baby_back_ribs", "baklava", "beef_carpaccio", "beef_tartare",
            "beet_salad", "beignets", "bibimbap", "bread_pudding", "breakfast_burrito",
            "bruschetta", "caesar_salad", "cannoli", "caprese_salad", "carrot_cake",
            "ceviche", "cheese_plate", "cheesecake", "chicken_curry", "chicken_quesadilla",
            "chicken_wings", "chocolate_cake", "chocolate_mousse", "churros", "clam_chowder",
            "club_sandwich", "crab_cakes", "creme_brulee", "croque_madame", "cup_cakes",
            "deviled_eggs", "donuts", "dumplings", "edamame", "eggs_benedict",
            "escargots", "falafel", "filet_mignon", "fish_and_chips", "foie_gras",
            "french_fries", "french_onion_soup", "french_toast", "fried_calamari", "fried_rice",
            "frozen_yogurt", "garlic_bread", "gnocchi", "greek_salad", "grilled_cheese_sandwich",
            "grilled_salmon", "guacamole", "gyoza", "hamburger", "hot_and_sour_soup",
            "hot_dog", "huevos_rancheros", "hummus", "ice_cream", "lasagna",
            "lobster_bisque", "lobster_roll_sandwich", "macaroni_and_cheese", "macarons", "miso_soup",
            "mussels", "nachos", "omelette", "onion_rings", "oysters",
            "pad_thai", "paella", "pancakes", "panna_cotta", "peking_duck",
            "pho", "pizza", "pork_chop", "poutine", "prime_rib",
            "pulled_pork_sandwich", "ramen", "ravioli", "red_velvet_cake", "risotto",
            "samosa", "sashimi", "scallops", "seaweed_salad", "shrimp_and_grits",
            "spaghetti_bolognese", "spaghetti_carbonara", "spring_rolls", "steak", "strawberry_shortcake",
            "sushi", "tacos", "takoyaki", "tiramisu", "tuna_tartare",
            "waffles"
        ]
    
    def load_model(self, model_type):
        """Load a specific pre-trained model"""
        if model_type in self.models:
            return self.models[model_type]
        
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                  'models', self.model_names[model_type])
        
        if not os.path.exists(model_path):
            print(f"Model file not found: {model_path}")
            return None
        
        try:
            # Create model architecture based on type using torchvision
            if model_type == 'convnext':
                model = models.convnext_base(weights=None)
                # Replace the classifier head
                model.classifier[2] = torch.nn.Linear(model.classifier[2].in_features, len(self.class_names))
            elif model_type == 'efficientnet':
                model = models.efficientnet_v2_m(weights=None)
                # Replace the classifier head
                model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(self.class_names))
            elif model_type == 'vit':
                model = models.vit_b_16(weights=None)
                # Replace the classifier head
                model.heads.head = torch.nn.Linear(model.heads.head.in_features, len(self.class_names))
            
            # Load weights
            checkpoint = torch.load(model_path, map_location=self.device)
            
            # Handle different checkpoint formats
            if isinstance(checkpoint, dict):
                if 'model_state_dict' in checkpoint:
                    model.load_state_dict(checkpoint['model_state_dict'])
                elif 'state_dict' in checkpoint:
                    model.load_state_dict(checkpoint['state_dict'])
                else:
                    model.load_state_dict(checkpoint)
            else:
                model.load_state_dict(checkpoint)
            
            model = model.to(self.device)
            model.eval()
            
            self.models[model_type] = model
            print(f"Successfully loaded {model_type} model")
            return model
            
        except Exception as e:
            print(f"Error loading {model_type} model: {e}")
            return None
    
    def predict_single_model(self, image, model_type):
        """Make prediction with a single model"""
        model = self.load_model(model_type)
        if model is None:
            return None, 0.0, model_type
        
        try:
            # Preprocess image
            if isinstance(image, str):
                image = Image.open(image).convert('RGB')
            elif not isinstance(image, Image.Image):
                image = Image.fromarray(image).convert('RGB')
            
            img_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)
                
                confidence = confidence.item()
                predicted_class = self.class_names[predicted_idx.item()]
                
                return predicted_class, confidence, model_type
                
        except Exception as e:
            print(f"Error in prediction with {model_type}: {e}")
            return None, 0.0, model_type
    
    def predict_ensemble(self, image):
        """
        Use ensemble of all models and return best prediction
        Returns: (food_name, confidence, model_used, all_predictions)
        """
        predictions = []
        
        # Try all models
        for model_type in ['convnext', 'efficientnet', 'vit']:
            food_name, confidence, model_name = self.predict_single_model(image, model_type)
            if food_name is not None:
                predictions.append({
                    'food_name': food_name,
                    'confidence': confidence,
                    'model': model_name
                })
        
        if not predictions:
            return None, 0.0, None, []
        
        # Sort by confidence and get best prediction
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        best_prediction = predictions[0]
        
        return (
            best_prediction['food_name'],
            best_prediction['confidence'],
            best_prediction['model'],
            predictions
        )
    
    def should_use_gemini(self, confidence):
        """Determine if we should fall back to Gemini API"""
        return confidence < self.confidence_threshold
    
    def format_food_name(self, food_name):
        """Convert snake_case to Title Case"""
        return ' '.join(word.capitalize() for word in food_name.replace('_', ' ').split())
