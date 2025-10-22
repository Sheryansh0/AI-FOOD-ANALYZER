import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Upload, User, Activity, AlertCircle, Loader } from "lucide-react";
import axios from "axios";
import { API_ENDPOINTS } from "../config/api";

const FoodAnalyzerForm = ({ onAnalysisComplete, loading, setLoading }) => {
  const [imagePreview, setImagePreview] = useState(null);
  const [formData, setFormData] = useState({
    image: null,
    height: "",
    weight: "",
    diseases: "",
  });
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setError("Image size should be less than 10MB");
        return;
      }

      setFormData({ ...formData, image: file });
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
      setError("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!formData.image) {
      setError("Please upload a food image");
      return;
    }

    if (!formData.height || !formData.weight) {
      setError("Please enter your height and weight");
      return;
    }

    setLoading(true);

    try {
      const submitData = new FormData();
      submitData.append("image", formData.image);
      submitData.append("height", formData.height);
      submitData.append("weight", formData.weight);
      submitData.append("diseases", formData.diseases);

      const response = await axios.post(API_ENDPOINTS.analyze, submitData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      onAnalysisComplete(response.data);
    } catch (err) {
      setError(
        err.response?.data?.error || "Failed to analyze food. Please try again."
      );
      setLoading(false);
    }
  };

  return (
    <motion.div
      className="max-w-2xl mx-auto"
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="glass-effect rounded-3xl p-8 glow-border">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Image Upload Section */}
          <div className="space-y-4">
            <label className="block text-lg font-semibold text-neon-blue flex items-center gap-2">
              <Upload className="w-5 h-5" />
              Upload Food Image
            </label>

            <motion.div
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => fileInputRef.current?.click()}
              className="relative border-2 border-dashed border-neon-blue/50 rounded-2xl p-8 cursor-pointer hover:border-neon-blue transition-all duration-300"
            >
              {imagePreview ? (
                <div className="relative">
                  <img
                    src={imagePreview}
                    alt="Preview"
                    className="w-full h-64 object-cover rounded-xl"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 hover:opacity-100 transition-opacity duration-300 rounded-xl flex items-center justify-center">
                    <p className="text-white font-semibold">
                      Click to change image
                    </p>
                  </div>
                </div>
              ) : (
                <div className="text-center">
                  <Upload className="w-16 h-16 mx-auto mb-4 text-neon-blue animate-float" />
                  <p className="text-gray-300 text-lg">
                    Click or drag to upload food image
                  </p>
                  <p className="text-gray-500 text-sm mt-2">
                    Supports JPG, PNG (Max 10MB)
                  </p>
                </div>
              )}
            </motion.div>

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="hidden"
            />
          </div>

          {/* Personal Information */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-neon-purple mb-2 flex items-center gap-2">
                <User className="w-4 h-4" />
                Height (cm)
              </label>
              <input
                type="number"
                value={formData.height}
                onChange={(e) =>
                  setFormData({ ...formData, height: e.target.value })
                }
                placeholder="170"
                className="w-full bg-card-bg/50 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon-purple transition-all duration-300"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-neon-purple mb-2 flex items-center gap-2">
                <Activity className="w-4 h-4" />
                Weight (kg)
              </label>
              <input
                type="number"
                value={formData.weight}
                onChange={(e) =>
                  setFormData({ ...formData, weight: e.target.value })
                }
                placeholder="70"
                className="w-full bg-card-bg/50 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon-purple transition-all duration-300"
              />
            </div>
          </div>

          {/* Health Conditions */}
          <div>
            <label className="block text-sm font-semibold text-neon-pink mb-2 flex items-center gap-2">
              <AlertCircle className="w-4 h-4" />
              Health Conditions (Optional)
            </label>
            <input
              type="text"
              value={formData.diseases}
              onChange={(e) =>
                setFormData({ ...formData, diseases: e.target.value })
              }
              placeholder="e.g., diabetes, hypertension (comma-separated)"
              className="w-full bg-card-bg/50 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-neon-pink transition-all duration-300"
            />
            <p className="text-gray-500 text-xs mt-1">
              Enter any health conditions or dietary restrictions
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-red-500/20 border border-red-500 rounded-xl p-4 text-red-300"
            >
              {error}
            </motion.div>
          )}

          {/* Submit Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-neon-blue via-neon-purple to-neon-pink text-white font-bold py-4 rounded-xl hover:shadow-2xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                Analyzing with AI...
              </>
            ) : (
              "Analyze Food"
            )}
          </motion.button>
        </form>
      </div>
    </motion.div>
  );
};

export default FoodAnalyzerForm;
