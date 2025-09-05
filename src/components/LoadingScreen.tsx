import React from 'react'
import { motion } from 'framer-motion'

const LoadingScreen = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-white flex items-center justify-center z-50"
    >
      <div className="text-center">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="mb-8"
        >
          <div className="w-32 h-32 mx-auto mb-6 relative">
            {/* Holographic swirling marble */}
            <motion.div
              animate={{ 
                rotate: 360,
                scale: [1, 1.1, 1],
              }}
              transition={{ 
                rotate: { duration: 3, repeat: Infinity, ease: "linear" },
                scale: { duration: 2, repeat: Infinity, ease: "easeInOut" }
              }}
              className="w-full h-full relative"
            >
              {/* Outer holographic ring */}
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 opacity-80 blur-sm"></div>
              
              {/* Middle swirling layer */}
              <motion.div
                animate={{ rotate: -360 }}
                transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                className="absolute inset-2 rounded-full bg-gradient-to-r from-cyan-300 via-blue-400 to-indigo-500 opacity-70"
              ></motion.div>
              
              {/* Inner marble core */}
              <motion.div
                animate={{ 
                  rotate: 360,
                  background: [
                    "linear-gradient(45deg, #667eea 0%, #764ba2 100%)",
                    "linear-gradient(45deg, #f093fb 0%, #f5576c 100%)",
                    "linear-gradient(45deg, #4facfe 0%, #00f2fe 100%)",
                    "linear-gradient(45deg, #667eea 0%, #764ba2 100%)"
                  ]
                }}
                transition={{ 
                  rotate: { duration: 2.5, repeat: Infinity, ease: "linear" },
                  background: { duration: 6, repeat: Infinity, ease: "easeInOut" }
                }}
                className="absolute inset-4 rounded-full flex items-center justify-center shadow-2xl"
              >
                <motion.span 
                  animate={{ 
                    color: ["#ffffff", "#f0f9ff", "#e0f2fe", "#ffffff"],
                    textShadow: [
                      "0 0 10px rgba(255,255,255,0.5)",
                      "0 0 20px rgba(59,130,246,0.8)",
                      "0 0 10px rgba(255,255,255,0.5)"
                    ]
                  }}
                  transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                  className="text-white font-bold text-2xl"
                >
                  II
                </motion.span>
              </motion.div>
              
              {/* Floating particles */}
              {[...Array(6)].map((_, i) => (
                <motion.div
                  key={i}
                  animate={{
                    x: [0, Math.cos(i * 60 * Math.PI / 180) * 40, 0],
                    y: [0, Math.sin(i * 60 * Math.PI / 180) * 40, 0],
                    opacity: [0.3, 0.8, 0.3],
                    scale: [0.5, 1, 0.5]
                  }}
                  transition={{
                    duration: 3 + i * 0.2,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: i * 0.3
                  }}
                  className="absolute top-1/2 left-1/2 w-2 h-2 bg-white rounded-full transform -translate-x-1/2 -translate-y-1/2"
                  style={{
                    background: `linear-gradient(45deg, hsl(${i * 60}, 70%, 60%), hsl(${(i * 60 + 120) % 360}, 70%, 60%))`
                  }}
                />
              ))}
            </motion.div>
          </div>
          
          <motion.h1
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.6 }}
            className="text-4xl font-bold gradient-text mb-4"
          >
            II-Agent
          </motion.h1>
          
          <motion.p
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.6 }}
            className="text-white/70 text-lg"
            className="text-gray-600 text-lg"
          >
            Initializing Intelligent Assistant...
          </motion.p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.5 }}
          className="flex justify-center space-x-2"
        >
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: i * 0.2,
              }}
              className="w-3 h-3 bg-gray-900 rounded-full"
            />
          ))}
        </motion.div>
      </div>
    </motion.div>
  )
}

export default LoadingScreen