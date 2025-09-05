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
            {/* Oil-in-water holographic lava lamp */}
            <motion.div
              className="w-full h-full relative overflow-hidden rounded-full"
              style={{
                background: 'radial-gradient(circle at 30% 20%, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%)',
                filter: 'blur(1px) contrast(1.2) saturate(1.3)'
              }}
            >
              {/* Floating oil blobs */}
              {[...Array(8)].map((_, i) => (
                <motion.div
                  key={i}
                  animate={{
                    x: [
                      Math.cos(i * 45 * Math.PI / 180) * 20,
                      Math.cos((i * 45 + 180) * Math.PI / 180) * 25,
                      Math.cos(i * 45 * Math.PI / 180) * 20
                    ],
                    y: [
                      Math.sin(i * 45 * Math.PI / 180) * 20,
                      Math.sin((i * 45 + 180) * Math.PI / 180) * 25,
                      Math.sin(i * 45 * Math.PI / 180) * 20
                    ],
                    scale: [0.8, 1.2, 0.8],
                    opacity: [0.6, 0.9, 0.6]
                  }}
                  transition={{
                    duration: 4 + i * 0.3,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: i * 0.2
                  }}
                  className="absolute top-1/2 left-1/2 rounded-full transform -translate-x-1/2 -translate-y-1/2"
                  style={{
                    width: `${12 + i * 2}px`,
                    height: `${12 + i * 2}px`,
                    background: `radial-gradient(circle, hsla(${i * 45 + 200}, 80%, 70%, 0.8) 0%, hsla(${i * 45 + 280}, 70%, 60%, 0.4) 100%)`,
                    filter: 'blur(0.5px)'
                  }}
                />
              ))}
              
              {/* Swirling background gradient */}
              <motion.div
                animate={{ 
                  rotate: 360,
                  background: [
                    'conic-gradient(from 0deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #667eea)',
                    'conic-gradient(from 120deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #667eea)',
                    'conic-gradient(from 240deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #667eea)',
                    'conic-gradient(from 360deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #667eea)'
                  ]
                }}
                transition={{ 
                  rotate: { duration: 8, repeat: Infinity, ease: "linear" },
                  background: { duration: 6, repeat: Infinity, ease: "easeInOut" }
                }}
                className="absolute inset-0 rounded-full opacity-60"
                style={{ filter: 'blur(2px)' }}
              />
              
              {/* Central holographic core */}
              <motion.div
                animate={{ 
                  scale: [1, 1.05, 1],
                  filter: [
                    'hue-rotate(0deg) saturate(1.2)',
                    'hue-rotate(60deg) saturate(1.4)',
                    'hue-rotate(120deg) saturate(1.2)',
                    'hue-rotate(0deg) saturate(1.2)'
                  ]
                }}
                transition={{ 
                  scale: { duration: 3, repeat: Infinity, ease: "easeInOut" },
                  filter: { duration: 5, repeat: Infinity, ease: "easeInOut" }
                }}
                className="absolute inset-6 rounded-full flex items-center justify-center"
                style={{
                  background: 'radial-gradient(circle at 40% 30%, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.3) 30%, transparent 70%)',
                  backdropFilter: 'blur(1px)',
                  border: '1px solid rgba(255,255,255,0.2)'
                }}
              >
                <motion.span 
                  animate={{ 
                    color: ["#ffffff", "#e0f2fe", "#f0f9ff", "#ffffff"],
                    textShadow: [
                      "0 0 8px rgba(255,255,255,0.8)",
                      "0 0 12px rgba(102,126,234,0.6)",
                      "0 0 8px rgba(255,255,255,0.8)"
                    ]
                  }}
                  transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                  className="text-white font-bold text-xl tracking-wider"
                >
                  II
                </motion.span>
              </motion.div>
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