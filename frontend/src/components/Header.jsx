import React from "react";
import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

const Header = () => {
  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className="py-8 px-4"
    >
      <div className="container mx-auto">
        <div className="flex items-center justify-center space-x-4">
          <motion.div
            animate={{
              rotate: [0, 360],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear",
            }}
          >
            <Sparkles className="w-12 h-12 text-neon-blue" />
          </motion.div>

          <div>
            <h1 className="text-5xl font-bold text-gradient mb-2">
              AI Food Analyzer
            </h1>
            <p className="text-gray-400 text-center">
              Advanced Nutritional Intelligence & Personalized Health Assessment
            </p>
          </div>
        </div>
      </div>
    </motion.header>
  );
};

export default Header;
