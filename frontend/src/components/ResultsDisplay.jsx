import React from "react";
import { motion } from "framer-motion";
import {
  Award,
  Flame,
  Apple,
  Activity,
  Heart,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  XCircle,
  RotateCcw,
  Utensils,
  Droplet,
  Zap,
} from "lucide-react";

const ResultsDisplay = ({ results, onReset }) => {
  const { foodAnalysis, healthAssessment } = results;

  const getScoreColor = (score) => {
    if (score >= 8) return "text-green-400";
    if (score >= 6) return "text-yellow-400";
    return "text-red-400";
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { duration: 0.5 },
    },
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="max-w-6xl mx-auto space-y-6"
    >
      {/* Header with Reset Button */}
      <motion.div
        variants={itemVariants}
        className="flex justify-between items-center"
      >
        <h2 className="text-3xl font-bold text-gradient">Analysis Results</h2>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onReset}
          className="flex items-center gap-2 bg-card-bg glass-effect px-6 py-3 rounded-xl hover:glow-border transition-all duration-300"
        >
          <RotateCcw className="w-5 h-5" />
          New Analysis
        </motion.button>
      </motion.div>

      {/* Main Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Food Identification */}
        <motion.div
          variants={itemVariants}
          className="glass-effect rounded-2xl p-6 glow-border"
        >
          <div className="flex items-center gap-3 mb-4">
            <Utensils className="w-8 h-8 text-neon-blue" />
            <h3 className="text-xl font-bold text-neon-blue">
              Food Identified
            </h3>
          </div>
          <p className="text-2xl font-bold mb-2">{foodAnalysis.foodName}</p>
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-yellow-400" />
            <p className="text-gray-300">
              Confidence:{" "}
              <span className="text-neon-blue font-bold">
                {(foodAnalysis.confidence * 100).toFixed(1)}%
              </span>
            </p>
          </div>
          {foodAnalysis.modelUsed && (
            <p className="text-gray-400 text-sm mt-2">
              Model: <span className="text-neon-purple font-semibold">{foodAnalysis.modelUsed}</span>
            </p>
          )}
          {foodAnalysis.portionSize && (
            <p className="text-gray-400 text-sm mt-2">
              {foodAnalysis.portionSize}
            </p>
          )}
        </motion.div>

        {/* Calories */}
        <motion.div
          variants={itemVariants}
          className="glass-effect rounded-2xl p-6 glow-border"
        >
          <div className="flex items-center gap-3 mb-4">
            <Flame className="w-8 h-8 text-neon-pink" />
            <h3 className="text-xl font-bold text-neon-pink">Calories</h3>
          </div>
          <p className="text-4xl font-bold text-neon-pink mb-2">
            {foodAnalysis.calories}
          </p>
          <p className="text-gray-400 text-sm">
            {healthAssessment.caloriePercentage}% of daily needs
          </p>
          <p className="text-gray-500 text-xs mt-1">
            Daily requirement: {healthAssessment.dailyCalorieNeeds} kcal
          </p>
        </motion.div>

        {/* Health Score */}
        <motion.div
          variants={itemVariants}
          className="glass-effect rounded-2xl p-6 glow-border"
        >
          <div className="flex items-center gap-3 mb-4">
            <Heart className="w-8 h-8 text-neon-purple" />
            <h3 className="text-xl font-bold text-neon-purple">Health Score</h3>
          </div>
          <p
            className={`text-4xl font-bold ${getScoreColor(
              healthAssessment.overallHealthScore
            )}`}
          >
            {healthAssessment.overallHealthScore}/10
          </p>
          <p className="text-gray-400 text-sm mt-2">
            BMI: {healthAssessment.bmi} ({healthAssessment.bmiCategory})
          </p>
        </motion.div>
      </div>

      {/* Nutritional Breakdown */}
      <motion.div
        variants={itemVariants}
        className="glass-effect rounded-2xl p-6 glow-border"
      >
        <div className="flex items-center gap-3 mb-6">
          <Apple className="w-8 h-8 text-neon-blue" />
          <h3 className="text-2xl font-bold text-neon-blue">
            Nutritional Breakdown
          </h3>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <NutritionItem
            icon={<Zap />}
            label="Protein"
            value={foodAnalysis.nutritionalBreakdown.protein}
            color="text-red-400"
          />
          <NutritionItem
            icon={<Droplet />}
            label="Carbs"
            value={foodAnalysis.nutritionalBreakdown.carbohydrates}
            color="text-blue-400"
          />
          <NutritionItem
            icon={<Activity />}
            label="Fats"
            value={foodAnalysis.nutritionalBreakdown.fats}
            color="text-yellow-400"
          />
          <NutritionItem
            icon={<TrendingUp />}
            label="Fiber"
            value={foodAnalysis.nutritionalBreakdown.fiber}
            color="text-green-400"
          />
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-400 mb-1">
              Sugar:{" "}
              <span className="text-white font-semibold">
                {foodAnalysis.nutritionalBreakdown.sugar}
              </span>
            </p>
            <p className="text-gray-400">
              Sodium:{" "}
              <span className="text-white font-semibold">
                {foodAnalysis.nutritionalBreakdown.sodium}
              </span>
            </p>
          </div>
          <div>
            <p className="text-gray-400 mb-1">
              Vitamins:{" "}
              <span className="text-white font-semibold">
                {foodAnalysis.nutritionalBreakdown.vitamins.join(", ")}
              </span>
            </p>
            <p className="text-gray-400">
              Minerals:{" "}
              <span className="text-white font-semibold">
                {foodAnalysis.nutritionalBreakdown.minerals.join(", ")}
              </span>
            </p>
          </div>
        </div>
      </motion.div>

      {/* Ingredients & Food Quality */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Ingredients */}
        <motion.div
          variants={itemVariants}
          className="glass-effect rounded-2xl p-6 glow-border"
        >
          <h3 className="text-xl font-bold text-neon-purple mb-4">
            Ingredients
          </h3>
          <div className="flex flex-wrap gap-2">
            {foodAnalysis.ingredients.map((ingredient, index) => (
              <span
                key={index}
                className="bg-neon-purple/20 border border-neon-purple/50 px-3 py-1 rounded-full text-sm"
              >
                {ingredient}
              </span>
            ))}
          </div>
        </motion.div>

        {/* Food Quality */}
        <motion.div
          variants={itemVariants}
          className="glass-effect rounded-2xl p-6 glow-border"
        >
          <h3 className="text-xl font-bold text-neon-pink mb-4">
            Food Quality Assessment
          </h3>
          <div className="space-y-3">
            <div>
              <p className="text-gray-400 text-sm">Freshness</p>
              <p className="text-white font-semibold">
                {foodAnalysis.foodQualityCycle.freshness}
              </p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Quality Score</p>
              <p
                className={`text-2xl font-bold ${getScoreColor(
                  foodAnalysis.foodQualityCycle.healthScore
                )}`}
              >
                {foodAnalysis.foodQualityCycle.healthScore}/10
              </p>
            </div>
            <div className="text-sm text-gray-300">
              {foodAnalysis.foodQualityCycle.qualityIndicators.map(
                (indicator, index) => (
                  <span key={index} className="block">
                    • {indicator}
                  </span>
                )
              )}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Health Assessment */}
      <motion.div
        variants={itemVariants}
        className="glass-effect rounded-2xl p-6 glow-border"
      >
        <div className="flex items-center gap-3 mb-6">
          <Activity className="w-8 h-8 text-neon-blue" />
          <h3 className="text-2xl font-bold text-neon-blue">
            Personalized Health Assessment
          </h3>
        </div>

        {/* Suitability Status */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-3">
            {healthAssessment.suitability.suitable ? (
              <>
                <CheckCircle className="w-6 h-6 text-green-400" />
                <p className="text-green-400 font-semibold text-lg">
                  Food is suitable for your health profile
                </p>
              </>
            ) : (
              <>
                <AlertTriangle className="w-6 h-6 text-yellow-400" />
                <p className="text-yellow-400 font-semibold text-lg">
                  Caution advised for your health profile
                </p>
              </>
            )}
          </div>
          <p className="text-gray-400">
            Suitability Score:{" "}
            <span
              className={`font-bold ${getScoreColor(
                healthAssessment.suitability.suitabilityScore
              )}`}
            >
              {healthAssessment.suitability.suitabilityScore}/10
            </span>
          </p>
        </div>

        {/* Warnings */}
        {healthAssessment.suitability.warnings.length > 0 && (
          <div className="mb-6">
            <h4 className="text-lg font-semibold text-yellow-400 mb-3 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Important Warnings
            </h4>
            <div className="space-y-2">
              {healthAssessment.suitability.warnings.map((warning, index) => (
                <div
                  key={index}
                  className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3 text-yellow-200"
                >
                  {warning}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        <div>
          <h4 className="text-lg font-semibold text-neon-purple mb-3 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Personalized Recommendations
          </h4>
          <div className="space-y-2">
            {healthAssessment.recommendations.map((recommendation, index) => (
              <div
                key={index}
                className="bg-neon-purple/10 border border-neon-purple/30 rounded-lg p-3 text-gray-200"
              >
                • {recommendation}
              </div>
            ))}
          </div>
        </div>

        {/* Health Conditions */}
        {healthAssessment.healthConditions.length > 0 &&
          healthAssessment.healthConditions[0] !== "None reported" && (
            <div className="mt-6">
              <h4 className="text-sm font-semibold text-gray-400 mb-2">
                Your Health Conditions
              </h4>
              <div className="flex flex-wrap gap-2">
                {healthAssessment.healthConditions.map((condition, index) => (
                  <span
                    key={index}
                    className="bg-red-500/20 border border-red-500/50 px-3 py-1 rounded-full text-sm text-red-300"
                  >
                    {condition}
                  </span>
                ))}
              </div>
            </div>
          )}
      </motion.div>
    </motion.div>
  );
};

const NutritionItem = ({ icon, label, value, color }) => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    className="bg-card-bg/50 rounded-xl p-4 text-center"
  >
    <div className={`${color} flex justify-center mb-2`}>
      {React.cloneElement(icon, { className: "w-6 h-6" })}
    </div>
    <p className="text-gray-400 text-xs mb-1">{label}</p>
    <p className="text-white font-bold text-lg">{value}</p>
  </motion.div>
);

export default ResultsDisplay;
